import React from 'react';
import { Download } from 'lucide-react';
import CropResult from './CropResult';
import FertilizerTips from './FertilizerTips';

const Results = ({ data, onDownload }) => {
    if (!data) return null;

    return (
        <div className="mt-8">
            <div className="flex justify-between items-center mb-6">
                <h3 className="text-2xl font-bold text-gray-800">Recommended Crops</h3>
                <button
                    onClick={onDownload}
                    className="flex items-center space-x-2 bg-primary text-white px-4 py-2 rounded-lg hover:bg-green-700 transition"
                >
                    <Download size={20} />
                    <span>Download Report</span>
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <CropResult results={data.crops} />
                <FertilizerTips tips={data.fertilizer_recommendations} />
            </div>

            {data.weather && (
                <div className="mt-8 bg-blue-50 p-6 rounded-lg border border-blue-100">
                    <h4 className="text-lg font-bold text-blue-800 mb-2">Weather Analysis</h4>
                    <div className="flex justify-between text-blue-900">
                        <span>Temp: {data.weather.temp}°C</span>
                        <span>Humidity: {data.weather.humidity}%</span>
                        <span>Rainfall: {data.weather.rainfall}mm</span>
                    </div>
                    <p className="mt-2 text-sm text-blue-700">
                        Current weather conditions are favorable for the recommended crops.
                    </p>
                </div>
            )}
        </div>
    );
};

export default Results;
