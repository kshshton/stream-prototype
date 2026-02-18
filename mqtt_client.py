import json
import logging

import paho.mqtt.client as mqtt

from config import (MQTT_BASE_TOPIC, MQTT_BROKER, MQTT_PASSWORD, MQTT_PORT,
                    MQTT_USER)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MQTTClient:
    def __init__(self):
        # Prefer MQTT v5 when available, fall back to MQTT v3.1.1
        try:
            protocol = mqtt.MQTTv5
        except AttributeError:
            protocol = mqtt.MQTTv311

        self.client = mqtt.Client(protocol=protocol)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_publish = self._on_publish
        self.connected = False

        # Set credentials if provided
        if MQTT_USER and MQTT_PASSWORD:
            self.client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

    def connect(self):
        """Connect to MQTT broker"""
        try:
            logger.info(
                f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
            self.client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
            self.client.loop_start()
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")
            return False

    def disconnect(self):
        """Disconnect from MQTT broker"""
        self.client.loop_stop()
        self.client.disconnect()
        logger.info("Disconnected from MQTT broker")

    def publish_sensor_data(self, sensor_type: str, sensor_id: str, data: dict):
        """Publish sensor data to MQTT topic"""
        topic = f"{MQTT_BASE_TOPIC}/{sensor_type}/{sensor_id}"
        payload = json.dumps(data)

        try:
            result = self.client.publish(topic, payload, qos=1)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.debug(f"Published to {topic}: {payload}")
            else:
                logger.warning(f"Failed to publish to {topic}: {result.rc}")
        except Exception as e:
            logger.error(f"Error publishing to {topic}: {e}")

    def _on_connect(self, client, userdata, connect_flags, reason_code, properties):
        """Callback when connected to broker"""
        if reason_code == 0:
            self.connected = True
            logger.info("Successfully connected to MQTT broker")
        else:
            self.connected = False
            logger.error(f"Failed to connect to MQTT broker: {reason_code}")

    def _on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties):
        """Callback when disconnected from broker"""
        self.connected = False
        logger.warning(
            f"Disconnected from MQTT broker with code {reason_code}")

    def _on_publish(self, client, userdata, mid):
        """Callback when message is published"""
        pass
