import pyarrow.parquet as pq
import pyarrow.compute as pc
import pyarrow as pa
from pathlib import Path
import sys
import gc
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FINAL_DATA_DIR = PROJECT_ROOT / 'outputs' / 'final_datasets'

def imprimir_progreso(actual, total, prefijo=''):
    ancho = 30
    progresion = int(actual / total * ancho)
    barra = f"[{'█' * progresion}{'.' * (ancho - progresion)}]"
    sys.stdout.write(f"\r{prefijo} {barra} {actual/total:>4.1%}")
    sys.stdout.flush()

def auditar_dataset(nombre_archivo: str):
    ruta = FINAL_DATA_DIR / nombre_archivo
    if not ruta.exists():
        print(f"❌ No se encuentra: {nombre_archivo}")
        return

    print(f"\n{'='*80}")
    print(f"🔍 AUDITORÍA DE INTEGRIDAD: {nombre_archivo}")
    print(f"{'='*80}")

    parquet_file = pq.ParquetFile(ruta)
    total_filas = parquet_file.metadata.num_rows
    schema = parquet_file.schema_arrow
    
    print(f"📈 Filas totales: {total_filas:,}")
    print(f"📂 Tamaño en disco: {ruta.stat().st_size / (1024**3):.2f} GB")

    # --- 1. ANÁLISIS DE NULOS ---
    print(f"\n❓ ANÁLISIS DE VALORES NULOS (Columna por Columna):")
    for i, col_name in enumerate(schema.names, 1):
        imprimir_progreso(i, len(schema.names), f"   Validando columnas")
        col_data = pq.read_table(ruta, columns=[col_name]).column(0)
        validos = pc.count(col_data).as_py()
        nulos = total_filas - validos
        porcentaje = (nulos / total_filas) * 100
        # Guardamos el resultado para imprimirlo después de la barra
        sys.stdout.write(f" -> {col_name}: {nulos:,} ({porcentaje:.2f}%)\n")
        del col_data
        gc.collect()

    # --- 2. ANÁLISIS DE RANGO TEMPORAL ---
    print(f"\n📅 ANÁLISIS DE RANGO TEMPORAL (2013-2017):")
    posibles_fechas = ['tpep_pickup_datetime', 'lpep_pickup_datetime', 'pickup_datetime']
    col_fecha = [c for c in schema.names if c in posibles_fechas]
    
    if col_fecha:
        f_name = col_fecha[0]
        table_fecha = pq.read_table(ruta, columns=[f_name])
        
        # Filtros
        f_min = pa.scalar(pd.Timestamp('2013-01-01'), type=table_fecha.column(0).type)
        f_max = pa.scalar(pd.Timestamp('2017-12-31 23:59:59'), type=table_fecha.column(0).type)
        
        fuera_rango = pc.sum(pc.or_(
            pc.less(table_fecha.column(0), f_min),
            pc.greater(table_fecha.column(0), f_max)
        )).as_py()
        
        print(f"   - Columna: {f_name}")
        print(f"   - Fuera de rango (2013-2017): {fuera_rango:,} ({ (fuera_rango/total_filas):.4%})")
        del table_fecha
    gc.collect()

    # --- 3. ANÁLISIS DE DUPLICADOS (Hashing optimizado) ---
    print(f"\n👥 ANÁLISIS DE DUPLICADOS:")
    seen_hashes = set()
    duplicados_detectados = 0
    batch_size = 500_000
    filas_procesadas = 0

    for batch in parquet_file.iter_batches(batch_size=batch_size):
        df_batch = batch.to_pandas()
        hashes = pd.util.hash_pandas_object(df_batch, index=False)
        
        for h in hashes:
            if h in seen_hashes:
                duplicados_detectados += 1
            else:
                seen_hashes.add(h)
        
        filas_procesadas += len(batch)
        imprimir_progreso(filas_procesadas, total_filas, "   Escaneando filas")
        
        # Límite de seguridad para RAM (15 millones de registros únicos)
        if len(seen_hashes) > 15_000_000:
            print(f"\n   ⚠️ Límite de RAM alcanzado (Muestra de 15M única finalizada).")
            break
            
    print(f"\n   - Total duplicados detectados en la muestra: {duplicados_detectados:,}")
    del seen_hashes
    gc.collect()

def main():
    servicios = ['yellow_taxi.parquet', 'green_taxi.parquet', 'for_hire_vehicle.parquet']
    for servicio in servicios:
        auditar_dataset(servicio)

if __name__ == "__main__":
    main()