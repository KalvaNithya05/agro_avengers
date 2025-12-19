import os

# API Configuration
# Default to localhost for local testing. In production, this would be the IP of the server.
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000/api")
API_URL = f"{API_BASE_URL}/sensor/data"

# Data Collection Configuration
COLLECTION_INTERVAL = 60  # Seconds between readings
RETRY_DELAY = 10         # Seconds to wait before retrying failed request

# Sensor Hardware Configuration (GPIO BCM)
DHT_PIN = 4
DHT_TYPE = 11  # 11 for DHT11, 22 for DHT22

# ADC / SPI Config (for pH, NPK if using analog)
ADC_CHANNEL_PH = 0
