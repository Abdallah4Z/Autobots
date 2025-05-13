# API Routes Documentation

The API routes module defines all the HTTP endpoints provided by the Flask application.

## File: `backend/src/app/api/routes.py`

This module exports a `register_routes` function that registers all API endpoints with the Flask application.

### Main Function

```python
def register_routes(app, graph)
```

Registers all API endpoints with the Flask application.

**Parameters:**
- `app`: The Flask application object
- `graph`: The transportation graph object

### API Endpoints

#### GET `/api/graph_data`

Returns graph data in JSON format for interactive frontend visualization.

**Query Parameters:**
- `potential` (optional): Set to 'true' to include potential roads

**Returns:**
- JSON with `nodes` and `edges` for visualization

#### GET `/api/graph_image`

Returns a base64 encoded image of the graph.

**Query Parameters:**
- `potential` (optional): Set to 'true' to include potential roads

**Returns:**
- JSON with `success` and `image` (base64 encoded)

#### GET `/api/nodes`

Returns all node data for dropdowns and selections.

**Returns:**
- JSON with `success` and `nodes` list

#### POST `/api/find_path`

API endpoint to find paths between locations.

**Request Body:**
- `start_id`: Starting location ID
- `end_id`: Destination location ID
- `mode` (optional): 'distance' or 'time' (default: 'distance')
- `time_of_day` (optional): 'morning', 'afternoon', 'evening', 'night' (default: 'morning')

**Returns:**
- JSON with path information:
  - `success`: Boolean indicating success
  - `path`: List of node IDs in the path
  - `path_names`: List of location names in the path
  - `distance`: Total distance of the path
  - `time`: Total travel time (if mode is 'time')
  - `edges`: Edge IDs for highlighting in the UI
  - If failure: `message` with reason

#### GET `/api/statistics`

Returns network statistics.

**Returns:**
- JSON with `success` and `statistics` data

#### GET `/api/metro_lines`

Returns metro line data.

**Returns:**
- JSON with `success` and `metro_lines` data

#### GET `/api/bus_routes`

Returns bus route data.

**Returns:**
- JSON with `success` and `bus_routes` data

#### GET `/api/population_density`

Returns population density data for heatmap visualization.

**Returns:**
- JSON with `success` and `density_map` data

#### GET `/api/traffic_analysis`

Analyzes traffic patterns and congestion.

**Query Parameters:**
- `time` (optional): 'morning', 'afternoon', 'evening', 'night' (default: 'morning')

**Returns:**
- JSON with `success` and `congestion_data`

#### GET `/api/transport_suggestions`

Gets suggestions for public transportation improvements.

**Returns:**
- JSON with `success` and `suggestions` list

#### POST `/api/emergency_route`

Finds optimal emergency routes with priority for emergency vehicles.

**Request Body:**
- `start_id`: Starting location ID
- `end_id`: Destination location ID
- `emergency_type` (optional): 'ambulance', 'fire', 'police' (default: 'ambulance')
- `time_of_day` (optional): 'morning', 'afternoon', 'evening', 'night' (default: 'morning')

**Returns:**
- JSON with emergency route information:
  - `success`: Boolean indicating success
  - `path`: List of node IDs in the path
  - `path_names`: List of location names in the path
  - `distance`: Total distance of the path
  - `time`: Total travel time
  - `edges`: Edge IDs for highlighting in the UI
  - If failure: `message` with reason

#### POST `/api/multimodal_route`

Finds optimal route using multiple transportation modes.

**Request Body:**
- `start_id`: Starting location ID
- `end_id`: Destination location ID
- `time_of_day` (optional): 'morning', 'afternoon', 'evening', 'night' (default: 'morning')
- `preferred_modes` (optional): List of preferred modes (e.g., ['road', 'metro'])
- `max_transfers` (optional): Maximum number of transfers allowed

**Returns:**
- JSON with multimodal route information:
  - `success`: Boolean indicating success
  - `path`: List of node IDs in the path
  - `path_names`: List of location names in the path
  - `distance`: Total distance of the path
  - `time`: Total travel time
  - `modes`: List of transportation modes used
  - `transfers`: Number of transfers
  - `edges`: Edge IDs for highlighting in the UI
  - If failure: `message` with reason

#### GET `/api/optimize_road_network`

Optimizes road network using MST algorithm.

**Query Parameters:**
- `prioritize_population` (optional): 'true' or 'false' (default: 'false')
- `include_existing` (optional): 'true' or 'false' (default: 'true')
- `max_budget` (optional): Maximum budget in million EGP (default: 1000000)

**Returns:**
- JSON with optimization results

#### GET `/api/optimize_bus_routes`

Optimizes bus routes using dynamic programming.

**Query Parameters:**
- `max_buses` (optional): Maximum number of buses (default: 100)
- `target_coverage` (optional): Target population coverage (0.0-1.0, default: 0.8)

**Returns:**
- JSON with optimization results

#### GET `/api/optimize_metro_schedule`

Optimizes metro schedule using dynamic programming.

**Query Parameters:**
- `peak_hours` (optional): Comma-separated peak hours (default: 'morning,evening')
- `off_peak_hours` (optional): Comma-separated off-peak hours (default: 'afternoon,night')

**Returns:**
- JSON with `success` and `optimized_schedules` data

### Helper Functions

```python
def convert_keys_to_str(obj)
```

Recursively converts all dictionary keys to strings, required for JSON serialization of tuple keys.

**Parameters:**
- `obj`: The object to convert (dict, list, or other)

**Returns:**
- Converted object with string keys for any dictionaries
