# Data Formatting Module Documentation

The data formatting module provides functions to convert internal graph data structures into JSON formats suitable for frontend visualization and API responses.

## File: `backend/src/app/utils/data_formatting.py`

This module contains utility functions for converting graph data to standardized JSON formats.

### Functions

#### get_all_nodes_json

```python
def get_all_nodes_json(graph)
```

Converts all nodes in the graph to a JSON-compatible format.

**Parameters:**
- `graph`: The transportation graph object

**Returns:**
- A list of node dictionaries with standardized fields:
  - `id`: Node identifier
  - `name`: Node name
  - `type`: Node type (residential, commercial, etc.)
  - `x`, `y`: Coordinates
  - `population`: Population (for neighborhoods)
  - `is_facility`: Boolean indicating if the node is a facility

#### get_all_edges_json

```python
def get_all_edges_json(graph, include_potential=False)
```

Converts all edges (roads) in the graph to a JSON-compatible format.

**Parameters:**
- `graph`: The transportation graph object
- `include_potential`: Whether to include potential (not yet built) roads

**Returns:**
- A list of edge dictionaries with standardized fields:
  - `id`: Edge identifier (source_target)
  - `source`: Source node ID
  - `target`: Target node ID
  - `distance`: Distance in kilometers
  - `capacity`: Road capacity in vehicles per hour
  - `flow`: Current traffic flow
  - `congestion`: Congestion ratio (flow/capacity)
  - `condition`: Road condition score
  - `potential`: Boolean indicating if this is a potential road

#### get_metro_lines_json

```python
def get_metro_lines_json(graph)
```

Converts metro line data to a JSON-compatible format.

**Parameters:**
- `graph`: The transportation graph object

**Returns:**
- A list of metro line dictionaries with standardized fields:
  - `id`: Line identifier
  - `name`: Line name
  - `stations`: List of station IDs
  - `station_names`: List of station names
  - `daily_passengers`: Passenger volume

#### get_bus_routes_json

```python
def get_bus_routes_json(graph)
```

Converts bus route data to a JSON-compatible format.

**Parameters:**
- `graph`: The transportation graph object

**Returns:**
- A list of bus route dictionaries with standardized fields:
  - `id`: Route identifier
  - `stops`: List of stop IDs
  - `stop_names`: List of stop names
  - `buses_assigned`: Number of buses on the route
  - `daily_passengers`: Passenger volume

#### get_population_density_map

```python
def get_population_density_map(graph)
```

Creates a population density representation for heatmap visualization.

**Parameters:**
- `graph`: The transportation graph object

**Returns:**
- A list of dictionaries with population data points:
  - `x`, `y`: Coordinates
  - `weight`: Population value normalized for visualization
  - `raw_population`: Actual population value
  - `name`: Node name

#### format_path_for_response

```python
def format_path_for_response(graph, path, total_distance=None, total_time=None)
```

Formats a path for API response.

**Parameters:**
- `graph`: The transportation graph object
- `path`: List of node IDs representing the path
- `total_distance`: Total distance of the path (optional)
- `total_time`: Total travel time (optional)

**Returns:**
- A dictionary with formatted path information:
  - `success`: Always true
  - `path`: Original path
  - `path_names`: List of node names
  - `distance`: Total distance (if provided)
  - `time`: Total time (if provided)
  - `edges`: List of edge IDs for visualization

#### normalize_node_id

```python
def normalize_node_id(node_id)
```

Normalizes node IDs to ensure consistent format.

**Parameters:**
- `node_id`: Node ID to normalize

**Returns:**
- Normalized ID (converts numeric strings to integers if appropriate)

### Usage Examples

```python
# Get node data for frontend visualization
nodes_json = get_all_nodes_json(graph)

# Get edge data with potential roads included
edges_json = get_all_edges_json(graph, include_potential=True)

# Get metro lines for a transit map
metro_lines = get_metro_lines_json(graph)

# Format a path for API response
path_result = format_path_for_response(
    graph,
    path=["1", "5", "10"],
    total_distance=12.5,
    total_time=24.3
)
```
