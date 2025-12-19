const { spawn } = require('child_process');
const path = require('path');

exports.predictCrop = (inputData) => {
    return new Promise((resolve, reject) => {
        // Path to python script
        const scriptPath = path.join(__dirname, '../../ml/predict.py');

        // Prepare arguments
        const args = [
            inputData.n,
            inputData.p,
            inputData.k,
            inputData.ph,
            inputData.temp,
            inputData.humidity,
            inputData.rainfall
        ];

        console.log('Running ML script with args:', args);

        const pythonProcess = spawn('python', [scriptPath, ...args]);

        let dataString = '';

        pythonProcess.stdout.on('data', (data) => {
            dataString += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`ML Error: ${data}`);
        });

        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                // Fallback if python fails (for demo purposes if python env not set)
                console.warn('ML script failed, returning fallback data');
                resolve(['rice', 'maize', 'jute']); // Fallback
                return;
            }

            try {
                const results = JSON.parse(dataString);
                resolve(results);
            } catch (e) {
                console.error('Failed to parse ML output');
                resolve(['rice', 'maize', 'jute']); // Fallback
            }
        });
    });
};
