from flask import Flask
from flask_cors import CORS
from app.api.infrastructure_routes import planner_bp
from app.api.flow_optimization_routes import flow_bp
from app.api.transportation_routes import transportation_bp
from app.api.emergency_routes import emergency_bp
def create_app():
    app = Flask(__name__)
    CORS(app)  # Enables CORS for all routes    # Register infrastructure-related routes
    app.register_blueprint(planner_bp, url_prefix="/planner")

    # Register flow optimization routes
    app.register_blueprint(flow_bp, url_prefix="/flow")

    # Register transportation routes
    app.register_blueprint(transportation_bp, url_prefix="/transportation")

    # Register emergency response routes
    app.register_blueprint(emergency_bp, url_prefix="/emergency")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)