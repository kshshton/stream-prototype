import logging
import signal
import sys
import time

from config import ACTIVE_SENSORS, SENSOR_LOCATIONS, SENSOR_READ_INTERVAL
from mqtt_client import MQTTClient
from sensors import BME280, DS18B20, ENS160, PMS5003, SCD41, SEN0441

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class SensorServer:
    def __init__(self):
        self.mqtt_client = MQTTClient()
        self.sensors = {}
        self.running = False

        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, sig, frame):
        """Handle interrupt signals"""
        logger.info("Received interrupt signal. Shutting down gracefully...")
        self.stop()
        sys.exit(0)

    def initialize_sensors(self):
        """Initialize all active sensors"""
        logger.info("Initializing sensors...")

        # Define sensor configurations
        sensor_classes = {
            "pms5003": PMS5003,
            "ens160": ENS160,
            "scd41": SCD41,
            "sen0441": SEN0441,
            "bme280": BME280,
            "ds18b20": DS18B20,
        }

        for sensor_type, sensor_class in sensor_classes.items():
            if ACTIVE_SENSORS.get(sensor_type, False):
                sensor_id = f"{sensor_type}_01"
                location = SENSOR_LOCATIONS.get(sensor_type, "unknown")
                sensor = sensor_class(sensor_id, location, self.mqtt_client)
                self.sensors[sensor_type] = sensor
                logger.info(f"Initialized {sensor_type} at {location}")
            else:
                logger.info(f"Sensor {sensor_type} is disabled")

    def start(self):
        """Start the sensor server"""
        logger.info("Starting Sensor Server...")

        # Connect to MQTT broker
        if not self.mqtt_client.connect():
            logger.error("Failed to connect to MQTT broker. Exiting.")
            return False

        # Wait for connection to be established
        time.sleep(2)

        if not self.mqtt_client.connected:
            logger.error("MQTT connection failed. Exiting.")
            return False

        # Initialize sensors
        self.initialize_sensors()

        if not self.sensors:
            logger.error("No sensors initialized. Exiting.")
            return False

        self.running = True
        logger.info("Sensor Server started successfully")
        return True

    def stop(self):
        """Stop the sensor server"""
        logger.info("Stopping Sensor Server...")
        self.running = False
        self.mqtt_client.disconnect()
        logger.info("Sensor Server stopped")

    def run(self):
        """Main server loop - continuously read and publish sensor data"""
        if not self.start():
            return

        logger.info(
            f"Publishing sensor data every {SENSOR_READ_INTERVAL} seconds...")

        try:
            while self.running:
                for sensor_type, sensor in self.sensors.items():
                    try:
                        data = sensor.publish()
                        logger.info(f"{sensor_type}: Data published")
                    except Exception as e:
                        logger.error(
                            f"Error publishing {sensor_type} data: {e}")

                time.sleep(SENSOR_READ_INTERVAL)

        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")
        finally:
            self.stop()


def main():
    """Entry point for the server"""
    server = SensorServer()
    server.run()


if __name__ == "__main__":
    main()
