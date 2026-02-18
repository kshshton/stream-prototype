# MQTT Sensor Backend Server

A Python backend server that simulates multiple electronic sensors and publishes their data via MQTT (Eclipse Mosquitto broker).

## Features

- **Multiple Sensor Types**: Simulates 6 different sensor types (PMS5003, ENS160, SCD41, SEN0441, BME280, DS18B20)
- **MQTT Publishing**: Publishes sensor readings to configurable MQTT topics
- **Configurable Intervals**: Adjustable sensor read interval
- **Graceful Shutdown**: Proper signal handling for clean server termination
- **Docker Support**: Includes Docker Compose for easy Mosquitto deployment

## Supported Sensors

1. **PMS5003** - Particulate Matter Sensor
   - Topic: `sensors/pms5003/pms5003_01`
   - Location: `living_room`

2. **ENS160** - Indoor Air Quality Sensor
   - Topic: `sensors/ens160/ens160_01`
   - Location: `office`

3. **SCD41** - CO₂ Sensor
   - Topic: `sensors/scd41/scd41_01`
   - Location: `office`

4. **SEN0441** - Formaldehyde Sensor
   - Topic: `sensors/sen0441/sen0441_01`
   - Location: `bedroom`

5. **BME280** - Environmental Sensor
   - Topic: `sensors/bme280/bme280_01`
   - Location: `living_room`

6. **DS18B20** - Temperature Sensor
   - Topic: `sensors/ds18b20/ds18b20_01`
   - Location: `outdoor_sensor`

## Project Structure

```
stream-prototype/
├── main.py                 # Main server script
├── config.py              # Configuration settings
├── mqtt_client.py         # MQTT client wrapper
├── requirements.txt       # Python dependencies
├── mosquitto.conf         # Mosquitto broker configuration
├── docker-compose.yml     # Docker Compose file for Mosquitto
├── .env.example          # Environment variables example
└── sensors/              # Sensor implementations
    ├── __init__.py
    ├── base_sensor.py    # Base sensor class
    ├── pms5003.py
    ├── ens160.py
    ├── scd41.py
    ├── sen0441.py
    ├── bme280.py
    └── ds18b20.py
```

## Prerequisites

- Python 3.7+
- Docker & Docker Compose (for running Mosquitto)
- OR an existing MQTT broker running elsewhere

## Installation

### 1. Clone the Repository

```bash
cd c:\Users\owenk\Documents\Projects\stream-prototype
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment (Optional)

```bash
cp .env.example .env
```

Edit `.env` if needed to change MQTT broker settings.

## Usage

### Option 1: Using Docker Compose (Recommended)

#### Start Mosquitto Broker

```bash
docker-compose up -d
```

This will start the Eclipse Mosquitto MQTT broker on:
- **MQTT**: `tcp://localhost:1883`
- **WebSocket**: `ws://localhost:9001`

#### Start the Sensor Server

```bash
python main.py
```

### Option 2: Using Existing MQTT Broker

If you already have an MQTT broker running:

1. Update `config.py` or create a `.env` file:
   ```
   MQTT_BROKER=your-broker-ip
   MQTT_PORT=1883
   ```

2. Run the server:
   ```bash
   python main.py
```

## MQTT Topic Structure

All sensor data is published to: `sensors/{sensor_type}/{sensor_id}`

### Examples

- `sensors/pms5003/pms5003_01` - Particulate matter readings
- `sensors/ens160/ens160_01` - Air quality readings
- `sensors/scd41/scd41_01` - CO₂ readings
- `sensors/sen0441/sen0441_01` - Formaldehyde readings
- `sensors/bme280/bme280_01` - Environmental readings
- `sensors/ds18b20/ds18b20_01` - Temperature readings

## Message Format

All messages are published as JSON with the following structure:

```json
{
  "sensor_id": "pms5003_01",
  "timestamp": "2026-02-18T12:00:00Z",
  "location": "living_room",
  "pm": {
    "pm1_0": 12.3,
    "pm2_5": 25.6,
    ...
  }
}
```

