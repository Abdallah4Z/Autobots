from flask import Flask
from flask_cors import CORS
from app.api.infrastructure_routes import planner_bp
from app.api.flow_optimization_routes import flow_bp
from app.api.transportation_routes import transportation_bp  # newly added
def create_app():
    app = Flask(__name__)
    CORS(app)  # Enables CORS for all routes

    # Register infrastructure-related routes
    app.register_blueprint(planner_bp, url_prefix="/planner")

    # Register flow optimization routes
    app.register_blueprint(flow_bp, url_prefix="/flow")

    app.register_blueprint(transportation_bp, url_prefix="/transportation")  # Register transportation routes

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)