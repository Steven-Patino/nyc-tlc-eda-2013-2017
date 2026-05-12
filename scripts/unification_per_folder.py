from pathlib import Path
from typing import List
import gc
import os

from dotenv import load_dotenv
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq


DEFAULT_BATCH_SIZE = 250_000
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
    value = os.environ.get('NYC_TLC_BATCH_SIZE')
    if not value:
        return DEFAULT_BATCH_SIZE

    try:
        batch_size = int(value)
    except ValueError:
        print(f"⚠️  NYC_TLC_BATCH_SIZE invalido ({value}); usando {DEFAULT_BATCH_SIZE:,}")
        return DEFAULT_BATCH_SIZE

    if batch_size <= 0:
        print(f"⚠️  NYC_TLC_BATCH_SIZE debe ser mayor a 0; usando {DEFAULT_BATCH_SIZE:,}")
        return DEFAULT_BATCH_SIZE

    return batch_size


def normalize_column_name(name: str) -> str:
    """Normaliza nombres para evitar duplicados por mayusculas/minusculas."""
    return name.strip().lower()


def unify_types(type1: pa.DataType, type2: pa.DataType) -> pa.DataType:
    """Unifica dos tipos de PyArrow en uno compatible."""
    if type1 == type2:
        return type1

    if pa.types.is_null(type1):
        return type2

    if pa.types.is_null(type2):
        return type1

    type_hierarchy = {
        pa.null(): 0,
        pa.int8(): 1,
        pa.int16(): 2,
        pa.int32(): 3,
        pa.int64(): 4,
        pa.float32(): 5,
        pa.float64(): 6,
    }

    if type1 in type_hierarchy and type2 in type_hierarchy:
        return max([type1, type2], key=lambda t: type_hierarchy[t])

    if pa.types.is_string(type1) or pa.types.is_string(type2):
        return pa.string()

    if pa.types.is_timestamp(type1) and pa.types.is_timestamp(type2):
        return pa.timestamp('us')

    return pa.string()


def unify_schemas(schemas: List[pa.Schema]) -> pa.Schema:
    """Unifica multiples esquemas y normaliza nombres de columnas."""
    if not schemas:
        return pa.schema([])

    fields_by_name = {}

    for schema in schemas:
        for field in schema:
            field_name = normalize_column_name(field.name)

            if field_name not in fields_by_name:
                fields_by_name[field_name] = {
                    'type': field.type,
                    'nullable': field.nullable,
                }
                continue

            fields_by_name[field_name]['type'] = unify_types(
                fields_by_name[field_name]['type'],
                field.type,
            )
            fields_by_name[field_name]['nullable'] = (
                fields_by_name[field_name]['nullable'] or field.nullable
            )

    return pa.schema(
        [
            pa.field(name, info['type'], nullable=info['nullable'])
            for name, info in sorted(fields_by_name.items())
        ]
    )


def align_table_to_schema(table: pa.Table, unified_schema: pa.Schema) -> pa.Table:
    """Ajusta nombres, columnas faltantes y tipos al esquema unificado."""
    normalized_columns = {}

    for index, original_name in enumerate(table.column_names):
        normalized_name = normalize_column_name(original_name)
        if normalized_name not in normalized_columns:
            normalized_columns[normalized_name] = table.column(index)

    aligned_columns = []
    for field in unified_schema:
        if field.name not in normalized_columns:
            aligned_columns.append(pa.nulls(table.num_rows, type=field.type))
            continue

        column = normalized_columns[field.name]
        if column.type != field.type:
            column = pc.cast(column, field.type)
        aligned_columns.append(column)

    return pa.Table.from_arrays(aligned_columns, schema=unified_schema)


