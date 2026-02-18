import random

from .base_sensor import BaseSensor


class ENS160(BaseSensor):
    """ENS160 - Indoor Air Quality Sensor"""

    def read_data(self) -> dict:
        """
        Simulate ENS160 sensor reading.
        Returns VOC index, eCO2, temperature, and humidity.
        """
        return {
            "sensor_id": self.sensor_id,
            "timestamp": self.get_timestamp(),
            "iaq": {
                "voc_index": random.randint(20, 100),
                "eco2": random.randint(400, 1000),
                "temperature": round(random.uniform(20, 26), 1),
                "humidity": round(random.uniform(30, 60), 1),
            },
            "location": self.location,
        }
