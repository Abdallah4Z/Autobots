from flask import request, jsonify
import sys
import os

# Add parent directories to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
api_dir = os.path.dirname(current_dir)  # app/
app_dir = os.path.dirname(api_dir)  # src/app
src_dir = os.path.dirname(app_dir)  # src
backend_dir = os.path.dirname(src_dir)  # backend
project_dir = os.path.dirname(backend_dir)  # Project

# Add them to the path in reverse order to prioritize modules
sys.path.insert(0, api_dir)
sys.path.insert(0, app_dir)
sys.path.insert(0, src_dir)
sys.path.insert(0, backend_dir)
sys.path.insert(0, project_dir)

# Import the required modules directly without relative paths
from utils.data_formatting import (
    get_all_nodes_json, get_all_edges_json, get_metro_lines_json,
    get_bus_routes_json, get_population_density_map
)
from utils.visualization import get_graph_image_base64
from services.pathfinding import find_shortest_path, compute_travel_time, emergency_route_astar, multimodal_route
from services.analysis import analyze_traffic_congestion, suggest_public_transport_improvements, get_network_statistics
from services.optimization import optimize_road_network_with_mst, optimize_bus_routes_dp, optimize_metro_schedule_dp

def register_routes(app, graph):
    """Register all API routes with the Flask application"""
    
    @app.route('/api/graph_data')
    def graph_data():
        """Return graph data in JSON format for interactive frontend visualization"""
        include_potential = request.args.get('potential', 'false').lower() == 'true'
        
        return jsonify({
            'nodes': get_all_nodes_json(graph),
            'edges': get_all_edges_json(graph, include_potential)
        })

    @app.route('/api/graph_image')
    def graph_image():
        """Return a base64 encoded image of the graph"""
        include_potential = request.args.get('potential', 'false').lower() == 'true'
        image_base64 = get_graph_image_base64(graph, include_potential)
        
        return jsonify({
            'success': True,
            'image': image_base64
        })

    @app.route('/api/nodes')
    def get_nodes():
        """Return all node data for dropdowns and selections"""
        return jsonify({
            'success': True,
            'nodes': get_all_nodes_json(graph)
        })

    @app.route('/api/find_path', methods=['POST'])
    def find_path():
        """API endpoint to find paths between locations"""
        data = request.get_json()
        start_id = data.get('start_id')
        end_id = data.get('end_id')
        mode = data.get('mode', 'distance')  # 'distance' or 'time'
        time_of_day = data.get('time_of_day', 'morning')
        
        # Convert string IDs to correct type if needed
        if isinstance(start_id, str) and start_id.isdigit():
            start_id = int(start_id)
        if isinstance(end_id, str) and end_id.isdigit():
            end_id = int(end_id)
        
        if mode == 'distance':
            path_result = find_shortest_path(graph, start_id, end_id)
        else:  # time-based
            path_result = compute_travel_time(graph, start_id, end_id, time_of_day=time_of_day)
        
        # Check if the result indicates success
        if path_result.get('success', False):
            return jsonify({
                'success': True,
                'path': path_result['path'],
                'path_names': path_result['path_names'],
                'distance': path_result.get('distance', path_result.get('total_distance_km')),
                'time': path_result.get('total_time_minutes', None),
                # Include edge IDs for highlighting in the UI
                'edges': [f"{path_result['path'][i]}_{path_result['path'][i+1]}" 
                        for i in range(len(path_result['path'])-1)]
            })
        else:
            # Handle the error case - use the message from the result if available
            return jsonify({
                'success': False,
                'message': path_result.get('message', 'No path found between these locations'),
                'details': path_result.get('details', '')
            })

    @app.route('/api/statistics')
    def statistics():
        """Return network statistics"""
        stats = get_network_statistics(graph)
        return jsonify({
            'success': True,
            'statistics': stats
        })
        
    @app.route('/api/metro_lines')
    def metro_lines():
        """Return metro line data"""
        return jsonify({
            'success': True,
            'metro_lines': get_metro_lines_json(graph)
        })
        
    @app.route('/api/bus_routes')
    def bus_routes():
        """Return bus route data"""
        return jsonify({
            'success': True,
            'bus_routes': get_bus_routes_json(graph)
        })
        
    @app.route('/api/population_density')
    def population_density():
        """Return population density data for heatmap visualization"""
        return jsonify({
            'success': True,
            'density_map': get_population_density_map(graph)
        })
        
    @app.route('/api/traffic_analysis')
    def traffic_analysis():
        """Analyze traffic patterns and congestion"""
        time_of_day = request.args.get('time', 'morning')
        analysis = analyze_traffic_congestion(graph, time_of_day)
        
        # We need to convert any tuple keys to strings since JSON cannot have tuple keys
        # This is a helper function to recursively convert all dict keys to strings
        def convert_keys_to_str(obj):
            if isinstance(obj, dict):
                return {str(k) if isinstance(k, tuple) else k: convert_keys_to_str(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_keys_to_str(item) for item in obj]
            else:
                return obj
                
        # Convert any tuple keys to strings
        analysis = convert_keys_to_str(analysis)
        
        return jsonify({
            'success': True,
            'congestion_data': analysis
        })
        
    @app.route('/api/transport_suggestions')
    def transport_suggestions():
        """Get suggestions for public transportation improvements"""
        suggestions = suggest_public_transport_improvements(graph)
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
        
    @app.route('/api/emergency_route', methods=['POST'])
    def emergency_route():
        """Find optimal emergency routes with priority for emergency vehicles"""
        data = request.get_json()
        start_id = data.get('start_id')
        end_id = data.get('end_id')
        
        # Convert string IDs to correct type if needed
        if isinstance(start_id, str) and start_id.isdigit():
            start_id = int(start_id)
        if isinstance(end_id, str) and end_id.isdigit():
            end_id = int(end_id)
            
        emergency_path = emergency_route_astar(graph, start_id, end_id)
        
        # Check if the result indicates success
        if emergency_path.get('success', False):
            return jsonify({
                'success': True,
                'path': emergency_path['path'],
                'path_names': emergency_path['path_names'],
                'distance': emergency_path.get('distance', emergency_path.get('total_distance_km')),
                'time': emergency_path.get('total_time_minutes', None),
                # Include edge IDs for highlighting in the UI
                'edges': [f"{emergency_path['path'][i]}_{emergency_path['path'][i+1]}" 
                        for i in range(len(emergency_path['path'])-1)]
            })
        else:
            # Handle the error case
            return jsonify({
                'success': False,
                'message': emergency_path.get('message', 'No emergency route found between these locations'),
                'details': emergency_path.get('details', '')
            })
            
    @app.route('/api/multimodal_route', methods=['POST'])
    def multimodal_path():
        """Find optimal route using multiple transportation modes"""
        data = request.get_json()
        start_id = data.get('start_id')
        end_id = data.get('end_id')
        time_of_day = data.get('time_of_day', 'morning')
        preferred_modes = data.get('preferred_modes')
        max_transfers = data.get('max_transfers')
        
        # Convert string IDs to correct type if needed
        if isinstance(start_id, str) and start_id.isdigit():
            start_id = int(start_id)
        if isinstance(end_id, str) and end_id.isdigit():
            end_id = int(end_id)
            
        multimodal_result = multimodal_route(
            graph, start_id, end_id, time_of_day, preferred_modes, max_transfers
        )
        
        # Check if the result indicates success
        if multimodal_result.get('success', False):
            return jsonify({
                'success': True,
                'path': multimodal_result['path'],
                'path_names': multimodal_result['path_names'],
                'distance': multimodal_result.get('total_distance_km', 0),
                'time': multimodal_result.get('total_time_minutes', 0),
                'modes': multimodal_result.get('modes', []),
                'transfers': multimodal_result.get('transfers', 0),
                # Include edge IDs for highlighting in the UI
                'edges': [f"{multimodal_result['path'][i]}_{multimodal_result['path'][i+1]}" 
                        for i in range(len(multimodal_result['path'])-1)]
            })
        else:
            # Handle the error case
            return jsonify({
                'success': False,
                'message': multimodal_result.get('message', 'No multimodal route found between these locations'),
                'details': multimodal_result.get('details', '')
            })
            
    @app.route('/api/optimize_road_network')
    def optimize_roads():
        """Optimize road network using MST algorithm"""
        prioritize_population = request.args.get('prioritize_population', 'false').lower() == 'true'
        include_existing = request.args.get('include_existing', 'true').lower() == 'true'
        max_budget = float(request.args.get('max_budget', 1000000))
        
        # Change function call to match the expected number of parameters
        optimization = optimize_road_network_with_mst(
            graph, prioritize_population, include_existing
        )
        
        return jsonify({
            'success': True,
            **optimization
        })
        
    @app.route('/api/optimize_bus_routes')
    def optimize_buses():
        """Optimize bus routes using dynamic programming"""
        max_buses = int(request.args.get('max_buses', 100))
        target_coverage = float(request.args.get('target_coverage', 0.8))
        
        optimization = optimize_bus_routes_dp(graph, target_coverage, max_buses)
        
        return jsonify({
            'success': True,
            **optimization
        })
        
    @app.route('/api/optimize_metro_schedule')
    def optimize_metro():
        """Optimize metro schedule using dynamic programming"""
        peak_hours = request.args.get('peak_hours', 'morning,evening').split(',')
        off_peak_hours = request.args.get('off_peak_hours', 'afternoon,night').split(',')
        
        optimization = optimize_metro_schedule_dp(graph, peak_hours, off_peak_hours)
        
        # Fix: If optimization is a list, we need to wrap it in a dictionary
        # instead of trying to unpack it
        return jsonify({
            'success': True,
            'optimized_schedules': optimization  # Directly include the list without unpacking
        })