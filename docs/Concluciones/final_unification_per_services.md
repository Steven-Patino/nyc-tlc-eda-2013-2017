# Resultados de `scripts/final_unification_per_services.py`

## 📌 Resumen del proceso

El script `final_unification_per_services.py` ejecutó la unificación final de los datasets consolidados por servicio, aplicando normalización de esquemas y manejo por batches para procesar más de 1,178 millones de filas sin agotar la memoria.

La unificación se realizó sobre los archivos en `outputs/new_datasets` y los resultados se guardaron en `outputs/final_datasets`.

## 📊 Hallazgos por servicio

### Yellow Taxi
- **Años procesados**: 2013, 2014, 2015, 2016, 2017
- **Grupos por año**:
  - 2013: 693 grupos
  - 2014: 669 grupos
  - 2015: 590 grupos
  - 2016: 530 grupos
  - 2017: 461 grupos
- **Total de registros**: 727,935,282
- **Observaciones**: El número de grupos disminuye con el tiempo, indicando posible reducción en volumen anual o mejor compresión.

### Green Taxi
- **Años procesados**: 2014, 2015, 2016, 2017
- **Grupos por año**:
  - 2014: 71 grupos
  - 2015: 84 grupos
  - 2016: 72 grupos
  - 2017: 53 grupos
- **Total de registros**: 63,193,374
- **Observaciones**: Dataset manejable para análisis detallados.

### For Hire Vehicle (FHV)
- **Años procesados**: 2015, 2016, 2017
- **Grupos por año**:
  - 2015: 259 grupos
  - 2016: 534 grupos
  - 2017: 775 grupos
- **Total de registros**: 387,812,173
- **Observaciones**: Crecimiento significativo, reflejando la expansión de servicios como Uber y Lyft.

## 📈 Volumen total procesado

- **Total de registros unificados**: 1,178,940,829
- **Servicios procesados**: 3 (yellow_taxi, green_taxi, for_hire_vehicle)
- **Archivos generados**: Ubicados en `outputs/final_datasets/`

## 🧠 Conclusiones

1. La unificación fue exitosa sin errores de memoria, confirmando la efectividad del manejo por batches.
2. Los esquemas se normalizaron correctamente, resolviendo las inconsistencias de tipos detectadas previamente.
3. Los volúmenes de datos son masivos, especialmente para Yellow Taxi y FHV, lo que requiere herramientas optimizadas para EDA.
4. El crecimiento en FHV refleja cambios en el mercado de transporte en NYC durante el período.

## ✅ Estado actual del proyecto

- Los datasets finales están listos en `outputs/final_datasets`.
- Se puede proceder a la fase de EDA y visualizaciones con datos consolidados y normalizados.