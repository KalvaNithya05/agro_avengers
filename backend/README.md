# MITTI MITRA - Backend

## Overview
The backend is a Node.js + Express application that handles API requests, fetches weather data, and communicates with the Python ML model.

## Structure
- `app.py`: Main entry point (Flask).
- `server.js`: Legacy/Alternative entry point (Node.js).
- `routes/`: API route definitions.
- `controllers/`: Request handling logic.
- `services/`: External integrations (Weather, ML).

## API Endpoints
- `POST /api/recommend`: Get crop recommendations.
  - Body: `{ n, p, k, ph, city }`

## Running Locally
1. `pip install -r ../requirements.txt`
2. `python app.py`
