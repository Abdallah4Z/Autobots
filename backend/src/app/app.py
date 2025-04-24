from flask import Flask, request, jsonify
from flask_cors import CORS
import networkx as nx
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64
import json

class CairoTransportationGraph:
    def __init__(self):
        self.nodes = {}  # Maps ID to node data
        self.existing_roads = []
        self.potential_roads = []
        self.metro_lines = []
        self.bus_routes = []
        self.traffic_data = {}
        self.transport_demand = {}
        
    def load_from_csv(self, neighborhoods_file, facilities_file, existing_roads_file, 
                      potential_roads_file, traffic_file, metro_file, bus_file, demand_file):
        """Load all data from CSV files"""
        
        # Load neighborhoods and districts
        neighborhoods_df = pd.read_csv(neighborhoods_file)
        for _, row in neighborhoods_df.iterrows():
            self.nodes[row['ID']] = {
                'name': row['Name'],
                'population': row['Population'],
                'type': row['Type'],
                'x': row['X-coordinate'],
                'y': row['Y-coordinate'],
                'is_facility': False
            }
            
        # Load facilities
        facilities_df = pd.read_csv(facilities_file)
        for _, row in facilities_df.iterrows():
            self.nodes[row['ID']] = {
                'name': row['Name'],
                'type': row['Type'],
                'x': row['X-coordinate'],
                'y': row['Y-coordinate'],
                'is_facility': True
            }
            
        # Load existing roads
        roads_df = pd.read_csv(existing_roads_file)
        self.existing_roads = [
            (row['FromID'], row['ToID'], row['Distance(km)'], 
             row['Current Capacity(vehicles/hour)'], row['Condition(1-10)']) 
            for _, row in roads_df.iterrows()
        ]
        
        # Load potential roads
        potential_df = pd.read_csv(potential_roads_file)
        self.potential_roads = [
            (row['FromID'], row['ToID'], row['Distance(km)'], 
             row['Estimated Capacity(vehicles/hour)'], row['Construction Cost(Million EGP)']) 
            for _, row in potential_df.iterrows()
        ]
        
        # Load traffic data
        traffic_df = pd.read_csv(traffic_file)
        for _, row in traffic_df.iterrows():
            road_id = f"{row['FromID']}{row['ToID']}"
            self.traffic_data[road_id] = {
                'morning': row['Morning Peak(veh/h)'],
                'afternoon': row['Afternoon(veh/h)'],
                'evening': row['Evening Peak(veh/h)'],
                'night': row['Night(veh/h)']
            }
            
        # Load metro lines
        metro_df = pd.read_csv(metro_file)
        self.metro_lines = [
            (row['LineID'], row['Name'], row['Stations(comma-separated IDs)'], row['Daily Passengers']) 
            for _, row in metro_df.iterrows()
        ]
        
        # Load bus routes
        bus_df = pd.read_csv(bus_file)
        self.bus_routes = [
            (row['RouteID'], row['Stops(comma-separated IDs)'], 
             row['Buses Assigned'], row['Daily Passengers']) 
            for _, row in bus_df.iterrows()
        ]
        
        # Load transport demand
        demand_df = pd.read_csv(demand_file)
        for _, row in demand_df.iterrows():
            from_id, to_id = row['FromID'], row['ToID']
            key = f"{from_id}_{to_id}"
            self.transport_demand[key] = row['Daily Passengers']
    
    def build_networkx_graph(self, include_potential=False):
        """Create a NetworkX graph from the loaded data"""
        G = nx.Graph()
        
        # Add nodes
        for node_id, data in self.nodes.items():
            G.add_node(node_id, **data)
            
        # Add existing roads as edges
        for road in self.existing_roads:
            from_id, to_id, distance, capacity, condition = road
            G.add_edge(from_id, to_id, 
                       distance=distance, 
                       capacity=capacity, 
                       condition=condition,
                       type='existing')
            
        # Add potential roads if requested
        if include_potential:
            for road in self.potential_roads:
                from_id, to_id, distance, capacity, cost = road
                G.add_edge(from_id, to_id, 
                           distance=distance, 
                           capacity=capacity, 
                           cost=cost,
                           type='potential')
                
        return G
    
    def get_graph_image_base64(self, include_potential=False):
        """Return the graph visualization as a base64 encoded image"""
        plt.figure(figsize=(12, 10))
        G = self.build_networkx_graph(include_potential)
        
        # Create visualization
        pos = {node: (self.nodes[node]['x'], self.nodes[node]['y']) for node in G.nodes()}
        
        # Draw nodes with different colors
        residential = [n for n in G.nodes() if not self.nodes[n]['is_facility'] and self.nodes[n]['type'] == 'Residential']
        business = [n for n in G.nodes() if not self.nodes[n]['is_facility'] and self.nodes[n]['type'] == 'Business']
        mixed = [n for n in G.nodes() if not self.nodes[n]['is_facility'] and self.nodes[n]['type'] == 'Mixed']
        other_districts = [n for n in G.nodes() if not self.nodes[n]['is_facility'] and self.nodes[n]['type'] not in ['Residential', 'Business', 'Mixed']]
        facilities = [n for n in G.nodes() if self.nodes[n]['is_facility']]
        
        nx.draw_networkx_nodes(G, pos, nodelist=residential, node_color='green', node_size=300, label='Residential')
        nx.draw_networkx_nodes(G, pos, nodelist=business, node_color='red', node_size=300, label='Business')
        nx.draw_networkx_nodes(G, pos, nodelist=mixed, node_color='purple', node_size=300, label='Mixed')
        nx.draw_networkx_nodes(G, pos, nodelist=other_districts, node_color='gray', node_size=300, label='Other Districts')
        nx.draw_networkx_nodes(G, pos, nodelist=facilities, node_color='blue', node_size=200, label='Facilities', node_shape='s')
        
        # Draw existing edges
        existing_edges = [(u, v) for u, v, d in G.edges(data=True) if d['type'] == 'existing']
        nx.draw_networkx_edges(G, pos, edgelist=existing_edges, width=1.5)
        
        # Draw potential edges if requested
        if include_potential:
            potential_edges = [(u, v) for u, v, d in G.edges(data=True) if d['type'] == 'potential']
            nx.draw_networkx_edges(G, pos, edgelist=potential_edges, width=1.5, edge_color='red', style='dashed')
        
        # Add labels
        labels = {node: node for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=8)
        
        plt.title('Greater Cairo Transportation Network')
        plt.legend()
        plt.axis('off')
        plt.tight_layout()
        
        # Save plot to a bytes buffer and convert to base64 for HTML embedding
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close()
        
        return image_base64
    
    def get_all_nodes_json(self):
        """Return all nodes as JSON for the frontend"""
        return {
            str(node_id): {
                'id': node_id,
                'name': data['name'],
                'type': data['type'],
                'x': data['x'],
                'y': data['y'],
                'population': data.get('population', 0),
                'is_facility': data['is_facility']
            } for node_id, data in self.nodes.items()
        }
    
    def get_all_edges_json(self, include_potential=False):
        """Return all edges as JSON for the frontend"""
        edges = []
        
        # Add existing roads
        for from_id, to_id, distance, capacity, condition in self.existing_roads:
            edges.append({
                'id': f"{from_id}_{to_id}",
                'from': from_id,
                'to': to_id,
                'distance': distance,
                'capacity': capacity,
                'condition': condition,
                'type': 'existing'
            })
        
        # Add potential roads if requested
        if include_potential:
            for from_id, to_id, distance, capacity, cost in self.potential_roads:
                edges.append({
                    'id': f"{from_id}_{to_id}_potential",
                    'from': from_id,
                    'to': to_id,
                    'distance': distance,
                    'capacity': capacity,
                    'cost': cost,
                    'type': 'potential'
                })
        
        return edges
        
    def find_shortest_path(self, start_id, end_id, weight='distance'):
        """Find shortest path between two nodes based on specified weight."""
        G = self.build_networkx_graph()
        
        try:
            path = nx.shortest_path(G, source=start_id, target=end_id, weight=weight)
            distance = nx.shortest_path_length(G, source=start_id, target=end_id, weight=weight)
            
            # Get the names of locations in the path
            path_names = [self.nodes[node_id]['name'] for node_id in path]
            
            return {
                'path': path,
                'path_names': path_names,
                'distance': distance
            }
        except nx.NetworkXNoPath:
            return None
    
    def analyze_traffic_congestion(self, time_of_day='morning'):
        """Analyze traffic congestion based on time of day."""
        G = self.build_networkx_graph()
        congestion_ratios = {}
        
        for from_id, to_id, _, capacity, _ in self.existing_roads:
            road_id = f"{from_id}{to_id}"
            
            if road_id in self.traffic_data:
                current_traffic = self.traffic_data[road_id][time_of_day]
                congestion_ratio = current_traffic / capacity
                congestion_ratios[(from_id, to_id)] = congestion_ratio
                
        return congestion_ratios
    
    def suggest_public_transport_improvements(self):
        """Suggest improvements based on demand and current transport."""
        # Find high-demand routes without good public transport
        suggestions = []
        
        for demand_key, passengers in self.transport_demand.items():
            from_id, to_id = demand_key.split('_')
            
            # Check if this route has metro coverage
            has_metro = False
            for line_id, name, stations, _ in self.metro_lines:
                station_list = stations.replace('"', '').split(',')
                if from_id in station_list and to_id in station_list:
                    has_metro = True
                    break
            
            # Check if this route has bus coverage
            has_bus = False
            for route_id, stops, _, _ in self.bus_routes:
                stop_list = stops.replace('"', '').split(',')
                if from_id in stop_list and to_id in stop_list:
                    has_bus = True
                    break
            
            # If high demand but no good public transport, suggest improvement
            if passengers > 15000 and not (has_metro or has_bus):
                suggestions.append({
                    'from': self.nodes[from_id]['name'],
                    'to': self.nodes[to_id]['name'],
                    'demand': passengers,
                    'suggestion': 'New bus route' if passengers < 20000 else 'Consider metro extension'
                })
                
        return suggestions

    def compute_travel_time(self, start_id, end_id, time_of_day='morning', speed_factor=1.0):
        """Compute estimated travel time between two points based on distance and traffic."""
        G = self.build_networkx_graph()
        
        # Set travel time as edge weight based on distance and traffic
        for u, v, data in G.edges(data=True):
            distance = data['distance']
            # Base speed in km/h - adjust based on road condition
            base_speed = 50 * (data['condition'] / 10)
            
            # Check if we have traffic data for this road
            road_id = f"{u}{v}"
            if road_id in self.traffic_data:
                traffic = self.traffic_data[road_id][time_of_day]
                capacity = data['capacity']
                # Traffic factor: reduces speed when congested
                traffic_factor = max(0.2, 1 - (traffic / capacity))
            else:
                # Default traffic factor if no data
                traffic_factor = 0.8
                
            # Calculate time in minutes
            time = (distance / (base_speed * traffic_factor * speed_factor)) * 60
            G[u][v]['time'] = time
        
        # Find path with lowest travel time
        try:
            path = nx.shortest_path(G, source=start_id, target=end_id, weight='time')
            total_time = sum(G[path[i]][path[i+1]]['time'] for i in range(len(path)-1))
            
            return {
                'path': path,
                'path_names': [self.nodes[node_id]['name'] for node_id in path],
                'total_time_minutes': total_time,
                'total_distance_km': sum(G[path[i]][path[i+1]]['distance'] for i in range(len(path)-1))
            }
        except nx.NetworkXNoPath:
            return None

    def get_population_density_map(self):
        """Create a population density map of the areas."""
        density_data = {}
        
        for node_id, data in self.nodes.items():
            if not data['is_facility'] and 'population' in data:
                density_data[node_id] = {
                    'name': data['name'],
                    'population': data['population'],
                    'x': data['x'],
                    'y': data['y']
                }
        
        return density_data
    
    def get_metro_lines_json(self):
        """Return metro lines in JSON format for the frontend"""
        result = []
        for line_id, name, stations, passengers in self.metro_lines:
            station_ids = stations.replace('"', '').split(',')
            station_names = [self.nodes[station_id]['name'] for station_id in station_ids if station_id in self.nodes]
            result.append({
                'id': line_id,
                'name': name,
                'stations': station_ids,
                'station_names': station_names,
                'daily_passengers': passengers
            })
        return result
    
    def get_bus_routes_json(self):
        """Return bus routes in JSON format for the frontend"""
        result = []
        for route_id, stops, buses, passengers in self.bus_routes:
            stop_ids = stops.replace('"', '').split(',')
            stop_names = [self.nodes[stop_id]['name'] for stop_id in stop_ids if stop_id in self.nodes]
            result.append({
                'id': route_id,
                'stops': stop_ids,
                'stop_names': stop_names,
                'buses_assigned': buses,
                'daily_passengers': passengers
            })
        return result

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Create and load the graph (do this at startup)
cairo_graph = CairoTransportationGraph()

