# Assumptions & Constraints

## Technical Assumptions
1. **Connectivity**: Raspberry Pi has intermittent internet. Data is cached locally if API fails.
2. **Sensor Calibration**: pH and NPK sensors provides analog voltage that is linearly mapped to values.
3. **Power**: System runs on consistent power (no battery optimization logic currently).

## Data Assumptions
1. **Weather**: OpenWeatherMap API is available. If not, historical averages or mock data is used.
2. **Soil Type**: User location defaults to 'Hyderabad' zone if GPS is unavailable.
3. **Crop Dataset**: Kaggle dataset is representative of current soil conditions in India.

## Limitations
- **ML Accuracy**: Models are trained on static CSV data; real-world shift may occur.
- **Sensor drift**: No auto-calibration routine implemented yet.
