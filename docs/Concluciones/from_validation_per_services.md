# Resultados de `scripts/validation_per_service.py`

## 📌 Resumen del análisis

La validación por servicio se ejecutó sobre los archivos consolidados en:

`outputs/new_datasets`

El rango de años detectado fue: **2013 - 2017**.

## 📊 Resultados generales

- Servicios inspeccionados: `yellow_taxi.parquet`, `green_taxi.parquet`, `for_hire_vehicle.parquet`
- Servicios consistentes: **0**
- Servicios con inconsistencia: **3**

## 🔍 Hallazgos principales

### `yellow_taxi.parquet`
- Años presentes: `2013`, `2014`, `2015`, `2016`, `2017`
- Inconsistencias detectadas:
  - `congestion_surcharge` cambia de `double` a `null` en `2015`, `2016` y `2017`.
- Implicación:
  - Aunque la columna existe en todos los años, no mantiene un tipo de dato único.
  - Esto impide una unión directa sin normalizar previamente el esquema.

### `green_taxi.parquet`
- Años presentes: `2014`, `2015`, `2016`, `2017`
- Años faltantes: `2013`
- Inconsistencias detectadas:
  - `congestion_surcharge` cambia de `null` a `double` en `2016`.
- Implicación:
  - El esquema es inconsistente entre años y el dato no se puede tratar como un campo uniforme sin homogeneizar el tipo.

### `for_hire_vehicle.parquet`
- Años presentes: `2015`, `2016`, `2017`
- Años faltantes: `2013`, `2014`
- Inconsistencias detectadas:
  - `sr_flag` cambia de `null` a `double` en `2017`.
- Implicación:
  - La columna está presente, pero su tipo no es estable entre los años analizados.

## 🧠 Conclusiones

1. El resultado muestra que los archivos homónimos no son completamente compatibles entre años.
2. La principal causa es la existencia de columnas con el mismo nombre pero con tipos distintos:
   - `congestion_surcharge` en `yellow_taxi` y `green_taxi`
   - `sr_flag` en `for_hire_vehicle`
3. No se detectaron columnas faltantes ni sobrantes entre los años presentes. Todas las columnas definidas en la referencia aparecen también en los demás archivos.
4. El resto de columnas que no aparecen en el reporte de errores mantiene el mismo tipo de dato entre años.
5. Por tanto, el pipeline no debe unir directamente los archivos sin una etapa de normalización de tipos.

## ✅ Recomendaciones

- Normalizar todos los esquemas antes de generar datasets consolidados.
- Convertir las columnas `null`/`double` a un único tipo consistente (por ejemplo, `double` con valores nulos explícitos).
- Agregar la validación por servicio a la revisión posterior a la unificación.
- Revisar específicamente las columnas:
  - `congestion_surcharge`
  - `sr_flag`

## 📌 Estado actual del proyecto

- La validación estructural ya está completa.
- La unificación por carpeta se realizó, pero la validación por servicio detectó problemas de tipo.
- Antes de avanzar a EDA y visualizaciones, es necesario corregir estas diferencias de esquema.
