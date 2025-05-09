from flask import Blueprint, request, jsonify
from .transportation import get_itinerary

transportation_bp = Blueprint('transportation_bp', __name__)


@transportation_bp.route('/itinerary', methods=['GET'])
def itinerary():
    origin = request.args.get('origin')
    dest = request.args.get('dest')

    if not origin or not dest:
        return jsonify({"error": "Missing origin or destination"}), 400

    try:
        result = get_itinerary(origin, dest)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500