import React, { useState } from 'react';
import { getLatestSensorData, getRecommendations } from '../services/api';
import CropResult from '../components/CropResult';
import FertilizerTips from '../components/FertilizerTips';

const Predict = () => {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handlePredict = async () => {
        setLoading(true);
        setError(null);
        try {
            // 1. Get Live Data
            const sensorData = await getLatestSensorData();
            if (!sensorData) throw new Error("Could not fetch live sensor data. Check if Pi is online.");

            // 2. Prepare Payload (Map keys for Backend ML model)
            const payload = {
                ...sensorData,
                N: sensorData.nitrogen,
                P: sensorData.phosphorus,
                K: sensorData.potassium,
                // 'temperature', 'humidity', 'ph', 'rainfall' match directly
            };

            // 3. Get Recommendations
            const recs = await getRecommendations(payload);
            if (recs && recs.status === 'success') {
                setResult(recs);
            } else {
                throw new Error("Prediction API Failed to return results.");
            }
        } catch (e) {
            setError(e.message || "An unexpected error occurred.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-6 max-w-5xl mx-auto">
            <div className="text-center mb-10">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">AI Implementation Mode</h1>
                <p className="text-gray-600">Analyze current soil conditions from sensors to generate smart crop recommendations.</p>
            </div>

            <div className="flex justify-center mb-10">
                <button
                    onClick={handlePredict}
                    disabled={loading}
                    className={`
            px-8 py-4 rounded-full font-bold text-lg shadow-lg transition-all transform hover:scale-105
            ${loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-green-600 text-white hover:bg-green-700'}
          `}
                >
                    {loading ? (
                        <span className="flex items-center">
                            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Running AI Models...
                        </span>
                    ) : "Analyze Soil & Predict"}
                </button>
            </div>

            {error && (
                <div className="mb-6 p-4 bg-red-100 border border-red-300 text-red-700 rounded-lg text-center">
                    <strong>Error:</strong> {error}
                </div>
            )}

            {result && (
                <div className="animate-fade-in-up space-y-8">
                    <div className="grid md:grid-cols-2 gap-8">
                        <CropResult results={result.crops} />
                        <FertilizerTips tips={result.fertilizer_recommendations} />
                    </div>

                    <div className="text-center text-xs text-gray-400 mt-8">
                        Analysis based on: N:{result.used_params.N} P:{result.used_params.P} K:{result.used_params.K} pH:{result.used_params.ph}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Predict;
