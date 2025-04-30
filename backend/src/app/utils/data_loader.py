import pandas as pd

def load_data_from_csv(graph, neighborhoods_file, facilities_file, existing_roads_file, 
                     potential_roads_file, traffic_file, metro_file, bus_file, demand_file):
    """Load all data from CSV files into the graph"""
    
    # Load neighborhoods and districts
    neighborhoods_df = pd.read_csv(neighborhoods_file)
    for _, row in neighborhoods_df.iterrows(): 
        graph.nodes[row['ID']] = {
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
        graph.nodes[row['ID']] = {
            'name': row['Name'],
            'type': row['Type'],
            'x': row['X-coordinate'],
            'y': row['Y-coordinate'],
            'is_facility': True
        }
        
    # Load existing roads
    roads_df = pd.read_csv(existing_roads_file)
    graph.existing_roads = [
        (row['FromID'], row['ToID'], row['Distance(km)'], 
         row['Current Capacity(vehicles/hour)'], row['Condition(1-10)']) 
        for _, row in roads_df.iterrows()
    ]
    
    # Load potential roads
    potential_df = pd.read_csv(potential_roads_file)
    graph.potential_roads = [
        (row['FromID'], row['ToID'], row['Distance(km)'], 
         row['Estimated Capacity(vehicles/hour)'], row['Construction Cost(Million EGP)']) 
        for _, row in potential_df.iterrows()
    ]
    
    # Load traffic data
    traffic_df = pd.read_csv(traffic_file)
    for _, row in traffic_df.iterrows():
        road_id = f"{row['FromID']}{row['ToID']}"
        graph.traffic_data[road_id] = {
            'morning': row['Morning Peak(veh/h)'],
            'afternoon': row['Afternoon(veh/h)'],
            'evening': row['Evening Peak(veh/h)'],
            'night': row['Night(veh/h)']
        }
        
    # Load metro lines
    metro_df = pd.read_csv(metro_file)
    graph.metro_lines = [
        (row['LineID'], row['Name'], row['Stations(comma-separated IDs)'], row['Daily Passengers']) 
        for _, row in metro_df.iterrows()
    ]
    
    # Load bus routes
    bus_df = pd.read_csv(bus_file)
    graph.bus_routes = [
        (row['RouteID'], row['Stops(comma-separated IDs)'], 
         row['Buses Assigned'], row['Daily Passengers']) 
        for _, row in bus_df.iterrows()
    ]
    
    # Load transport demand
    demand_df = pd.read_csv(demand_file)
    for _, row in demand_df.iterrows():
        from_id, to_id = row['FromID'], row['ToID']
        key = f"{from_id}_{to_id}"
        graph.transport_demand[key] = row['Daily Passengers']