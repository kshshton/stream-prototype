# Integration Guide - Sensor Backend Server

This guide explains how to integrate with the Sensor Backend Server and consume its MQTT messages.

## Quick Start

### 1. Start the Server (Windows PowerShell)

```powershell
.\start.ps1
```

### 2. Start the Server (Linux/macOS)

```bash
chmod +x start.sh
./start.sh
```

### 3. Manual Start (Any Platform)

```bash
# Install dependencies
pip install -r requirements.txt

# Start Mosquitto (if using Docker)
docker-compose up -d

# Run the server
python main.py
```

## Python Consumer Example

### Basic Subscriber

```python
import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, connect_flags, reason_code, properties):
    print(f"Connected with code {reason_code}")
    client.subscribe("sensors/#")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print(f"Topic: {msg.topic}")
        print(f"Data: {json.dumps(data, indent=2)}")
    except json.JSONDecodeError:
        print(f"Failed to decode message from {msg.topic}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()
```

### Sensor-Specific Subscriber

```python
import paho.mqtt.client as mqtt
import json

class SensorListener:
    def __init__(self, broker="localhost", port=1883):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.sensor_handlers = {}
        
        self.client.connect(broker, port, 60)

    def register_handler(self, sensor_type, callback):
        """Register a callback for a specific sensor type"""
        self.sensor_handlers[sensor_type] = callback

    def _on_connect(self, client, userdata, connect_flags, reason_code, properties):
        print(f"Connected to MQTT broker (code {reason_code})")
        client.subscribe("sensors/#")

    def _on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
            topic_parts = msg.topic.split("/")
            
            if len(topic_parts) >= 2:
                sensor_type = topic_parts[1]
                
                # Call registered handler
                if sensor_type in self.sensor_handlers:
                    self.sensor_handlers[sensor_type](data)
        except Exception as e:
            print(f"Error processing message: {e}")

    def start(self):
        """Start listening for messages"""
        self.client.loop_forever()

    def stop(self):
        """Stop listening"""
        self.client.loop_stop()

# Usage
def handle_pms5003(data):
    pm25 = data['pm']['pm2_5']
    print(f"PMS5003: PM2.5 = {pm25} µg/m³")

def handle_scd41(data):
    co2 = data['co2']['ppm']
    print(f"SCD41: CO₂ = {co2} ppm")

listener = SensorListener()
listener.register_handler("pms5003", handle_pms5003)
listener.register_handler("scd41", handle_scd41)
listener.start()
```

## Node.js Consumer Example

### Installation

```bash
npm install mqtt
```

### Basic Subscriber

```javascript
const mqtt = require('mqtt');

const client = mqtt.connect('mqtt://localhost:1883');

client.on('connect', () => {
  console.log('Connected to MQTT broker');
  client.subscribe('sensors/#', (err) => {
    if (err) console.error('Subscribe error:', err);
  });
});

client.on('message', (topic, message) => {
  try {
    const data = JSON.parse(message.toString());
    console.log(`Topic: ${topic}`);
    console.log('Data:', JSON.stringify(data, null, 2));
  } catch (e) {
    console.error('Failed to parse message:', e);
  }
});

client.on('error', (err) => {
  console.error('Connection error:', err);
});
```

## Data Processing Examples

### Storing to Database

#### SQLite Example

```python
import sqlite3
import json
import paho.mqtt.client as mqtt
from datetime import datetime

class DataStore:
    def __init__(self, db_path="sensor_data.db"):
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.setup_database()

    def setup_database(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_id TEXT NOT NULL,
                sensor_type TEXT NOT NULL,
                reading_time TEXT NOT NULL,
                data TEXT NOT NULL,
                location TEXT
            )
        """)
        self.connection.commit()

    def store_reading(self, sensor_type, data):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO sensor_readings 
            (sensor_id, sensor_type, reading_time, data, location)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data.get('sensor_id', 'unknown'),
            sensor_type,
            data.get('timestamp', datetime.utcnow().isoformat()),
            json.dumps(data),
            data.get('location', 'unknown')
        ))
        self.connection.commit()

# Usage
store = DataStore()

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        sensor_type = msg.topic.split("/")[1]
        store.store_reading(sensor_type, data)
        print(f"Stored reading from {sensor_type}")
    except Exception as e:
        print(f"Error: {e}")

# Continue MQTT connection with the callback above
```

### Real-time Aggregation

```python
from collections import defaultdict
from datetime import datetime
import paho.mqtt.client as mqtt
import json

class SensorAggregator:
    def __init__(self):
        self.latest_readings = defaultdict(dict)
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, connect_flags, reason_code, properties):
        client.subscribe("sensors/#")

    def _on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
            sensor_id = data.get('sensor_id', 'unknown')
            self.latest_readings[sensor_id] = {
                'data': data,
                'timestamp': datetime.fromisoformat(data['timestamp'])
            }
            self.print_summary()
        except Exception as e:
            print(f"Error: {e}")

    def print_summary(self):
        print("\n" + "="*50)
        print("LATEST SENSOR READINGS")
        print("="*50)
        for sensor_id, info in self.latest_readings.items():
            data = info['data']
            location = data.get('location', 'unknown')
            print(f"\n{sensor_id} ({location})")
            print(f"  Timestamp: {data['timestamp']}")
            # Print relevant fields based on sensor type
            if 'pm' in data:
                print(f"  PM2.5: {data['pm']['pm2_5']} µg/m³")
            if 'co2' in data:
                print(f"  CO₂: {data['co2']['ppm']} ppm")

    def start(self):
        self.client.connect("localhost", 1883, 60)
        self.client.loop_forever()

# Run aggregator
aggregator = SensorAggregator()
aggregator.start()
```

