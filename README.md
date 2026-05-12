# 🚕 NYC TLC EDA 2013-2017

![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![uv](https://img.shields.io/badge/uv-managed-6C47FF?style=for-the-badge)
![Parquet](https://img.shields.io/badge/Data-Parquet-0A7EA4?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Processing%20Ready-2EA44F?style=for-the-badge)

Proyecto de analisis exploratorio y preparacion de datos masivos de la **NYC Taxi and Limousine Commission (TLC)** para el periodo **2013-2017**.

El flujo actual valida archivos Parquet crudos, unifica datasets mensuales por anio/servicio y deja una base consolidada lista para EDA.

## 📌 Estado actual

| Fase | Estado | Resultado |
|---|---|---|
| ✅ Validacion estructural | Completada | 12/12 carpetas validas |
| ✅ Unificacion por carpeta | Completada | 1,178,940,829 filas procesadas |
| 🔎 Validación por servicio | Completada | Se detectaron inconsistencias de tipo en columnas homónimas |
| 🔄 Unificación final por servicio | Completada | Datasets normalizados y consolidados en outputs/final_datasets |
| 🧩 Configuracion replicable | Lista | Scripts configurables desde `.env` |
| 📊 EDA y visualizaciones | Pendiente | Siguiente fase del proyecto |

## 📊 Volumen procesado

| Servicio | Filas totales | Porcentaje |
|---|---:|---:|
| 🚕 Yellow Taxi | 727,935,282 | 61.7% |
| 🚙 For Hire Vehicle (FHV) | 387,812,173 | 32.9% |
| 🟢 Green Taxi | 63,193,374 | 5.4% |
| **Total** | **1,178,940,829** | **100%** |

## 🧰 Requisitos

- Python 3.13+
- uv de Astral
- Datos Parquet de NYC TLC descargados localmente
- Espacio en disco suficiente para datos crudos y salidas unificadas

Las dependencias estan en `pyproject.toml` y se instalan con `uv sync`.

## 🚀 Instalacion en Windows

```powershell
git clone https://github.com/Steven-Patino/nyc-tlc-eda-2013-2017.git
cd nyc-tlc-eda-2013-2017
uv sync
Copy-Item .env.example .env
```

Ejecutar validacion:

```powershell
uv run python .\scripts\validation_per_folder.py
```

Ejecutar validación por servicio:

```powershell
uv run python .\scripts\validation_per_service.py
```

Ejecutar unificacion:

```powershell
uv run python .\scripts\unification_per_folder.py
```

Ejecutar unificación final:

```powershell
uv run python .\scripts\final_unification_per_services.py
```

## 🐧 Instalacion en Ubuntu

Instalar `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Clonar e instalar:

```bash
git clone https://github.com/Steven-Patino/nyc-tlc-eda-2013-2017.git
cd nyc-tlc-eda-2013-2017
uv sync
cp .env.example .env
```

Ejecutar validacion:

```bash
uv run python scripts/validation_per_folder.py
```

Ejecutar validación por servicio:

```bash
uv run python scripts/validation_per_service.py
```

Ejecutar unificacion:

```bash
uv run python scripts/unification_per_folder.py
```

Ejecutar unificación final:

```bash
uv run python scripts/final_unification_per_services.py
```

## ⚙️ Configuracion con `.env`

Los scripts cargan automaticamente el archivo `.env` ubicado en la raiz del proyecto.

Plantilla:

```env
NYC_TLC_RAW_DATA_DIR=raw_datasets
NYC_TLC_OUTPUT_DIR=outputs/new_datasets
NYC_TLC_BATCH_SIZE=250000
```

Puedes usar rutas relativas al proyecto o rutas absolutas locales. El archivo `.env` real esta ignorado por Git.

| Variable | Uso | Valor sugerido |
|---|---|---|
| `NYC_TLC_RAW_DATA_DIR` | Carpeta donde van los Parquet crudos descargados | `raw_datasets` |
| `NYC_TLC_OUTPUT_DIR` | Carpeta donde se escriben los Parquet unificados | `outputs/new_datasets` |
| `NYC_TLC_BATCH_SIZE` | Filas procesadas por lote durante la unificacion | `250000` |

## 📥 Donde ubicar los datasets descargados

Descarga los archivos desde la fuente oficial:

🔗 https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Luego ubicalos en `raw_datasets/` respetando esta arquitectura:

```text
raw_datasets/
  2013/
    yellow_taxi/
      yellow_tripdata_2013-01.parquet
      yellow_tripdata_2013-02.parquet
      ...
  2014/
    green_taxi/
      green_tripdata_2014-01.parquet
      ...
    yellow_taxi/
      yellow_tripdata_2014-01.parquet
      ...
  2015/
    for_hire_vehicle/
      fhv_tripdata_2015-01.parquet
      ...
    green_taxi/
    yellow_taxi/
  2016/
    for_hire_vehicle/
    green_taxi/
    yellow_taxi/
  2017/
    for_hire_vehicle/
    green_taxi/
    yellow_taxi/
```

Las carpetas de datos y resultados se preservan en el repositorio mediante archivos `.gitkeep`; los datos Parquet crudos y consolidados no se suben a GitHub por su tamaño.

## 📤 Donde quedan los resultados

Al ejecutar `scripts/unification_per_folder.py`, los archivos consolidados se escriben en:

```text
outputs/new_datasets/{anio}/{servicio}.parquet
```

Ejemplos:

```text
outputs/new_datasets/2017/yellow_taxi.parquet
outputs/new_datasets/2017/green_taxi.parquet
outputs/new_datasets/2017/for_hire_vehicle.parquet
```

La carpeta `outputs/` preserva su estructura mediante archivos `.gitkeep`; los resultados pesados se mantienen fuera de Git.

## 🧪 Scripts principales

| Script | Funcion |
|---|---|
| `scripts/validation_per_folder.py` | Valida esquemas Parquet por carpeta usando metadatos, sin cargar datasets completos |
| `scripts/validation_per_service.py` | Valida que los mismos servicios entre años compartan columnas y tipos de datos consistentes |
| `scripts/unification_per_folder.py` | Unifica archivos mensuales por anio/servicio usando batches para cuidar la RAM |
| `scripts/final_unification_per_services.py` | Unifica datasets consolidados por servicio aplicando normalización de esquemas |

## 🧠 Notas de memoria

Si tu equipo tiene poca RAM, reduce el batch size en `.env`:

```env
NYC_TLC_BATCH_SIZE=100000
```

Si tienes mas RAM y quieres probar mayor velocidad:

```env
NYC_TLC_BATCH_SIZE=500000
```

## 📚 Documentacion

La documentación general del proyecto se concentra en el README principal y en los dos documentos centrales de `docs/Documentacion_general`. Los flujos de validación y unificación también están documentados en `docs/Concluciones/`.

- `docs/Documentacion_general/DATA_SOURCES.md`
- `docs/Documentacion_general/DATA_DICTIONARY.md`
- `docs/Concluciones/from_validaction_per_folder.md`
- `docs/Concluciones/from_validation_per_services.md`
- `docs/Concluciones/final_unification_per_services.md`
- `docs/Concluciones/from_unification_per_folder.md`

## 👨‍💻 Autor

Steven Alexander Patino Arenas  
Proyecto Final de Analisis de Datos, Mayo 2026.