@app.route('/api/graph_data')
def graph_data():
    """Return graph data in JSON format for interactive frontend visualization"""
    include_potential = request.args.get('potential', 'false').lower() == 'true'
    
    return jsonify({
        'nodes': cairo_graph.get_all_nodes_json(),
        'edges': cairo_graph.get_all_edges_json(include_potential)
    })

@app.route('/api/graph_image')
def graph_image():
    """Return a base64 encoded image of the graph"""
    include_potential = request.args.get('potential', 'false').lower() == 'true'
    image_base64 = cairo_graph.get_graph_image_base64(include_potential)
    
    return jsonify({
        'success': True,
        'image': image_base64
    })

@app.route('/api/nodes')
def get_nodes():
    """Return all node data for dropdowns and selections"""
    return jsonify({
        'success': True,
        'nodes': cairo_graph.get_all_nodes_json()
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
        path_result = cairo_graph.find_shortest_path(start_id, end_id)
    else:  # time-based
        path_result = cairo_graph.compute_travel_time(start_id, end_id, time_of_day=time_of_day)
    
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
    congestion = cairo_graph.analyze_traffic_congestion(time_of_day=time_of_day)
    
    # Format results for the frontend
    results = []
    for (from_id, to_id), ratio in congestion.items():
        from_name = cairo_graph.nodes[from_id]['name']
        to_name = cairo_graph.nodes[to_id]['name']
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
    suggestions = cairo_graph.suggest_public_transport_improvements()
    return jsonify({
        'success': True,
        'suggestions': suggestions
    })

@app.route('/api/metro_lines')
def metro_lines():
    """Return metro line data"""
    return jsonify({
        'success': True,
        'lines': cairo_graph.get_metro_lines_json()
    })

@app.route('/api/bus_routes')
def bus_routes():
    """Return bus route data"""
    return jsonify({
        'success': True,
        'routes': cairo_graph.get_bus_routes_json()
    })

@app.route('/api/population_density')
def population_density():
    """Return population density data"""
    return jsonify({
        'success': True,
        'density': cairo_graph.get_population_density_map()
    })

@app.route('/api/statistics')
def statistics():
    """Return general network statistics"""
    G = cairo_graph.build_networkx_graph(include_potential=False)
    
    total_population = sum(data.get('population', 0) for _, data in cairo_graph.nodes.items() 
                          if not data['is_facility'] and 'population' in data)
    
    residential_areas = len([n for n in cairo_graph.nodes.values() 
                            if not n['is_facility'] and n['type'] == 'Residential'])
    
    business_areas = len([n for n in cairo_graph.nodes.values() 
                         if not n['is_facility'] and n['type'] == 'Business'])
    
    mixed_areas = len([n for n in cairo_graph.nodes.values() 
                      if not n['is_facility'] and n['type'] == 'Mixed'])
    
    facilities = len([n for n in cairo_graph.nodes.values() if n['is_facility']])
    
    roads = len(cairo_graph.existing_roads)
    potential_roads = len(cairo_graph.potential_roads)
    
    total_road_length = sum(road[2] for road in cairo_graph.existing_roads)
    
    metro_lines = len(cairo_graph.metro_lines)
    bus_routes = len(cairo_graph.bus_routes)
    
    return jsonify({
        'success': True,
        'statistics': {
            'total_population': total_population,
            'residential_areas': residential_areas,
            'business_areas': business_areas,
            'mixed_areas': mixed_areas,
            'facilities': facilities,
            'roads': roads,
            'potential_roads': potential_roads,
            'total_road_length_km': total_road_length,
            'metro_lines': metro_lines,
            'bus_routes': bus_routes,
            'connectivity': {
                'average_degree': sum(dict(G.degree()).values()) / G.number_of_nodes(),
                'density': nx.density(G),
                'connected': nx.is_connected(G),
                'components': nx.number_connected_components(G)
            }
        }
    })

if __name__ == '__main__':
    # Load data from CSV files
    cairo_graph.load_from_csv(
        neighborhoods_file="data/neighborhoods.csv", 
        facilities_file="data/facilities.csv",
        existing_roads_file="data/existing_roads.csv",
        potential_roads_file="data/potential_roads.csv",
        traffic_file="data/traffic_data.csv",
        metro_file="data/metro_lines.csv",
        bus_file="data/bus_routes.csv",
        demand_file="data/transport_demand.csv"
    )
    
    # Start the Flask server
    app.run(debug=True, port=5000)