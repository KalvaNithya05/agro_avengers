import React, { useState } from 'react';
import { getRecommendations } from '../services/api';
import CropResult from '../components/CropResult';
import FertilizerTips from '../components/FertilizerTips';

const ManualInput = () => {
    const [formData, setFormData] = useState({
        N: 50, P: 40, K: 30, ph: 6.5, temperature: 25, humidity: 60, rainfall: 100, location: 'Hyderabad'
    });
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const recs = await getRecommendations(formData);
            if (recs && recs.status === 'success') {
                setResult(recs);
            }
        } catch (e) {
            alert("Error: " + e.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-6 max-w-4xl mx-auto">
            <h1 className="text-2xl font-bold mb-6 text-gray-800">Manual Data Entry</h1>

            {!result ? (
                <div className="bg-white p-8 rounded-lg shadow-md">
                    <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Nitrogen (N)</label>
                            <input type="number" name="N" value={formData.N} onChange={handleChange} className="mt-1 block w-full p-2 border rounded" required />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Phosphorus (P)</label>
                            <input type="number" name="P" value={formData.P} onChange={handleChange} className="mt-1 block w-full p-2 border rounded" required />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Potassium (K)</label>
                            <input type="number" name="K" value={formData.K} onChange={handleChange} className="mt-1 block w-full p-2 border rounded" required />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">pH Level</label>
                            <input type="number" step="0.1" name="ph" value={formData.ph} onChange={handleChange} className="mt-1 block w-full p-2 border rounded" required />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Temperature (°C)</label>
                            <input type="number" name="temperature" value={formData.temperature} onChange={handleChange} className="mt-1 block w-full p-2 border rounded" required />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Humidity (%)</label>
                            <input type="number" name="humidity" value={formData.humidity} onChange={handleChange} className="mt-1 block w-full p-2 border rounded" required />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Rainfall (mm)</label>
                            <input type="number" name="rainfall" value={formData.rainfall} onChange={handleChange} className="mt-1 block w-full p-2 border rounded" required />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Location</label>
                            <input type="text" name="location" value={formData.location} onChange={handleChange} className="mt-1 block w-full p-2 border rounded" placeholder="City or State" />
                        </div>

                        <div className="md:col-span-2 pt-4">
                            <button
                                type="submit"
                                disabled={loading}
                                className="w-full bg-blue-600 text-white p-3 rounded font-bold hover:bg-blue-700 transition"
                            >
                                {loading ? "Processing..." : "Get Recommendations"}
                            </button>
                        </div>
                    </form>
                </div>
            ) : (
                <div className="animate-fade-in-up space-y-8">
                    <button onClick={() => setResult(null)} className="text-blue-600 underline mb-4">← Back to Form</button>
                    <div className="grid md:grid-cols-2 gap-8">
                        <CropResult results={result.crops} />
                        <FertilizerTips tips={result.fertilizer_recommendations} />
                    </div>
                </div>
            )}
        </div>
    );
};
export default ManualInput;
