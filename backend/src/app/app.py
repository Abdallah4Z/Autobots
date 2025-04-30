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

    def optimize_road_network_with_mst(self, prioritize_population=True, include_existing=True):
        """
        Uses Minimum Spanning Tree algorithm to design an optimal road network.
        
        Args:
            prioritize_population: If True, edge weights are adjusted based on population density
            include_existing: If True, existing roads are included with reduced weight to prioritize them
            
        Returns:
            A dictionary containing the optimized network information
        """
        # Create a complete graph with all possible connections
        G = nx.Graph()
        
        # Add all nodes
        for node_id, data in self.nodes.items():
            # Add population factor for priority weighting
            population = data.get('population', 0) if not data['is_facility'] else 5000
            is_critical = data['is_facility'] or (not data['is_facility'] and data.get('population', 0) > 50000)
            
            G.add_node(node_id, 
                      population=population,
                      name=data['name'],
                      is_facility=data['is_facility'],
                      is_critical=is_critical,
                      type=data['type'],
                      x=data['x'],
                      y=data['y'])
        
        # First, add all existing roads with reduced weight to prioritize their use
        existing_edges = {}
        if include_existing:
            for from_id, to_id, distance, capacity, condition in self.existing_roads:
                # Use distance as the base weight, but reduce it to prioritize existing roads
                weight = distance * 0.3  # Reduced weight for existing roads
                # Further reduce weight for high capacity, good condition roads
                weight = weight * (1 - (capacity/10000) * 0.3) * (1 - (condition/10) * 0.2)
                
                G.add_edge(from_id, to_id, 
                          weight=weight, 
                          distance=distance,
                          type='existing',
                          capacity=capacity,
                          condition=condition)
                
                existing_edges[(from_id, to_id)] = True
                existing_edges[(to_id, from_id)] = True
        
        # Add potential new roads
        for from_id, to_id, distance, capacity, cost in self.potential_roads:
            # Skip if edge already exists (as an existing road)
            if (from_id, to_id) in existing_edges:
                continue
                
            weight = distance
            
            # If prioritizing by population, adjust weight based on connected nodes
            if prioritize_population:
                from_pop = G.nodes[from_id]['population']
                to_pop = G.nodes[to_id]['population']
                
                # Critical facilities and high population areas get priority (lower weight)
                from_critical = G.nodes[from_id]['is_critical']
                to_critical = G.nodes[to_id]['is_critical']
                
                if from_critical and to_critical:
                    # Strong priority for connections between critical nodes
                    weight = weight * 0.5
                elif from_critical or to_critical:
                    # Medium priority for connections to at least one critical node
                    weight = weight * 0.7
                
                # Population factor: higher population means lower weight (higher priority)
                pop_factor = 1.0 / (1.0 + (from_pop + to_pop) / 100000)
                weight = weight * pop_factor
            
            # Add cost factor - expensive roads get higher weights
            weight = weight * (1.0 + cost * 0.02)
            
            G.add_edge(from_id, to_id, 
                      weight=weight, 
                      distance=distance,
                      type='potential',
                      capacity=capacity,
                      cost=cost)
        
        # Apply Kruskal's MST algorithm
        mst = nx.minimum_spanning_tree(G, weight='weight')
        
        # Calculate total cost, distance, and categorize the edges
        total_cost = 0
        total_distance = 0
        existing_roads_used = []
        new_roads_proposed = []
        
        for u, v, data in mst.edges(data=True):
            edge_type = data.get('type', 'potential')
            if edge_type == 'existing':
                existing_roads_used.append({
                    'from_id': u,
                    'to_id': v,
                    'from_name': self.nodes[u]['name'],
                    'to_name': self.nodes[v]['name'],
                    'distance': data['distance'],
                    'capacity': data['capacity'],
                    'condition': data['condition']
                })
                total_distance += data['distance']
            else:
                # This is a potential new road
                cost = data.get('cost', 0)
                new_roads_proposed.append({
                    'from_id': u,
                    'to_id': v,
                    'from_name': self.nodes[u]['name'],
                    'to_name': self.nodes[v]['name'],
                    'distance': data['distance'],
                    'capacity': data['capacity'],
                    'cost': cost
                })
                total_cost += cost
                total_distance += data['distance']
        
        # Check connectivity for all critical nodes
        critical_subgraph = nx.subgraph(mst, [n for n, data in G.nodes(data=True) if data['is_critical']])
        is_critical_connected = nx.is_connected(critical_subgraph) if critical_subgraph.number_of_nodes() > 0 else True
        
        # Calculate improvement statistics
        improvement = {
            'original_edges': G.number_of_edges(),
            'mst_edges': mst.number_of_edges(),
            'efficiency': 1.0 - (mst.number_of_edges() / G.number_of_edges()) if G.number_of_edges() > 0 else 0
        }
        
        # Create result
        result = {
            'mst': mst,
            'existing_roads_used': existing_roads_used,
            'new_roads_proposed': new_roads_proposed,
            'total_cost': total_cost,
            'total_distance': total_distance,
            'improvement': improvement,
            'is_critical_connected': is_critical_connected,
            'critical_nodes_count': critical_subgraph.number_of_nodes() if critical_subgraph.number_of_nodes() > 0 else 0
        }
        
        return result

    def emergency_route_astar(self, start_id, end_id, time_of_day='morning', emergency_type='ambulance'):
        """
        Use A* search algorithm to find optimal emergency vehicle routes.
        
        Args:
            start_id: Starting location ID
            end_id: Destination location ID
            time_of_day: Time period for traffic consideration
            emergency_type: Type of emergency vehicle ('ambulance', 'fire', 'police')
            
        Returns:
            Dictionary containing the optimal route and related information
        """
        G = self.build_networkx_graph()
        
        # Set travel time as edge weight, considering emergency vehicle advantages
        for u, v, data in G.edges(data=True):
            distance = data['distance']
            condition = data.get('condition', 7)  # Default condition if not specified
            
            # Base speed in km/h - emergency vehicles can go faster
            # Different emergency types might have different speed capabilities
            if emergency_type == 'ambulance':
                base_speed = 60 * (condition / 10)
                priority_factor = 0.8  # Ambulances get highest priority
            elif emergency_type == 'fire':
                base_speed = 55 * (condition / 10)
                priority_factor = 0.85  # Fire trucks slightly slower due to size
            else:  # police
                base_speed = 70 * (condition / 10)
                priority_factor = 0.9  # Police cars can go fastest
            
            # Check if we have traffic data for this road
            road_id = f"{u}{v}"
            if road_id in self.traffic_data:
                traffic = self.traffic_data[road_id][time_of_day]
                capacity = data['capacity']
                # Traffic impact is reduced for emergency vehicles
                traffic_factor = max(0.4, 1 - (traffic / capacity) * 0.6)
            else:
                # Default traffic factor if no data
                traffic_factor = 0.9
                
            # Calculate time in minutes - emergency vehicles get priority lanes and signals
            time = (distance / (base_speed * traffic_factor)) * 60 * priority_factor
            G[u][v]['time'] = time
        
        # Define heuristic function for A* (straight-line distance)
        def heuristic(n1, n2):
            # Use coordinates to calculate straight-line distance
            x1, y1 = self.nodes[n1]['x'], self.nodes[n1]['y']
            x2, y2 = self.nodes[n2]['x'], self.nodes[n2]['y']
            
            # Simple Euclidean distance - scaled to be in minutes at emergency speed
            # Assumes 90 km/h average straight-line emergency speed
            distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            return (distance / 90) * 60  # Convert to minutes
        
        try:
            # Use NetworkX's A* search algorithm with our custom heuristic
            path = nx.astar_path(G, source=start_id, target=end_id, 
                                 heuristic=lambda n1, n2: heuristic(n1, n2),
                                 weight='time')
            
            # Calculate total time and distance
            total_time = sum(G[path[i]][path[i+1]]['time'] for i in range(len(path)-1))
            total_distance = sum(G[path[i]][path[i+1]]['distance'] for i in range(len(path)-1))
            
            # Get path details including critical intersections
            path_details = []
            for i in range(len(path)-1):
                u, v = path[i], path[i+1]
                road_id = f"{u}{v}"
                traffic_level = "Unknown"
                
                if road_id in self.traffic_data:
                    traffic = self.traffic_data[road_id][time_of_day]
                    capacity = G[u][v]['capacity']
                    congestion = traffic / capacity
                    if congestion > 0.8:
                        traffic_level = "High"
                    elif congestion > 0.5:
                        traffic_level = "Medium"
                    else:
                        traffic_level = "Low"
                
                # Identify if this is a critical intersection (multiple connections)
                is_critical_intersection = G.degree[v] > 2
                
                path_details.append({
                    'from_id': u,
                    'to_id': v,
                    'from_name': self.nodes[u]['name'],
                    'to_name': self.nodes[v]['name'],
                    'distance': G[u][v]['distance'],
                    'time': G[u][v]['time'],
                    'traffic_level': traffic_level,
                    'is_critical_intersection': is_critical_intersection,
                    'is_facility': self.nodes[v]['is_facility'],
                    'facility_type': self.nodes[v]['type'] if self.nodes[v]['is_facility'] else None
                })
            
            # Compare with normal route (dijkstra)
            normal_path = nx.shortest_path(G, source=start_id, target=end_id, weight='time')
            normal_time = sum(G[normal_path[i]][normal_path[i+1]]['time'] / 0.8 for i in range(len(normal_path)-1))
            
            time_saved = normal_time - total_time
            
            return {
                'success': True,
                'path': path,
                'path_names': [self.nodes[node_id]['name'] for node_id in path],
                'path_details': path_details,
                'total_time_minutes': total_time,
                'total_distance_km': total_distance,
                'emergency_type': emergency_type,
                'time_of_day': time_of_day,
                'time_saved_vs_normal': time_saved,
                'percent_improvement': (time_saved / normal_time) * 100 if normal_time > 0 else 0
            }
        except nx.NetworkXNoPath:
            return {
                'success': False,
                'message': f"No path found between {start_id} and {end_id}"
            }

    def optimize_bus_routes_dp(self, target_coverage=0.85, max_buses=100):
        """
        Use dynamic programming to optimize bus routes for coverage and efficiency.
        
        Args:
            target_coverage: Target percentage of demand to be covered
            max_buses: Maximum number of buses available for assignment
            
        Returns:
            Optimized bus routes with bus allocation
        """
        # Create a list of all high-demand routes
        demand_routes = []
        for demand_key, passengers in self.transport_demand.items():
            if passengers > 5000:  # Only consider routes with significant demand
                from_id, to_id = demand_key.split('_')
                
                # Check if route is already covered by metro
                has_metro = False
                for _, _, stations, _ in self.metro_lines:
                    station_list = stations.replace('"', '').split(',')
                    if from_id in station_list and to_id in station_list:
                        has_metro = True
                        break
                
                # If not covered by metro, add to potential bus routes
                if not has_metro:
                    demand_routes.append({
                        'from_id': from_id,
                        'to_id': to_id,
                        'from_name': self.nodes[from_id]['name'],
                        'to_name': self.nodes[to_id]['name'],
                        'demand': passengers
                    })
        
        # Sort routes by demand (descending)
        demand_routes.sort(key=lambda x: x['demand'], reverse=True)
        
        # Calculate shortest paths for each route
        G = self.build_networkx_graph()
        for route in demand_routes:
            try:
                path = nx.shortest_path(G, source=route['from_id'], target=route['to_id'], weight='distance')
                distance = sum(G[path[i]][path[i+1]]['distance'] for i in range(len(path)-1))
                
                # Estimate travel time (avg 30km/h in city)
                route['distance'] = distance
                route['travel_time'] = (distance / 30) * 60  # minutes
                route['path'] = path
                
                # Estimate bus requirements: assume 1 bus per 30 mins per 1000 passengers
                route['buses_needed'] = max(1, int((route['demand'] / 1000) * (route['travel_time'] / 30)))
            except nx.NetworkXNoPath:
                # Skip routes with no viable path
                route['skip'] = True
        
        # Remove routes with no path
        demand_routes = [route for route in demand_routes if not route.get('skip', False)]
        
        # Calculate total demand and buses needed
        total_demand = sum(route['demand'] for route in demand_routes)
        total_buses_needed = sum(route['buses_needed'] for route in demand_routes)
        
        # If we have enough buses for all routes, no optimization needed
        if total_buses_needed <= max_buses:
            optimized_routes = demand_routes
        else:
            # Dynamic programming approach for knapsack problem:
            # Maximize demand coverage with limited buses
            
            # Create weights (buses needed) and values (demand covered)
            weights = [route['buses_needed'] for route in demand_routes]
            values = [route['demand'] for route in demand_routes]
            
            # Initialize DP table
            dp = [[0 for _ in range(max_buses + 1)] for _ in range(len(demand_routes) + 1)]
            
            # Fill the DP table
            for i in range(1, len(demand_routes) + 1):
                for w in range(max_buses + 1):
                    if weights[i-1] <= w:
                        dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], dp[i-1][w])
                    else:
                        dp[i][w] = dp[i-1][w]
            
            # Backtrack to find selected routes
            selected_routes = []
            w = max_buses
            for i in range(len(demand_routes), 0, -1):
                if dp[i][w] != dp[i-1][w]:
                    selected_routes.append(demand_routes[i-1])
                    w -= weights[i-1]
            
            optimized_routes = selected_routes
        
        # Format the results
        result = []
        route_id_counter = len(self.bus_routes) + 1
        
        for route in optimized_routes:
            # Create stops list from path
            stops = route['path']
            stop_names = [self.nodes[node_id]['name'] for node_id in stops]
            
            # Calculate buses to assign (either what's needed or proportionally reduced)
            buses_assigned = min(route['buses_needed'], max(1, int(route['buses_needed'] * (max_buses / total_buses_needed))))
            
            result.append({
                'route_id': f"BR{route_id_counter}",
                'from': route['from_name'],
                'to': route['to_name'],
                'stops': stops,
                'stop_names': stop_names,
                'distance_km': route['distance'],
                'travel_time_mins': route['travel_time'],
                'demand': route['demand'],
                'buses_assigned': buses_assigned,
                'frequency_mins': max(5, min(60, int((buses_assigned * 60) / route['travel_time'])))
            })
            route_id_counter += 1
        
        # Calculate coverage statistics
        covered_demand = sum(route['demand'] for route in optimized_routes)
        coverage_percentage = (covered_demand / total_demand) * 100 if total_demand > 0 else 0
        buses_used = sum(route['buses_assigned'] for route in result)
        
        return {
            'optimized_routes': result,
            'total_routes': len(result),
            'total_demand': total_demand,
            'covered_demand': covered_demand,
            'coverage_percentage': coverage_percentage,
            'buses_used': buses_used,
            'max_buses': max_buses
        }
    
    def optimize_metro_schedule_dp(self, peak_hours=['morning', 'evening'], off_peak_hours=['afternoon', 'night']):
        """
        Use dynamic programming to optimize metro schedules based on demand patterns.
        
        Args:
            peak_hours: List of peak time periods
            off_peak_hours: List of off-peak time periods
            
        Returns:
            Optimized metro schedules
        """
        results = []
        
        for line_id, name, stations, daily_passengers in self.metro_lines:
            station_ids = stations.replace('"', '').split(',')
            
            if len(station_ids) < 2:
                continue  # Skip invalid lines
            
            # Calculate line length
            G = self.build_networkx_graph()
            total_distance = 0
            line_path = []
            
            for i in range(len(station_ids) - 1):
                try:
                    path = nx.shortest_path(G, source=station_ids[i], target=station_ids[i+1], weight='distance')
                    distance = sum(G[path[j]][path[j+1]]['distance'] for j in range(len(path)-1))
                    total_distance += distance
                    line_path.extend(path if i == 0 else path[1:])  # Avoid duplicates
                except nx.NetworkXNoPath:
                    # If no direct path, use a default distance estimate
                    try:
                        # Estimate using coordinates
                        x1, y1 = self.nodes[station_ids[i]]['x'], self.nodes[station_ids[i]]['y']
                        x2, y2 = self.nodes[station_ids[i+1]]['x'], self.nodes[station_ids[i+1]]['y']
                        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                        total_distance += distance
                    except:
                        # Default to 5km between stations if all else fails
                        total_distance += 5
            
            # Estimate average travel time (metro avg speed ~40km/h)
            travel_time_mins = (total_distance / 40) * 60
            
            # Distribute daily passengers across time periods
            # Assume: 35% morning, 15% afternoon, 40% evening, 10% night
            time_distribution = {
                'morning': 0.35,
                'afternoon': 0.15,
                'evening': 0.40,
                'night': 0.10
            }
            
            # Analyze traffic along the route to adjust demand
            congestion_factors = {}
            for time_period in list(peak_hours) + list(off_peak_hours):
                congestion = 0
                edge_count = 0
                
                for i in range(len(line_path) - 1):
                    road_id = f"{line_path[i]}{line_path[i+1]}"
                    if road_id in self.traffic_data:
                        congestion += self.traffic_data[road_id][time_period]
                        edge_count += 1
                
                avg_congestion = congestion / edge_count if edge_count > 0 else 0
                congestion_factors[time_period] = 1 + (avg_congestion / 5000)  # Higher traffic increases demand for metro
            
            # Dynamic Programming for optimal train frequency scheduling
            # We want to maximize passenger service while minimizing operational costs
            # States: time periods
            # Actions: number of trains per hour (1 to 15)
            # Rewards: passengers served minus operational costs
            
            # Constants for reward calculation
            train_capacity = 1000  # passengers per train
            operational_cost_per_train = 5000  # cost per train per hour
            
            # Calculate optimal train frequencies for each time period
            schedule = {}
            
            for time_period in list(peak_hours) + list(off_peak_hours):
                # Period-specific passenger demand (adjusted by congestion)
                period_demand = daily_passengers * time_distribution[time_period] * congestion_factors[time_period]
                
                # Dynamic programming table: [trains_per_hour] = net_benefit
                dp = [0] * 16  # 0 to 15 trains per hour
                
                for trains in range(1, 16):
                    # Hourly capacity with this many trains
                    capacity = trains * train_capacity
                    
                    # Passengers served (capped at demand)
                    passengers_served = min(period_demand, capacity)
                    
                    # Revenue (assume 5 EGP per passenger)
                    revenue = passengers_served * 5
                    
                    # Cost
                    cost = trains * operational_cost_per_train
                    
                    # Net benefit
                    net_benefit = revenue - cost
                    
                    dp[trains] = net_benefit
                
                # Find optimal number of trains (maximum net benefit)
                optimal_trains = max(range(1, 16), key=lambda x: dp[x])
                
                # Calculate intervals between trains in minutes
                interval_mins = int(60 / optimal_trains)
                
                # Store the schedule
                schedule[time_period] = {
                    'trains_per_hour': optimal_trains,
                    'interval_mins': interval_mins,
                    'capacity_per_hour': optimal_trains * train_capacity,
                    'demand': period_demand,
                    'net_benefit': dp[optimal_trains]
                }
            
            # Store the results
            results.append({
                'line_id': line_id,
                'name': name,
                'stations': station_ids,
                'station_names': [self.nodes[station_id]['name'] for station_id in station_ids if station_id in self.nodes],
                'total_distance_km': total_distance,
                'travel_time_mins': travel_time_mins,
                'daily_passengers': daily_passengers,
                'schedule': schedule
            })
                
        return results

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

@app.route('/api/optimize_road_network', methods=['GET'])
def optimize_road_network():
    """API endpoint for MST-based road network optimization"""
    prioritize_population = request.args.get('prioritize_population', 'true').lower() == 'true'
    include_existing = request.args.get('include_existing', 'true').lower() == 'true'
    
    optimization_result = cairo_graph.optimize_road_network_with_mst(
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
    
    result = cairo_graph.emergency_route_astar(
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
    
    result = cairo_graph.optimize_bus_routes_dp(
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
    
    result = cairo_graph.optimize_metro_schedule_dp(
        peak_hours=peak_hours,
        off_peak_hours=off_peak_hours
    )
    
    return jsonify({
        'success': True,
        'optimized_schedules': result
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