
import os
import sys
from dotenv import load_dotenv

# Ensure we can import from the current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

try:
    from config.supabase_client import supabase
except ImportError:
    print("Could not import supabase client. Check your dependencies.")
    sys.exit(1)

def test_connection():
    print("Testing Supabase Connection...")
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    print(f"URL: {url}")
    # Mask key for security
    masked_key = f"{key[:5]}...{key[-5:]}" if key and len(key) > 10 else "None/Short"
    print(f"Key: {masked_key}")

    if not supabase:
        print("Supabase client is None. Check .env content.")
        return

    try:
        # Try a simple select. Even if table is empty or doesn't exist, 
        # connection failure usually throws a different error or we can catch the table error.
        # We'll try to select from a non-existent table just to ping the server, 
        # or 'sensor_readings' if expected.
        response = supabase.table('sensor_readings').select("*").limit(1).execute()
        print("Connection Successful!")
        print(f"Data sample: {response.data}")
    except Exception as e:
        print(f"Connection Failed or Query Error: {e}")

if __name__ == "__main__":
    test_connection()
