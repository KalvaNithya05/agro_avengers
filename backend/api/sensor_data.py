from flask import Blueprint, request, jsonify
from config.supabase_client import supabase
from datetime import datetime

sensor_bp = Blueprint('sensor', __name__)

@sensor_bp.route('/data', methods=['POST'])
def receive_data():
    """
    Ingest data from Raspberry Pi.
    """
    data = request.json
    if not data:
        return jsonify({'error': 'No data received'}), 400
        
    # Validates output
    print(f"Received Sensor Data: {data}")

    if supabase:
        try:
            # Map input to DB schema
            record = {
                'device_id': data.get('device_id', 'pi_01'),
                'temperature': data.get('temperature'),
                'humidity': data.get('humidity'),
                'ph': data.get('ph'),
                'nitrogen': data.get('nitrogen'),
                'phosphorus': data.get('phosphorus'),
                'potassium': data.get('potassium'),
                'rainfall': data.get('rainfall', 0.0),
                'timestamp': data.get('timestamp', datetime.now().isoformat())
            }
            
            # Fire and forget / await
            supabase.table('sensor_readings').insert(record).execute()
            return jsonify({'status': 'stored'}), 201
            
        except Exception as e:
            print(f"Supabase Insert Error: {e}")
            # Do not fail the Pi request if DB is down, just log
            # The Pi has local backup logic
            return jsonify({'error': 'db_error', 'message': str(e)}), 500
    else:
        # Mock mode
        return jsonify({'status': 'mock_stored'}), 200

@sensor_bp.route('/latest', methods=['GET'])
def get_latest():
    """
    Get the latest sensor reading.
    """
    if supabase:
        try:
            response = supabase.table('sensor_readings')\
                .select('*')\
                .order('timestamp', desc=True)\
                .limit(1)\
                .execute()
            
            if response.data:
                return jsonify(response.data[0])
        except Exception as e:
            print(f"Fetch Error: {e}")
            
    # Mock Fallback
    return jsonify({
        'temperature': 26.5,
        'humidity': 55.0,
        'ph': 6.8,
        'nitrogen': 120,
        'phosphorus': 40,
        'potassium': 140,
        'rainfall': 0,
        'timestamp': datetime.now().isoformat()
    })
