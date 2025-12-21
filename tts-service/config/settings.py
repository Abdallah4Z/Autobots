"""
Configuration settings for TTS Service
"""
import os

class Config:
    """Base configuration"""
    # Service settings
    SERVICE_NAME = "tts-service"
    VERSION = "1.0.0"
    PORT = int(os.environ.get("TTS_PORT", 5001))
    HOST = os.environ.get("TTS_HOST", "0.0.0.0")
    DEBUG = os.environ.get("TTS_DEBUG", "False").lower() == "true"
    
    # Audio settings
    AUDIO_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "audio_output")
    DEFAULT_LANGUAGE = "en"
    DEFAULT_SPEED = 1.0
    DEFAULT_PITCH = 1.0
    
    # API settings
    MAX_TEXT_LENGTH = 5000
    ALLOWED_LANGUAGES = ["en", "es", "fr", "de", "it", "ar", "zh", "ja"]
    
    # CORS settings
    CORS_ORIGINS = "*"
    
    @staticmethod
    def init_app(app):
        """Initialize application with config"""
        # Create audio output directory if it doesn't exist
        os.makedirs(Config.AUDIO_OUTPUT_DIR, exist_ok=True)
