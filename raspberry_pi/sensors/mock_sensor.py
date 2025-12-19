import sys
import os
# Ensure this directory is in path so we can import siblings
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from temperature_sensor import TemperatureSensor
    from humidity_sensor import HumiditySensor
    from ph_sensor import PHSensor
    from npk_sensor import NPKSensor
except ImportError as e:
    print(f"MockSensorSuite Import Error: {e}")
    # Re-raise to see it in logs
    raise e

class MockSensorSuite:
    def __init__(self):
        """
        Initializes a suite of sensors in mock mode.
        """
        self.temp_sensor = TemperatureSensor(is_mock=True)
        self.hum_sensor = HumiditySensor(is_mock=True)
        self.ph_sensor = PHSensor(is_mock=True)
        self.npk_sensor = NPKSensor(is_mock=True)

    def get_all_data(self):
        """
        Returns a dictionary containing all sensor readings.
        """
        npk = self.npk_sensor.read()
        return {
            'temperature': self.temp_sensor.read(),
            'humidity': self.hum_sensor.read(),
            'ph': self.ph_sensor.read(),
            'nitrogen': npk.get('N') if npk else None,
            'phosphorus': npk.get('P') if npk else None,
            'potassium': npk.get('K') if npk else None
        }

if __name__ == "__main__":
    suite = MockSensorSuite()
    print("Mock Sensor Suite Data:", suite.get_all_data())
