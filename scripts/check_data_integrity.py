import dask.dataframe as dd
from dask.diagnostics import ProgressBar
import dask
from pathlib import Path
import pandas as pd
import time
import os

# --- CONFIGURACIÓN DE ESTABILIDAD ---
# Forzamos ejecución secuencial para evitar picos de RAM en VS Code
dask.config.set(scheduler='synchronous') 

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FINAL_DATA_DIR = PROJECT_ROOT / 'outputs' / 'final_datasets'

def auditar_dataset_ligero(nombre_archivo: str):
    ruta = FINAL_DATA_DIR / nombre_archivo
    if not ruta.exists():
        print(f"\n❌ No se encuentra el archivo: {nombre_archivo}")
        return

    print(f"\n{'='*80}")
    print(f"🔍 AUDITORÍA ESENCIAL (SIN DUPLICADOS): {nombre_archivo}")
    print(f"{'='*80}")

    # Carga perezosa del dataset
    ddf = dd.read_parquet(ruta)
    
    # --- 1. CONTEO TOTAL ---
    print(f"⏳ Calculando volumen de filas...")
    with ProgressBar():
        total_filas = len(ddf)
    
    print(f"📈 Filas totales: {total_filas:,}")
    print(f"📂 Tamaño en disco: {ruta.stat().st_size / (1024**3):.2f} GB")

    # --- 2. ANÁLISIS DE VALORES NULOS ---
    # Lo hacemos columna por columna para máxima seguridad de memoria
    print(f"\n❓ ANALIZANDO NULOS (Modo secuencial):")
    for col in ddf.columns:
        # Solo leemos la columna necesaria en cada iteración
        nulos = ddf[col].isnull().sum().compute()
        porcentaje = (nulos / total_filas) * 100
        status = "⚠️" if nulos > 0 else "✅"
        print(f"   {status} {col}: {nulos:,} ({porcentaje:.2f}%)")

    # --- 3. ANÁLISIS DE RANGO TEMPORAL ---
    posibles_fechas = ['tpep_pickup_datetime', 'lpep_pickup_datetime', 'pickup_datetime']
    col_fecha = [c for c in ddf.columns if c in posibles_fechas]
    
    if col_fecha:
        f_name = col_fecha[0]
        print(f"\n📅 VERIFICANDO RANGO TEMPORAL (2013-2017) en '{f_name}':")
        f_min = pd.Timestamp('2013-01-01')
        f_max = pd.Timestamp('2017-12-31 23:59:59')
        
        with ProgressBar():
            # Filtro directo sobre la columna de fecha
            fuera_rango = ddf[(ddf[f_name] < f_min) | (ddf[f_name] > f_max)].shape[0].compute()
        
        print(f"   - Registros fuera de rango: {fuera_rango:,} ({fuera_rango/total_filas:.4%})")

def main():
    # Lista de archivos a auditar
    servicios = ['yellow_taxi.parquet', 'green_taxi.parquet', 'for_hire_vehicle.parquet']
    
    tiempo_inicio = time.time()
    
    for servicio in servicios:
        auditar_dataset_ligero(servicio)
        print(f"\n✅ Auditoría de {servicio} completada.")
    
    print(f"\n{'='*80}")
    print(f"🏁 PROCESO FINALIZADO")
    print(f"⏱️ Tiempo total: {(time.time() - tiempo_inicio)/60:.2f} minutos")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()