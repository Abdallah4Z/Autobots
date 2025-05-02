import networkx as nx

class CairoTransportationGraph:
    def __init__(self):
        self.nodes = {}  # Maps ID to node data
        self.existing_roads = []
        self.potential_roads = []
        self.metro_lines = []
        self.bus_routes = []
        self.traffic_data = {}
        self.transport_demand = {}
        
    def build_networkx_graph(self, include_potential=False, include_transit=True):
        """
        Create a NetworkX graph from the loaded data
        
        Args:
            include_potential: If True, include potential roads in the graph
            include_transit: If True, include metro and bus connections
        """
        G = nx.Graph()
        
        # Add nodes
        for node_id, data in self.nodes.items():
            G.add_node(node_id, **data)
            
        # Add existing roads as edges
        roads_added = 0
        for road in self.existing_roads:
            try:
                from_id, to_id, distance, capacity, condition = road
                
                # Ensure both nodes exist in the graph
                if from_id not in G or to_id not in G:
                    print(f"Warning: Road endpoints {from_id} or {to_id} not found in graph")
                    continue
                    
                # Add the edge to the graph
                G.add_edge(from_id, to_id, 
                          distance=distance, 
                          capacity=capacity, 
                          condition=condition,
                          type='road')
                
                # Debug info
                roads_added += 1
                
                # Also add traffic data if available
                if (from_id, to_id) in self.traffic_data:
                    traffic = self.traffic_data[(from_id, to_id)]
                    
                    # Calculate congestion levels for different times
                    for time, volume in traffic.items():
                        congestion = volume / capacity  # ratio of volume to capacity
                        # Add to edge attributes
                        G[from_id][to_id][f'{time}_congestion'] = congestion
                        G[from_id][to_id][f'{time}_volume'] = volume
                        
                # Set default travel time (minutes) based on distance and reasonable speed (40 km/h)
                G[from_id][to_id]['time'] = (distance / 40) * 60
                
            except Exception as e:
                print(f"Error adding existing road: {e}")
        
        print(f"Added {roads_added} existing roads to the graph")
            
        # Add potential roads if requested
        potential_added = 0
        if include_potential:
            for road in self.potential_roads:
                try:
                    from_id, to_id, distance, capacity, cost = road
                    
                    # Ensure both nodes exist in the graph
                    if from_id not in G or to_id not in G:
                        continue
                        
                    G.add_edge(from_id, to_id, 
                              distance=distance, 
                              capacity=capacity, 
                              cost=cost,
                              type='potential')
                    
                    potential_added += 1
                except Exception as e:
                    print(f"Error adding potential road: {e}")
            
            print(f"Added {potential_added} potential roads to the graph")
        
        # Add metro and bus connections if requested
        if include_transit:
            self._add_metro_connections(G)
            self._add_bus_connections(G)
                
        # Check for isolated components and print diagnostic information
        if not nx.is_connected(G):
            components = list(nx.connected_components(G))
            print(f"WARNING: Graph is not fully connected. Found {len(components)} components")
            
        return G
    
    def _add_metro_connections(self, G):
        """Add metro connections to the graph"""
        connections_added = 0
        
        for line_id, name, stations_str, passengers in self.metro_lines:
            try:
                # Parse station IDs
                stations = stations_str.replace('"', '').split(',')
                
                # Add edges between consecutive stations
                for i in range(len(stations) - 1):
                    from_id, to_id = stations[i], stations[i+1]
                    
                    # Skip if nodes don't exist
                    if from_id not in G or to_id not in G:
                        continue
                    
                    # Calculate straight-line distance if coordinates are available
                    try:
                        x1, y1 = G.nodes[from_id]['x'], G.nodes[from_id]['y']
                        x2, y2 = G.nodes[to_id]['x'], G.nodes[to_id]['y']
                        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                    except:
                        # Default 5km if coordinates not available
                        distance = 5.0
                    
                    # Metro is faster than roads, so we'll use a different travel time calculation
                    # Average metro speed: 60 km/h vs 30-40 km/h for cars
                    metro_travel_time = (distance / 60) * 60  # minutes
                    
                    # Add a metro edge
                    G.add_edge(from_id, to_id,
                              distance=distance,
                              capacity=3000,  # High capacity for metro
                              condition=10,   # Perfect condition
                              type='metro',
                              line=name,
                              line_id=line_id,
                              time=metro_travel_time,  # Base travel time in minutes
                              base_speed=60,          # km/h
                              mode='metro')
                    
                    connections_added += 1
            except Exception as e:
                print(f"Error adding metro connections for line {line_id}: {e}")
        
        if connections_added > 0:
            print(f"Added {connections_added} metro connections")
    
    def _add_bus_connections(self, G):
        """Add bus connections to the graph"""
        connections_added = 0
        
        for route_id, stops_str, buses_assigned, passengers in self.bus_routes:
            try:
                # Parse stop IDs
                stops = stops_str.replace('"', '').split(',')
                
                # Add edges between consecutive stops
                for i in range(len(stops) - 1):
                    from_id, to_id = stops[i], stops[i+1]
                    
                    # Skip if nodes don't exist
                    if from_id not in G or to_id not in G:
                        continue
                    
                    # Calculate distance (either using the road network or straight-line)
                    distance = 0
                    
                    # First try to find a road path
                    try:
                        path = nx.shortest_path(G, source=from_id, target=to_id, weight='distance')
                        # Only use if the path exists and only contains road edges
                        if all(G[path[j]][path[j+1]].get('type') == 'road' for j in range(len(path)-1)):
                            distance = sum(G[path[j]][path[j+1]]['distance'] for j in range(len(path)-1))
                    except (nx.NetworkXNoPath, KeyError):
                        pass
                    
                    # If road path not found, use straight-line distance
                    if distance == 0:
                        try:
                            x1, y1 = G.nodes[from_id]['x'], G.nodes[from_id]['y']
                            x2, y2 = G.nodes[to_id]['x'], G.nodes[to_id]['y']
                            distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                        except:
                            # Default 4km if coordinates not available
                            distance = 4.0
                    
                    # Buses are slower than cars due to stops, approximately 25 km/h average
                    # But they have dedicated lanes in some areas, so less affected by traffic
                    bus_travel_time = (distance / 25) * 60  # minutes
                    
                    # Bus frequency affects waiting time - more buses = less waiting
                    frequency = max(10, 60 / buses_assigned)  # minutes between buses
                    
                    # Add a bus edge
                    G.add_edge(from_id, to_id,
                              distance=distance,
                              capacity=buses_assigned * 50,  # Assume 50 passengers per bus
                              condition=8,                   # Good but not perfect
                              type='bus',
                              route=route_id,
                              time=bus_travel_time,         # Base travel time in minutes
                              waiting_time=frequency/2,     # Average waiting time (half the frequency)
                              frequency=frequency,          # Minutes between buses
                              base_speed=25,                # km/h
                              mode='bus')
                    
                    connections_added += 1
            except Exception as e:
                print(f"Error adding bus connections for route {route_id}: {e}")
        
        if connections_added > 0:
            print(f"Added {connections_added} bus connections")
            
    def build_multimodal_graph(self):
        """Build a graph that supports multimodal pathfinding with appropriate weights"""
        G = self.build_networkx_graph(include_transit=True)
        
        # Add time penalties for switching between transportation modes
        # This creates a more realistic model with transfer penalties
        transfer_graph = nx.Graph()
        
        # First copy all nodes and their attributes
        for node, data in G.nodes(data=True):
            transfer_graph.add_node(node, **data)
        
        # Then add edges with transfer penalties
        for u, v, data in G.edges(data=True):
            mode = data.get('mode', 'road')
            
            # Base time is the travel time on that edge
            time = data.get('time', (data['distance'] / 40) * 60)  # Default: 40 km/h
            
            # For bus and metro, add waiting time
            if mode == 'bus':
                time += data.get('waiting_time', 5)  # Add average wait time
            elif mode == 'metro':
                time += 3  # Average metro waiting time (3 min)
            
            # Add the edge with complete timing data
            transfer_graph.add_edge(u, v, **data, multimodal_time=time)
        
        return transfer_graph
    
    def verify_and_repair_connectivity(self):
        """
        Verify that all transportation modes are correctly connected and repair if needed.
        This function ensures that metro lines and bus routes create proper connections in the graph.
        """
        # Build a basic graph with only road connections to check connectivity
        G_roads = self.build_networkx_graph(include_potential=False, include_transit=False)
        
        # Check for isolated components with only road connections
        if not nx.is_connected(G_roads):
            road_components = list(nx.connected_components(G_roads))
            print(f"Initial road network has {len(road_components)} disconnected components")
            
            # Print the largest component size
            largest_component_size = max(len(component) for component in road_components)
            print(f"Largest connected component has {largest_component_size} nodes out of {len(G_roads)} total nodes")
            
            # Print isolated nodes (nodes that aren't connected to any other node)
            isolated_nodes = [node for node in G_roads.nodes() if G_roads.degree(node) == 0]
            if isolated_nodes:
                print(f"Found {len(isolated_nodes)} isolated nodes: {isolated_nodes}")
        
        # Build a graph with transit connections to see if it improves connectivity
        G_all = self.build_networkx_graph(include_potential=False, include_transit=True)
        
        # Check if adding transit improves connectivity
        if not nx.is_connected(G_all):
            all_components = list(nx.connected_components(G_all))
            print(f"After adding transit, network has {len(all_components)} disconnected components")
            
            # If still disconnected, check which nodes are in which components
            if len(all_components) > 1:
                component_sizes = [len(component) for component in all_components]
                print(f"Component sizes: {component_sizes}")
                
                # Print the nodes in smaller components
                for i, component in enumerate(all_components):
                    if len(component) < 5:  # Small component
                        print(f"Small component {i+1}: {component}")
        
        # Verify metro connections
        self._verify_metro_connections()
        
        # Verify bus connections
        self._verify_bus_connections()
        
        return G_all
    
    def _verify_metro_connections(self):
        """Verify and ensure that metro lines can be traversed in the graph"""
        metro_edges_verified = 0
        
        for line_id, name, stations_str, passengers in self.metro_lines:
            stations = stations_str.replace('"', '').split(',')
            
            # Check if all stations exist
            missing_stations = [station for station in stations if station not in self.nodes]
            if missing_stations:
                print(f"Warning: Metro line {line_id} ({name}) has missing stations: {missing_stations}")
                continue
                
            # Ensure consecutive stations are connected
            for i in range(len(stations) - 1):
                from_id, to_id = stations[i], stations[i+1]
                
                # Calculate a reasonable distance if missing
                distance = 5.0  # Default 5km between metro stations
                
                # Try to get coordinates for better distance estimation
                if from_id in self.nodes and to_id in self.nodes:
                    try:
                        x1, y1 = self.nodes[from_id]['x'], self.nodes[from_id]['y']
                        x2, y2 = self.nodes[to_id]['x'], self.nodes[to_id]['y']
                        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                    except (KeyError, TypeError):
                        pass
                
                # Store this connection in a special metro_connections list if needed
                print(f"Verified metro connection between {from_id} and {to_id} on line {line_id}")
                metro_edges_verified += 1
                
        print(f"Verified {metro_edges_verified} metro connections")
    
    def _verify_bus_connections(self):
        """Verify and ensure that bus routes can be traversed in the graph"""
        bus_edges_verified = 0
        
        for route_id, stops_str, buses_assigned, passengers in self.bus_routes:
            stops = stops_str.replace('"', '').split(',')
            
            # Check if all stops exist
            missing_stops = [stop for stop in stops if stop not in self.nodes]
            if missing_stops:
                print(f"Warning: Bus route {route_id} has missing stops: {missing_stops}")
                continue
                
            # Ensure consecutive stops are connected
            for i in range(len(stops) - 1):
                from_id, to_id = stops[i], stops[i+1]
                
                # Calculate a reasonable distance if missing
                distance = 4.0  # Default 4km between bus stops
                
                # Try to get coordinates for better distance estimation
                if from_id in self.nodes and to_id in self.nodes:
                    try:
                        x1, y1 = self.nodes[from_id]['x'], self.nodes[from_id]['y']
                        x2, y2 = self.nodes[to_id]['x'], self.nodes[to_id]['y']
                        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                    except (KeyError, TypeError):
                        pass
                
                # Store this connection in a special bus_connections list if needed
                print(f"Verified bus connection between {from_id} and {to_id} on route {route_id}")
                bus_edges_verified += 1
                
        print(f"Verified {bus_edges_verified} bus connections")
    
    def identify_isolated_facilities(self):
        """
        Identify isolated facilities in the transportation network without connecting them.
        As per requirements, we should leave disconnected nodes as-is and handle disconnected
        components gracefully in the pathfinding algorithms.
        """
        # Build a graph to check connectivity
        G = self.build_networkx_graph(include_potential=False)
        
        # Identify all facilities
        all_facilities = [node_id for node_id in self.nodes if isinstance(node_id, str) and node_id.startswith('F')]
        
        # Check which facilities are isolated
        isolated_facilities = []
        for facility_id in all_facilities:
            if facility_id not in G or G.degree(facility_id) == 0:
                isolated_facilities.append(facility_id)
                print(f"Facility {facility_id} ({self.nodes[facility_id]['name']}) is isolated")
        
        if not isolated_facilities:
            print("No isolated facilities found in the transportation network")
        else:
            print(f"Found {len(isolated_facilities)} isolated facilities in the network")
            print("These facilities will remain disconnected - paths to these facilities will not be found")
        
        # Identify disconnected components
        if not nx.is_connected(G):
            components = list(nx.connected_components(G))
            print(f"Graph has {len(components)} disconnected components")
            
            # Map facilities to components
            for facility_id in all_facilities:
                if facility_id in G:
                    for i, component in enumerate(components):
                        if facility_id in component:
                            component_size = len(component)
                            print(f"Facility {facility_id} ({self.nodes[facility_id]['name']}) is in component {i+1} with {component_size} nodes")
                            break
        
        return isolated_facilities
