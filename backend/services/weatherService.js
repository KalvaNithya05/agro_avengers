const axios = require('axios');

exports.getWeather = async (city) => {
    // Mock implementation for now as we don't have a real API key yet
    // In production, use: process.env.WEATHER_API_KEY

    console.log(`Fetching weather for ${city}...`);

    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));

    // Return mock data based on city hash or random
    return {
        temp: 28.5,
        humidity: 70,
        rainfall: 150
    };
};
