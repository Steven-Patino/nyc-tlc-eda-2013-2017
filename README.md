# EDA NYC TLC 2013-2017

Proyecto de analisis exploratorio de datos sobre viajes de la NYC Taxi and Limousine Commission (TLC), cubriendo Yellow Taxi, Green Taxi y For-Hire Vehicle entre 2013 y 2017.

## Estado actual

| Fase | Estado | Resultado |
|---|---|---|
| Validacion estructural | Completada | 12/12 carpetas validas |
| Unificacion por carpeta | Completada | 1,178,940,829 filas procesadas |
| Configuracion replicable | En progreso | Scripts configurables desde `.env` |
| EDA y visualizaciones | Pendiente | Por implementar |

## Datos procesados

| Servicio | Filas totales | Porcentaje |
|---|---:|---:|
| Yellow Taxi | 727,935,282 | 61.7% |
| For Hire Vehicle (FHV) | 387,812,173 | 32.9% |
| Green Taxi | 63,193,374 | 5.4% |
| **Total** | **1,178,940,829** | **100%** |

## Requisitos

- Python 3.13+
- uv de Astral
- Datos Parquet de NYC TLC organizados por anio y servicio
- Espacio en disco suficiente para datos crudos y salidas unificadas

Las dependencias estan declaradas en `pyproject.toml` y se instalan con `uv sync`.

## Instalacion en Windows

```powershell
git clone <URL_DEL_REPOSITORIO>
cd EDA_2013_to_2017
uv sync
```

Crear el archivo local de configuracion:

```powershell
Copy-Item .env.example .env
```

Edita `.env` y ajusta las rutas si tus datos no estan dentro del proyecto.

Ejecutar validacion:

```powershell
uv run python .\scripts\validation_per_folder.py
```

Ejecutar unificacion:

```powershell
uv run python .\scripts\unification_per_folder.py
```

## Instalacion en Ubuntu

Instalar `uv` si no lo tienes:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Clonar e instalar dependencias:

```bash
git clone <URL_DEL_REPOSITORIO>
cd EDA_2013_to_2017
uv sync
```

Crear el archivo local de configuracion:

```bash
cp .env.example .env
```

Edita `.env`:

```bash
nano .env
```

Ejecutar validacion:

```bash
uv run python scripts/validation_per_folder.py
```

Ejecutar unificacion:

```bash
uv run python scripts/unification_per_folder.py
```

## Configuracion con `.env`

Los scripts cargan automaticamente el archivo `.env` ubicado en la raiz del proyecto. El `.env` real esta ignorado por Git para no publicar rutas personales.

Plantilla:

```env
NYC_TLC_RAW_DATA_DIR=raw_datasets
NYC_TLC_OUTPUT_DIR=outputs/new_datasets
NYC_TLC_BATCH_SIZE=250000
```

Puedes usar rutas relativas al proyecto o rutas absolutas de tu equipo.

| Variable | Uso | Valor sugerido |
|---|---|---|
| `NYC_TLC_RAW_DATA_DIR` | Carpeta con datos crudos organizados por anio/servicio | `raw_datasets` |
| `NYC_TLC_OUTPUT_DIR` | Carpeta de salida para Parquet unificados | `outputs/new_datasets` |
| `NYC_TLC_BATCH_SIZE` | Filas por batch durante la unificacion | `250000` |

Para equipos con poca RAM, prueba:

```env
NYC_TLC_BATCH_SIZE=100000
```

Para equipos con mas RAM, puedes probar:

```env
NYC_TLC_BATCH_SIZE=500000
```

## Estructura esperada de datos

```text
raw_datasets/
  2013/
    yellow_taxi/
      *.parquet
  2014/
    green_taxi/
      *.parquet
    yellow_taxi/
      *.parquet
  2015/
    for_hire_vehicle/
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

Los archivos `.parquet` no se suben al repositorio. Cada persona debe descargar o ubicar los datos localmente y configurar `NYC_TLC_RAW_DATA_DIR` en su `.env`.

## Scripts

| Script | Funcion |
|---|---|
| `scripts/validation_per_folder.py` | Valida esquemas Parquet por carpeta usando metadatos, sin cargar datasets completos |
| `scripts/unification_per_folder.py` | Unifica archivos mensuales por anio/servicio usando batches para cuidar la RAM |

## Salidas

La unificacion escribe archivos en:

```text
outputs/new_datasets/{anio}/{servicio}.parquet
```

Ejemplos:

```text
outputs/new_datasets/2017/yellow_taxi.parquet
outputs/new_datasets/2017/green_taxi.parquet
outputs/new_datasets/2017/for_hire_vehicle.parquet
```

## Documentacion

- `docs/Documentacion_general/PROJECT_OVERVIEW.md`
- `docs/Documentacion_general/PROCESSING_GUIDE.md`
- `docs/Documentacion_general/DATA_SOURCES.md`
- `docs/Documentacion_general/DATA_DICTIONARY.md`
- `docs/Concluciones/from_validaction_per_folder.md`
- `docs/Concluciones/from_unification_per_folder.md`

## Fuente de datos

NYC Taxi and Limousine Commission:

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

## Autor

Steven Alexander Patino Arenas - Proyecto Final de Analisis de Datos, Mayo 2026.
