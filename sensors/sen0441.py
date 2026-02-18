import random

from .base_sensor import BaseSensor


class SEN0441(BaseSensor):
    """SEN0441 - Formaldehyde Sensor"""

    def read_data(self) -> dict:
        """
        Simulate SEN0441 sensor reading.
        Returns formaldehyde concentration, temperature, and humidity.
        """
        return {
            "sensor_id": self.sensor_id,
            "timestamp": self.get_timestamp(),
            "hcho": {
                "ppm": round(random.uniform(0.01, 0.1), 2),
                "temperature": round(random.uniform(20, 26), 1),
                "humidity": round(random.uniform(30, 60), 1),
            },
            "location": self.location,
        }
