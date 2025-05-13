# Transportation API Module Documentation

The transportation module provides the core routing functionality for the public transportation network.

## File: `backend/src/app/api/transportation.py`

This module contains functions for calculating optimal routes through the public transportation network.

### Global Variables

```python
# Global objects initialized once
tn = TransportationNetwork.from_json_folder('data')
G = tn.build_public_transport_network()
NODES = tn.nodes

# Memoization table to store computed routes
ROUTE_CACHE = {}
```

- `tn`: Main transportation network object
- `G`: Directed graph representing the public transportation network
- `NODES`: Dictionary of all nodes in the network
- `ROUTE_CACHE`: Memoization cache for route calculations

### Functions

#### calculate_metrics

```python
def calculate_metrics(G: nx.DiGraph, path: List[str]) -> Tuple[float, float]
```

Calculates total time (minutes) and distance (km) for a given path.

**Parameters:**
- `G`: NetworkX DiGraph representing the transportation network
- `path`: List of node IDs representing the path

**Returns:**
- Tuple of (total_time, total_distance)

#### summarise_path

```python
def summarise_path(G: nx.DiGraph, path: List[str]) -> List[Dict]
```

Breaks a path into segments based on transportation mode changes.

**Parameters:**
- `G`: NetworkX DiGraph representing the transportation network
- `path`: List of node IDs representing the path

**Returns:**
- List of dictionaries, each representing a segment with consistent mode and route

#### name

```python
def name(nid: str) -> str
```

Gets the name of a node.

**Parameters:**
- `nid`: Node ID

**Returns:**
- Name of the node

#### get_itinerary

```python
def get_itinerary(origin: str, dest: str) -> Dict
```

Gets the itinerary between origin and destination using dynamic programming (memoization).

**Parameters:**
- `origin`: Origin node ID
- `destination`: Destination node ID

**Returns:**
- Dictionary with itinerary information:
  - `origin`: Origin node name
  - `destination`: Destination node name
  - `steps`: List of steps in the itinerary
  - `total_time`: Total travel time in minutes
  - `total_distance`: Total distance in kilometers

### Implementation Details

#### Dynamic Programming with Memoization

The module uses memoization to cache computed routes:

```python
# Check if the route is already in the cache
cache_key = (origin, dest)
if cache_key in ROUTE_CACHE:
    cached_result = ROUTE_CACHE[cache_key]
    return {
        "origin": name(origin),
        "destination": name(dest),
        "steps": cached_result["steps"],
        "total_time": cached_result["total_time"],
        "total_distance": cached_result["total_distance"]
    }
```

This significantly improves performance for frequently requested routes.

#### Path Segmentation

The `summarise_path` function groups consecutive edges with the same transportation mode and route into segments:

```python
for u, v in zip(path[:-1], path[1:]):
    data = G[u][v]
    mode, route = data["mode"], data["route"]
    if (mode, route) != (cur_mode, cur_route):
        if cur_mode is not None:
            legs.append({"mode": cur_mode, "route": cur_route, "nodes": segment})
        cur_mode, cur_route, segment = mode, route, [u]
    segment.append(v)
```

This creates a more user-friendly representation of the journey by combining consecutive stops on the same transit line.

#### Travel Time and Distance Calculation

The `calculate_metrics` function estimates travel time and distance based on transportation mode:

```python
# Estimated time and distance factors by mode of transport
time_factor = {"walk": 5, "bus": 2, "metro": 1.5, "tram": 2}.get(mode, 3)
distance_factor = {"walk": 0.5, "bus": 1, "metro": 1.5, "tram": 1}.get(mode, 1)
```

Different modes have different speeds and distance coverage.

### Usage Examples

```python
# Get an itinerary between two points
itinerary = get_itinerary("1", "15")

# Access the summarized steps
for step in itinerary["steps"]:
    print(f"Take {step['mode']} {step['route']} from {step['start']} to {step['end']}")

# Get the total metrics
print(f"Total journey time: {itinerary['total_time']} minutes")
print(f"Total distance: {itinerary['total_distance']} km")
```
