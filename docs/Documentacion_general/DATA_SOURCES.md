# Fuentes de Datos y Referencias

## 🌐 Fuente Principal

**NYC Taxi and Limousine Commission (TLC)**
- **URL**: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- **Descripción**: Base de datos oficial de viajes en taxi de Nueva York
- **Período cubierto**: 2009 - Presente
- **Frecuencia de actualización**: Mensual

## 📋 Tipos de Datos Disponibles

### 1. **Yellow Taxi (Medallion Taxi)**
- Taxis con licencia medallón tradicionales
- Operan principalmente en Manhattan
- Cobertura: Disponibles desde 2009
- **Disponibilidad en este proyecto**: 2013-2017

### 2. **Green Taxi (Street-Hail Livery)**
- Taxis verdes de servicio por calles
- Operan principalmente fuera de Manhattan (excepto aeropuertos)
- Cobertura: Disponibles desde 2010
- **Disponibilidad en este proyecto**: 2014-2017

### 3. **For-Hire Vehicle (Vehículos de Alquiler)**
- Servicios de transporte como Uber, Lyft
- Cobertura: Disponibles desde 2015
- **Disponibilidad en este proyecto**: 2015-2017

## 📅 Cobertura Temporal

| Servicio | 2013 | 2014 | 2015 | 2016 | 2017 |
|----------|:----:|:----:|:----:|:----:|:----:|
| Yellow Taxi | ✓ | ✓ | ✓ | ✓ | ✓ |
| Green Taxi | - | ✓ | ✓ | ✓ | ✓ |
| For-Hire | - | - | ✓ | ✓ | ✓ |

## 📊 Formato de Datos

- **Formato original**: CSV (disponible en sitio del TLC)
- **Formato utilizado en este proyecto**: Parquet (.parquet)
  - Compresión eficiente
  - Mejor rendimiento para análisis
  - Metadatos preservados

## 🔍 Granularidad de Datos

Los datasets se encuentran organizados:
- **Temporalmente**: Por año (2013, 2014, ..., 2017)
- **Por tipo de servicio**: yellow_taxi, green_taxi, for_hire_vehicle
- **Frecuencia**: Archivos mensuales (12 archivos por año/tipo cuando aplica)

### Estructura de Nomenclatura

Basada en estándares de NYC TLC:
```
{servicio}_tripdata_{año}-{mes}.parquet
```

**Ejemplos**:
- `yellow_tripdata_2013-01.parquet`
- `green_tripdata_2015-06.parquet`
- `for_hire_vehicle_tripdata_2017-12.parquet`

## 📖 Documentación de Referencia

### NYC TLC Resources
- **Official Data Dictionary**: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- **Descripción de campos**: Disponible en la página oficial de TLC
- **Actualizaciones**: Se publican regularmente

### Archivos Relacionados
- `DATA_DICTIONARY.md`: Definiciones detalladas de todas las columnas
- `PROCESSING_GUIDE.md`: Guía de procesamiento de datos

## ⚙️ Proceso de Descarga

Los datos se descargan desde el portal de TLC en formato CSV y se convierten a Parquet para este proyecto:

1. Acceder a https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
2. Descargar archivos mensuales por tipo de servicio
3. Convertir a formato Parquet
4. Organizar en estructura `datasets/{año}/{tipo_servicio}/`
5. Ejecutar validación con `scripts/validation.py`

## 📝 Notas Importantes

- **Privacidad**: Los datos han sido procesados para preservar privacidad (ej: licencias editadas)
- **Tamaño**: Los datasets completos pueden ser bastante grandes (~1GB+ por año)
- **Actualizaciones**: TLC ocasionalmente revisa o corrige datos históricos
- **Cambios de estructura**: Las columnas pueden variar ligeramente entre años

## 🔗 Enlaces Útiles

| Recurso | Enlace |
|---------|--------|
| TLC Data Page | https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page |
| Diccionario de Datos | https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page |
| Contacto TLC | https://www.nyc.gov/site/tlc/about/contact.page |

---

**Nota**: Este proyecto utiliza datos públicos proporcionados por NYC TLC bajo licencia pública.
