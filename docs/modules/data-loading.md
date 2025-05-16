# Data Loading Module Documentation

The data loading module provides functionality to load transportation network data from CSV files.

## File: `backend/src/app/utils/data_loader.py`

### Main Function

```python
def load_data_from_csv(graph, neighborhoods_file, facilities_file, existing_roads_file, 
                     potential_roads_file, traffic_file, metro_file, bus_file, demand_file)
```

Loads all transportation network data from CSV files into the provided graph object.

**Parameters:**

- `graph`: The graph object to populate (CairoTransportationGraph instance)
- `neighborhoods_file`: Path to the neighborhoods CSV file
- `facilities_file`: Path to important facilities CSV file
- `existing_roads_file`: Path to existing roads CSV file
- `potential_roads_file`: Path to potential new roads CSV file
- `traffic_file`: Path to traffic flow patterns CSV file
- `metro_file`: Path to current metro lines CSV file
- `bus_file`: Path to current bus routes CSV file
- `demand_file`: Path to public transportation demand CSV file

### Loading Process Details

The function handles:

1. **Flexible Column Name Detection**: Uses variant column name mapping to handle different CSV formats
2. **Data Type Conversion**: Ensures consistent data types (e.g., converts string IDs to integers)
3. **Node and Edge Population**: Populates graph.nodes, graph.existing_roads, and graph.potential_roads
4. **Special Format Handling**: Handles complex formats like RoadID strings with tuples
5. **Traffic Data Processing**: Maps traffic data to road segments for different times of day
6. **Public Transport Integration**: Loads metro lines and bus routes with their stops
7. **Transport Demand Loading**: Maps origin-destination demand for public transport

### CSV File Format Flexibility

The function is built to handle variations in CSV column names:

```python
# Example column name variations for existing roads
from_id_variants = ['FromID', 'From ID', 'From_ID', 'Source', 'Source ID']
to_id_variants = ['ToID', 'To ID', 'To_ID', 'Target', 'Target ID']
distance_variants = ['Distance (km)', 'Distance(km)', 'Distance_km', 'Length (km)']
```

### Error Handling

The function includes comprehensive error handling:

1. Logs warnings for nodes referenced but not found
2. Handles missing files and columns gracefully
3. Uses try-except blocks to prevent crashes on malformed data

### Usage Example

```python
# Create an instance of the transportation graph
graph = CairoTransportationGraph()

# Load data from CSV files
load_data_from_csv(
    graph,
    neighborhoods_file="data/Neighborhoods and Districts.csv",
    facilities_file="data/Important Facilities.csv",
    existing_roads_file="data/Existing Roads.csv",
    potential_roads_file="data/Potential New Roads.csv",
    traffic_file="data/Traffic Flow Patterns.csv",
    metro_file="data/Current Metro Lines.csv",
    bus_file="data/Current Bus Routes.csv",
    demand_file="data/Public Transportation Demand.csv"
)
```
