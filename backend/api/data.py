from flask import Blueprint, jsonify, request
from config.supabase_client import supabase

data_bp = Blueprint('data', __name__)


@data_bp.route('/options', methods=['GET'])
def get_options():
    """Return distinct values for states, crops, seasons, crop_type and zones."""
    try:
        if supabase is None:
            return jsonify({'error': 'supabase client not configured'}), 500

        fields = ['state', 'crop', 'season', 'crop_type', 'agro_climatic_zone', 'district']
        result = {}
        for f in fields:
            try:
                resp = supabase.table('mitti_mitra_data').select(f).neq(f, None).limit(1000).execute()
                # resp.data is list of dicts
                vals = []
                if hasattr(resp, 'data') and resp.data:
                    vals = list({r.get(f) for r in resp.data if r.get(f) is not None})
                result[f] = sorted(vals)
            except Exception:
                result[f] = []

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/records', methods=['GET'])
def get_records():
    """Return filtered records from mitti_mitra_data. Query params are allowed: state, crop, season, crop_type.

    This is a simple passthrough to allow frontend to fetch matching rows for previews.
    """
    try:
        if supabase is None:
            return jsonify({'error': 'supabase client not configured'}), 500

        q = supabase.table('mitti_mitra_data').select('*').limit(500)
        # Apply filters
        for param in ['state', 'crop', 'season', 'crop_type', 'agro_climatic_zone']:
            val = request.args.get(param)
            if val:
                q = q.eq(param, val)

        resp = q.execute()
        data = getattr(resp, 'data', [])
        return jsonify({'count': len(data), 'data': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
