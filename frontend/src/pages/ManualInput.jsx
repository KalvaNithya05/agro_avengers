import React, { useState, useEffect } from "react";
import { getRecommendations, getDataOptions } from "../services/api";
import CropResult from "../components/CropResult";
import FertilizerTips from "../components/FertilizerTips";

/* 🔹 Fallback states (used if backend list is incomplete) */
const FALLBACK_STATES = [
  "Andhra Pradesh",
  "Arunachal Pradesh",
  "Assam",
  "Bihar",
  "Chhattisgarh",
  "Goa",
  "Gujarat",
  "Haryana",
  "Himachal Pradesh",
  "Jharkhand",
  "Karnataka",
  "Kerala",
  "Madhya Pradesh",
  "Maharashtra",
  "Manipur",
  "Meghalaya",
  "Mizoram",
  "Nagaland",
  "Odisha",
  "Punjab",
  "Rajasthan",
  "Sikkim",
  "Tamil Nadu",
  "Telangana", // ✅ FIXED
  "Tripura",
  "Uttar Pradesh",
  "Uttarakhand",
  "West Bengal"
];

const ManualInput = () => {
  const [formData, setFormData] = useState({
    N: 50,
    P: 40,
    K: 30,
    ph: 6.5,
    temperature: 25,
    humidity: 60,
    rainfall: 100,
    location: "Hyderabad", // UI only
    state: "",
    season: "",
    crop_type: ""
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [options, setOptions] = useState(null);
  const [optsLoading, setOptsLoading] = useState(true);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.state) {
      alert("Please select a State (required)");
      return;
    }

    setLoading(true);
      try {
      const recs = await getRecommendations(formData);
      if (recs && recs.status === "success") {
        setResult({
          ...recs,
          fertilizer_recommendations: recs.fertilizer_recommendations || []
        });
      }
    } catch (err) {
      alert("Error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let mounted = true;
    (async () => {
      setOptsLoading(true);
      try {
        const o = await getDataOptions();
        if (mounted) setOptions(o);
      } catch (e) {
        console.warn("Failed to load data options, using fallback");
      } finally {
        setOptsLoading(false);
      }
    })();
    return () => (mounted = false);
  }, []);

 const stateOptions = Array.from(
  new Set([...(options?.state || []), ...FALLBACK_STATES])
).sort();


  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-gray-800">
        Manual Data Entry
      </h1>

      {!result ? (
        <div className="bg-white p-8 rounded-lg shadow-md">
          <form
            onSubmit={handleSubmit}
            className="grid grid-cols-1 md:grid-cols-2 gap-6"
          >
            {/* Soil Inputs */}
            {[
              ["N", "Nitrogen (N)"],
              ["P", "Phosphorus (P)"],
              ["K", "Potassium (K)"]
            ].map(([key, label]) => (
              <div key={key}>
                <label className="block text-sm font-medium text-gray-700">
                  {label}
                </label>
                <input
                  type="number"
                  name={key}
                  value={formData[key]}
                  onChange={handleChange}
                  className="mt-1 block w-full p-2 border rounded"
                  required
                />
              </div>
            ))}

            <div>
              <label className="block text-sm font-medium text-gray-700">
                pH Level
              </label>
              <input
                type="number"
                step="0.1"
                name="ph"
                value={formData.ph}
                onChange={handleChange}
                className="mt-1 block w-full p-2 border rounded"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Temperature (°C)
              </label>
              <input
                type="number"
                name="temperature"
                value={formData.temperature}
                onChange={handleChange}
                className="mt-1 block w-full p-2 border rounded"
                required
              />
            </div>

            {/* State */}
            <div>
              <label className="block text-sm font-medium text-gray-700">
                State (Required)
              </label>
              <select
  name="state"
  value={formData.state}
  onChange={handleChange}
  className="mt-1 block w-full p-2 border rounded"
  required
>
  <option value="">Select state</option>
  {stateOptions.map((s) => (
    <option key={s} value={s}>{s}</option>
  ))}
</select>

            </div>

            {/* Season */}
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Season
              </label>
              <select
                name="season"
                value={formData.season}
                onChange={handleChange}
                className="mt-1 block w-full p-2 border rounded"
              >
                <option value="">Select season</option>
                {options?.season?.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>
            </div>

            {/* Crop Type */}
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Crop Type
              </label>
              <select
                name="crop_type"
                value={formData.crop_type}
                onChange={handleChange}
                className="mt-1 block w-full p-2 border rounded"
              >
                <option value="">Select crop type</option>
                {options?.crop_type?.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Humidity (%)
              </label>
              <input
                type="number"
                name="humidity"
                value={formData.humidity}
                onChange={handleChange}
                className="mt-1 block w-full p-2 border rounded"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Rainfall (mm)
              </label>
              <input
                type="number"
                name="rainfall"
                value={formData.rainfall}
                onChange={handleChange}
                className="mt-1 block w-full p-2 border rounded"
                required
              />
            </div>

            {/* Location (UI only) */}
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Location (optional)
              </label>
              <input
                type="text"
                name="location"
                value={formData.location}
                onChange={handleChange}
                className="mt-1 block w-full p-2 border rounded"
                placeholder="City or village"
              />
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
        <div className="space-y-8">
          <button
            onClick={() => setResult(null)}
            className="text-blue-600 underline"
          >
            ← Back to Form
          </button>
            <div className="grid md:grid-cols-2 gap-8">
            <CropResult results={result?.crops} />
            <FertilizerTips tips={result?.fertilizer_recommendations || []} />
          </div>
        </div>
      )}
    </div>
  );
};

export default ManualInput;
