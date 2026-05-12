# 📚 Diccionario de datos

Este documento resume las columnas mas relevantes de los datasets NYC TLC usados en el proyecto. Las columnas pueden variar entre servicios y anios; la validacion exacta se realiza con `scripts/validation_per_folder.py`.

## Yellow Taxi y Green Taxi

| Grupo | Columnas frecuentes | Descripcion |
|---|---|---|
| Tiempo | `tpep_pickup_datetime`, `tpep_dropoff_datetime`, `lpep_pickup_datetime`, `lpep_dropoff_datetime` | Inicio y fin del viaje |
| Ubicacion | `pickup_location_id`, `dropoff_location_id`, `pulocationid`, `dolocationid` | Zonas de origen y destino |
| Viaje | `passenger_count`, `trip_distance`, `trip_type` | Caracteristicas operativas del viaje |
| Pago | `fare_amount`, `extra`, `mta_tax`, `tip_amount`, `tolls_amount`, `total_amount`, `payment_type` | Componentes de cobro |
| Proveedor | `vendorid`, `store_and_fwd_flag` | Proveedor y bandera de almacenamiento |

## For-Hire Vehicle

| Columna frecuente | Descripcion |
|---|---|
| `dispatching_base_num` | Base que despacho el viaje |
| `pickup_datetime` | Fecha/hora de recogida |
| `dropoff_datetime` | Fecha/hora de finalizacion, cuando existe |
| `pulocationid` | Zona de origen |
| `dolocationid` | Zona de destino |
| `sr_flag` | Indicador de viaje compartido, cuando existe |

## Codigos comunes

### `payment_type`

| Codigo | Significado |
|---:|---|
| 1 | Credit card |
| 2 | Cash |
| 3 | No charge |
| 4 | Dispute |
| 5 | Unknown |
| 6 | Voided trip |

### `ratecodeid`

| Codigo | Significado |
|---:|---|
| 1 | Standard rate |
| 2 | JFK |
| 3 | Newark |
| 4 | Nassau or Westchester |
| 5 | Negotiated fare |
| 6 | Group ride |

## Consideraciones

- El script de unificacion normaliza nombres de columnas a minusculas.
- Algunas columnas aparecen solo en ciertos anios o servicios.
- Para revisar la estructura real de cada carpeta, ejecutar:

```bash
uv run python scripts/validation_per_folder.py
```

La referencia oficial de campos esta en la pagina de NYC TLC indicada en `DATA_SOURCES.md`.
