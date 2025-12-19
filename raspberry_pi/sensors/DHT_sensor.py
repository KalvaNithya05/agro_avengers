import random

# Try to import the DHT hardware library.
# If it fails (e.g., not running on Raspberry Pi),
# we automatically fall back to mock mode.
try:
    import Adafruit_DHT
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False


class DHTSensor:
    def __init__(self, pin=4, sensor_type=11, is_mock=False):
        """
        Initialize the DHT sensor.

        :param pin: GPIO pin number (BCM mode).
        :param sensor_type: DHT sensor type (11 or 22).
        :param is_mock: Force mock readings if True.
        """
        self.pin = pin

        # Select correct DHT sensor model
        self.sensor_type = (
            Adafruit_DHT.DHT11 if sensor_type == 11 else Adafruit_DHT.DHT22
        )

        # Use mock mode if forced OR if hardware library is unavailable
        self.is_mock = is_mock or not HAS_HARDWARE

    def read(self):
        """
        Read temperature and humidity from the DHT sensor.

        :return: Dictionary with temperature and humidity,
                 or None if the read fails.
        """
        # If running without real hardware, return fake data
        if self.is_mock:
            return self._read_mock()

        try:
            # Read both humidity and temperature in a single call
            humidity, temperature = Adafruit_DHT.read_retry(
                self.sensor_type, self.pin
            )

            # Validate the sensor readings
            if humidity is None or temperature is None:
                return None

            # Return rounded values for cleaner output
            return {
                "temperature": round(temperature, 2),
                "humidity": round(humidity, 2)
            }

        except Exception as e:
            # Catch and log unexpected errors
            print(f"Error reading DHT sensor: {e}")
            return None

    def _read_mock(self):
        """
        Generate simulated sensor data for testing.

        :return: Dictionary with fake temperature and humidity values.
        """
        return {
            # Simulated temperature between 20–40 °C
            "temperature": round(random.uniform(20.0, 40.0), 2),

            # Simulated humidity between 30–90 %
            "humidity": round(random.uniform(30.0, 90.0), 2)
        }


# Run this block only when the file is executed directly
if __name__ == "__main__":
    # Create sensor instance in mock mode
    sensor = DHTSensor(is_mock=True)

    # Read data from the sensor
    data = sensor.read()

    # Display the results
    print(data)
