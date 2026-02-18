import random

from .base_sensor import BaseSensor


class SCD41(BaseSensor):
    """SCD41 - CO₂ Sensor"""

    def read_data(self) -> dict:
        """
        Simulate SCD41 sensor reading.
        Returns CO2 concentration, temperature, and humidity.
        """
        return {
            "sensor_id": self.sensor_id,
            "timestamp": self.get_timestamp(),
            "co2": {
                "ppm": random.randint(380, 800),
                "temperature": round(random.uniform(20, 26), 1),
                "humidity": round(random.uniform(30, 60), 1),
            },
            "location": self.location,
        }
