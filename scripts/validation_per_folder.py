import os
from pathlib import Path

from dotenv import load_dotenv
import pyarrow.parquet as pq


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


def get_env_path(env_name: str, default: Path) -> Path:
    value = os.environ.get(env_name)
    if value:
        path = Path(value).expanduser()
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        return path.resolve()
    return default.resolve()


def validar_carpeta(ruta_carpeta: str) -> dict:
    """Valida esquemas Parquet de una carpeta sin cargar los datos completos."""
    ruta_carpeta = Path(ruta_carpeta)

    if not ruta_carpeta.exists():
        return {"error": f"La ruta no existe: {ruta_carpeta}", "valido": False}

    archivos = sorted(ruta_carpeta.glob('*.parquet'))

    if not archivos:
        return {
            "error": "No se encontraron archivos .parquet",
            "valido": False,
            "archivos_procesados": 0,
        }

    print(f"\n{'=' * 78}")
    print(f"📁 Carpeta: {ruta_carpeta}")
    print(f"📄 Archivos encontrados: {len(archivos)}")
    print(f"{'=' * 78}")

    columnas_referencia = None
    archivo_referencia = ""
    errores_encontrados = 0
    archivos_procesados = 0
    filas_estimadas = 0

    for archivo in archivos:
        try:
            parquet_file = pq.ParquetFile(archivo)
            columnas_actuales = parquet_file.schema_arrow.names
            filas_estimadas += parquet_file.metadata.num_rows
            archivos_procesados += 1

            if columnas_referencia is None:
                columnas_referencia = columnas_actuales
                archivo_referencia = archivo.name
                print(f"✅ {archivo.name}: leido como referencia")
                continue

            if columnas_actuales == columnas_referencia:
                print(f"✅ {archivo.name}: estructura identica")
            else:
                errores_encontrados += 1
                print(f"❌ {archivo.name}: diferencias detectadas")

                set_ref = set(columnas_referencia)
                set_act = set(columnas_actuales)

                faltantes = set_ref - set_act
                sobrantes = set_act - set_ref

                if faltantes:
                    print(f"   • Faltan: {sorted(faltantes)}")
                if sobrantes:
                    print(f"   • Sobran: {sorted(sobrantes)}")
                if set_ref == set_act and columnas_actuales != columnas_referencia:
                    print("   • Aviso: mismas columnas, orden diferente")

        except Exception as exc:
            print(f"❌ {archivo.name}: error - {exc}")
            errores_encontrados += 1

    print(f"\n{'-' * 78}")
    if errores_encontrados == 0:
        print(
            f"✅ RESULTADO: valido. {archivos_procesados} archivos comparten "
            "la misma estructura."
        )
        print(f"📌 Referencia: {archivo_referencia}")
        print(f"📊 Filas estimadas por metadatos: {filas_estimadas:,}")
        print(f"📚 Columnas ({len(columnas_referencia)}): {columnas_referencia}")
        return {
            "valido": True,
            "archivos_procesados": archivos_procesados,
            "filas_estimadas": filas_estimadas,
            "columnas": columnas_referencia,
        }

    print(f"❌ RESULTADO: {errores_encontrados} inconsistencia(s) encontrada(s).")
    return {
        "valido": False,
        "archivos_procesados": archivos_procesados,
        "filas_estimadas": filas_estimadas,
        "errores": errores_encontrados,
    }


def validar_datasets_completo(ruta_base: str) -> None:
    """Valida todas las carpetas de datasets disponibles."""
    ruta_base = Path(ruta_base)

    if not ruta_base.exists():
        print(f"❌ Error: la ruta base no existe: {ruta_base}")
        return

    print("\n🔍 VALIDACION COMPLETA DE DATASETS NYC TLC")
    print(f"📥 Origen: {ruta_base}")

    resultados_por_anio = {}
    carpetas_validas = 0
    carpetas_invalidas = 0

    for year_dir in sorted([d for d in ruta_base.iterdir() if d.is_dir()]):
        print(f"\n{'█' * 78}")
        print(f"📅 ANIO: {year_dir.name}")
        print(f"{'█' * 78}")

        resultados_por_anio[year_dir.name] = {}
        subcarpetas = sorted([d for d in year_dir.iterdir() if d.is_dir()])

        if not subcarpetas:
            print(f"⚠️  No se encontraron carpetas de servicio para {year_dir.name}")
            continue

        for service_dir in subcarpetas:
            resultado = validar_carpeta(str(service_dir))
            resultados_por_anio[year_dir.name][service_dir.name] = resultado

            if resultado.get("valido"):
                carpetas_validas += 1
            else:
                carpetas_invalidas += 1

    print(f"\n{'=' * 78}")
    print("📊 RESUMEN GENERAL")
    print(f"✅ Carpetas validas: {carpetas_validas}")
    print(f"❌ Carpetas con problemas: {carpetas_invalidas}")
    print("\nResultados por anio:")

    for anio in sorted(resultados_por_anio.keys()):
        tipos = resultados_por_anio[anio]
        validos = sum(1 for r in tipos.values() if r.get("valido"))
        print(f"  {anio}: {validos}/{len(tipos)} carpetas validas")

    print(f"{'=' * 78}\n")


if __name__ == "__main__":
    ruta_datasets = get_env_path(
        "NYC_TLC_RAW_DATA_DIR",
        PROJECT_ROOT / "raw_datasets",
    )
    validar_datasets_completo(str(ruta_datasets))
