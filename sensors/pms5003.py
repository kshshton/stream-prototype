import random

from .base_sensor import BaseSensor


class PMS5003(BaseSensor):
    """PMS5003 - Particulate Matter Sensor"""

    def read_data(self) -> dict:
        """
        Simulate PMS5003 sensor reading.
        Returns particulate matter measurements and particle counts.
        """
        return {
            "sensor_id": self.sensor_id,
            "timestamp": self.get_timestamp(),
            "pm": {
                "pm1_0": round(random.uniform(5, 20), 1),
                "pm2_5": round(random.uniform(15, 35), 1),
                "pm10": round(random.uniform(30, 60), 1),
                "particles_0_3um": random.randint(5000, 15000),
                "particles_0_5um": random.randint(2000, 8000),
                "particles_1_0um": random.randint(500, 2000),
                "particles_2_5um": random.randint(100, 800),
                "particles_5_0um": random.randint(20, 100),
                "particles_10um": random.randint(5, 30),
            },
            "location": self.location,
        }
