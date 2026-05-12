# 🧭 Guia de procesamiento

![uv](https://img.shields.io/badge/uv-sync-6C47FF)
![Config](https://img.shields.io/badge/config-.env-yellow)
![Parquet](https://img.shields.io/badge/data-Parquet-0A7EA4)

Esta guia describe el flujo actual para validar y unificar los datos Parquet de NYC TLC 2013-2017.

## 1. 🧰 Preparar entorno

```powershell
cd EDA_2013_to_2017
uv sync
```

Opcionalmente activa el entorno:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 2. ⚙️ Configurar rutas

Los scripts cargan automaticamente un archivo `.env` ubicado en la raiz del proyecto.

Windows:

```powershell
Copy-Item .env.example .env
```

Ubuntu:

```bash
cp .env.example .env
```

Contenido base:

```env
NYC_TLC_RAW_DATA_DIR=raw_datasets
NYC_TLC_OUTPUT_DIR=outputs/new_datasets
NYC_TLC_BATCH_SIZE=250000
```

Puedes usar rutas relativas al proyecto o rutas absolutas locales. El archivo `.env` no se sube a Git.

Si no existe `.env`, se usan estas rutas dentro del proyecto:

```text
raw_datasets
outputs/new_datasets
```

## 3. 📥 Estructura esperada

```text
raw_datasets/
  2013/yellow_taxi/*.parquet
  2014/green_taxi/*.parquet
  2014/yellow_taxi/*.parquet
  2015/for_hire_vehicle/*.parquet
  2015/green_taxi/*.parquet
  2015/yellow_taxi/*.parquet
  2016/for_hire_vehicle/*.parquet
  2016/green_taxi/*.parquet
  2016/yellow_taxi/*.parquet
  2017/for_hire_vehicle/*.parquet
  2017/green_taxi/*.parquet
  2017/yellow_taxi/*.parquet
```

## 4. 🔍 Validar datos crudos

```powershell
uv run python .\scripts\validation_per_folder.py
```

La validacion revisa:

- Existencia de carpetas y archivos Parquet.
- Lectura de metadatos Parquet.
- Consistencia de columnas dentro de cada carpeta.
- Conteo estimado de filas desde metadatos.

No carga los datasets completos en memoria.

## 5. 📦 Unificar datasets

```powershell
uv run python .\scripts\unification_per_folder.py
```

El script genera un archivo por anio/servicio:

```text
outputs/new_datasets/{anio}/{servicio}.parquet
```

El proceso:

- Lee esquemas de todos los Parquet de una carpeta.
- Normaliza nombres de columnas a minusculas.
- Unifica tipos compatibles.
- Procesa datos por batches con `iter_batches`.
- Escribe salida comprimida con Snappy.

## 6. 🧠 Ajuste de memoria

La variable `NYC_TLC_BATCH_SIZE` controla cuantas filas se procesan por batch.

Para equipos con poca RAM:

```env
NYC_TLC_BATCH_SIZE=100000
```

Para equipos con mas RAM:

```env
NYC_TLC_BATCH_SIZE=500000
```

## 7. 📊 Resultado actual

La ejecucion final de unificacion proceso:

| Servicio | Filas |
|---|---:|
| Yellow Taxi | 727,935,282 |
| For Hire Vehicle | 387,812,173 |
| Green Taxi | 63,193,374 |
| **Total** | **1,178,940,829** |

## 8. 🚫 Archivos que no deben subirse a Git

El proyecto ignora:

- `.venv/`
- `raw_datasets/`
- `datasets/`
- `outputs/`
- `*.parquet`
- `*.csv`
- `.env`

Esto mantiene el repositorio liviano y replicable.
