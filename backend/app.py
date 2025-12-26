from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import sys

# Ensure backend directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)  # Allow Frontend to communicate

    # Import Blueprints (Assumes these files will be created next)
    # We use deferred imports inside create_app to avoid circular dependencies if any
    try:
        from api.predict import predict_bp
        from api.sensor_data import sensor_bp
        from api.report import report_bp
        from api.data import data_bp

        app.register_blueprint(predict_bp, url_prefix='/api/predict')
        app.register_blueprint(sensor_bp, url_prefix='/api/sensor') # '/api/sensor' matches pi config
        app.register_blueprint(report_bp, url_prefix='/api/report')
        app.register_blueprint(data_bp, url_prefix='/api/data')
    except ImportError as e:
        print(f"Warning: Could not import some API blueprints: {e}")
        print("Note: This is expected during initial generation phase.")

    @app.route('/')
    def health_check():
        return jsonify({
            "project": "Mitti Mitra",
            "status": "online",
            "version": "1.0.0"
        })

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
