def get_all_nodes_json(graph):
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
        } for node_id, data in graph.nodes.items()
    }

def get_all_edges_json(graph, include_potential=False):
    """Return all edges as JSON for the frontend"""
    edges = []
    
    # Add existing roads
    for from_id, to_id, distance, capacity, condition in graph.existing_roads:
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
        for from_id, to_id, distance, capacity, cost in graph.potential_roads:
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

def get_metro_lines_json(graph):
    """Return metro lines in JSON format for the frontend"""
    result = []
    for line_id, name, stations, passengers in graph.metro_lines:
        station_ids = stations.replace('"', '').split(',')
        station_names = [graph.nodes[station_id]['name'] for station_id in station_ids if station_id in graph.nodes]
        result.append({
            'id': line_id,
            'name': name,
            'stations': station_ids,
            'station_names': station_names,
            'daily_passengers': passengers
        })
    return result

def get_bus_routes_json(graph):
    """Return bus routes in JSON format for the frontend"""
    result = []
    for route_id, stops, buses, passengers in graph.bus_routes:
        stop_ids = stops.replace('"', '').split(',')
        stop_names = [graph.nodes[stop_id]['name'] for stop_id in stop_ids if stop_id in graph.nodes]
        result.append({
            'id': route_id,
            'stops': stop_ids,
            'stop_names': stop_names,
            'buses_assigned': buses,
            'daily_passengers': passengers
        })
    return result

def get_population_density_map(graph):
    """Create a population density map of the areas."""
    density_data = {}
    
    for node_id, data in graph.nodes.items():
        if not data['is_facility'] and 'population' in data:
            density_data[node_id] = {
                'name': data['name'],
                'population': data['population'],
                'x': data['x'],
                'y': data['y']
            }
    
    return density_data