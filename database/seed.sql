-- Seed Data for Testing

INSERT INTO sensor_readings (device_id, temperature, humidity, rainfall, ph, nitrogen, phosphorus, potassium, timestamp)
VALUES 
('pi_01', 28.5, 60.0, 0.0, 6.5, 100.0, 40.0, 120.0, NOW()),
('pi_01', 29.1, 58.0, 0.0, 6.6, 98.0, 39.5, 118.0, NOW() - INTERVAL '1 hour'),
('pi_01', 27.4, 65.0, 12.5, 6.4, 102.0, 41.0, 122.0, NOW() - INTERVAL '2 hours'),
('pi_01', 26.0, 70.0, 50.0, 6.3, 105.0, 42.0, 125.0, NOW() - INTERVAL '3 hours');
