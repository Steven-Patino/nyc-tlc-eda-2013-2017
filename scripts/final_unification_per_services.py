import os
import gc
import sys
from pathlib import Path
from typing import List, Dict

from dotenv import load_dotenv
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

# Configuración de constantes y carga de entorno
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

def get_batch_size() -> int:
    """Lee el batch size de las variables de entorno o usa un default seguro."""
    value = os.environ.get('NYC_TLC_BATCH_SIZE')
    try:
        return int(value) if value else 100_000
    except ValueError:
        return 100_000

def unify_types(type1: pa.DataType, type2: pa.DataType) -> pa.DataType:
    """
    Resuelve el conflicto de tipos (ej. null vs double).
    Si un año tiene la columna como null y otro como double, el final será double.
    """
    if type1 == type2: return type1
    if pa.types.is_null(type1): return type2
    if pa.types.is_null(type2): return type1
    
    # Si ambos son numéricos pero diferentes, promovemos a float64 (double)
    numeric_types = [pa.int8(), pa.int16(), pa.int32(), pa.int64(), pa.float32(), pa.float64()]
    if type1 in numeric_types and type2 in numeric_types:
        return pa.float64()
    
    return pa.string() # Fallback a string para máxima compatibilidad

def get_master_schema(archivos: List[Path]) -> pa.Schema:
    """Escanea los encabezados de todos los archivos para crear un esquema unificado."""
    print(f"🔎 Analizando esquemas de {len(archivos)} archivos para definir el esquema maestro...")
    fields_dict: Dict[str, dict] = {}

    for archivo in archivos:
        schema = pq.read_schema(archivo)
        for field in schema:
            name = field.name.lower() # Normalizamos a minúsculas
            if name not in fields_dict:
                fields_dict[name] = {'type': field.type, 'nullable': True}
            else:
                fields_dict[name]['type'] = unify_types(fields_dict[name]['type'], field.type)
    
    # Creamos el esquema final ordenado alfabéticamente
    return pa.schema([
        pa.field(name, info['type'], info['nullable']) 
        for name, info in sorted(fields_dict.items())
    ])

def align_batch(table: pa.Table, master_schema: pa.Schema) -> pa.Table:
    """Ajusta las columnas y tipos de un batch al esquema maestro."""
    columns = []
    # Normalizar nombres de la tabla actual
    table = table.rename_columns([c.lower() for c in table.column_names])
    
    for field in master_schema:
        if field.name in table.column_names:
            col = table.column(field.name)
            # Casting si el tipo no coincide (ej. null -> double)
            if col.type != field.type:
                col = pc.cast(col, field.type)
            columns.append(col)
        else:
            # Si al archivo le falta una columna del esquema maestro, rellenamos con nulos
            columns.append(pa.nulls(table.num_rows, type=field.type))
    
    return pa.Table.from_arrays(columns, schema=master_schema)

def unificar_servicio(nombre: str, archivos: List[Path], ruta_destino: Path):
    """Procesa la unificación por bloques para optimizar RAM y dar feedback en terminal."""
    if not archivos: return

    print(f"\n{'='*70}")
    print(f"📦 UNIFICANDO: {nombre.upper()}")
    print(f"{'='*70}")

    schema_maestro = get_master_schema(archivos)
    batch_size = get_batch_size()
    
    ruta_destino.parent.mkdir(parents=True, exist_ok=True)
    total_filas = 0

    with pq.ParquetWriter(ruta_destino, schema_maestro, compression='snappy') as writer:
        for i, archivo in enumerate(archivos, 1):
            anio = archivo.parent.name
            pf = pq.ParquetFile(archivo)
            
            print(f"  [{i}/{len(archivos)}] Procesando año {anio} ({pf.num_row_groups} grupos)...")
            
            # iter_batches permite leer sin cargar el archivo completo
            for batch in pf.iter_batches(batch_size=batch_size):
                table = pa.Table.from_batches([batch])
                aligned_table = align_batch(table, schema_maestro)
                
                writer.write_table(aligned_table)
                total_filas += aligned_table.num_rows
                
                # Feedback en tiempo real para que la terminal no se 'congele'
                sys.stdout.write(f"\r    ✨ Filas totales acumuladas: {total_filas:,}")
                sys.stdout.flush()
                
                del batch, table, aligned_table # Liberar memoria
            
            print(f" -> Completado.")
            gc.collect() # Limpieza forzada tras cada año

    print(f"\n✅ Guardado en: {ruta_destino}")
    print(f"📊 Registros unificados: {total_filas:,}")

def main():
    # Rutas basadas en tu estructura
    ruta_origen = get_env_path('NYC_TLC_OUTPUT_DIR', PROJECT_ROOT / 'outputs' / 'new_datasets')
    ruta_final_base = PROJECT_ROOT / 'outputs' / 'final_datasets'

    # Agrupar archivos homónimos (ej: todos los yellow_taxi.parquet)
    servicios: Dict[str, List[Path]] = {}
    for p in ruta_origen.rglob("*.parquet"):
        servicios.setdefault(p.name, []).append(p)

    if not servicios:
        print("❌ No se encontraron archivos en outputs/new_datasets")
        return

    for nombre_archivo, paths in servicios.items():
        # Ordenar por año (nombre de la carpeta padre)
        paths.sort(key=lambda x: x.parent.name)
        
        destino = ruta_final_base / nombre_archivo
        unificar_servicio(nombre_archivo, paths, destino)

    print(f"\n🚀 PROCESO FINALIZADO. Los 3 servicios están en: {ruta_final_base}")

if __name__ == "__main__":
    main()