import React, { useState } from 'react';
import Layout from '../components/Layout';
import SoilForm from '../components/SoilForm';
import Results from '../components/Results';
import { getRecommendation, downloadReport } from '../services/api';

const Home = () => {
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);
    const [lastFormData, setLastFormData] = useState(null);

    const handleFormSubmit = async (formData) => {
        setLoading(true);
        setLastFormData(formData);
        try {
            const data = await getRecommendation(formData);
            setResults(data);
        } catch (error) {
            console.error("Error fetching recommendation:", error);
            alert("Failed to get recommendations. Please ensure the backend is running.");
        } finally {
            setLoading(false);
        }
    };

    const handleDownloadReport = async () => {
        if (!lastFormData) return;
        try {
            const blob = await downloadReport(lastFormData);
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'mitti-mitra-report.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            console.error("Error downloading report:", error);
            alert("Failed to download report.");
        }
    };

    return (
        <Layout>
            <div className="max-w-4xl mx-auto">
                <div className="text-center mb-10">
                    <h1 className="text-4xl font-bold text-gray-900 mb-4">Find the Perfect Crop for Your Soil</h1>
                    <p className="text-lg text-gray-600">
                        Use our AI-powered tool to get personalized crop recommendations based on your soil health and local weather.
                    </p>
                </div>

                <SoilForm onSubmit={handleFormSubmit} loading={loading} />

                <Results data={results} onDownload={handleDownloadReport} />
            </div>
        </Layout>
    );
};

export default Home;
