import networkx as nx

def optimize_road_network_with_mst(graph, prioritize_population=True, include_existing=True):
    """
    Uses Minimum Spanning Tree algorithm to design an optimal road network.
    
    Args:
        graph: The transportation graph object
        prioritize_population: If True, edge weights are adjusted based on population density
        include_existing: If True, existing roads are included with reduced weight to prioritize them
            
    Returns:
        A dictionary containing the optimized network information
    """
    # Create a complete graph with all possible connections
    G = nx.Graph()
    
    # Add all nodes
    for node_id, data in graph.nodes.items():
        # Add population factor for priority weighting - set default if missing
        population = data.get('population', 0) 
        if not isinstance(population, (int, float)):
            population = 0
            
        # For facilities, assume they serve significant population
        if data['is_facility']:
            population = 5000
            
        is_critical = data['is_facility'] or (not data['is_facility'] and population > 50000)
        
        G.add_node(node_id, 
                  population=population,
                  name=data['name'],
                  is_facility=data['is_facility'],
                  is_critical=is_critical,
                  type=data.get('type', 'Unknown'),
                  x=data.get('x', 0),
                  y=data.get('y', 0))
    
    # First, add all existing roads with reduced weight to prioritize their use
    existing_edges = {}
    if include_existing:
        for from_id, to_id, distance, capacity, condition in graph.existing_roads:
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
    for from_id, to_id, distance, capacity, cost in graph.potential_roads:
        # Skip if edge already exists (as an existing road)
        if (from_id, to_id) in existing_edges:
            continue
            
        weight = distance
        
        # If prioritizing by population, adjust weight based on connected nodes
        if prioritize_population:
            # Handle case where node might not exist in G
            if from_id in G.nodes and to_id in G.nodes:
                # Set default population values to avoid KeyError
                from_pop = G.nodes[from_id].get('population', 0)
                to_pop = G.nodes[to_id].get('population', 0)
                
                # Critical facilities and high population areas get priority (lower weight)
                from_critical = G.nodes[from_id].get('is_critical', False)
                to_critical = G.nodes[to_id].get('is_critical', False)
                
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
        
        # Only add the edge if both nodes exist in the graph
        if from_id in G.nodes and to_id in G.nodes:
            G.add_edge(from_id, to_id, 
                      weight=weight, 
                      distance=distance,
                      type='potential',
                      capacity=capacity,
                      cost=cost)
    
    # Apply Kruskal's MST algorithm if graph is not empty
    if G.number_of_edges() > 0:
        try:
            mst = nx.minimum_spanning_tree(G, weight='weight')
        except Exception as e:
            print(f"Error computing MST: {e}")
            # Return empty result as fallback
            return {
                'existing_roads_used': [],
                'new_roads_proposed': [],
                'total_cost': 0,
                'total_distance': 0,
                'improvement': {'original_edges': G.number_of_edges(), 'mst_edges': 0, 'efficiency': 0},
                'is_critical_connected': False,
                'critical_nodes_count': 0
            }
    else:
        # Empty graph case
        return {
            'existing_roads_used': [],
            'new_roads_proposed': [],
            'total_cost': 0,
            'total_distance': 0,
            'improvement': {'original_edges': 0, 'mst_edges': 0, 'efficiency': 0},
            'is_critical_connected': False,
            'critical_nodes_count': 0
        }
    
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
                'from_name': graph.nodes.get(u, {}).get('name', f'Node {u}'),
                'to_name': graph.nodes.get(v, {}).get('name', f'Node {v}'),
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
                'from_name': graph.nodes.get(u, {}).get('name', f'Node {u}'),
                'to_name': graph.nodes.get(v, {}).get('name', f'Node {v}'),
                'distance': data['distance'],
                'capacity': data['capacity'],
                'cost': cost
            })
            total_cost += cost
            total_distance += data['distance']
    
    # Check connectivity for all critical nodes
    critical_nodes = [n for n, data in G.nodes(data=True) if data.get('is_critical', False)]
    if critical_nodes:
        try:
            critical_subgraph = nx.subgraph(mst, critical_nodes)
            is_critical_connected = nx.is_connected(critical_subgraph) if critical_subgraph.number_of_nodes() > 0 else True
            critical_nodes_count = critical_subgraph.number_of_nodes()
        except Exception as e:
            print(f"Error checking critical connectivity: {e}")
            is_critical_connected = False
            critical_nodes_count = 0
    else:
        is_critical_connected = True
        critical_nodes_count = 0
    
    # Calculate improvement statistics
    improvement = {
        'original_edges': G.number_of_edges(),
        'mst_edges': mst.number_of_edges(),
        'efficiency': 1.0 - (mst.number_of_edges() / G.number_of_edges()) if G.number_of_edges() > 0 else 0
    }
    
    # Create result
    result = {
        'existing_roads_used': existing_roads_used,
        'new_roads_proposed': new_roads_proposed,
        'total_cost': total_cost,
        'total_distance': total_distance,
        'improvement': improvement,
        'is_critical_connected': is_critical_connected,
        'critical_nodes_count': critical_nodes_count
    }
    
    return result

