# Application Module Documentation

The app module serves as the entry point for the Flask application, initializing all components and connecting them together.

## File: `backend/src/app/app.py`

This module contains the Flask application initialization and setup code.

### Main Application Object

```python
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
```

The main Flask application object with CORS (Cross-Origin Resource Sharing) enabled.

### Functions

#### initialize_app

```python
def initialize_app()
```

Initializes the Flask application by:
1. Locating the correct data directory
2. Loading data from CSV files
3. Building the transportation graph
4. Connecting isolated facilities to the transportation network
5. Verifying and repairing network connectivity
6. Registering API routes

**Returns:**
- The initialized Flask application

### Path Resolution Logic

The module contains logic to correctly resolve paths to data files regardless of the application's execution context:

```python
# Find the 'Project' directory in the path
project_idx = project_dir_parts.index('Project')
# Build path to the backend/data directory
data_dir = '\\'.join(project_dir_parts[:project_idx+1]) + '\\backend\\data'
```

### Data Loading

The module loads data from CSV files into the transportation graph:

```python
load_data_from_csv(
    cairo_graph,
    neighborhoods_file=os.path.join(data_dir, "Neighborhoods and Districts.csv"), 
    facilities_file=os.path.join(data_dir, "Important Facilities.csv"),
    existing_roads_file=os.path.join(data_dir, "Existing Roads.csv"),
    potential_roads_file=os.path.join(data_dir, "Potential New Roads.csv"),
    traffic_file=os.path.join(data_dir, "Traffic Flow Patterns.csv"),
    metro_file=os.path.join(data_dir, "Current Metro Lines.csv"),
    bus_file=os.path.join(data_dir, "Current Bus Routes.csv"),
    demand_file=os.path.join(data_dir, "Public Transportation Demand.csv")
)
```

### Network Connectivity

The module verifies and repairs network connectivity:

```python
# Simply diagnose disconnected components without forcing connections
print("Connecting isolated facilities to the transportation network...")
cairo_graph.identify_isolated_facilities()

# Verify connectivity and report on disconnected components
cairo_graph.verify_and_repair_connectivity()
```

### Application Execution

The module contains conditional execution logic for both direct running and importing:

```python
# Create and initialize the application when running directly
if __name__ == '__main__':
    app = initialize_app()
    # Start the Flask server
    app.run(debug=True, port=5000)
else:
    # When imported as a module, just initialize without running
    app = initialize_app()
```

## Import Structure

The module uses conditional import paths to work both when run directly and when imported:

```python
# Import our modules - use absolute imports when run directly, fallback to relative imports when imported
if __name__ == '__main__':
    from models.graph import CairoTransportationGraph
    from utils.data_loader import load_data_from_csv
    from api.routes import register_routes
else:
    from app.models.graph import CairoTransportationGraph
    from app.utils.data_loader import load_data_from_csv
    from app.api.routes import register_routes
```

## Usage

This module is typically used in one of two ways:

1. Run directly to start the Flask development server:
   ```
   python backend/src/app/app.py
   ```

2. Imported by a WSGI server (like Gunicorn):
   ```python
   from backend.src.app.app import app
   # app is now the initialized Flask application
   ```
