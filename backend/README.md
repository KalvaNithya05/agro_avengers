# MITTI MITRA - Backend

## Overview
The backend is a Node.js + Express application that handles API requests, fetches weather data, and communicates with the Python ML model.

## Structure
- `server.js`: Main entry point.
- `routes/`: API route definitions.
- `controllers/`: Request handling logic.
- `services/`: External integrations (Weather, ML).

## API Endpoints
- `POST /api/recommend`: Get crop recommendations.
  - Body: `{ n, p, k, ph, city }`

## Running Locally
1. `npm install`
2. `npm start`
