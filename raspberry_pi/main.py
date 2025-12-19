import sys
import os
import signal
import time

# Ensure relative imports work by adding current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from collector.collect_data import collect_loop
except ImportError as e:
    print(f"Error importing collector: {e}")
    sys.exit(1)

def signal_handler(sig, frame):
    """
    Handle Ctrl+C for clean shutdown.
    """
    print("\nStopping Mitti Mitra Pi Collector...")
    sys.exit(0)

def main():
    print("=========================================")
    print("   Mitti Mitra - Raspberry Pi Module     ")
    print("=========================================")
    
    # Register Ctrl+C handler
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        collect_loop()
    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print(f"Critical Error in Main Loop: {e}")
        # Basic retry logic
        print("Retrying in 5 seconds...")
        time.sleep(5)
        main()

if __name__ == "__main__":
    main()