## Filtering and Processing

### By Location

```python
import paho.mqtt.client as mqtt
import json

class LocationFilter:
    def __init__(self, location_filter):
        self.location = location_filter
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, connect_flags, reason_code, properties):
        client.subscribe("sensors/#")

    def _on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
            if data.get('location') == self.location:
                print(f"Message from {self.location}: {msg.topic}")
                print(json.dumps(data, indent=2))
        except Exception as e:
            print(f"Error: {e}")

    def start(self):
        self.client.connect("localhost", 1883, 60)
        self.client.loop_forever()

# Monitor only office sensors
office_monitor = LocationFilter("office")
office_monitor.start()
```

### By Threshold

```python
import paho.mqtt.client as mqtt
import json

class ThresholdMonitor:
    def __init__(self):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        
        # Set thresholds
        self.thresholds = {
            'pm2_5': 35,  # µg/m³- high level
            'eco2': 800,  # ppm - high level
            'formaldehyde': 0.05  # ppm
        }

    def _on_connect(self, client, userdata, connect_flags, reason_code, properties):
        client.subscribe("sensors/#")

    def _on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
            
            # Check PM2.5 threshold
            if 'pm' in data and data['pm']['pm2_5'] > self.thresholds['pm2_5']:
                print(f"⚠️  HIGH PM2.5: {data['pm']['pm2_5']} µg/m³ from {data.get('sensor_id')}")
            
            # Check eCO2 threshold
            if 'iaq' in data and data['iaq']['eco2'] > self.thresholds['eco2']:
                print(f"⚠️  HIGH eCO2: {data['iaq']['eco2']} ppm from {data.get('sensor_id')}")
            
            # Check formaldehyde threshold
            if 'hcho' in data and data['hcho']['ppm'] > self.thresholds['formaldehyde']:
                print(f"⚠️  HIGH FORMALDEHYDE: {data['hcho']['ppm']} ppm from {data.get('sensor_id')}")
        except Exception as e:
            print(f"Error: {e}")

    def start(self):
        self.client.connect("localhost", 1883, 60)
        self.client.loop_forever()

# Run threshold monitor
monitor = ThresholdMonitor()
monitor.start()
```

## Testing with Command Line Tools

### Using mosquitto_sub (with Docker)

```bash
# All sensors
docker exec mosquitto-broker mosquitto_sub -h localhost -t "sensors/#" -v

# Specific sensor type
docker exec mosquitto-broker mosquitto_sub -h localhost -t "sensors/pms5003/#" -v

# Real-time pretty printing
docker exec mosquitto-broker mosquitto_sub -h localhost -t "sensors/#" | jq .
```

### Using mqtt-cli

```bash
# Install
brew install mqtt-cli  # macOS
# or download from https://hivemq.github.io/mqtt-cli/

# Subscribe to all
mqtt-cli sub -h localhost -t "sensors/#"

# Subscribe with format
mqtt-cli sub -h localhost -t "sensors/+/+" -of MQTT3
```

## Handling Errors

### Connection Retries

```python
import paho.mqtt.client as mqtt
import json
import time

class RobustSensorClient:
    def __init__(self, broker="localhost", port=1883, max_retries=5):
        self.broker = broker
        self.port = port
        self.max_retries = max_retries
        self.retry_count = 0
        
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, connect_flags, reason_code, properties):
        print(f"Connected (code {reason_code})")
        self.retry_count = 0
        client.subscribe("sensors/#")

    def _on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties):
        if reason_code != 0:
            print(f"Disconnected (code {reason_code}), attempting reconnect...")
            self._reconnect()

    def _reconnect(self):
        if self.retry_count < self.max_retries:
            wait_time = min(2 ** self.retry_count, 60)  # Exponential backoff
            print(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            try:
                self.client.reconnect()
                self.retry_count += 1
            except Exception as e:
                print(f"Reconnect failed: {e}")

    def _on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
            # Process data
        except Exception as e:
            print(f"Error processing message: {e}")

    def start(self):
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_forever()
        except Exception as e:
            print(f"Fatal error: {e}")

# Usage
client = RobustSensorClient()
client.start()
```

## Performance Tips

1. **Use QoS 1** for reliability without unnecessary overhead
2. **Batch updates** for database writes
3. **Use message filters** to reduce processing
4. **Implement rate limiting** for high-frequency sensors
5. **Monitor memory** usage with many connected clients

## Advanced Integrations

See individual technology guidelines:
- [InfluxDB Integration](./docs/integrations/influxdb.md)
- [Grafana Dashboard Setup](./docs/integrations/grafana.md)
- [AWS IoT Integration](./docs/integrations/aws-iot.md)
- [Home Assistant Integration](./docs/integrations/home-assistant.md)
