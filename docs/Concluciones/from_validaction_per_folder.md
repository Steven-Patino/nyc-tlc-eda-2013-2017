# Conclusiones de `validation_per_folder.py`

## Proposito

Este documento resume los hallazgos de `scripts/validation_per_folder.py`, que valida la estructura de los archivos Parquet dentro de cada carpeta de anio/servicio.

La version actual valida esquemas y conteos desde metadatos Parquet, sin cargar los datos completos en memoria.

## Resultado general

| Indicador | Resultado |
|---|---:|
| Carpetas validas | 12 |
| Carpetas con problemas | 0 |
| Periodo cubierto | 2013-2017 |
| Servicios cubiertos | Yellow Taxi, Green Taxi, For Hire Vehicle |

## Carpetas validadas

| Anio | Servicio | Estado |
|---|---|---|
| 2013 | yellow_taxi | Valida |
| 2014 | green_taxi | Valida |
| 2014 | yellow_taxi | Valida |
| 2015 | for_hire_vehicle | Valida |
| 2015 | green_taxi | Valida |
| 2015 | yellow_taxi | Valida |
| 2016 | for_hire_vehicle | Valida |
| 2016 | green_taxi | Valida |
| 2016 | yellow_taxi | Valida |
| 2017 | for_hire_vehicle | Valida |
| 2017 | green_taxi | Valida |
| 2017 | yellow_taxi | Valida |

## Observaciones clave

- Todas las carpetas disponibles son consistentes internamente.
- Las columnas no tienen que ser iguales entre servicios; la validacion compara archivos dentro de la misma carpeta.
- Las diferencias entre `yellow_taxi`, `green_taxi` y `for_hire_vehicle` son esperadas por la naturaleza de cada servicio.
- La validacion por metadatos es adecuada para este proyecto porque evita cargar archivos masivos en RAM.

## Configuracion

El script toma la ruta de entrada desde `NYC_TLC_RAW_DATA_DIR`, cargada automaticamente desde el archivo `.env` local.

Si la variable no existe, usa por defecto:

```text
raw_datasets
```

## Conclusion

El estado actual del dataset crudo es saludable para el flujo de unificacion: las 12 carpetas esperadas pasaron la validacion estructural interna.
