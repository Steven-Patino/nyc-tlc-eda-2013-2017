# 🚕 EDA NYC TLC 2013-2017

![Python](https://img.shields.io/badge/Python-3.13+-3776AB)
![Status](https://img.shields.io/badge/status-processing%20ready-2EA44F)
![Dataset](https://img.shields.io/badge/dataset-NYC%20TLC-orange)

## 📌 Descripcion

Este proyecto prepara una base de datos historica de viajes de NYC TLC para analisis exploratorio. El periodo cubierto es 2013-2017 e incluye Yellow Taxi, Green Taxi y For-Hire Vehicle.

## 🎯 Objetivos

- Validar la integridad estructural de los archivos Parquet.
- Unificar archivos mensuales por anio y servicio.
- Mantener un flujo replicable con `uv` y variables de entorno.
- Preparar datos consolidados para EDA, visualizaciones y reportes.

## 🧩 Estado del proyecto

| Fase | Estado |
|---|---|
| Validacion de carpetas | Completada |
| Unificacion por anio/servicio | Completada |
| Documentacion de flujo replicable | En progreso |
| Analisis exploratorio | Pendiente |
| Visualizaciones | Pendiente |

## 🗓️ Cobertura de datos

| Anio | Yellow Taxi | Green Taxi | For-Hire Vehicle |
|---|:---:|:---:|:---:|
| 2013 | Si | No | No |
| 2014 | Si | Si | No |
| 2015 | Si | Si | Si |
| 2016 | Si | Si | Si |
| 2017 | Si | Si | Si |

## 📊 Volumen consolidado

| Servicio | Filas totales | Porcentaje |
|---|---:|---:|
| Yellow Taxi | 727,935,282 | 61.7% |
| For Hire Vehicle | 387,812,173 | 32.9% |
| Green Taxi | 63,193,374 | 5.4% |
| **Total** | **1,178,940,829** | **100%** |

## 🗂️ Estructura principal

```text
EDA_2013_to_2017/
  README.md
  pyproject.toml
  uv.lock
  scripts/
    validation_per_folder.py
    unification_per_folder.py
  docs/
    Concluciones/
    Documentacion_general/
  raw_datasets/       # local, ignorado por Git
  outputs/            # local, ignorado por Git
```

## ⚙️ Configuracion

Los scripts cargan estas variables desde el archivo `.env` local:

| Variable | Descripcion |
|---|---|
| `NYC_TLC_RAW_DATA_DIR` | Ruta a datos crudos Parquet |
| `NYC_TLC_OUTPUT_DIR` | Ruta de salida para datos unificados |
| `NYC_TLC_BATCH_SIZE` | Filas por batch durante unificacion |

## 🛠️ Tecnologia

- Python 3.13+
- uv
- PyArrow
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Fastparquet

## 🔗 Referencia

Datos publicos de NYC Taxi and Limousine Commission:

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
