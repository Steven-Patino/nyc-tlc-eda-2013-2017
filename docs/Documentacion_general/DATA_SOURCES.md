# 🌐 Fuentes de datos

## Fuente oficial

Los datos provienen de la **NYC Taxi and Limousine Commission (TLC)**:

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

## Cobertura usada en este proyecto

| Servicio | Periodo incluido | Carpeta |
|---|---|---|
| Yellow Taxi | 2013-2017 | `yellow_taxi` |
| Green Taxi | 2014-2017 | `green_taxi` |
| For-Hire Vehicle | 2015-2017 | `for_hire_vehicle` |

## Ubicacion local

Los archivos descargados deben ubicarse en:

```text
raw_datasets/{anio}/{servicio}/*.parquet
```

La arquitectura exacta esta documentada en el README principal y en `raw_datasets/DATA_LAYOUT.md`.

## Notas

- Los archivos de datos no se versionan por su tamano.
- TLC puede publicar correcciones historicas; por eso conviene registrar la fecha de descarga cuando se cierre el analisis final.
- Este proyecto trabaja con Parquet para reducir espacio y mejorar rendimiento.
