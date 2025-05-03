from flask import Flask
from app.api.infrastructure_routes import planner_bp
from app.api.flow_optimization_routes import flow_bp
from app.api.transportation_routes import transportation_bp  # newly added

def create_app():
    app = Flask(__name__)

    # Register infrastructure-related routes
    app.register_blueprint(planner_bp, url_prefix="/planner")

    # Register flow optimization routes
    app.register_blueprint(flow_bp, url_prefix="/flow")

    # Register transportation route
    app.register_blueprint(transportation_bp, url_prefix="/transport")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
