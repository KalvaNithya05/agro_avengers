import random
import time

try:
    import Adafruit_DHT
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

class TemperatureSensor:
    def __init__(self, pin=4, sensor_type=11, is_mock=False):
        self.pin = pin
        self.is_mock = is_mock or not HAS_HARDWARE
        if HAS_HARDWARE:
             self.sensor_type = Adafruit_DHT.DHT11 if sensor_type == 11 else Adafruit_DHT.DHT22
        else:
             self.sensor_type = None

    def read(self):
        if self.is_mock: return self._read_mock()
        try:
            humidity, temperature = Adafruit_DHT.read_retry(self.sensor_type, self.pin)
            return round(temperature, 2) if temperature is not None else None
        except: return None

    def _read_mock(self):
        return round(random.uniform(20.0, 40.0), 2)
