import time
import requests
import json
import os
import sys
from datetime import datetime

# Adjust path to import from sibling/parent packages
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

try:
    from sensors.mock_sensor import MockSensorSuite
    from config.pi_config import API_URL, COLLECTION_INTERVAL
except ImportError:
    # Fallback if config not yet created or running standalone
    API_URL = "http://localhost:5000/api/sensor-data"
    COLLECTION_INTERVAL = 60 # seconds
    from sensors.mock_sensor import MockSensorSuite

def save_locally(data):
    """
    Saves data to a local CSV file when offline.
    """
    file_path = os.path.join(current_dir, "offline_data.csv")
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, "a") as f:
        if not file_exists:
            f.write("timestamp,temperature,humidity,ph,nitrogen,phosphorus,potassium\n")
        
        line = f"{data['timestamp']},{data['temperature']},{data['humidity']},{data['ph']},{data['nitrogen']},{data['phosphorus']},{data['potassium']}\n"
        f.write(line)
        print("Data saved locally (offline mode).")

def collect_loop():
    print(f"Starting Data Collector... Sending to {API_URL}")
    suite = MockSensorSuite()
    
    while True:
        try:
            # 1. Read Data
            data = suite.get_all_data()
            data['timestamp'] = datetime.now().isoformat()
            
            print(f"[{data['timestamp']}] Read: {data}")

            # 2. Send to Backend
            try:
                response = requests.post(API_URL, json=data, timeout=5)
                if response.status_code == 201 or response.status_code == 200:
                    print(" > Sent to API successfully.")
                else:
                    print(f" ! API Error {response.status_code}: {response.text}")
                    save_locally(data)
            except requests.exceptions.RequestException as e:
                print(f" ! Network Error: {e}")
                save_locally(data)

        except Exception as e:
            print(f" ! Critical Error: {e}")
        
        time.sleep(COLLECTION_INTERVAL)

if __name__ == "__main__":
    collect_loop()
