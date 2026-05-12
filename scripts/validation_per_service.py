import os
import sys
from collections import defaultdict
from pathlib import Path

from dotenv import load_dotenv
import pyarrow.parquet as pq

# Configuración de rutas
PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / '.env')

def get_env_path(env_name: str, default: Path) -> Path:
    value = os.environ.get(env_name)
    if value:
        path = Path(value).expanduser()
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        return path.resolve()
    return default.resolve()

def obtener_esquema_detallado(archivo: Path) -> dict[str, str]:
    """Extrae nombres de columnas y sus tipos de datos."""
    try:
        parquet_file = pq.ParquetFile(archivo)
        schema = parquet_file.schema_arrow
        return {name: str(tipo) for name, tipo in zip(schema.names, schema.types)}
    except Exception as e:
        print(f"\n⚠️ Error al leer {archivo.name}: {e}")
        return {}

def imprimir_progreso(actual, total, servicio=""):
    """Dibuja una barra de progreso simple en la terminal."""
    ancho = 40
    progreso = int(actual / total * ancho)
    barra = f"[{'█' * progreso}{'.' * (ancho - progreso)}]"
    sys.stdout.write(f"\r{barra} {actual}/{total} Validando: {servicio[:20]}... ")
    sys.stdout.flush()

def listar_archivos_por_servicio(ruta_base: Path) -> tuple[dict[str, list[Path]], list[str]]:
    ruta_base = ruta_base.resolve()
    if not ruta_base.exists():
        raise FileNotFoundError(f"La ruta no existe: {ruta_base}")

    service_files: dict[str, list[Path]] = defaultdict(list)
    # Buscamos en todas las subcarpetas (años)
    year_dirs = sorted([d for d in ruta_base.iterdir() if d.is_dir()])
    years = [d.name for d in year_dirs]

    for year_dir in year_dirs:
        for archivo in year_dir.glob('*.parquet'):
            service_files[archivo.name].append(archivo)

    return service_files, years

def validar_servicio(service_name: str, archivos: list[Path], all_years: list[str]) -> dict:
    archivos_ordenados = sorted(archivos, key=lambda path: path.parent.name)
    resultado = {
        'servicio': service_name,
        'valido': True,
        'anio_referencia': None,
        'esquema_referencia': {},
        'errores': [],
        'anios_presentes': [path.parent.name for path in archivos_ordenados],
        'anios_faltantes': [],
    }

    if not archivos_ordenados:
        resultado['valido'] = False
        resultado['errores'].append('Sin archivos.')
        return resultado

    # Tomamos el primer año como base de comparación
    ref_file = archivos_ordenados[0]
    resultado['anio_referencia'] = ref_file.parent.name
    resultado['esquema_referencia'] = obtener_esquema_detallado(ref_file)

    if not resultado['esquema_referencia']:
        resultado['valido'] = False
        resultado['errores'].append(f"No se pudo leer el esquema base en {ref_file}")
        return resultado

    for archivo in archivos_ordenados[1:]:
        esquema_actual = obtener_esquema_detallado(archivo)
        if not esquema_actual:
            resultado['valido'] = False
            resultado['errores'].append(f"Archivo corrupto o ilegible: {archivo.parent.name}/{archivo.name}")
            continue

        if esquema_actual != resultado['esquema_referencia']:
            resultado['valido'] = False
            
            # Comparación detallada
            cols_ref = set(resultado['esquema_referencia'].keys())
            cols_act = set(esquema_actual.keys())
            
            faltantes = sorted(cols_ref - cols_act)
            sobrantes = sorted(cols_act - cols_ref)
            
            msg = [f"Inconsistencia en {archivo.parent.name}:"]
            if faltantes: msg.append(f"   - Faltan columnas: {faltantes}")
            if sobrantes: msg.append(f"   - Sobran columnas: {sobrantes}")
            
            # Verificar si las columnas están pero cambió el tipo de dato
            comunes = cols_ref & cols_act
            for col in comunes:
                tipo_ref = resultado['esquema_referencia'][col]
                tipo_act = esquema_actual[col]
                if tipo_ref != tipo_act:
                    msg.append(f"   - Tipo distinto en '{col}': {tipo_ref} -> {tipo_act}")
            
            resultado['errores'].append("\n".join(msg))

    # Verificar integridad temporal
    servicio_years = {path.parent.name for path in archivos_ordenados}
    resultado['anios_faltantes'] = sorted(set(all_years) - servicio_years)
    
    return resultado

def ejecutar_validacion(ruta_base: Path):
    try:
        service_files, years = listar_archivos_por_servicio(ruta_base)
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        return

    print(f"\n🚀 Iniciando validación de esquemas en: {ruta_base}")
    print(f"📅 Rango de años detectados: {years[0]} - {years[-1]}\n")

    servicios = sorted(service_files.keys())
    total_servicios = len(servicios)
    validos, invalidos = 0, 0
    reportes_errores = []

    for i, servicio in enumerate(servicios, 1):
        imprimir_progreso(i, total_servicios, servicio)
        res = validar_servicio(servicio, service_files[servicio], years)
        
        if res['valido']:
            validos += 1
        else:
            invalidos += 1
            reportes_errores.append(res)

    # Limpiar la línea de progreso antes del resumen
    sys.stdout.write("\r" + " " * 80 + "\r")
    
    print("="*70)
    print("📊 RESUMEN DE VALIDACIÓN")
    print("="*70)
    
    if reportes_errores:
        for err in reportes_errores:
            print(f"\n❌ SERVICIO: {err['servicio']}")
            print(f"   Años presentes: {', '.join(err['anios_presentes'])}")
            if err['anios_faltantes']:
                print(f"   ⚠️ Años faltantes: {', '.join(err['anios_faltantes'])}")
            for e in err['errores']:
                print(f"   {e}")
    
    print("\n" + "-"*70)
    print(f"✅ Servicios Consistentes: {validos}")
    print(f"❌ Servicios con Errores:   {invalidos}")
    print("-"*70)

    if invalidos == 0:
        print("\n🎉 ¡Éxito! Todos los servicios son compatibles entre años.")
    else:
        print("\n⚠️ Se recomienda revisar los esquemas antes de proceder con la carga.")

if __name__ == '__main__':
    ruta_salidas = get_env_path(
        'NYC_TLC_OUTPUT_DIR',
        PROJECT_ROOT / 'outputs' / 'new_datasets',
    )
    ejecutar_validacion(ruta_salidas)