# Pathfinding Module Documentation

The pathfinding module provides algorithms for finding optimal routes through the transportation network.

## File: `backend/src/app/services/pathfinding.py`

This module implements various path-finding algorithms for different scenarios:

1. **Basic shortest path finding**
2. **Time-optimized travel considering traffic**
3. **Emergency vehicle routing with priority**
4. **Multimodal transportation routing**

### Functions

#### find_shortest_path

```python
def find_shortest_path(graph, start_id, end_id, weight='distance')
```

Finds the shortest path between two nodes based on a specified weight metric.

**Parameters:**
- `graph`: The transportation graph object
- `start_id`: Starting location ID
- `end_id`: Destination location ID
- `weight`: Edge weight to minimize ('distance' by default)

**Returns:**
- Dictionary with path information:
  - `success`: Boolean indicating if path was found
  - `path`: List of node IDs in the path
  - `path_names`: List of location names in the path
  - `distance`: Total distance of the path
  - If failure: `message` with reason

#### compute_travel_time

```python
def compute_travel_time(graph, start_id, end_id, time_of_day='morning', speed_factor=1.0)
```

Computes the estimated travel time between two points based on distance and traffic conditions.

**Parameters:**
- `graph`: The transportation graph object
- `start_id`: Starting location ID
- `end_id`: Destination location ID
- `time_of_day`: Time period ('morning', 'afternoon', 'evening', 'night')
- `speed_factor`: Speed multiplier for adjusting vehicle speed (default 1.0)

**Returns:**
- Dictionary with travel information:
  - `success`: Boolean indicating if path was found
  - `path`: List of node IDs in the path
  - `path_names`: List of location names in the path
  - `total_time_minutes`: Estimated travel time in minutes
  - `total_distance_km`: Total distance in kilometers
  - If failure: `message` with reason

#### emergency_route_astar

```python
def emergency_route_astar(graph, start_id, end_id, time_of_day='morning', emergency_type='ambulance')
```

Uses A* search algorithm to find optimal emergency vehicle routes with reduced impact from traffic.

**Parameters:**
- `graph`: The transportation graph object
- `start_id`: Starting location ID
- `end_id`: Destination location ID
- `time_of_day`: Time period ('morning', 'afternoon', 'evening', 'night')
- `emergency_type`: Type of emergency vehicle ('ambulance', 'fire', 'police')

**Returns:**
- Dictionary with detailed emergency route information:
  - `success`: Boolean indicating if path was found
  - `path`: List of node IDs in the path
  - `path_names`: List of location names in the path
  - `path_details`: Detailed segment-by-segment information
  - `total_time_minutes`: Estimated travel time in minutes
  - `total_distance_km`: Total distance in kilometers
  - `time_saved_vs_normal`: Time saved compared to normal routing
  - `percent_improvement`: Percentage improvement over normal routing
  - If failure: `message` with reason

#### multimodal_route

```python
def multimodal_route(graph, start_id, end_id, time_of_day='morning', preferred_modes=None, max_transfers=None)
```

Finds the optimal route using all available transportation modes.

**Parameters:**
- `graph`: The transportation graph object
- `start_id`: Starting location ID
- `end_id`: Destination location ID
- `time_of_day`: Time period ('morning', 'afternoon', 'evening', 'night')
- `preferred_modes`: List of preferred transportation modes (e.g., ['road', 'metro'])
- `max_transfers`: Maximum number of mode transfers allowed

**Returns:**
- Dictionary with multimodal route information:
  - `success`: Boolean indicating if path was found
  - `path`: List of node IDs in the path
  - `path_names`: List of location names in the path
  - `total_time_minutes`: Estimated travel time in minutes
  - `total_distance_km`: Total distance in kilometers
  - `transfers`: Number of transfers between modes
  - `segments`: Detailed segment information
  - `route_summary`: Summarized route by transportation mode
  - Comparison with road-only route
  - If failure: `message` with reason

### Algorithm Details

#### A* Search for Emergency Routing

The `emergency_route_astar` function uses the A* algorithm with a custom heuristic:

```python
def heuristic(n1, n2):
    # Use coordinates to calculate Haversine distance
    x1, y1 = graph.nodes[n1]['x'], graph.nodes[n1]['y']
    x2, y2 = graph.nodes[n2]['x'], graph.nodes[n2]['y']
    
    # Use Haversine for more accurate distance
    # Convert decimal degrees to radians
    lon1, lat1 = math.radians(x1), math.radians(y1)
    lon2, lat2 = math.radians(x2), math.radians(y2)
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    distance = c * r
    
    # Convert to minutes at emergency speed (90 km/h)
    return (distance / 90) * 60  # Convert to minutes
```

The emergency routing also adjusts speeds based on:
- Emergency vehicle type
- Road conditions
- Traffic congestion (with reduced impact for emergency vehicles)

#### Multimodal Routing

The multimodal routing function handles:
- Different transportation modes (road, bus, metro)
- Transfer points between modes
- Different speeds and wait times for each mode
- Penalties for transfers
- Route grouping by transportation mode

### Usage Examples

```python
# Find shortest path by distance
result = find_shortest_path(graph, "1", "15")

# Find fastest route considering morning traffic
result = compute_travel_time(graph, "1", "15", time_of_day="morning")

# Find emergency route for an ambulance
result = emergency_route_astar(graph, "H1", "7", emergency_type="ambulance")

# Find multimodal route with preference for metro
result = multimodal_route(graph, "2", "12", preferred_modes=["metro", "road"])
```
