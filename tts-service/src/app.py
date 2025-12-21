"""
Main application entry point for TTS Service
"""
from src import create_app
from config.settings import Config

app = create_app()

if __name__ == '__main__':
    print(f"Starting {Config.SERVICE_NAME} v{Config.VERSION}")
    print(f"Server running on http://{Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
