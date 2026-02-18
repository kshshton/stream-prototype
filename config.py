import os

from dotenv import load_dotenv

load_dotenv()

# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USER", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
MQTT_BASE_TOPIC = os.getenv("MQTT_BASE_TOPIC", "sensors")

# Sensor Configuration
SENSOR_READ_INTERVAL = int(os.getenv("SENSOR_READ_INTERVAL", "5"))  # seconds

# Sensor Locations
SENSOR_LOCATIONS = {
    "pms5003": "living_room",
    "ens160": "office",
    "scd41": "office",
    "sen0441": "bedroom",
    "bme280": "living_room",
    "ds18b20": "outdoor_sensor",
}

# Active Sensors (set to False to disable a sensor)
ACTIVE_SENSORS = {
    "pms5003": True,
    "ens160": True,
    "scd41": True,
    "sen0441": True,
    "bme280": True,
    "ds18b20": True,
}