def unify_folder(ruta_carpeta: str, ruta_salida_base: str) -> dict:
    """Unifica los Parquet de una carpeta en un unico archivo.

    Procesa por batches para evitar cargar archivos completos en RAM.
    """
    ruta_carpeta = Path(ruta_carpeta)
    archivos = sorted([p for p in ruta_carpeta.iterdir() if p.suffix == '.parquet'])

    if not archivos:
        return {
            'valido': False,
            'ruta': str(ruta_carpeta),
            'mensaje': 'No se encontraron archivos .parquet',
        }

    batch_size = get_batch_size()

    print(f"\n{'=' * 78}")
    print(f"📦 Unificando carpeta: {ruta_carpeta}")
    print(f"📄 Archivos encontrados: {len(archivos)}")
    print(f"🧩 Batch size: {batch_size:,} filas")
    print(f"{'=' * 78}")

    try:
        print("🔎 Analizando esquemas de todos los archivos...")
        all_schemas = []
        for archivo in archivos:
            try:
                all_schemas.append(pq.read_schema(archivo))
                print(f"  ✅ Esquema leido: {archivo.name}")
            except Exception as exc:
                print(f"  ❌ Error leyendo esquema {archivo.name}: {exc}")
                return {
                    'valido': False,
                    'ruta': str(ruta_carpeta),
                    'mensaje': f'Error leyendo esquema de {archivo.name}: {exc}',
                }

        unified_schema = unify_schemas(all_schemas)
        print(f"🧱 Esquema unificado creado con {len(unified_schema)} columnas")
        print(f"📚 Columnas finales: {unified_schema.names}")

        year = ruta_carpeta.parent.name
        ruta_output = Path(ruta_salida_base) / year
        ruta_output.mkdir(parents=True, exist_ok=True)
        ruta_salida_final = ruta_output / f"{ruta_carpeta.name}.parquet"

        registros_totales = 0

        with pq.ParquetWriter(
            str(ruta_salida_final),
            unified_schema,
            compression='snappy',
            use_dictionary=True,
        ) as parquet_writer:
            for archivo_idx, archivo in enumerate(archivos, start=1):
                try:
                    parquet_file = pq.ParquetFile(archivo)
                    print(
                        f"\n🚕 Procesando archivo {archivo_idx}/{len(archivos)}: "
                        f"{archivo.name} ({parquet_file.num_row_groups} row groups)"
                    )

                    filas_archivo = 0
                    for batch_idx, record_batch in enumerate(
                        parquet_file.iter_batches(
                            batch_size=batch_size,
                            use_threads=True,
                        ),
                        start=1,
                    ):
                        table = pa.Table.from_batches([record_batch])
                        aligned_table = align_table_to_schema(table, unified_schema)
                        parquet_writer.write_table(aligned_table)

                        filas_archivo += aligned_table.num_rows
                        registros_totales += aligned_table.num_rows

                        print(
                            f"  ✅ Batch {batch_idx} | "
                            f"filas acumuladas carpeta: {registros_totales:,}"
                        )

                        del record_batch, table, aligned_table
                        gc.collect()

                    print(
                        f"🎯 Archivo completado: {archivo.name} | "
                        f"filas: {filas_archivo:,}"
                    )

                except Exception as exc:
                    print(f"❌ Error procesando {archivo.name}: {exc}")
                    return {
                        'valido': False,
                        'ruta': str(ruta_carpeta),
                        'mensaje': f'Error procesando {archivo.name}: {exc}',
                    }

        print(f"\n✅ Archivo unificado guardado en: {ruta_salida_final}")
        print(f"📊 Filas totales: {registros_totales:,}")
        print(f"📚 Columnas: {unified_schema.names}")

        return {
            'valido': True,
            'ruta': str(ruta_carpeta),
            'salida': str(ruta_salida_final),
            'filas': registros_totales,
            'columnas': unified_schema.names,
            'archivos_unificados': len(archivos),
        }

    except Exception as exc:
        return {
            'valido': False,
            'ruta': str(ruta_carpeta),
            'mensaje': f'Error durante la unificacion: {exc}',
        }


def unify_datasets(ruta_base: str, ruta_salida_base: str) -> None:
    """Unifica todas las carpetas de datasets por anio y servicio."""
    ruta_base = Path(ruta_base)

    if not ruta_base.exists():
        raise FileNotFoundError(f"La ruta base no existe: {ruta_base}")

    print("\n🚀 Iniciando unificacion de datasets por carpeta")
    print(f"📥 Origen: {ruta_base}")
    print(f"📤 Salida: {Path(ruta_salida_base)}")

    resultados = []

    for year_dir in sorted([d for d in ruta_base.iterdir() if d.is_dir()]):
        subcarpetas = sorted([d for d in year_dir.iterdir() if d.is_dir()])

        if not subcarpetas:
            print(f"⚠️  No se encontraron subcarpetas en {year_dir}")
            continue

        for carpeta in subcarpetas:
            resultado = unify_folder(str(carpeta), ruta_salida_base)
            resultados.append(resultado)

    print(f"\n{'=' * 78}")
    print("🏁 Resumen de unificacion")
    exitos = sum(1 for r in resultados if r.get('valido'))
    fallos = sum(1 for r in resultados if not r.get('valido'))
    print(f"✅ Carpetas unificadas: {exitos}")
    print(f"❌ Carpetas con error: {fallos}")
    print(f"📦 Total de carpetas procesadas: {len(resultados)}")
    print(f"{'=' * 78}")

    if exitos:
        print("Carpetas completadas:")
        for resultado in resultados:
            if resultado.get('valido'):
                print(
                    f"✅ {resultado.get('ruta')} -> {resultado.get('salida')} "
                    f"({resultado.get('filas'):,} filas)"
                )

    if fallos:
        print("Detalles de errores:")
        for resultado in resultados:
            if not resultado.get('valido'):
                print(f"❌ {resultado.get('ruta')}: {resultado.get('mensaje')}")


if __name__ == '__main__':
    ruta_datasets = get_env_path(
        'NYC_TLC_RAW_DATA_DIR',
        PROJECT_ROOT / 'raw_datasets',
    )
    ruta_salida = get_env_path(
        'NYC_TLC_OUTPUT_DIR',
        PROJECT_ROOT / 'outputs' / 'new_datasets',
    )

    print(f"Ruta de origen utilizada: {ruta_datasets}")
    print(f"Ruta de salida utilizada: {ruta_salida}")
    unify_datasets(str(ruta_datasets), str(ruta_salida))