def optimize_bus_routes_dp(graph, target_coverage=0.85, max_buses=100):
    """
    Use dynamic programming to optimize bus routes for coverage and efficiency.
    
    Args:
        graph: The transportation graph object
        target_coverage: Target percentage of demand to be covered
        max_buses: Maximum number of buses available for assignment
        
    Returns:
        Optimized bus routes with bus allocation
    """
    # Create a list of all high-demand routes
    demand_routes = []
    for demand_key, passengers in graph.transport_demand.items():
        if passengers > 5000:  # Only consider routes with significant demand
            try:
                # Handle both string keys with underscores and tuple keys
                if isinstance(demand_key, tuple):
                    from_id, to_id = demand_key
                else:
                    from_id, to_id = demand_key.split('_')
                
                # Verify that both nodes exist in the graph
                if from_id not in graph.nodes or to_id not in graph.nodes:
                    continue
                
                # Check if route is already covered by metro
                has_metro = False
                for _, _, stations, _ in graph.metro_lines:
                    station_list = stations.replace('"', '').split(',')
                    if from_id in station_list and to_id in station_list:
                        has_metro = True
                        break
                
                # If not covered by metro, add to potential bus routes
                if not has_metro:
                    demand_routes.append({
                        'from_id': from_id,
                        'to_id': to_id,
                        'from_name': graph.nodes[from_id]['name'],
                        'to_name': graph.nodes[to_id]['name'],
                        'demand': passengers
                    })
            except (ValueError, KeyError) as e:
                # Skip invalid demand entries
                print(f"Skipping invalid demand entry {demand_key}: {e}")
                continue
    
    # Sort routes by demand (descending)
    demand_routes.sort(key=lambda x: x['demand'], reverse=True)
    
    # Calculate shortest paths for each route
    G = graph.build_networkx_graph()
    valid_routes = []
    
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
            valid_routes.append(route)
        except (nx.NetworkXNoPath, KeyError) as e:
            # Skip routes with no viable path or missing nodes
            print(f"Skipping route {route['from_id']} to {route['to_id']}: {e}")
    
    # If no valid routes, return empty result
    if not valid_routes:
        return {
            'optimized_routes': [],
            'total_routes': 0,
            'total_demand': 0,
            'covered_demand': 0,
            'coverage_percentage': 0,
            'buses_used': 0,
            'max_buses': max_buses
        }
    
    # Calculate total demand and buses needed
    total_demand = sum(route['demand'] for route in valid_routes)
    total_buses_needed = sum(route['buses_needed'] for route in valid_routes)
    
    # If we have enough buses for all routes, no optimization needed
    if total_buses_needed <= max_buses:
        optimized_routes = valid_routes
    else:
        # Dynamic programming approach for knapsack problem:
        # Maximize demand coverage with limited buses
        
        # Create weights (buses needed) and values (demand covered)
        weights = [route['buses_needed'] for route in valid_routes]
        values = [route['demand'] for route in valid_routes]
        
        # Initialize DP table
        dp = [[0 for _ in range(max_buses + 1)] for _ in range(len(valid_routes) + 1)]
        
        # Fill the DP table
        for i in range(1, len(valid_routes) + 1):
            for w in range(max_buses + 1):
                if weights[i-1] <= w:
                    dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], dp[i-1][w])
                else:
                    dp[i][w] = dp[i-1][w]
        
        # Backtrack to find selected routes
        selected_routes = []
        w = max_buses
        for i in range(len(valid_routes), 0, -1):
            if dp[i][w] != dp[i-1][w]:
                selected_routes.append(valid_routes[i-1])
                w -= weights[i-1]
        
        optimized_routes = selected_routes
    
    # Format the results
    result = []
    route_id_counter = len(graph.bus_routes) + 1
    
    for route in optimized_routes:
        try:
            # Create stops list from path
            stops = route['path']
            stop_names = [graph.nodes[node_id]['name'] for node_id in stops if node_id in graph.nodes]
            
            # Skip routes with missing nodes
            if len(stop_names) != len(stops):
                continue
            
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
        except KeyError as e:
            print(f"Skipping route during result formatting: {e}")
    
    # Calculate coverage statistics
    covered_demand = sum(route['demand'] for route in optimized_routes)
    coverage_percentage = (covered_demand / total_demand) * 100 if total_demand > 0 else 0
    buses_used = sum(result[i]['buses_assigned'] for i in range(len(result)))
    
    return {
        'optimized_routes': result,
        'total_routes': len(result),
        'total_demand': total_demand,
        'covered_demand': covered_demand,
        'coverage_percentage': coverage_percentage,
        'buses_used': buses_used,
        'max_buses': max_buses
    }

