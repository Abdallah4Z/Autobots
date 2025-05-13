# Visualization Module Documentation

The visualization module provides functions to generate visual representations of the transportation network.

## File: `backend/src/app/utils/visualization.py`

This module contains functions for creating network visualizations as images.

### Functions

#### get_graph_image_base64

```python
def get_graph_image_base64(graph, include_potential=False, width=1200, height=900, 
                         highlight_path=None, highlight_congestion=False)
```

Generates a visualization of the transportation network as a base64-encoded image.

**Parameters:**
- `graph`: The transportation graph object
- `include_potential`: Whether to include potential (not yet built) roads
- `width`: Image width in pixels
- `height`: Image height in pixels
- `highlight_path`: Optional list of node IDs to highlight as a path
- `highlight_congestion`: Whether to color roads based on congestion levels

**Returns:**
- Base64 encoded PNG image as a string with data URI prefix

#### _create_networkx_graph

```python
def _create_networkx_graph(graph, include_potential=False)
```

Creates a NetworkX graph from the transportation graph for visualization.

**Parameters:**
- `graph`: The transportation graph object
- `include_potential`: Whether to include potential roads

**Returns:**
- A NetworkX graph object for visualization

#### _calculate_node_sizes

```python
def _calculate_node_sizes(G)
```

Calculates appropriate node sizes for visualization based on population or importance.

**Parameters:**
- `G`: NetworkX graph with node attributes

**Returns:**
- Dictionary mapping node IDs to size values

#### _calculate_edge_colors

```python
def _calculate_edge_colors(G, highlight_congestion=False)
```

Determines edge colors based on road type or congestion.

**Parameters:**
- `G`: NetworkX graph with edge attributes
- `highlight_congestion`: Whether to color based on congestion

**Returns:**
- Dictionary mapping edge IDs to color values

#### _calculate_node_colors

```python
def _calculate_node_colors(G)
```

Determines node colors based on node type.

**Parameters:**
- `G`: NetworkX graph with node attributes

**Returns:**
- Dictionary mapping node IDs to color values

#### _draw_graph_with_matplotlib

```python
def _draw_graph_with_matplotlib(G, node_sizes, node_colors, edge_colors, 
                              width, height, highlight_path=None)
```

Renders the graph using Matplotlib.

**Parameters:**
- `G`: NetworkX graph to visualize
- `node_sizes`: Dictionary of node sizes
- `node_colors`: Dictionary of node colors
- `edge_colors`: Dictionary of edge colors
- `width`: Image width in pixels
- `height`: Image height in pixels
- `highlight_path`: Optional list of node IDs to highlight as a path

**Returns:**
- Matplotlib figure containing the rendered graph

#### _figure_to_base64

```python
def _figure_to_base64(fig)
```

Converts a Matplotlib figure to a base64 encoded string.

**Parameters:**
- `fig`: Matplotlib figure

**Returns:**
- Base64 encoded PNG image as a string with data URI prefix

### Usage Examples

```python
# Generate a basic visualization of the transportation network
image_base64 = get_graph_image_base64(graph)

# Generate a visualization including potential roads with congestion highlighting
image_base64 = get_graph_image_base64(
    graph,
    include_potential=True,
    highlight_congestion=True
)

# Generate a visualization with a highlighted path
path = ["1", "5", "10", "15"]
image_base64 = get_graph_image_base64(
    graph,
    highlight_path=path
)
```

### Implementation Details

The visualization uses a multi-step process:

1. Convert the transportation graph to a NetworkX graph
2. Calculate visual attributes (sizes, colors) based on data
3. Render the graph using NetworkX and Matplotlib
4. Convert the resulting image to base64 for web display

The module uses color schemes to differentiate:
- Node types (residential, commercial, industrial, facilities)
- Road types (existing, potential)
- Congestion levels (from green for low to red for high)

Path highlighting is implemented by drawing wider, brightly colored edges along the specified path.
