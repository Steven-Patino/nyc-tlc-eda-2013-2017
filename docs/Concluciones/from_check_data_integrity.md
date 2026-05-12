# 🧪 Conclusiones de `scripts/check_data_integrity.py`

**Resumen rápido:** la auditoría de datos final se ejecutó correctamente y confirmó la integridad temporal del periodo 2013-2017, junto con la identificación de columnas con alta tasa de nulos.

## 📌 Resumen de ejecución
- `scripts/check_data_integrity.py` se ejecutó con éxito en el entorno virtual.
- Total de filas inspeccionadas:
  - `yellow_taxi.parquet`: 614,434,955 filas (~8.25 GB)
  - `green_taxi.parquet`: 51,456,315 filas (~1.01 GB)
  - `for_hire_vehicle.parquet`: 195,502,615 filas (~0.84 GB)
- Tiempo total de ejecución: **4.78 minutos**.

## 🔎 Hallazgos clave

### 1. Columnas con nulos masivos
Estas columnas tienen valores ausentes en el 100% o casi el 100% de los registros, lo que sugiere que no aportan valor en el periodo 2013-2017.

- `congestion_surcharge`: 100% nulo en `yellow_taxi` y `green_taxi`
- `airport_fee`: 100% nulo en `yellow_taxi`
- `ehail_fee`: 100% nulo en `green_taxi`
- `sr_flag`: 100% nulo en `for_hire_vehicle`

> Recomendación: eliminar estas columnas durante el preprocesamiento para reducir dimensionalidad y mejorar eficiencia.

### 2. Observaciones por servicio

#### 🚕 Yellow Taxi
- `store_and_fwd_flag`: 22.06% nulo. No es crítico; indica viajes en los que no se registró el almacenamiento temporal de la información.
- `improvement_surcharge`: 8.75% nulo. Este cargo se introdujo a mitad de periodo, por lo que es lógico que registros anteriores no lo contengan.

#### 🟢 Green Taxi
- `trip_type`: 3.46% nulo. Baja tasa de ausentes; el campo es útil para segmentaciones entre viajes de calle y por despacho.
- `improvement_surcharge`: 27.58% nulo. Refleja la misma evolución normativa que en yellow taxi.

#### 🚙 For-Hire Vehicle (FHV)
- `dolocationid`: 98.50% nulo. Indica que casi no se registró el destino de los viajes FHV.
- `pulocationid`: 29.22% nulo. Alrededor de 57 millones de viajes sin origen geográfico.
- `affiliated_base_number`: 6 nulos, irrelevante por su baja incidencia.

> Alerta crítica: el 29.22% de nulos en `pulocationid` limita el uso de FHV para análisis geográficos.

### 3. Integridad temporal
- Ningún registro fuera del periodo 2013-2017.
- Las fechas de recogida (`tpep_pickup_datetime`, `lpep_pickup_datetime`, `pickup_datetime`) son consistentes y están dentro del rango esperado.

> Resultado: la auditoría temporal es una victoria; los procesos previos de filtrado funcionaron correctamente.

## 🧠 Conclusiones estratégicas

1. Los datasets están bien acotados al periodo 2013-2017.
2. Existen columnas “fantasma” que conviene eliminar para optimizar almacenamiento y procesamiento.
3. FHV presenta una debilidad importante en calidad geográfica, por lo que:
   - debe evaluarse el uso de una versión filtrada para análisis espaciales;
   - o bien usarse solo para análisis no geoespaciales y de volumen.
4. La ausencia de datos en `improvement_surcharge` es coherente con cambios regulatorios, no es un error de corrupción de datos.

## ✅ Recomendaciones siguientes

- Eliminar columnas con >95% de nulos: `congestion_surcharge`, `airport_fee`, `ehail_fee`, `sr_flag`.
- Mantener `trip_type` en green taxi como campo de segmentación útil.
- Crear una versión filtrada de FHV para análisis geoespaciales y otra versión completa para análisis de volumen.
- Reintentar la auditoría de duplicados en un entorno con más RAM o usando herramientas de streaming, especialmente para `for_hire_vehicle`.

## 📎 Referencias
- Script: `scripts/check_data_integrity.py`
- Documento de soporte: `docs/Concluciones/from_check_data_integrity.md`

## 📝 Nota final
La auditoría entregó una radiografía clara de la calidad de los datos y deja un camino definido para simplificar columnas y manejar la falta de datos geográficos en FHV.
