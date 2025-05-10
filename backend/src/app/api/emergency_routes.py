from flask import Blueprint, request, jsonify
from ..graph.networks import TransportationNetwork
from ..algorithm.emergency_routing import EmergencyRouter

emergency_bp = Blueprint('emergency', __name__)

# Global transportation network
tn = TransportationNetwork.from_json_folder('data')

@emergency_bp.route('/route', methods=['GET'])
def get_emergency_route():
    """Get optimal route for emergency vehicle."""
    origin = request.args.get('origin')
    dest = request.args.get('dest')
    emergency_type = request.args.get('type', 'ambulance')
    period = request.args.get('period', 'current')
    
    if not origin or not dest:
        return jsonify({"error": "Missing origin or destination"}), 400
        
    try:
        # Get traffic-aware road network
        G = tn.build_road_network(period=period)
        
        # Create emergency router
        router = EmergencyRouter(G, emergency_type)
        
        # Find emergency route
        path, response_time = router.find_emergency_route(origin, dest)
        
        # Convert path to edge list for frontend
        edges = [{"from": path[i], "to": path[i + 1]} 
                for i in range(len(path) - 1)]
        
        return jsonify({
            "edges": edges,
            "estimated_response_time": response_time,
            "emergency_type": emergency_type,
            "path": path
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@emergency_bp.route('/nearest-facility', methods=['GET'])
def find_nearest_facility():
    """Find nearest emergency facility (hospital, fire station, etc.)"""
    location = request.args.get('location')
    facility_type = request.args.get('type', 'hospital')
    period = request.args.get('period', 'current')
    
    if not location:
        return jsonify({"error": "Missing location parameter"}), 400
        
    try:
        # Get current network
        G = tn.build_road_network(period=period)
        
        # Find nearest facility
        nearest = EmergencyRouter.find_nearest_facility(
            G, location, facility_type, tn.facilities
        )
        
        if nearest:
            facility_data = tn.facilities[nearest]
            return jsonify({
                "facility_id": nearest,
                "facility_name": facility_data.get('name'),
                "facility_type": facility_data.get('type'),
                "coordinates": {
                    "x": facility_data.get('x'),
                    "y": facility_data.get('y')
                }
            })
        else:
            return jsonify({"error": f"No {facility_type} facility found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
