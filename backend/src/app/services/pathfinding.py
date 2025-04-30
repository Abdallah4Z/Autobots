import networkx as nx

def find_shortest_path(graph, start_id, end_id, weight='distance'):
    """Find shortest path between two nodes based on specified weight."""
    G = graph.build_networkx_graph()
    
    try:
        path = nx.shortest_path(G, source=start_id, target=end_id, weight=weight)
        distance = nx.shortest_path_length(G, source=start_id, target=end_id, weight=weight)
        
        # Get the names of locations in the path
        path_names = [graph.nodes[node_id]['name'] for node_id in path]
        
        return {
            'path': path,
            'path_names': path_names,
            'distance': distance
        }
    except nx.NetworkXNoPath:
        return None

def compute_travel_time(graph, start_id, end_id, time_of_day='morning', speed_factor=1.0):
    """Compute estimated travel time between two points based on distance and traffic."""
    G = graph.build_networkx_graph()
    
    # Set travel time as edge weight based on distance and traffic
    for u, v, data in G.edges(data=True):
        distance = data['distance']
        # Base speed in km/h - adjust based on road condition
        base_speed = 50 * (data['condition'] / 10)
        
        # Check if we have traffic data for this road
        road_id = f"{u}{v}"
        if road_id in graph.traffic_data:
            traffic = graph.traffic_data[road_id][time_of_day]
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
            'path_names': [graph.nodes[node_id]['name'] for node_id in path],
            'total_time_minutes': total_time,
            'total_distance_km': sum(G[path[i]][path[i+1]]['distance'] for i in range(len(path)-1))
        }
    except nx.NetworkXNoPath:
        return None

def emergency_route_astar(graph, start_id, end_id, time_of_day='morning', emergency_type='ambulance'):
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
    G = graph.build_networkx_graph()
    
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
        if road_id in graph.traffic_data:
            traffic = graph.traffic_data[road_id][time_of_day]
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
        x1, y1 = graph.nodes[n1]['x'], graph.nodes[n1]['y']
        x2, y2 = graph.nodes[n2]['x'], graph.nodes[n2]['y']
        
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
            
            if road_id in graph.traffic_data:
                traffic = graph.traffic_data[road_id][time_of_day]
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
                'from_name': graph.nodes[u]['name'],
                'to_name': graph.nodes[v]['name'],
                'distance': G[u][v]['distance'],
                'time': G[u][v]['time'],
                'traffic_level': traffic_level,
                'is_critical_intersection': is_critical_intersection,
                'is_facility': graph.nodes[v]['is_facility'],
                'facility_type': graph.nodes[v]['type'] if graph.nodes[v]['is_facility'] else None
            })
        
        # Compare with normal route (dijkstra)
        normal_path = nx.shortest_path(G, source=start_id, target=end_id, weight='time')
        normal_time = sum(G[normal_path[i]][normal_path[i+1]]['time'] / 0.8 for i in range(len(normal_path)-1))
        
        time_saved = normal_time - total_time
        
        return {
            'success': True,
            'path': path,
            'path_names': [graph.nodes[node_id]['name'] for node_id in path],
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