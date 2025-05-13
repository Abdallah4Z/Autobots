import pandas as pd
import ast

def load_data_from_csv(graph, neighborhoods_file, facilities_file, existing_roads_file, 
                     potential_roads_file, traffic_file, metro_file, bus_file, demand_file):
    """Load all data from CSV files into the graph"""
    
    # Load neighborhoods and districts
    neighborhoods_df = pd.read_csv(neighborhoods_file)
    print(f"Neighborhoods CSV columns: {neighborhoods_df.columns.tolist()}")
    for _, row in neighborhoods_df.iterrows(): 
        node_id = row['ID']
        # Convert numeric IDs to integers
        if isinstance(node_id, str) and node_id.isdigit():
            node_id = int(node_id)
            
        graph.nodes[node_id] = {
            'id': node_id,
            'name': row['Name'],
            'population': row['Population'],
            'type': row['Type'],
            'x': row['X-coordinate'],
            'y': row['Y-coordinate'],
            'is_facility': False
        }
        
    # Load facilities
    facilities_df = pd.read_csv(facilities_file)
    print(f"Facilities CSV columns: {facilities_df.columns.tolist()}")
    for _, row in facilities_df.iterrows():
        node_id = row['ID']
        graph.nodes[node_id] = {
            'id': node_id,
            'name': row['Name'],
            'type': row['Type'],
            'x': row['X-coordinate'],
            'y': row['Y-coordinate'],
            'is_facility': True,
            'population': 0  # Facilities don't have population
        }
        
    # Load existing roads
    roads_df = pd.read_csv(existing_roads_file)
    print(f"Existing Roads CSV columns: {roads_df.columns.tolist()}")
    
    # Define possible column name variations for existing roads
    from_id_variants = ['FromID', 'From ID', 'From_ID', 'Source', 'Source ID']
    to_id_variants = ['ToID', 'To ID', 'To_ID', 'Target', 'Target ID']
    distance_variants = ['Distance (km)', 'Distance(km)', 'Distance_km', 'Length (km)']
    capacity_variants = ['Current Capacity (vehicles/hour)', 'Capacity (veh/h)', 'Current Capacity']
    condition_variants = ['Condition (1-10)', 'Condition', 'Road Condition']
    
    # Find the actual column names in the dataframe
    from_id_col = next((col for col in from_id_variants if col in roads_df.columns), None)
    to_id_col = next((col for col in to_id_variants if col in roads_df.columns), None)
    distance_col = next((col for col in distance_variants if col in roads_df.columns), None)
    capacity_col = next((col for col in capacity_variants if col in roads_df.columns), None)
    condition_col = next((col for col in condition_variants if col in roads_df.columns), None)
    
    print(f"Using column names: {from_id_col}, {to_id_col}, {distance_col}, {capacity_col}, {condition_col}")
    
    graph.existing_roads = []
    for _, row in roads_df.iterrows():
        from_id = row[from_id_col]
        to_id = row[to_id_col]
        
        # Convert numeric IDs to integers for consistent processing
        if isinstance(from_id, str) and from_id.isdigit():
            from_id = int(from_id)
        if isinstance(to_id, str) and to_id.isdigit():
            to_id = int(to_id)
        
        # Only add roads where both endpoints exist in our nodes list
        if from_id in graph.nodes and to_id in graph.nodes:
            graph.existing_roads.append(
                (from_id, to_id, row[distance_col], row[capacity_col], row[condition_col])
            )
        else:
            print(f"Warning: Road from {from_id} to {to_id} references nodes that don't exist")
    
    # Load potential roads
    potential_df = pd.read_csv(potential_roads_file)
    print(f"Potential Roads CSV columns: {potential_df.columns.tolist()}")
    
    # Define possible column name variations for potential roads
    construction_cost_variants = ['Construction Cost (Million EGP)', 'Cost (Million EGP)', 'Construction Cost']
    estimated_capacity_variants = ['Estimated Capacity (vehicles/hour)', 'Est. Capacity', 'Estimated Capacity']
    
    # Find the actual column names
    from_id_col = next((col for col in from_id_variants if col in potential_df.columns), None)
    to_id_col = next((col for col in to_id_variants if col in potential_df.columns), None)
    distance_col = next((col for col in distance_variants if col in potential_df.columns), None)
    capacity_col = next((col for col in estimated_capacity_variants if col in potential_df.columns), None)
    cost_col = next((col for col in construction_cost_variants if col in potential_df.columns), None)
    
    print(f"Using column names for potential roads: {from_id_col}, {to_id_col}, {distance_col}, {capacity_col}, {cost_col}")
    
    graph.potential_roads = []
    for _, row in potential_df.iterrows():
        from_id = row[from_id_col]
        to_id = row[to_id_col]
        
        # Convert numeric IDs to integers for consistent processing
        if isinstance(from_id, str) and from_id.isdigit():
            from_id = int(from_id)
        if isinstance(to_id, str) and to_id.isdigit():
            to_id = int(to_id)
        
        # Only add roads where both endpoints exist in our nodes list
        if from_id in graph.nodes and to_id in graph.nodes:
            graph.potential_roads.append(
                (from_id, to_id, row[distance_col], row[capacity_col], row[cost_col])
            )
        else:
            print(f"Warning: Potential road from {from_id} to {to_id} references nodes that don't exist")
    
    # Load traffic data with improved handling for different formats
    traffic_df = pd.read_csv(traffic_file)
    print(f"Traffic CSV columns: {traffic_df.columns.tolist()}")
    
    # Define traffic column variations
    morning_variants = ['Morning Peak (veh/h)', 'Morning', 'AM Peak']
    afternoon_variants = ['Afternoon (veh/h)', 'Afternoon', 'Midday']
    evening_variants = ['Evening Peak (veh/h)', 'Evening', 'PM Peak']
    night_variants = ['Night (veh/h)', 'Night', 'Late Night']
    
    # Find actual column names for time periods
    morning_col = next((col for col in morning_variants if col in traffic_df.columns), None)
    afternoon_col = next((col for col in afternoon_variants if col in traffic_df.columns), None)
    evening_col = next((col for col in evening_variants if col in traffic_df.columns), None)
    night_col = next((col for col in night_variants if col in traffic_df.columns), None)
    
    # Check if the traffic data format uses a single RoadID column or separate FromID/ToID columns
    if 'RoadID' in traffic_df.columns:
        print("Traffic data uses RoadID format")
        # Format with a single RoadID column
        for _, row in traffic_df.iterrows():
            try:
                # Handle the complex string format from the CSV: "(""1"",""3"")"
                road_id_str = row['RoadID']
                
                # Clean up and parse the tuple string
                if isinstance(road_id_str, str) and "," in road_id_str:
                    # Try to extract the IDs from the string format
                    road_id_str = road_id_str.replace('"', '').replace('(', '').replace(')', '')
                    parts = road_id_str.split(',')
                    if len(parts) == 2:
                        # Create the road ID tuple as expected by the algorithm
                        from_id = parts[0].strip()
                        to_id = parts[1].strip()
                        
                        # Convert numeric IDs to integers for consistent processing
                        if from_id.isdigit():
                            from_id = int(from_id)
                        if to_id.isdigit():
                            to_id = int(to_id)
                        
                        # Use the tuple as the key - this matches how roads are identified in the graph
                        road_id = (from_id, to_id)
                    else:
                        # Use the original as fallback
                        road_id = road_id_str
                else:
                    road_id = road_id_str
                
                graph.traffic_data[road_id] = {
                    'morning': row[morning_col],
                    'afternoon': row[afternoon_col],
                    'evening': row[evening_col],
                    'night': row[night_col]
                }
                
                # Also add the reverse direction with the same traffic data
                # This ensures bidirectional traffic is properly modeled
                if isinstance(road_id, tuple):
                    to_from_id = (road_id[1], road_id[0])
                    graph.traffic_data[to_from_id] = {
                        'morning': row[morning_col],
                        'afternoon': row[afternoon_col],
                        'evening': row[evening_col],
                        'night': row[night_col]
                    }
            except Exception as e:
                print(f"Error processing traffic data row {row['RoadID']}: {e}")
    else:
        from_id_col = next((col for col in from_id_variants if col in traffic_df.columns), None)
        to_id_col = next((col for col in to_id_variants if col in traffic_df.columns), None)
        
        print(f"Using traffic column names: {from_id_col}, {to_id_col}, {morning_col}, {afternoon_col}, {evening_col}, {night_col}")
        
        for _, row in traffic_df.iterrows():
            from_id = row[from_id_col]
            to_id = row[to_id_col]
            
            # Convert numeric IDs to integers for consistent processing
            if isinstance(from_id, str) and from_id.isdigit():
                from_id = int(from_id)
            if isinstance(to_id, str) and to_id.isdigit():
                to_id = int(to_id)
                
            road_id = (from_id, to_id)
            graph.traffic_data[road_id] = {
                'morning': row[morning_col],
                'afternoon': row[afternoon_col],
                'evening': row[evening_col],
                'night': row[night_col]
            }
    
    # Load metro lines with improved handling
    try:
        metro_df = pd.read_csv(metro_file)
        print(f"Metro CSV columns: {metro_df.columns.tolist()}")
        
        # Define metro column variations
        line_id_variants = ['LineID', 'Line ID', 'Line Number']
        stations_variants = ['Stations (comma-separated IDs)', 'Stations', 'Station IDs']
        passengers_variants = ['Daily Passengers', 'Passengers', 'Daily Ridership']
        
        line_id_col = next((col for col in line_id_variants if col in metro_df.columns), None)
        name_col = 'Name' if 'Name' in metro_df.columns else next((col for col in ['Line Name', 'Route'] if col in metro_df.columns), None)
        stations_col = next((col for col in stations_variants if col in metro_df.columns), None)
        passengers_col = next((col for col in passengers_variants if col in metro_df.columns), None)
        
        print(f"Using metro column names: {line_id_col}, {name_col}, {stations_col}, {passengers_col}")
        
        if line_id_col and name_col and stations_col and passengers_col:
            graph.metro_lines = [
                (row[line_id_col], row[name_col], row[stations_col], row[passengers_col]) 
                for _, row in metro_df.iterrows()
            ]
        else:
            print("Warning: Could not find all required columns for metro lines")
            graph.metro_lines = []
    except Exception as e:
        print(f"Error loading metro data: {e}")
        graph.metro_lines = []
    
    # Load bus routes with improved handling
    try:
        bus_df = pd.read_csv(bus_file)
        print(f"Bus CSV columns: {bus_df.columns.tolist()}")
        
        route_id_variants = ['RouteID', 'Route ID', 'Route Number']
        stops_variants = ['Stops (comma-separated IDs)', 'Stops', 'Stop IDs']
        buses_variants = ['Buses Assigned', 'Buses', 'Fleet Size']
        
        route_id_col = next((col for col in route_id_variants if col in bus_df.columns), None)
        stops_col = next((col for col in stops_variants if col in bus_df.columns), None)
        buses_col = next((col for col in buses_variants if col in bus_df.columns), None)
        passengers_col = next((col for col in passengers_variants if col in bus_df.columns), None)
        
        print(f"Using bus column names: {route_id_col}, {stops_col}, {buses_col}, {passengers_col}")
        
        if route_id_col and stops_col and buses_col and passengers_col:
            graph.bus_routes = [
                (row[route_id_col], row[stops_col], row[buses_col], row[passengers_col]) 
                for _, row in bus_df.iterrows()
            ]
        else:
            print("Warning: Could not find all required columns for bus routes")
            graph.bus_routes = []
    except Exception as e:
        print(f"Error loading bus data: {e}")
        graph.bus_routes = []
    
    # Load transport demand with improved handling
    try:
        demand_df = pd.read_csv(demand_file)
        print(f"Demand CSV columns: {demand_df.columns.tolist()}")
        
        from_id_col = next((col for col in from_id_variants if col in demand_df.columns), None)
        to_id_col = next((col for col in to_id_variants if col in demand_df.columns), None)
        passengers_col = next((col for col in passengers_variants if col in demand_df.columns), None)
        
        print(f"Using demand column names: {from_id_col}, {to_id_col}, {passengers_col}")
        
        if from_id_col and to_id_col and passengers_col:
            for _, row in demand_df.iterrows():
                from_id = row[from_id_col]
                to_id = row[to_id_col]
                
                # Convert numeric IDs to integers for consistent processing
                if isinstance(from_id, str) and from_id.isdigit():
                    from_id = int(from_id)
                if isinstance(to_id, str) and to_id.isdigit():
                    to_id = int(to_id)
                
                key = (from_id, to_id)
                graph.transport_demand[key] = row[passengers_col]
        else:
            print("Warning: Could not find all required columns for transport demand")
    except Exception as e:
        print(f"Error loading demand data: {e}")