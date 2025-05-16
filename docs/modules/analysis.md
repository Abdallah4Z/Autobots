# Analysis Module Documentation

The analysis module provides functions for analyzing traffic patterns, congestion, and public transportation efficiency.

## File: `backend/src/app/services/analysis.py`

This module contains analysis functions that examine the transportation network data and provide insights.

### Functions

#### analyze_traffic_congestion

```python
def analyze_traffic_congestion(graph, time_of_day='morning')
```

Analyzes traffic congestion patterns across the transportation network.

**Parameters:**
- `graph`: The transportation graph object
- `time_of_day`: Time period to analyze ('morning', 'afternoon', 'evening', 'night')

**Returns:**
- Dictionary with congestion analysis:
  - `congestion_by_road`: Dictionary mapping road IDs to congestion values
  - `highest_congestion_roads`: List of roads with highest congestion
  - `congestion_histogram`: Distribution of congestion values
  - `average_congestion`: Average congestion value
  - `time_period`: Analyzed time period
  - `congestion_hotspots`: Locations with multiple congested roads

#### suggest_public_transport_improvements

```python
def suggest_public_transport_improvements(graph)
```

Analyzes the transportation network and suggests improvements to public transportation.

**Parameters:**
- `graph`: The transportation graph object

**Returns:**
- List of improvement suggestion dictionaries:
  - New bus routes
  - Metro line extensions
  - Frequency improvements
  - New transportation hubs
  - Each with priority, cost, and expected benefits

#### get_network_statistics

```python
def get_network_statistics(graph)
```

Computes comprehensive statistics about the transportation network.

**Parameters:**
- `graph`: The transportation graph object

**Returns:**
- Dictionary with network statistics:
  - `node_count`: Total number of nodes
  - `edge_count`: Total number of road connections
  - `total_road_length_km`: Total road network length
  - `average_congestion`: Average congestion across the network
  - `connected_components`: Number of disconnected graph components
  - `metro_stations`: Number of metro stations
  - `bus_stops`: Number of bus stops
  - `population_covered`: Total population with access to transportation
  - `road_condition_average`: Average road condition score
  - `potential_road_count`: Number of potential new roads
  - `potential_road_length_km`: Total length of potential roads
  - `potential_construction_cost`: Total cost to build all potential roads

#### analyze_transportation_demand

```python
def analyze_transportation_demand(graph)
```

Analyzes transportation demand patterns to identify underserved areas.

**Parameters:**
- `graph`: The transportation graph object

**Returns:**
- Dictionary with demand analysis:
  - `high_demand_pairs`: Origin-destination pairs with high demand
  - `underserved_demand`: High demand pairs with poor service
  - `demand_by_district`: Demand aggregated by district
  - `recommendation_areas`: Areas recommended for service improvements

#### compute_accessibility_metrics

```python
def compute_accessibility_metrics(graph)
```

Computes accessibility metrics for different areas and facilities.

**Parameters:**
- `graph`: The transportation graph object

**Returns:**
- Dictionary with accessibility metrics:
  - `facility_accessibility`: Accessibility scores for facilities
  - `district_accessibility`: Accessibility scores for districts
  - `accessibility_by_mode`: Breakdown by transportation mode
  - `areas_low_accessibility`: Areas with poor transportation access
  - `potential_improvement_impact`: Impact of potential roads on accessibility

### Implementation Details

#### Traffic Congestion Analysis

The `analyze_traffic_congestion` function:

1. Builds a NetworkX graph from the transportation data
2. Calculates congestion ratio (flow/capacity) for each road
3. Identifies roads with congestion above threshold values
4. Creates a histogram of congestion values
5. Identifies geographic clusters of high congestion (hotspots)

#### Public Transport Improvement Suggestions

The `suggest_public_transport_improvements` function:

1. Analyzes current public transportation coverage
2. Identifies high-demand corridors not well-served
3. Evaluates potential for new routes or increased frequency
4. Prioritizes suggestions based on population served and demand
5. Estimates costs and benefits of each suggestion

#### Network Statistics Computation

The `get_network_statistics` function:

1. Computes basic graph metrics (nodes, edges)
2. Calculates transportation-specific metrics (road length, congestion)
3. Analyzes connectivity and accessibility
4. Provides summary statistics about public transportation
5. Includes information about potential future developments

### Usage Examples

```python
# Analyze morning traffic congestion
congestion_data = analyze_traffic_congestion(graph, time_of_day='morning')
print(f"Average congestion: {congestion_data['average_congestion']}")
print(f"Found {len(congestion_data['congestion_hotspots'])} congestion hotspots")

# Get suggestions for public transportation improvements
suggestions = suggest_public_transport_improvements(graph)
high_priority = [s for s in suggestions if s['priority'] == 'high']
print(f"Found {len(high_priority)} high-priority improvement suggestions")

# Get comprehensive network statistics
stats = get_network_statistics(graph)
print(f"Network has {stats['node_count']} nodes and {stats['edge_count']} connections")
print(f"Total road length: {stats['total_road_length_km']} km")
```
