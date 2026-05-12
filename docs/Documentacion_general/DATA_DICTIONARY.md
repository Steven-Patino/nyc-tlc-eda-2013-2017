# Diccionario de Datos - NYC TLC Trip Records

## 📋 Descripción General

Este documento describe todas las columnas presentes en los datasets de NYC TLC. Las columnas pueden variar ligeramente entre tipos de servicio (Yellow, Green, For-Hire) y años.

---

## 🟨 Yellow Taxi & Green Taxi - Columnas Comunes

### Fecha y Hora

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `tpep_pickup_datetime` | DateTime | Fecha y hora de inicio del viaje |
| `tpep_dropoff_datetime` | DateTime | Fecha y hora de fin del viaje |

### Ubicación

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `pickup_location_id` | Int | ID de zona de recogida (referencia a lookup table) |
| `dropoff_location_id` | Int | ID de zona de destino (referencia a lookup table) |
| `RatecodeID` | Int | Código de tarifa (1=Standard, 2=JFK, 3=Newark, etc.) |

### Características del Viaje

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `passenger_count` | Int | Número de pasajeros (1-9+) |
| `trip_distance` | Float | Distancia del viaje en millas |
| `trip_type` | Int | Tipo de viaje (1=Street-hail, 2=Dispatch) - Aplica a Green |

### Montos Financieros

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `fare_amount` | Float | Tarifa base según el taxímetro ($) |
| `extra` | Float | Cargas adicionales: $0.50 (rush hour), $1 (overnight) |
| `mta_tax` | Float | Impuesto MTA: $0.50 por viaje |
| `tip_amount` | Float | Propina (generalmente $0 en tarjeta de crédito) |
| `tolls_amount` | Float | Montos pagados por peajes |
| `total_amount` | Float | Cantidad total cobrada = fare + extra + mta_tax + tip + tolls |

### Método de Pago

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `payment_type` | Int | 1=Credit card, 2=Cash, 3=No charge, 4=Dispute, 5=Unknown, 6=Voided trip |

### Información del Vehículo

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `VendorID` | Int | Identificador del proveedor de datos (1=Creative Mobile, 2=VeriFone) |
| `congestion_surcharge` | Float | Recargo de congestión ($0 o $2.50) - Agregado en 2019 |

---

## 🟢 Green Taxi - Columnas Adicionales

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `store_and_fwd_flag` | String | Y/N - Indica si el viaje fue almacenado temporalmente |

---

## 🚗 For-Hire Vehicle - Estructura Similar

Formato similar a Yellow/Green con algunas variaciones:
- Puede incluir o excluir ciertos campos
- Estructura de ubicación similar (location_id)
- Montos financieros similares

---

## 📊 Códigos y Valores de Referencia

### RatecodeID (Código de Tarifa)

```
1 = Standard rate
2 = JFK
3 = Newark
4 = Nassau or Westchester
5 = Negotiated fare
6 = Group ride
```

### Payment Type (Tipo de Pago)

```
1 = Credit card
2 = Cash
3 = No charge
4 = Dispute
5 = Unknown
6 = Voided trip
```

### VendorID (Proveedor de Datos)

```
1 = Creative Mobile Technologies, LLC
2 = VeriFone Inc.
```

### Trip Type (Tipo de Viaje - Green Taxi)

```
1 = Street-hail
2 = Dispatch
```

---

## 📐 Estadísticas Típicas (Yellow Taxi 2013-2017)

| Métrica | Rango Típico | Notas |
|---------|--------------|-------|
| **passenger_count** | 1-6 | Mayoría viajes de 1 pasajero |
| **trip_distance** | 0.1-50 millas | Mayoría < 10 millas |
| **fare_amount** | $2.50-$100 | Varía con distancia y hora |
| **tip_amount** | $0-$20+ | Típicamente 15-20% de tarifa |
| **total_amount** | $3-$150+ | Depende de tarifa y propina |

---

## ⚠️ Notas Importantes

### Datos Faltantes
- Algunos registros pueden tener valores NULL en campos opcionales
- `trip_type`, `congestion_surcharge` pueden no estar en años anteriores

### Variaciones por Año
- **2013**: Estructura base de Yellow Taxi
- **2014**: Green Taxi agregado
- **2015+**: For-Hire Vehicle agregado
- **2019+**: Se agrega `congestion_surcharge`

### Cambios de Ubicación
- **Antes de 2015**: Pueden usar lat/long en lugar de location_id
- **2015+**: Cambio a system de location_id

### Consideraciones de Privacidad
- Todas las licencias han sido editadas
- Datos de ubicación agregados a nivel de zona
- Sin información personal de pasajeros

---

## 🔍 Validación de Datos

Consultar `scripts/validation.py` para verificar que todos los archivos en una carpeta mantengan la misma estructura de columnas.

**Ejecutar validación**:
```bash
python scripts/validation.py
```

---

**Última actualización**: Mayo 2026
