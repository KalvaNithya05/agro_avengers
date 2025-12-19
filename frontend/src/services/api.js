const API_BASE_URL = 'http://localhost:5000/api';

export const getLatestSensorData = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/sensor/latest`);
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error("Error fetching sensor data:", error);
        return null;
    }
};

export const getRecommendations = async (inputData) => {
    try {
        const response = await fetch(`${API_BASE_URL}/predict/recommend`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(inputData),
        });
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error("Error getting recommendations:", error);
        return null;
    }
};

export const getSoilReport = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/report/summary`);
        if (!response.ok) throw new Error('Failed to fetch report');
        return await response.json();
    } catch (error) {
        console.error("Error fetching report:", error);
        return null;
    }
}
