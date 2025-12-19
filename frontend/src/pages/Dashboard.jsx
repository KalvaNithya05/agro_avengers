import React, { useEffect, useState } from 'react';
import SensorCard from '../components/SensorCard';
import { getLatestSensorData } from '../services/api';

const Dashboard = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    const fetchData = async () => {
        const result = await getLatestSensorData();
        if (result) setData(result);
        setLoading(false);
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 60000); // 1 min refresh
        return () => clearInterval(interval);
    }, []);

    if (loading) return <div className="text-center p-10 text-gray-500">Connecting to Pi...</div>;
    if (!data) return (
        <div className="text-center p-10">
            <p className="text-red-500 font-bold">System Offline</p>
            <p className="text-gray-500">Could not fetch data from Backend/Pi.</p>
            <button onClick={fetchData} className="mt-4 px-4 py-2 bg-blue-100 text-blue-700 rounded hover:bg-blue-200">Retry Connection</button>
        </div>
    );

    return (
        <div className="p-6 fade-in">
            <header className="mb-8 flex justify-between items-end">
                <div>
                    <h1 className="text-3xl font-bold text-gray-800">Live Soil Monitor</h1>
                    <p className="text-gray-500 mt-1">Real-time data from Raspberry Pi Sensors</p>
                </div>
                <div className="text-right text-xs text-gray-400">
                    Last Updated: <br />
                    <span className="font-mono text-gray-600">{data.timestamp ? new Date(data.timestamp).toLocaleTimeString() : '--'}</span>
                </div>
            </header>

            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                <SensorCard title="Temperature" value={data.temperature} unit="°C" colorClass="border-red-500 text-red-600" />
                <SensorCard title="Humidity" value={data.humidity} unit="%" colorClass="border-blue-500 text-blue-600" />
                <SensorCard title="Soil pH" value={data.ph} unit="pH" colorClass="border-purple-500 text-purple-600" />
                <SensorCard title="Rainfall (Est)" value={data.rainfall} unit="mm" colorClass="border-cyan-500 text-cyan-600" />

                <SensorCard title="Nitrogen (N)" value={data.nitrogen} unit="mg/kg" colorClass="border-green-600 text-green-700" />
                <SensorCard title="Phosphorus (P)" value={data.phosphorus} unit="mg/kg" colorClass="border-orange-500 text-orange-600" />
                <SensorCard title="Potassium (K)" value={data.potassium} unit="mg/kg" colorClass="border-yellow-500 text-yellow-600" />
            </div>

            <div className="mt-8 p-4 bg-gray-50 rounded border border-gray-200 text-center">
                <p className="text-sm text-gray-500">Device ID: <span className="font-mono font-bold">{data.device_id || 'Unknown'}</span></p>
            </div>
        </div>
    );
};

export default Dashboard;
