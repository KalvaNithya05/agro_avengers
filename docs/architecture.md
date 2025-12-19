# System Architecture

## Overview
Mitti Mitra is a Hybrid IoT + AI Crop Recommendation System.

## Layers

### 1. Edge Layer (Raspberry Pi)
- **Inputs**: DHT11/22, Capacitive Soil Moisture, pH Sensor, NPK Modbus.
- **Process**: `collect_data.py` polls sensors every 60s.
- **Aggregator**: `aggregate_30_days.py` computes local stats if offline.
- **Output**: JSON payload to Backend API.

### 2. Backend Layer (Flask)
- **API**: 
  - `/api/sensor/data`: Ingests raw data.
  - `/api/predict/recommend`: Runs ML inference.
- **ML Engine**:
  - `Agricultural Model`: For field crops (Rice, Maize).
  - `Horticultural Model`: For fruits/veg.
  - `Zone Mapper`: Filters results based on 15 Agro-Climatic Zones of India.

### 3. Data Layer (Supabase)
- **Table**: `sensor_readings` (Time-series data).
- **Storage**: Postgres-backed.

### 4. Presentation Layer (React)
- **Dashboard**: Live view of soil parameters.
- **Predictor**: Interface to trigger Analysis.
