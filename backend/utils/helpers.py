from datetime import datetime

def format_timestamp(dt_obj):
    """
    Standardize timestamp formatting.
    """
    if isinstance(dt_obj, datetime):
        return dt_obj.strftime('%Y-%m-%d %H:%M:%S')
    return str(dt_obj)

def validate_sensor_data(data):
    """
    Checks if sensor readings are within physically possible ranges.
    Returns (bool, message).
    """
    if not isinstance(data, dict):
        return False, "Invalid data format"
        
    ph = data.get('ph')
    if ph is not None and (ph < 0 or ph > 14):
        return False, "pH out of range (0-14)"
        
    hum = data.get('humidity')
    if hum is not None and (hum < 0 or hum > 100):
        return False, "Humidity out of range (0-100)"
        
    return True, "Valid"
