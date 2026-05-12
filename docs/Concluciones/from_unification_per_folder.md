# 📦 Conclusiones de `unification_per_folder.py`

![Resultado](https://img.shields.io/badge/Resultado-12%2F12%20carpetas%20unificadas-2EA44F)
![Filas](https://img.shields.io/badge/Filas-1.17B-blue)
![Formato](https://img.shields.io/badge/Formato-Parquet-0A7EA4)

## 🎯 Proposito

Este documento resume los resultados obtenidos al ejecutar `scripts/unification_per_folder.py`, encargado de unificar los archivos Parquet mensuales por carpeta de anio y servicio.

El proceso toma como entrada la estructura de datos crudos y genera un unico archivo Parquet por servicio/anio en `outputs/new_datasets`.

## ✅ Resultado general

La ejecucion final completo la unificacion de las 12 carpetas esperadas para el periodo 2013-2017.

| Indicador | Resultado |
|---|---:|
| Carpetas procesadas | 12 |
| Carpetas unificadas | 12 |
| Carpetas con error | 0 |
| Filas procesadas | 1,178,940,829 |
| Formato de salida | Parquet |
| Compresion | Snappy |

## 🚕 Desglose por servicio

| Servicio | Filas totales | Porcentaje del total |
|---|---:|---:|
| Yellow Taxi | 727,935,282 | 61.7% |
| For Hire Vehicle (FHV) | 387,812,173 | 32.9% |
| Green Taxi | 63,193,374 | 5.4% |
| **Total** | **1,178,940,829** | **100%** |

## 🔎 Observaciones clave

- `yellow_taxi` concentra la mayor parte del volumen, con aproximadamente 61.7% de los registros.
- `for_hire_vehicle` representa casi un tercio del dataset consolidado.
- `green_taxi` es el servicio con menor volumen relativo, pero sigue aportando mas de 63 millones de registros.
- La unificacion por carpetas permite trabajar con archivos consolidados por anio/servicio sin mezclar estructuras incompatibles entre servicios.

## 🧰 Mejoras aplicadas al script

- Lectura por batches con `iter_batches`, evitando cargar archivos completos en RAM.
- Normalizacion de nombres de columnas a minusculas para reducir duplicados por diferencias de casing.
- Unificacion de tipos numericos, nulos, strings y timestamps.
- Escritura segura con `ParquetWriter` dentro de un bloque `with`.
- Configuracion por archivo `.env` local:
  - `NYC_TLC_RAW_DATA_DIR`
  - `NYC_TLC_OUTPUT_DIR`
  - `NYC_TLC_BATCH_SIZE`
- Prints mas informativos para seguir el avance por carpeta, archivo, batch y filas acumuladas.

## 🏁 Conclusiones

El proceso de unificacion quedo funcional para datos masivos y es mas resiliente frente a problemas de memoria. El resultado actual deja una base consolidada de mas de 1.17 mil millones de viajes, lista para validaciones posteriores y analisis exploratorio.

Para ejecuciones futuras, se recomienda conservar el procesamiento por batches y ajustar `NYC_TLC_BATCH_SIZE` segun la RAM disponible.
