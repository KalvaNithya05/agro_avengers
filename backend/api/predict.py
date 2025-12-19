from flask import Blueprint, request, jsonify
from ml.predictor import CropPredictor
from ml.fertilizer_recommender import FertilizerRecommender
from ml.preprocess import DataPreprocessor
from services.weather_service import WeatherService

predict_bp = Blueprint('predict', __name__)

# Initialize services once
predictor = CropPredictor()
fertilizer = FertilizerRecommender()
preprocessor = DataPreprocessor()
weather_service = WeatherService()

@predict_bp.route('/recommend', methods=['POST'])
def recommend():
    """
    Endpoint checks suitable crops and fertilizer.
    Input JSON: { N, P, K, ph, temperature?, humidity?, rainfall?, location? }
    """
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        # Auto-fill weather data if missing
        if 'humidity' not in data or 'rainfall' not in data or 'temperature' not in data:
            location = data.get('location', 'Hyderabad')
            weather = weather_service.get_current_weather(location)
            
            # Only fill missing fields
            if 'temperature' not in data: data['temperature'] = weather['temperature']
            if 'humidity' not in data: data['humidity'] = weather['humidity']
            if 'rainfall' not in data: data['rainfall'] = weather['rainfall']

        # Preprocess features
        # Expects: N, P, K, temperature, humidity, ph, rainfall
        try:
            features = preprocessor.preprocess(data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

        # Get Predictions
        # TODO: Pass zone if available in data
        predictions = predictor.predict(features, top_n=3)

        # Get Fertilizer Tips
        fert_recs = fertilizer.recommend(
            float(data.get('N', 0)), 
            float(data.get('P', 0)), 
            float(data.get('K', 0)), 
            float(data.get('ph', 7))
        )

        return jsonify({
            'status': 'success',
            'crops': predictions,
            'fertilizer_recommendations': fert_recs,
            'used_params': data
        })

    except Exception as e:
        print(f"Prediction API Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
