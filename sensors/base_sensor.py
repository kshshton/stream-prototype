from abc import ABC, abstractmethod
from datetime import datetime

from mqtt_client import MQTTClient


class BaseSensor(ABC):
    """Base class for all sensor simulators"""

    def __init__(self, sensor_id: str, location: str, mqtt_client: MQTTClient):
        self.sensor_id = sensor_id
        self.location = location
        self.mqtt_client = mqtt_client
        self.sensor_type = self.__class__.__name__.lower()

    @abstractmethod
    def read_data(self) -> dict:
        """
        Read sensor data and return as dictionary.
        Must be implemented by subclasses.
        """
        pass

    def get_timestamp(self) -> str:
        """Get current timestamp in ISO 8601 format"""
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    def publish(self):
        """Read data and publish to MQTT"""
        data = self.read_data()
        self.mqtt_client.publish_sensor_data(
            self.sensor_type, self.sensor_id, data)
        return data

    def get_full_data(self) -> dict:
        """Get complete sensor data including metadata"""
        return self.read_data()
