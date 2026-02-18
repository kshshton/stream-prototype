import random

from .base_sensor import BaseSensor


class BME280(BaseSensor):
    """BME280 - Environmental Sensor"""

    def read_data(self) -> dict:
        """
        Simulate BME280 sensor reading.
        Returns temperature, humidity, and atmospheric pressure.
        """
        return {
            "sensor_id": self.sensor_id,
            "timestamp": self.get_timestamp(),
            "environment": {
                "temperature": round(random.uniform(20, 26), 1),
                "humidity": round(random.uniform(30, 60), 1),
                "pressure": round(random.uniform(1000, 1030), 1),
            },
            "location": self.location,
        }
