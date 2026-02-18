# Electronic Sensor Network Documentation

## Overview

This project contains schemas and data formats for a comprehensive electronic sensor network that monitors environmental parameters and air quality. The system collects data from various sensors deployed across different locations to provide real-time environmental monitoring.

## Supported Sensors

### 1. PMS5003 - Particulate Matter Sensor

**Purpose**: Monitors air quality by detecting particulate matter of different sizes.

**Data Schema**:
```json
{
  "sensor_id": "pms5003_01",
  "timestamp": "2026-02-18T12:00:00Z",
  "pm": {
    "pm1_0": 12.3,
    "pm2_5": 25.6,
    "pm10": 45.1,
    "particles_0_3um": 10234,
    "particles_0_5um": 5432,
    "particles_1_0um": 1234,
    "particles_2_5um": 567,
    "particles_5_0um": 45,
    "particles_10um": 12
  },
  "location": "living_room"
}
```

**Field Descriptions**:
- `sensor_id` (string): Unique identifier for the sensor
- `timestamp` (ISO 8601 string): UTC timestamp of measurement
- `pm1_0` (float): Particulate matter ≤ 1.0 μm (µg/m³)
- `pm2_5` (float): Particulate matter ≤ 2.5 μm (µg/m³) - Fine particles
- `pm10` (float): Particulate matter ≤ 10 μm (µg/m³) - Coarse particles
- `particles_0_3um` (integer): Particle count ≤ 0.3 μm per 0.1L
- `particles_0_5um` (integer): Particle count ≤ 0.5 μm per 0.1L
- `particles_1_0um` (integer): Particle count ≤ 1.0 μm per 0.1L
- `particles_2_5um` (integer): Particle count ≤ 2.5 μm per 0.1L
- `particles_5_0um` (integer): Particle count ≤ 5.0 μm per 0.1L
- `particles_10um` (integer): Particle count ≤ 10 μm per 0.1L
- `location` (string): Physical location of sensor

---

### 2. ENS160 - Indoor Air Quality Sensor

**Purpose**: Monitors volatile organic compounds (VOC) and carbon dioxide equivalent levels with temperature and humidity sensing.

**Data Schema**:
```json
{
  "sensor_id": "ens160_01",
  "timestamp": "2026-02-18T12:00:00Z",
  "iaq": {
    "voc_index": 45,
    "eco2": 620,
    "temperature": 23.5,
    "humidity": 45.2
  },
  "location": "office"
}
```

**Field Descriptions**:
- `sensor_id` (string): Unique identifier for the sensor
- `timestamp` (ISO 8601 string): UTC timestamp of measurement
- `voc_index` (integer): Volatile Organic Compound index (0-500, higher indicates more pollution)
- `eco2` (integer): Estimated CO₂ equivalent (ppm)
- `temperature` (float): Ambient temperature (°C)
- `humidity` (float): Relative humidity (%)
- `location` (string): Physical location of sensor

---

### 3. SCD41 - CO₂ Sensor

**Purpose**: Measures carbon dioxide concentration with integrated temperature and humidity sensing.

**Data Schema**:
```json
{
  "sensor_id": "scd41_01",
  "timestamp": "2026-02-18T12:00:00Z",
  "co2": {
    "ppm": 415,
    "temperature": 23.4,
    "humidity": 44.8
  },
  "location": "office"
}
```

**Field Descriptions**:
- `sensor_id` (string): Unique identifier for the sensor
- `timestamp` (ISO 8601 string): UTC timestamp of measurement
- `ppm` (integer): CO₂ concentration (parts per million)
- `temperature` (float): Ambient temperature (°C)
- `humidity` (float): Relative humidity (%)
- `location` (string): Physical location of sensor

---

### 4. SEN0441 - Formaldehyde Sensor

**Purpose**: Detects formaldehyde (HCHO) levels in indoor environments.

**Data Schema**:
```json
{
  "sensor_id": "sen0441_01",
  "timestamp": "2026-02-18T12:00:00Z",
  "hcho": {
    "ppm": 0.05,
    "temperature": 23.5,
    "humidity": 45.0
  },
  "location": "bedroom"
}
```

**Field Descriptions**:
- `sensor_id` (string): Unique identifier for the sensor
- `timestamp` (ISO 8601 string): UTC timestamp of measurement
- `ppm` (float): Formaldehyde concentration (parts per million)
- `temperature` (float): Ambient temperature (°C)
- `humidity` (float): Relative humidity (%)
- `location` (string): Physical location of sensor

---

### 5. BME280 - Environmental Sensor

**Purpose**: Measures atmospheric pressure, temperature, and humidity.

**Data Schema**:
```json
{
  "sensor_id": "bme280_01",
  "timestamp": "2026-02-18T12:00:00Z",
  "environment": {
    "temperature": 23.5,
    "humidity": 45.2,
    "pressure": 1013.2
  },
  "location": "living_room"
}
```

**Field Descriptions**:
- `sensor_id` (string): Unique identifier for the sensor
- `timestamp` (ISO 8601 string): UTC timestamp of measurement
- `temperature` (float): Ambient temperature (°C)
- `humidity` (float): Relative humidity (%)
- `pressure` (float): Atmospheric pressure (hPa)
- `location` (string): Physical location of sensor

---

### 6. DS18B20 - Temperature Sensor

**Purpose**: Dedicated digital temperature sensor with high accuracy, ideal for outdoor monitoring.

**Data Schema**:
```json
{
  "sensor_id": "ds18b20_01",
  "timestamp": "2026-02-18T12:00:00Z",
  "temperature": 22.8,
  "location": "outdoor_sensor"
}
```

**Field Descriptions**:
- `sensor_id` (string): Unique identifier for the sensor
- `timestamp` (ISO 8601 string): UTC timestamp of measurement
- `temperature` (float): Ambient temperature (°C)
- `location` (string): Physical location of sensor

---

## Common Fields

All sensor readings include these common fields:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `sensor_id` | string | Unique identifier for the sensor | `pms5003_01` |
| `timestamp` | ISO 8601 | UTC timestamp of measurement | `2026-02-18T12:00:00Z` |
| `location` | string | Physical location of sensor | `living_room` |

---

## Data Units Reference

| Parameter | Unit | Description |
|-----------|------|-------------|
| Particulate Matter | µg/m³ | Micrograms per cubic meter |
| CO₂ / eCO₂ | ppm | Parts per million |
| Volatile Organics | Index | 0-500 scale |
| Temperature | °C | Degrees Celsius |
| Humidity | % | Relative humidity percentage |
| Pressure | hPa | Hectopascals |
| Particles | count/0.1L | Particle count per 0.1 liters |
