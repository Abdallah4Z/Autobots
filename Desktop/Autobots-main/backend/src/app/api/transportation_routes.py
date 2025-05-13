from flask import Blueprint, request, jsonify
from .transportation import get_itinerary, ROUTE_CACHE

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


@transportation_bp.route('/cache/status', methods=['GET'])
def cache_status():
    """Return information about the route cache."""
    return jsonify({
        "cached_routes_count": len(ROUTE_CACHE),
        "sample_routes": list(ROUTE_CACHE.keys())[:10]  # Show first 10 routes
    })


@transportation_bp.route('/cache/precompute', methods=['POST'])
def precompute_routes():
    """Precompute routes between important nodes."""
    from .transportation import G

# Find important nodes (hubs with many connections)
    important_nodes = [node for node in G.nodes() if G.degree(node) > 2][:20]

# Precompute some common routes
    for origin in important_nodes[:10]:  # Limit to avoid long computation
        for dest in important_nodes[:10]:
            if origin != dest:
                try:
                    get_itinerary(origin, dest)
                except Exception:
                    pass

    return jsonify({
        "success": True,
        "cached_routes": len(ROUTE_CACHE)
    })