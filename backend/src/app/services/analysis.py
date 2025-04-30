import networkx as nx

def analyze_traffic_congestion(graph, time_of_day='morning'):
    """Analyze traffic congestion based on time of day."""
    G = graph.build_networkx_graph()
    congestion_ratios = {}
    
    for from_id, to_id, _, capacity, _ in graph.existing_roads:
        road_id = f"{from_id}{to_id}"
        
        if road_id in graph.traffic_data:
            current_traffic = graph.traffic_data[road_id][time_of_day]
            congestion_ratio = current_traffic / capacity
            congestion_ratios[(from_id, to_id)] = congestion_ratio
            
    return congestion_ratios

def suggest_public_transport_improvements(graph):
    """Suggest improvements based on demand and current transport."""
    # Find high-demand routes without good public transport
    suggestions = []
    
    for demand_key, passengers in graph.transport_demand.items():
        from_id, to_id = demand_key.split('_')
        
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
            
    return suggestions

def get_network_statistics(graph):
    """Return general network statistics"""
    G = graph.build_networkx_graph(include_potential=False)
    
    total_population = sum(data.get('population', 0) for _, data in graph.nodes.items() 
                          if not data['is_facility'] and 'population' in data)
    
    residential_areas = len([n for n in graph.nodes.values() 
                            if not n['is_facility'] and n['type'] == 'Residential'])
    
    business_areas = len([n for n in graph.nodes.values() 
                         if not n['is_facility'] and n['type'] == 'Business'])
    
    mixed_areas = len([n for n in graph.nodes.values() 
                      if not n['is_facility'] and n['type'] == 'Mixed'])
    
    facilities = len([n for n in graph.nodes.values() if n['is_facility']])
    
    roads = len(graph.existing_roads)
    potential_roads = len(graph.potential_roads)
    
    total_road_length = sum(road[2] for road in graph.existing_roads)
    
    metro_lines = len(graph.metro_lines)
    bus_routes = len(graph.bus_routes)
    
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
        'connectivity': {
            'average_degree': sum(dict(G.degree()).values()) / G.number_of_nodes(),
            'density': nx.density(G),
            'connected': nx.is_connected(G),
            'components': nx.number_connected_components(G)
        }
    }