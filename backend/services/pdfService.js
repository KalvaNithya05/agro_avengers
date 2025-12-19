const PDFDocument = require('pdfkit');
const fs = require('fs');
const path = require('path');

exports.generateReport = (data, res) => {
    const doc = new PDFDocument({ margin: 50 });

    // Set response headers
    res.setHeader('Content-Type', 'application/pdf');
    res.setHeader('Content-Disposition', 'attachment; filename=crop-recommendation-report.pdf');

    doc.pipe(res);

    // 1. Title
    doc.fontSize(24).fillColor('#2E7D32').text('MITTI MITRA', { align: 'center' });
    doc.fontSize(16).fillColor('#4caf50').text('Crop Recommendation Report', { align: 'center' });
    doc.moveDown(2);

    // 2. Farmer Input Summary
    doc.fontSize(14).fillColor('#000000').text('Farmer Input Summary', { underline: true });
    doc.moveDown(0.5);
    doc.fontSize(12).text(`Location: ${data.city}`);
    doc.text(`Soil pH: ${data.ph}`);
    doc.text(`Nitrogen (N): ${data.n}`);
    doc.text(`Phosphorus (P): ${data.p}`);
    doc.text(`Potassium (K): ${data.k}`);
    doc.moveDown(2);

    // 3. Recommended Crops
    doc.fontSize(14).text('Recommended Crops', { underline: true });
    doc.moveDown(0.5);

    data.recommendations.forEach((rec, index) => {
        const isBest = index === 0;
        const color = isBest ? '#2E7D32' : '#000000';

        doc.fontSize(13).fillColor(color).text(`${index + 1}. ${rec.crop.toUpperCase()} (${rec.confidence}% Suitability)`, {
            continued: false
        });

        if (isBest) {
            doc.fontSize(10).fillColor('#FF9800').text('★ Top Recommendation', { indent: 20 });
        }

        doc.moveDown(0.5);
        doc.fontSize(10).fillColor('#555555');
        rec.reasoning.forEach(reason => {
            doc.text(`• ${reason}`, { indent: 20 });
        });
        doc.moveDown(1);
    });

    // 4. Weather Summary
    doc.addPage();
    doc.fontSize(14).fillColor('#000000').text('Weather Analysis', { underline: true });
    doc.moveDown(0.5);
    doc.fontSize(12);
    doc.text(`Temperature: ${data.weather.temp}°C`);
    doc.text(`Humidity: ${data.weather.humidity}%`);
    doc.text(`Rainfall: ${data.weather.rainfall}mm`);

    doc.moveDown(1);
    doc.fontSize(10).text('Based on current weather data, conditions are favorable for the recommended crops.');

    // 5. Disclaimer
    doc.moveDown(4);
    doc.fontSize(10).fillColor('#999999').text('Disclaimer: This recommendation is advisory and based on available data. Please consult with a local agronomist before making final decisions.', { align: 'center' });

    doc.end();
};
