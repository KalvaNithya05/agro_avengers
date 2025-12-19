const weatherService = require('../services/weatherService');
const mlService = require('../services/mlService');
const pdfService = require('../services/pdfService');

exports.getRecommendation = async (req, res) => {
    try {
        const { n, p, k, ph, city } = req.body;

        if (!n || !p || !k || !ph || !city) {
            return res.status(400).json({ error: 'All fields are required' });
        }

        // 1. Fetch Weather Data
        const weatherData = await weatherService.getWeather(city);

        // 2. Call ML Model
        const recommendations = await mlService.predictCrop({ n, p, k, ph, ...weatherData });

        // 3. Return Response
        res.json({
            recommendations,
            weather: weatherData
        });

    } catch (error) {
        console.error('Error in recommendation:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
};

exports.downloadReport = async (req, res) => {
    try {
        const { n, p, k, ph, city } = req.body;

        if (!n || !p || !k || !ph || !city) {
            return res.status(400).json({ error: 'All fields are required' });
        }

        // Re-fetch data to ensure fresh report (or pass full data from frontend if prefered, but fetching is safer)
        const weatherData = await weatherService.getWeather(city);
        const recommendations = await mlService.predictCrop({ n, p, k, ph, ...weatherData });

        const reportData = {
            n, p, k, ph, city,
            weather: weatherData,
            recommendations
        };

        pdfService.generateReport(reportData, res);

    } catch (error) {
        console.error('Error generating PDF:', error);
        res.status(500).json({ error: 'Failed to generate report' });
    }
};
