"""
TTS Service initialization
"""
from flask import Flask
from flask_cors import CORS
from config.settings import Config

def create_app(config_class=Config):
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize CORS
    CORS(app, resources={r"/api/*": {"origins": config_class.CORS_ORIGINS}})
    
    # Initialize config
    config_class.init_app(app)
    
    # Register blueprints
    from src.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/tts')
    
    return app
