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
from services.pathfinding import find_shortest_path, compute_travel_time, emergency_route_astar
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
        
        if path_result:
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
            return jsonify({
                'success': False,
                'message': 'No path found between these locations'
            })

    @app.route('/api/traffic_analysis')
    def traffic_analysis():
        """API endpoint for traffic congestion analysis"""
        time_of_day = request.args.get('time', 'morning')
        congestion = analyze_traffic_congestion(graph, time_of_day=time_of_day)
        
        # Format results for the frontend
        results = []
        for (from_id, to_id), ratio in congestion.items():
            from_name = graph.nodes[from_id]['name']
            to_name = graph.nodes[to_id]['name']
            congestion_level = "High" if ratio > 0.8 else "Medium" if ratio > 0.5 else "Low"
            
            results.append({
                'from_id': from_id,
                'to_id': to_id,
                'from_name': from_name,
                'to_name': to_name,
                'ratio': ratio,
                'level': congestion_level,
                'edge_id': f"{from_id}_{to_id}"
            })
        
        return jsonify({
            'success': True,
            'time_of_day': time_of_day,
            'results': sorted(results, key=lambda x: x['ratio'], reverse=True)
        })

    @app.route('/api/transport_suggestions')
    def transport_suggestions():
        """API endpoint for public transport improvement suggestions"""
        suggestions = suggest_public_transport_improvements(graph)
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })

    @app.route('/api/metro_lines')
    def metro_lines():
        """Return metro line data"""
        return jsonify({
            'success': True,
            'lines': get_metro_lines_json(graph)
        })

    @app.route('/api/bus_routes')
    def bus_routes():
        """Return bus route data"""
        return jsonify({
            'success': True,
            'routes': get_bus_routes_json(graph)
        })

    @app.route('/api/population_density')
    def population_density():
        """Return population density data"""
        return jsonify({
            'success': True,
            'density': get_population_density_map(graph)
        })

    @app.route('/api/statistics')
    def statistics():
        """Return general network statistics"""
        return jsonify({
            'success': True,
            'statistics': get_network_statistics(graph)
        })

    @app.route('/api/optimize_road_network', methods=['GET'])
    def optimize_road_network():
        """API endpoint for MST-based road network optimization"""
        prioritize_population = request.args.get('prioritize_population', 'true').lower() == 'true'
        include_existing = request.args.get('include_existing', 'true').lower() == 'true'
        
        optimization_result = optimize_road_network_with_mst(
            graph,
            prioritize_population=prioritize_population,
            include_existing=include_existing
        )
        
        # Extract necessary data for the frontend
        result = {
            'success': True,
            'existing_roads_used': optimization_result['existing_roads_used'],
            'new_roads_proposed': optimization_result['new_roads_proposed'],
            'total_cost': optimization_result['total_cost'],
            'total_distance': optimization_result['total_distance'],
            'improvement': optimization_result['improvement'],
            'is_critical_connected': optimization_result['is_critical_connected'],
            'critical_nodes_count': optimization_result['critical_nodes_count'],
            # Include edge IDs for highlighting in the UI
            'existing_edges': [f"{road['from_id']}_{road['to_id']}" for road in optimization_result['existing_roads_used']],
            'new_edges': [f"{road['from_id']}_{road['to_id']}" for road in optimization_result['new_roads_proposed']]
        }
        
        return jsonify(result)

    @app.route('/api/emergency_route', methods=['POST'])
    def emergency_route():
        """API endpoint for emergency vehicle routing using A* search algorithm"""
        data = request.get_json()
        start_id = data.get('start_id')
        end_id = data.get('end_id')
        emergency_type = data.get('emergency_type', 'ambulance')
        time_of_day = data.get('time_of_day', 'morning')
        
        # Convert string IDs to correct type if needed
        if isinstance(start_id, str) and start_id.isdigit():
            start_id = int(start_id)
        if isinstance(end_id, str) and end_id.isdigit():
            end_id = int(end_id)
        
        result = emergency_route_astar(
            graph,
            start_id, 
            end_id, 
            time_of_day=time_of_day,
            emergency_type=emergency_type
        )
        
        if result['success']:
            return jsonify({
                'success': True,
                'path': result['path'],
                'path_names': result['path_names'],
                'path_details': result['path_details'],
                'total_time_minutes': result['total_time_minutes'],
                'total_distance_km': result['total_distance_km'],
                'emergency_type': result['emergency_type'],
                'time_saved_minutes': result['time_saved_vs_normal'],
                'percent_improvement': result['percent_improvement'],
                # Include edge IDs for highlighting in the UI
                'edges': [f"{result['path'][i]}_{result['path'][i+1]}" 
                        for i in range(len(result['path'])-1)]
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            })

    @app.route('/api/optimize_bus_routes', methods=['GET'])
    def optimize_bus_routes():
        """API endpoint for bus route optimization using dynamic programming"""
        max_buses = request.args.get('max_buses', 100, type=int)
        target_coverage = request.args.get('target_coverage', 0.85, type=float)
        
        result = optimize_bus_routes_dp(
            graph,
            target_coverage=target_coverage,
            max_buses=max_buses
        )
        
        return jsonify({
            'success': True,
            'optimized_routes': result['optimized_routes'],
            'total_routes': result['total_routes'],
            'covered_demand': result['covered_demand'],
            'total_demand': result['total_demand'],
            'coverage_percentage': result['coverage_percentage'],
            'buses_used': result['buses_used'],
            'max_buses': result['max_buses']
        })

    @app.route('/api/optimize_metro_schedule', methods=['GET'])
    def optimize_metro_schedule():
        """API endpoint for metro schedule optimization using dynamic programming"""
        peak_hours = request.args.get('peak_hours', 'morning,evening').split(',')
        off_peak_hours = request.args.get('off_peak_hours', 'afternoon,night').split(',')
        
        result = optimize_metro_schedule_dp(
            graph,
            peak_hours=peak_hours,
            off_peak_hours=off_peak_hours
        )
        
        return jsonify({
            'success': True,
            'optimized_schedules': result
        })