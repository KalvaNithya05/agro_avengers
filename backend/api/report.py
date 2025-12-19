from flask import Blueprint, jsonify, request
from datetime import datetime
from services.aggregation_service import AggregationService

report_bp = Blueprint('report', __name__)
agg_service = AggregationService()

@report_bp.route('/summary', methods=['GET'])
def get_summary_report():
    """
    Returns a unified soil health report based on aggregated data.
    """
    try:
        # Fetch 30-day aggregation
        stats = agg_service.get_30_day_average()
        
        report = {
            'report_id': f"RPT-{int(datetime.now().timestamp())}",
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'period': 'Last 30 Days',
            'soil_health_summary': stats,
            'overall_status': 'Good' # Logic to determine status could be added
        }
        
        return jsonify(report)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
