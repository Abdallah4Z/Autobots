from flask import Flask
from flask_cors import CORS
import os
import sys

# Add the src directory to the Python path for proper imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.insert(0, src_dir)

# Import our modules - use absolute imports when run directly, fallback to relative imports when imported
if __name__ == '__main__':
    from models.graph import CairoTransportationGraph
    from utils.data_loader import load_data_from_csv
    from api.routes import register_routes
else:
    from app.models.graph import CairoTransportationGraph
    from app.utils.data_loader import load_data_from_csv
    from app.api.routes import register_routes

# Create an instance of the graph
cairo_graph = CairoTransportationGraph()

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define a function to initialize the application
def initialize_app():
    # Correct path to the data directory - explicitly use the backend/data folder
    project_dir_parts = current_dir.split('\\')
    # Find the 'Project' directory in the path
    project_idx = project_dir_parts.index('Project')
    # Build path to the backend/data directory
    data_dir = '\\'.join(project_dir_parts[:project_idx+1]) + '\\backend\\data'
    
    print(f"Looking for data files in: {data_dir}")
    
    # Load data from CSV files
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
    
    # Register API routes
    register_routes(app, cairo_graph)
    
    return app

# Create and initialize the application when running directly
if __name__ == '__main__':
    app = initialize_app()
    # Start the Flask server
    app.run(debug=True, port=5000)
else:
    # When imported as a module, just initialize without running
    app = initialize_app()