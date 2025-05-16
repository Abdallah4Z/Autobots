# Graph Model Documentation

The graph model module provides the CairoTransportationGraph class, which is the core data structure for the transportation network.

## File: `backend/src/app/models/graph.py`

This module contains the main graph model class used throughout the application.

### Classes

#### CairoTransportationGraph

```python
class CairoTransportationGraph:
    """
    Main graph model for the Cairo transportation network.
    Handles nodes, edges, and various transportation elements.
    """
```

The CairoTransportationGraph class stores all transportation data and provides methods for graph operations.

##### Properties and Attributes

- `nodes`: Dictionary mapping node IDs to node attributes
- `existing_roads`: List of tuples representing existing roads
- `potential_roads`: List of tuples representing potential roads
- `traffic_data`: Dictionary mapping road tuples to traffic data
- `metro_lines`: List of metro line data
- `bus_routes`: List of bus route data
- `transport_demand`: Dictionary mapping origin-destination pairs to demand

##### Methods

###### __init__

```python
def __init__(self)
```

Initializes an empty transportation graph.

###### build_networkx_graph

```python
def build_networkx_graph(self, include_potential=False)
```

Builds a NetworkX graph from the stored data.

**Parameters:**
- `include_potential`: Whether to include potential roads in the graph

**Returns:**
- A NetworkX Graph object

###### identify_isolated_facilities

```python
def identify_isolated_facilities(self)
```

Identifies facilities that are not connected to the main transportation network.

**Returns:**
- List of node IDs representing isolated facilities

###### verify_and_repair_connectivity

```python
def verify_and_repair_connectivity(self)
```

Verifies that the network is fully connected and attempts to repair disconnected components.

**Returns:**
- Dictionary with connectivity information:
  - `connected`: Boolean indicating if network is connected
  - `component_count`: Number of connected components
  - `fixed_connections`: List of added connections (if any)

###### get_node_coordinates

```python
def get_node_coordinates(self, node_id)
```

Gets the coordinates of a node.

**Parameters:**
- `node_id`: ID of the node

**Returns:**
- Tuple of (x, y) coordinates

###### calculate_haversine_distance

```python
def calculate_haversine_distance(self, node1_id, node2_id)
```

Calculates the Haversine distance between two nodes.

**Parameters:**
- `node1_id`: ID of the first node
- `node2_id`: ID of the second node

**Returns:**
- Distance in kilometers

###### add_potential_connection

```python
def add_potential_connection(self, from_id, to_id, distance=None, capacity=2000, construction_cost=10)
```

Adds a potential connection between two nodes.

**Parameters:**
- `from_id`: ID of the source node
- `to_id`: ID of the target node
- `distance`: Distance in kilometers (calculated if None)
- `capacity`: Road capacity in vehicles per hour
- `construction_cost`: Construction cost in million EGP

**Returns:**
- The tuple representing the added connection

###### get_component_for_node

```python
def get_component_for_node(self, node_id, nx_graph=None)
```

Gets the connected component containing a specific node.

**Parameters:**
- `node_id`: ID of the node
- `nx_graph`: Optional pre-built NetworkX graph

**Returns:**
- Set of node IDs in the same connected component

###### get_connected_components

```python
def get_connected_components(self)
```

Gets all connected components in the network.

**Returns:**
- List of sets, where each set contains node IDs in the same component

### Usage Examples

```python
# Create a transportation graph
graph = CairoTransportationGraph()

# After loading data, build a NetworkX graph for algorithms
nx_graph = graph.build_networkx_graph()

# Check for isolated facilities
isolated = graph.identify_isolated_facilities()
print(f"Found {len(isolated)} isolated facilities")

# Verify and repair connectivity
connectivity = graph.verify_and_repair_connectivity()
print(f"Network has {connectivity['component_count']} connected components")

# Add a potential connection between nodes
graph.add_potential_connection("1", "15", distance=5.2, capacity=3000, construction_cost=28)
```

### Implementation Details

The CairoTransportationGraph class is implemented as a wrapper around several internal data structures:

- Dictionary-based storage for nodes and their attributes
- List-based storage for roads (as tuples)
- Dictionary-based storage for traffic data with road tuples as keys
- Lists for public transportation routes

The class provides methods to convert these internal structures into a NetworkX graph for algorithmic operations like pathfinding, connectivity analysis, and optimization.
