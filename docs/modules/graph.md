# Graph Module Documentation

The graph module provides the core transportation network modeling functionality.

## TransportationNetwork Class

`TransportationNetwork` is the central class for modeling transportation networks, including roads, public transit, and traffic patterns.

### File: `backend/src/app/graph/networks.py`

```python
class TransportationNetwork:
    """
    Blueprint for both public-transport connectivity and road networks,
    loading data from JSON files in a given folder.
    """
```

### Constructor

```python
def __init__(
    self,
    neighbourhoods: Dict[str, dict],
    facilities: Dict[str, dict],
    bus_routes: List[Dict],
    metro_lines: List[Dict],
    roads: List[Dict],
    flow: Dict[Tuple[str,str], Dict[str,int]],
)
```

Initializes a transportation network with all components:
- `neighbourhoods`: Dictionary mapping ID to neighborhood attributes
- `facilities`: Dictionary mapping ID to facility attributes
- `bus_routes`: List of bus route dictionaries
- `metro_lines`: List of metro line dictionaries
- `roads`: List of road dictionaries with connectivity and attributes
- `flow`: Dictionary mapping road segments to traffic flow values

### Class Methods

#### `from_json_folder`

```python
@classmethod
def from_json_folder(cls, data_dir: str) -> TransportationNetwork
```

Creates a TransportationNetwork instance by loading data from JSON files in the specified directory.

**Parameters:**
- `data_dir`: Path to the directory containing JSON data files

**Returns:**
- A TransportationNetwork instance populated with the loaded data

#### `_symmetrise_flow`

```python
@staticmethod
def _symmetrise_flow(raw: Dict[Tuple[str,str], dict]) -> Dict[Tuple[str,str], dict]
```

Makes traffic flow data symmetric, copying flow data from (u,v) to (v,u).

**Parameters:**
- `raw`: Raw traffic flow data

**Returns:**
- Symmetrized traffic flow data

### Properties

#### `nodes`

```python
@property
def nodes(self) -> Dict[str, dict]
```

Returns a merged dictionary of all nodes (neighbourhoods and facilities) in the network.

### Network Building Methods

#### `build_public_transport_network`

```python
def build_public_transport_network(self) -> nx.DiGraph
```

Builds a directed graph representing the public transportation network.

**Returns:**
- A NetworkX DiGraph with nodes for locations and edges for transit connections

#### `build_road_network`

```python
def build_road_network(self, period: str = 'morning') -> nx.Graph
```

Builds an undirected graph representing the road network for a specific time period.

**Parameters:**
- `period`: Time period ('morning', 'afternoon', 'evening', 'night')

**Returns:**
- A NetworkX Graph with road connections and traffic data

#### `build_combined_road_network`

```python
def build_combined_road_network(self, period: str = 'morning') -> nx.Graph
```

Builds a road network graph that includes both existing and potential roads.

**Parameters:**
- `period`: Time period ('morning', 'afternoon', 'evening', 'night')

**Returns:**
- A NetworkX Graph with existing and potential road connections

## Usage Examples

```python
# Load transportation network from JSON files
tn = TransportationNetwork.from_json_folder('data')

# Create different network views
public_transport_graph = tn.build_public_transport_network()
morning_road_graph = tn.build_road_network(period='morning')
combined_graph = tn.build_combined_road_network(period='evening')
```
