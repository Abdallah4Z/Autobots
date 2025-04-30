from flask import Flask
from flask_cors import CORS
import os

# Import our modules
from .models.graph import CairoTransportationGraph
from .utils.data_loader import load_data_from_csv
from .api.routes import register_routes

# Create an instance of the graph
cairo_graph = CairoTransportationGraph()

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define a function to initialize the application
def initialize_app():
    # Determine the data directory path relative to this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))), 'data')
    
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

# Create and initialize the application
app = initialize_app()

if __name__ == '__main__':
    # Start the Flask server
    app.run(debug=True, port=5000)