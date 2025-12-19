import random
import time

class NPKSensor:
    def __init__(self, port='/dev/ttyUSB0', is_mock=False):
        """
        Initialize the NPK Sensor.
        :param port: Serial port for RS485 connection.
        :param is_mock: Force mock mode.
        """
        self.port = port
        self.is_mock = is_mock
        # Real hardware init would require setting up Serial/Modbus connection here

    def read(self):
        """
        Reads the soil NPK values.
        :return: Dictionary {'N': float, 'P': float, 'K': float} or None.
        """
        if self.is_mock:
            return self._read_mock()
        
        try:
            # Placeholder for actual RS485 Modbus reading
            # bytes_to_send = b'\x01\x03\x00\x1e\x00\x03\x65\xcd'
            # response = serial.write_and_read(self.port, bytes_to_send)
            # n, p, k = parse_response(response)
            # return {'N': n, 'P': p, 'K': k}
            print("Hardware implementation requires Modbus/RS485 libraries (e.g. pymodbus or pyserial).")
            return None
        except Exception as e:
            print(f"Error reading NPK sensor: {e}")
            return None

    def _read_mock(self):
        """
        Simulates NPK readings.
        Ranges based on typical agricultural soil content (mg/kg or ppm).
        """
        return {
            'N': round(random.uniform(20.0, 150.0), 1), # Nitrogen
            'P': round(random.uniform(10.0, 60.0), 1),  # Phosphorus
            'K': round(random.uniform(50.0, 200.0), 1)  # Potassium
        }

if __name__ == "__main__":
    sensor = NPKSensor(is_mock=True)
    print(f"Current Soil NPK: {sensor.read()}")
