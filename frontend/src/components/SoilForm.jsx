import React, { useState } from 'react';

const SoilForm = ({ onSubmit, loading }) => {
    const [formData, setFormData] = useState({
        n: '',
        p: '',
        k: '',
        ph: '',
        city: ''
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(formData);
    };

    return (
        <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md max-w-lg mx-auto">
            <h2 className="text-2xl font-bold mb-6 text-center text-primary">Enter Soil Details</h2>

            <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                    <label className="block text-gray-700 mb-2">Nitrogen (N)</label>
                    <input
                        type="number"
                        name="n"
                        value={formData.n}
                        onChange={handleChange}
                        className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary"
                        required
                        placeholder="e.g. 90"
                    />
                </div>
                <div>
                    <label className="block text-gray-700 mb-2">Phosphorus (P)</label>
                    <input
                        type="number"
                        name="p"
                        value={formData.p}
                        onChange={handleChange}
                        className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary"
                        required
                        placeholder="e.g. 42"
                    />
                </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                    <label className="block text-gray-700 mb-2">Potassium (K)</label>
                    <input
                        type="number"
                        name="k"
                        value={formData.k}
                        onChange={handleChange}
                        className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary"
                        required
                        placeholder="e.g. 43"
                    />
                </div>
                <div>
                    <label className="block text-gray-700 mb-2">pH Level</label>
                    <input
                        type="number"
                        step="0.1"
                        name="ph"
                        value={formData.ph}
                        onChange={handleChange}
                        className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary"
                        required
                        placeholder="e.g. 6.5"
                    />
                </div>
            </div>

            <div className="mb-6">
                <label className="block text-gray-700 mb-2">City / Location</label>
                <input
                    type="text"
                    name="city"
                    value={formData.city}
                    onChange={handleChange}
                    className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary"
                    required
                    placeholder="e.g. Pune"
                />
            </div>

            <button
                type="submit"
                disabled={loading}
                className="w-full bg-primary text-white py-3 rounded-lg font-semibold hover:bg-green-700 transition disabled:opacity-50"
            >
                {loading ? 'Analyzing...' : 'Get Recommendation'}
            </button>
        </form>
    );
};

export default SoilForm;