## Configuration

### Environment Variables

Edit `.env` file to customize:

| Variable | Default | Description |
|----------|---------|-------------|
| `MQTT_BROKER` | localhost | MQTT broker address |
| `MQTT_PORT` | 1883 | MQTT port |
| `MQTT_USER` | (empty) | MQTT username (optional) |
| `MQTT_PASSWORD` | (empty) | MQTT password (optional) |
| `MQTT_BASE_TOPIC` | sensors | Base topic for all sensors |
| `SENSOR_READ_INTERVAL` | 5 | Seconds between readings |

### Active Sensors

In `config.py`, modify `ACTIVE_SENSORS` to enable/disable sensors:

```python
ACTIVE_SENSORS = {
    "pms5003": True,      # Enable
    "ens160": True,
    "scd41": False,       # Disable
    ...
}
```

### Sensor Locations

Customize sensor locations in `config.py`:

```python
SENSOR_LOCATIONS = {
    "pms5003": "living_room",
    "ens160": "office",
    ...
}
```

## Testing MQTT Messages

### Using Docker (mosquitto_sub)

```bash
# Subscribe to all sensor messages
docker exec mosquitto-broker mosquitto_sub -h localhost -t "sensors/#" -v

# Subscribe to specific sensor
docker exec mosquitto-broker mosquitto_sub -h localhost -t "sensors/pms5003/#" -v
```

### Using Python mqtt Client

```python
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    print(f"Topic: {msg.topic}, Payload: {msg.payload.decode()}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.subscribe("sensors/#")
client.loop_forever()
```

### Using MQTT.js (Node.js)

```bash
npm install mqtt
```

```javascript
const mqtt = require('mqtt');
const client = mqtt.connect('mqtt://localhost:1883');

client.on('connect', () => {
  client.subscribe('sensors/#', (err) => {
    if (!err) console.log('Subscribed');
  });
});

client.on('message', (topic, message) => {
  console.log(`Topic: ${topic}, Message: ${message}`);
});
```

## Stopping the Server

### Graceful Shutdown

Press `Ctrl+C` in the terminal running the server. The server will:
1. Receive the interrupt signal
2. Disconnect from MQTT broker
3. Clean up resources
4. Exit gracefully

### Stop Docker Compose (Mosquitto)

```bash
docker-compose down
```

Remove volumes if you want to clear persisted data:

```bash
docker-compose down -v
```

## Logging

The server logs:
- Connection status to MQTT broker
- Sensor initialization
- Data publication events
- Errors and warnings

Log level can be changed in `main.py`:

```python
logging.basicConfig(level=logging.DEBUG)  # For more verbose output
```

## Troubleshooting

### Connection Refused

**Error**: `Connection refused` when connecting to MQTT broker

**Solution**:
- Ensure Mosquitto is running: `docker ps | grep mosquitto`
- Check `MQTT_BROKER` and `MQTT_PORT` in config
- If using remote broker, ensure it's accessible

### No Data Published

**Error**: Data is not appearing in MQTT topics

**Solution**:
- Check server status: `python main.py` should show "Sensor Server started"
- Verify MQTT connection: should see "Successfully connected to MQTT broker"
- Check if sensors are enabled in `config.py`
- Verify MQTT topic is correct: `sensors/{sensor_type}/{sensor_id}`

### Module Not Found

**Error**: `ModuleNotFoundError: No module named 'mqtt'`

**Solution**:
```bash
pip install -r requirements.txt
```

Or manually install:
```bash
pip install paho-mqtt python-dotenv
```

## License

This project is part of the stream-prototype repository.

## Next Steps

1. Deploy and test the server with your MQTT broker
2. Create consumer applications that subscribe to sensor topics
3. Implement data storage (database, InfluxDB, etc.)
4. Build visualization dashboards (Grafana, etc.)
