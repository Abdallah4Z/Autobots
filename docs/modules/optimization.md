# Optimization Module Documentation

The optimization module provides algorithms for optimizing different aspects of the transportation network.

## File: `backend/src/app/services/optimization.py`

This module contains optimization algorithms using techniques like dynamic programming, minimum spanning trees, and other advanced algorithms.

### Functions

#### optimize_road_network_with_mst

```python
def optimize_road_network_with_mst(graph, prioritize_population=False, include_existing=True)
```

Uses Minimum Spanning Tree (MST) algorithm to find an optimal road network.

**Parameters:**
- `graph`: The transportation graph object
- `prioritize_population`: Whether to weight edges by population served
- `include_existing`: Whether to include existing roads in the optimization

**Returns:**
- Dictionary with optimization results:
  - `optimized_roads`: List of road segments in the optimized network
  - `total_cost`: Total construction cost
  - `total_distance`: Total road network length
  - `population_covered`: Total population covered by the network
  - `connectivity_improvement`: Measure of connectivity improvement

#### optimize_bus_routes_dp

```python
def optimize_bus_routes_dp(graph, target_coverage=0.8, max_buses=100)
```

Uses dynamic programming to optimize bus route allocation.

**Parameters:**
- `graph`: The transportation graph object
- `target_coverage`: Target population coverage (0.0-1.0)
- `max_buses`: Maximum number of buses available

**Returns:**
- Dictionary with optimization results:
  - `optimized_routes`: List of optimized bus routes
  - `total_buses`: Total buses assigned
  - `population_coverage`: Achieved population coverage
  - `estimated_total_ridership`: Estimated daily ridership

#### optimize_metro_schedule_dp

```python
def optimize_metro_schedule_dp(graph, peak_hours=['morning', 'evening'], 
                             off_peak_hours=['afternoon', 'night'])
```

Uses dynamic programming to optimize metro schedules.

**Parameters:**
- `graph`: The transportation graph object
- `peak_hours`: List of peak hours periods
- `off_peak_hours`: List of off-peak hours periods

**Returns:**
- List of optimized schedule dictionaries:
  - `line_id`: Metro line ID
  - `peak_headway_minutes`: Time between trains during peak hours
  - `off_peak_headway_minutes`: Time between trains during off-peak hours
  - `trains_required`: Number of trains required
  - `daily_capacity`: Daily passenger capacity

#### optimize_multimodal_connectivity

```python
def optimize_multimodal_connectivity(graph, budget_constraint=None)
```

Optimizes connectivity between different transportation modes.

**Parameters:**
- `graph`: The transportation graph object
- `budget_constraint`: Maximum budget for new connections

**Returns:**
- Dictionary with optimization results:
  - `new_connections`: List of new connections to improve intermodal transfer
  - `total_cost`: Total implementation cost
  - `transfer_time_reduction`: Average reduction in transfer time
  - `accessibility_improvement`: Measure of accessibility improvement

#### optimize_road_repairs

```python
def optimize_road_repairs(graph, budget_constraint=None, prioritize_traffic=True)
```

Optimizes road repair prioritization based on condition and usage.

**Parameters:**
- `graph`: The transportation graph object
- `budget_constraint`: Maximum budget for repairs
- `prioritize_traffic`: Whether to prioritize high-traffic roads

**Returns:**
- Dictionary with optimization results:
  - `repair_priority`: List of roads to repair in priority order
  - `total_cost`: Total repair cost
  - `traffic_flow_improvement`: Estimated traffic flow improvement
  - `road_condition_improvement`: Overall condition improvement

### Implementation Details

#### Minimum Spanning Tree for Road Network

The `optimize_road_network_with_mst` function:

1. Creates a complete graph where all nodes can potentially connect
2. Assigns edge weights based on distance and optionally population
3. Applies Kruskal's or Prim's algorithm to find the MST
4. Filters the result based on budget constraints
5. Combines with existing roads if specified

```python
# Example of MST algorithm application
G = nx.Graph()
for node_id, node_data in graph.nodes.items():
    G.add_node(node_id, **node_data)
    
# Add edges with appropriate weights
for i, node1 in enumerate(graph.nodes):
    for node2 in graph.nodes:
        if node1 != node2:
            distance = graph.calculate_haversine_distance(node1, node2)
            weight = distance
            if prioritize_population:
                pop1 = graph.nodes[node1].get('population', 0)
                pop2 = graph.nodes[node2].get('population', 0)
                weight = distance / (pop1 + pop2 + 1)  # Add 1 to avoid division by zero
            G.add_edge(node1, node2, weight=weight, distance=distance)

# Find MST
mst = nx.minimum_spanning_tree(G, weight='weight')
```

#### Dynamic Programming for Bus Route Optimization

The `optimize_bus_routes_dp` function:

1. Evaluates each potential bus route for cost-benefit ratio
2. Uses dynamic programming to maximize coverage within constraints
3. Creates a 2D table indexed by [routes_used][buses_available]
4. Reconstructs the optimal solution from the table
5. Provides allocation of buses to routes

#### Metro Schedule Optimization

The `optimize_metro_schedule_dp` function:

1. Analyzes passenger demand by time period
2. Estimates required frequency based on demand
3. Optimizes train allocation to minimize wait times
4. Accounts for physical constraints (number of trains, minimum headway)
5. Balances service level and operational costs

### Usage Examples

```python
# Optimize road network prioritizing population centers
road_optimization = optimize_road_network_with_mst(
    graph, 
    prioritize_population=True, 
    include_existing=True
)

# Optimize bus routes with 120 buses targeting 85% coverage
bus_optimization = optimize_bus_routes_dp(
    graph,
    target_coverage=0.85,
    max_buses=120
)

# Optimize metro schedules
metro_optimization = optimize_metro_schedule_dp(
    graph,
    peak_hours=['morning', 'evening'],
    off_peak_hours=['afternoon', 'night']
)

# Optimize road repair prioritization
repair_optimization = optimize_road_repairs(
    graph,
    budget_constraint=50,  # 50 million EGP
    prioritize_traffic=True
)
```
