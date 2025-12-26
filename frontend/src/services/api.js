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
        // Do not pass `location` to the ML backend; state is required for ML
        const payload = { ...inputData };
        if ('location' in payload) delete payload.location;

        const response = await fetch(`${API_BASE_URL}/predict/recommend`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
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

export const getDataOptions = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/data/options`);
        if (!response.ok) throw new Error('Failed to fetch options');
        return await response.json();
    } catch (error) {
        console.error('Error fetching data options:', error);
        return null;
    }
};

export const getRecords = async (filters = {}) => {
    try {
        const params = new URLSearchParams(filters);
        const response = await fetch(`${API_BASE_URL}/data/records?${params.toString()}`);
        if (!response.ok) throw new Error('Failed to fetch records');
        return await response.json();
    } catch (error) {
        console.error('Error fetching records:', error);
        return null;
    }
};
