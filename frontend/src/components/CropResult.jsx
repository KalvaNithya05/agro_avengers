import React from 'react';

const CropResult = ({ results }) => {
    if (!results || results.length === 0) return null;

    return (
        <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-gray-800">Top Recommendations</h2>
                <span className="text-sm text-green-600 bg-green-100 px-2 py-1 rounded-full">AI Powered</span>
            </div>

            <div className="space-y-3">
                {results.map((item, index) => (
                    <div
                        key={index}
                        className="flex items-center justify-between p-4 bg-gray-50 hover:bg-green-50 rounded-lg border border-gray-100 transition-colors"
                    >
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 bg-green-200 rounded-full flex items-center justify-center text-xl">
                                {/* Icon placeholder logic could go here based on crop name */}
                                🌱
                            </div>
                            <div>
                                <h3 className="font-bold text-lg text-gray-800 capitalize leading-tight">
                                    {item.crop}
                                </h3>
                                <p className="text-xs text-gray-500">Highly Suitable</p>
                            </div>
                        </div>

                        <div className="flex flex-col items-end">
                            <span className="text-sm font-bold text-green-700">
                                {Math.round(item.confidence * 100)}%
                            </span>
                            <div className="w-24 h-2 bg-gray-200 rounded-full mt-1 overflow-hidden">
                                <div
                                    className="h-full bg-green-500 rounded-full"
                                    style={{ width: `${item.confidence * 100}%` }}
                                ></div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default CropResult;
