from flask import Blueprint, request, jsonify
from .flow_optimization import (
    find_astar_route,
    find_dijkstra_route,
    path_to_edges,
    calculate_total_distance,
    calculate_total_time
)

flow_bp = Blueprint('flow_bp', 'flow_bp')

@flow_bp.route('/route/astar', methods=['GET'])
def astar_route():
    origin = request.args.get('origin')
    dest = request.args.get('dest')
    period = request.args.get('period')
    if not origin or not dest:
        return jsonify({"error": "Missing origin or destination"}), 400
    try:
        path, graph = find_astar_route(origin, dest, period)
        edges = path_to_edges(path)
        total_distance = calculate_total_distance(path, graph)
        total_time = calculate_total_time(path, graph)
        
        return jsonify({
            "edges": edges, 
            "total_distance": total_distance,
            "total_time": total_time
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@flow_bp.route('/route/dijkstra', methods=['GET'])
def dijkstra_route():
    origin = request.args.get('origin')
    dest = request.args.get('dest')
    period= request.args.get('period')
    if not origin or not dest:
        return jsonify({"error": "Missing origin or destination"}), 400
    try:
        path, graph = find_dijkstra_route(origin, dest, period)
        edges = path_to_edges(path)
        total_distance = calculate_total_distance(path, graph)
        total_time = calculate_total_time(path, graph)
        
        return jsonify({
            "edges": edges, 
            "total_distance": total_distance,
            "total_time": total_time
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
