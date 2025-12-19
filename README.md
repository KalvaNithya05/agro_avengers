# Mitti Mitra - Smart Crop Recommendation System

An AI-powered IoT solution to help Indian farmers optimize crop selection and fertilizer usage.

## 📁 Project Structure

- **raspberry_pi/**: Sensor interface, data collection, and local aggregation.
- **backend/**: Flask API, ML Models (Agri/Horti), and Services (Supabase/Weather).
- **frontend/**: React UI for Dashboard, Prediction, and Manual Entry.
- **database/**: SQL schemas and seed data.

## 🚀 Setup Instructions

### 1. Database (Supabase)
1. Create a new Supabase project.
2. Go to SQL Editor and run the contents of `database/schema.sql`.
3. (Optional) Run `database/seed.sql` to populate test data.
4. Note your `SUPABASE_URL` and `SUPABASE_KEY`.

### 2. Backend
1. Navigate to `backend/`.
2. Install dependencies: `pip install -r ../requirements.txt`.
3. Create a `.env` file based on `.env.example` (add Supabase & OpenWeather keys).
4. Run server: 
   ```bash
   python app.py
   ```
   Server runs on `http://localhost:5000`.

### 3. Frontend
1. Navigate to `frontend/`.
2. Install dependencies: `npm install`.
3. Start the app:
   ```bash
   npm start
   ```
   App runs on `http://localhost:3000`.

### 4. Raspberry Pi (Sensor Node)
1. Navigate to `raspberry_pi/`.
2. Ensure hardware (Sensors) is connected or rely on Mock mode (default).
3. Update `config/pi_config.py` if needed.
4. Run collector:
   ```bash
   python main.py
   ```

## 🧠 ML & Features
- **Hybrid Approach**: Distinct models for Agricultural and Horticultural crops.
- **Zone Awareness**: Maps states to Agro-Climatic Zones for better context.
- **Offline Support**: Pi caches data locally; Frontend offers Manual Input mode.