def optimize_metro_schedule_dp(graph, peak_hours=['morning', 'evening'], off_peak_hours=['afternoon', 'night']):
    """
    Use dynamic programming to optimize metro schedules based on demand patterns.
    
    Args:
        graph: The transportation graph object
        peak_hours: List of peak time periods
        off_peak_hours: List of off-peak time periods
        
    Returns:
        Optimized metro schedules
    """
    results = []
    
    for line_id, name, stations, daily_passengers in graph.metro_lines:
        station_ids = stations.replace('"', '').split(',')
        
        if len(station_ids) < 2:
            continue  # Skip invalid lines
        
        # Calculate line length
        G = graph.build_networkx_graph()
        total_distance = 0
        line_path = []
        
        for i in range(len(station_ids) - 1):
            try:
                # Check if both station IDs exist in the graph before attempting to find paths
                if station_ids[i] not in G.nodes or station_ids[i+1] not in G.nodes:
                    # Use a default distance if nodes don't exist
                    print(f"Warning: Metro station ID not found in graph: {station_ids[i]} or {station_ids[i+1]}")
                    total_distance += 5  # Default 5km between stations
                    continue
                    
                path = nx.shortest_path(G, source=station_ids[i], target=station_ids[i+1], weight='distance')
                distance = sum(G[path[j]][path[j+1]]['distance'] for j in range(len(path)-1))
                total_distance += distance
                line_path.extend(path if i == 0 else path[1:])  # Avoid duplicates
            except nx.NetworkXNoPath:
                # If no direct path, use a default distance estimate
                try:
                    # Estimate using coordinates
                    x1, y1 = graph.nodes[station_ids[i]]['x'], graph.nodes[station_ids[i]]['y']
                    x2, y2 = graph.nodes[station_ids[i+1]]['x'], graph.nodes[station_ids[i+1]]['y']
                    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                    total_distance += distance
                except:
                    # Default to 5km between stations if all else fails
                    total_distance += 5
            except Exception as e:
                print(f"Error processing metro line segment: {e}")
                # Default to 5km between stations if an error occurs
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
                # Create road_id as string tuple to match traffic data format
                road_id = (str(line_path[i]), str(line_path[i+1]))
                
                if road_id in graph.traffic_data:
                    congestion += graph.traffic_data[road_id][time_period]
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
            'station_names': [graph.nodes[station_id]['name'] for station_id in station_ids if station_id in graph.nodes],
            'total_distance_km': total_distance,
            'travel_time_mins': travel_time_mins,
            'daily_passengers': daily_passengers,
            'schedule': schedule
        })
            
    return results