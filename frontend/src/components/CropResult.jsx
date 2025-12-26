const CropResult = ({ results }) => {
    if (!results || results.length === 0) {
        return <p className="text-gray-600">No crop recommendations available.</p>;
    }

    return (
        <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Recommended Crops</h2>

            {results.map((item, index) => (
                <div key={index} className="border-b last:border-b-0 pb-3 mb-3">
                    <p className="font-bold text-lg">{item.crop}</p>

                    <p className="text-sm text-gray-700">
                        Probability: {(item.probability * 100).toFixed(2)}%
                    </p>

                    {item.predicted_yield !== null && item.predicted_yield !== undefined ? (
                        <p className="text-sm text-green-700">
                            Expected Yield: {item.predicted_yield.toFixed(2)} tons/hectare
                        </p>
                    ) : (
                        <p className="text-sm text-gray-500">Expected Yield: N/A</p>
                    )}
                </div>
            ))}
        </div>
    );
};

export default CropResult;
