import random

from .base_sensor import BaseSensor


class DS18B20(BaseSensor):
    """DS18B20 - Temperature Sensor"""

    def read_data(self) -> dict:
        """
        Simulate DS18B20 sensor reading.
        Returns temperature measurement.
        """
        return {
            "sensor_id": self.sensor_id,
            "timestamp": self.get_timestamp(),
            "temperature": round(random.uniform(15, 30), 1),
            "location": self.location,
        }
