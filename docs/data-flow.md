# Data Flow

## End-to-End Flow

1. **User Input**
   - Farmer enters soil data (N, P, K, pH) and location on the Frontend.

2. **Frontend Request**
   - React app sends a POST request to `/api/recommend` with the payload.

3. **Backend Processing**
   - **Weather Fetch**: Backend calls Weather API using the location to get Temp, Humidity, Rainfall.
   - **Data Aggregation**: Backend combines Soil Data + Weather Data.
   - **ML Inference**: Backend passes this vector to the Python script (`predict.py`).

4. **ML Prediction**
   - Python script loads the trained model.
   - Predicts the best crops based on the input vector.
   - Returns JSON output to Backend.

5. **Response**
   - Backend formats the response (adding images/descriptions if available).
   - Sends JSON response back to Frontend.

6. **Display**
   - Frontend renders the recommended crops in a card layout.
