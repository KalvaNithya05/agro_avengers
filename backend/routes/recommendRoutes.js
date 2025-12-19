const express = require('express');
const router = express.Router();
const recommendController = require('../controllers/recommendController');

router.post('/', recommendController.getRecommendation);
router.post('/pdf', recommendController.downloadReport);

module.exports = router;
