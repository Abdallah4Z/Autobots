import networkx as nx

def analyze_traffic_congestion(graph, time_of_day='morning'):
    """Analyze traffic patterns and congestion based on time of day."""
    G = graph.build_networkx_graph()
    congestion_ratios = {}
    
    # Debug info
    roads_analyzed = 0
    roads_with_traffic_data = 0
    
    for from_id, to_id, distance, capacity, condition in graph.existing_roads:
        # Create road_id tuples in both string and original format to handle possible variations
        road_id_str = (str(from_id), str(to_id))
        road_id_orig = (from_id, to_id)
        road_id_formatted = f'("{str(from_id)}","{str(to_id)}")'  # Format as seen in CSV
        
        try:
            # Try different formats of road_id to match traffic data
            traffic_volume = None
            
            if road_id_str in graph.traffic_data:
                traffic_volume = graph.traffic_data[road_id_str][time_of_day]
                roads_with_traffic_data += 1
            elif road_id_orig in graph.traffic_data:
                traffic_volume = graph.traffic_data[road_id_orig][time_of_day]
                roads_with_traffic_data += 1
            elif road_id_formatted in graph.traffic_data:
                traffic_volume = graph.traffic_data[road_id_formatted][time_of_day]
                roads_with_traffic_data += 1
            
            if traffic_volume is not None:
                congestion_ratio = traffic_volume / capacity
                
                # Ensure node IDs exist in the graph before accessing
                if from_id in graph.nodes and to_id in graph.nodes:
                    congestion_ratios[(from_id, to_id)] = {
                        'from_id': from_id,
                        'to_id': to_id,
                        'from_name': graph.nodes[from_id]['name'],
                        'to_name': graph.nodes[to_id]['name'],
                        'congestion_ratio': congestion_ratio,
                        'traffic_volume': traffic_volume,
                        'capacity': capacity,
                        'distance': distance,
                        'status': 'Heavy' if congestion_ratio > 0.8 else 'Moderate' if congestion_ratio > 0.5 else 'Light'
                    }
            
            roads_analyzed += 1
        except Exception as e:
            print(f"Error analyzing traffic for road {from_id} to {to_id}: {e}")
    
    print(f"Traffic analysis: {roads_with_traffic_data} roads had traffic data out of {roads_analyzed} total roads analyzed")
    return congestion_ratios

def suggest_public_transport_improvements(graph):
    """Suggest improvements based on demand and current transport."""
    # Find high-demand routes without good public transport
    suggestions = []
    
    for demand_key, passengers in graph.transport_demand.items():
        try:
            # Handle both string keys with underscores and tuple keys
            if isinstance(demand_key, tuple):
                from_id, to_id = demand_key
            else:
                from_id, to_id = demand_key.split('_')
            
            # Check if both nodes exist in the graph
            if from_id not in graph.nodes or to_id not in graph.nodes:
                continue
            
            # Check if this route has metro coverage
            has_metro = False
            for line_id, name, stations, _ in graph.metro_lines:
                station_list = stations.replace('"', '').split(',')
                if from_id in station_list and to_id in station_list:
                    has_metro = True
                    break
            
            # Check if this route has bus coverage
            has_bus = False
            for route_id, stops, _, _ in graph.bus_routes:
                stop_list = stops.replace('"', '').split(',')
                if from_id in stop_list and to_id in stop_list:
                    has_bus = True
                    break
            
            # If high demand but no good public transport, suggest improvement
            if passengers > 15000 and not (has_metro or has_bus):
                suggestions.append({
                    'from': graph.nodes[from_id]['name'],
                    'to': graph.nodes[to_id]['name'],
                    'demand': passengers,
                    'suggestion': 'New bus route' if passengers < 20000 else 'Consider metro extension'
                })
        except (ValueError, KeyError) as e:
            # Skip invalid entries
            print(f"Skipping invalid demand entry {demand_key}: {e}")
            continue
            
    return suggestions

def get_network_statistics(graph):
    """Return general network statistics"""
    G = graph.build_networkx_graph(include_potential=False)
    
    total_population = sum(data.get('population', 0) for _, data in graph.nodes.items() 
                          if not data.get('is_facility', False) and 'population' in data)
    
    residential_areas = len([n for n in graph.nodes.values() 
                            if not n.get('is_facility', False) and n.get('type') == 'Residential'])
    
    business_areas = len([n for n in graph.nodes.values() 
                         if not n.get('is_facility', False) and n.get('type') == 'Business'])
    
    mixed_areas = len([n for n in graph.nodes.values() 
                      if not n.get('is_facility', False) and n.get('type') == 'Mixed'])
    
    facilities = len([n for n in graph.nodes.values() if n.get('is_facility', False)])
    
    roads = len(graph.existing_roads)
    potential_roads = len(graph.potential_roads)
    
    total_road_length = sum(road[2] for road in graph.existing_roads)
    
    metro_lines = len(graph.metro_lines)
    bus_routes = len(graph.bus_routes)
    
    # Handle potential NetworkX errors if graph is empty or disconnected
    connectivity_metrics = {
        'average_degree': 0,
        'density': 0,
        'connected': False,
        'components': 0
    }
    
    if G.number_of_nodes() > 0:
        try:
            connectivity_metrics = {
                'average_degree': sum(dict(G.degree()).values()) / G.number_of_nodes() if G.number_of_nodes() > 0 else 0,
                'density': nx.density(G),
                'connected': nx.is_connected(G),
                'components': nx.number_connected_components(G)
            }
        except Exception as e:
            print(f"Error calculating connectivity metrics: {e}")
    
    return {
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
        'connectivity': connectivity_metrics
    }