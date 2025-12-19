import React from 'react';

const SensorCard = ({ title, value, unit, colorClass = "border-blue-500 text-blue-600" }) => {
    return (
        <div className={`p-4 bg-white rounded-lg shadow hover:shadow-md transition-shadow duration-200 border-l-4 ${colorClass}`}>
            <h3 className="text-gray-500 text-xs font-semibold uppercase tracking-wider">{title}</h3>
            <div className="mt-2 flex items-baseline">
                <span className="text-2xl font-bold text-gray-800">
                    {value !== null && value !== undefined ? value : '--'}
                </span>
                <span className="ml-1 text-gray-600 text-sm font-medium">{unit}</span>
            </div>
        </div>
    );
};

export default SensorCard;
