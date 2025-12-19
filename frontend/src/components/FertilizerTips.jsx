import React from 'react';

const FertilizerTips = ({ tips }) => {
    if (!tips || tips.length === 0) return null;

    return (
        <div className="bg-white p-6 rounded-lg shadow-md mt-6">
            <h2 className="text-xl font-bold text-amber-700 mb-4 flex items-center">
                <span className="mr-2">📝</span> Soil Health & Fertilizer Guide
            </h2>

            <ul className="space-y-3">
                {tips.map((tip, index) => (
                    <li key={index} className="flex items-start p-3 bg-amber-50 rounded-md border border-amber-100 text-gray-800 text-sm">
                        <span className="text-amber-500 mr-2 text-lg font-bold">•</span>
                        <span className="mt-0.5 leading-relaxed">{tip}</span>
                    </li>
                ))}
            </ul>

            <div className="mt-4 text-xs text-gray-500 text-center italic">
                * Please consult a local agronomist before large-scale application.
            </div>
        </div>
    );
};

export default FertilizerTips;
