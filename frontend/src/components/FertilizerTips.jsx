import React from "react";

const FertilizerTips = ({ tips }) => {
  console.log("FertilizerTips received:", tips); // 🔍 debug (keep for now)

  if (!Array.isArray(tips) || tips.length === 0) {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Fertilizer Advice</h2>
        <p className="text-gray-600">No fertilizer recommendations.</p>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4">Fertilizer Advice</h2>

      <ul className="space-y-4">
        {tips.map((tip, index) => (
          <li key={index} className="border-b last:border-b-0 pb-2">
            {tip.nutrient && (
              <p className="font-semibold text-gray-800">
                {tip.nutrient}
              </p>
            )}
            <p className="text-green-700 font-bold">
              {tip.fertilizer}
            </p>
            <p className="text-sm text-gray-600">
              {tip.reason}
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FertilizerTips;
