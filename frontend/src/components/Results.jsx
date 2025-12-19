import React from 'react';
import { Download } from 'lucide-react';

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

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {data.recommendations.map((rec, index) => (
                    <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition border border-gray-100">
                        <div className="h-40 bg-green-50 flex flex-col items-center justify-center relative">
                            {index === 0 && (
                                <span className="absolute top-2 right-2 bg-yellow-400 text-yellow-900 text-xs font-bold px-2 py-1 rounded-full">
                                    Top Choice
                                </span>
                            )}
                            <span className="text-4xl mb-2">🌱</span>
                            <span className="text-sm font-semibold text-green-800">{rec.confidence}% Match</span>
                        </div>
                        <div className="p-4">
                            <h4 className="text-xl font-bold text-primary capitalize mb-2">{rec.crop}</h4>
                            <div className="text-gray-600 text-sm space-y-1">
                                <p className="font-semibold text-gray-700">Why this crop?</p>
                                <ul className="list-disc list-inside">
                                    {rec.reasoning.map((reason, i) => (
                                        <li key={i}>{reason}</li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    </div>
                ))}
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
