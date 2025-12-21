"""
Text-to-Speech service implementation
"""
import os
import uuid
from datetime import datetime
from gtts import gTTS
from config.settings import Config

class TTSService:
    """Text-to-Speech service using Google TTS"""
    
    def __init__(self):
        self.output_dir = Config.AUDIO_OUTPUT_DIR
        
    def synthesize(self, text, language=None, speed=None):
        """
        Convert text to speech and save as audio file
        
        Args:
            text (str): Text to convert to speech
            language (str): Language code (default: en)
            speed (float): Speech speed multiplier (default: 1.0)
            
        Returns:
            dict: Result with audio file info
        """
        if not text or len(text) > Config.MAX_TEXT_LENGTH:
            raise ValueError(f"Text must be between 1 and {Config.MAX_TEXT_LENGTH} characters")
            
        if language is None:
            language = Config.DEFAULT_LANGUAGE
            
        if language not in Config.ALLOWED_LANGUAGES:
            raise ValueError(f"Language must be one of: {Config.ALLOWED_LANGUAGES}")
            
        if speed is None:
            speed = Config.DEFAULT_SPEED
            
        # Generate unique filename
        filename = f"{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(self.output_dir, filename)
        
        # Convert text to speech
        try:
            tts = gTTS(text=text, lang=language, slow=(speed < 0.9))
            tts.save(filepath)
            
            # Get file size
            file_size = os.path.getsize(filepath)
            
            return {
                "success": True,
                "filename": filename,
                "filepath": filepath,
                "file_size": file_size,
                "language": language,
                "text_length": len(text),
                "created_at": datetime.utcnow().isoformat()
            }
        except Exception as e:
            raise RuntimeError(f"Failed to synthesize speech: {str(e)}")
    
    def get_audio_path(self, filename):
        """Get full path to audio file"""
        return os.path.join(self.output_dir, filename)
    
    def cleanup_old_files(self, max_age_hours=24):
        """Clean up audio files older than max_age_hours"""
        if not os.path.exists(self.output_dir):
            return 0
            
        now = datetime.utcnow()
        deleted_count = 0
        
        for filename in os.listdir(self.output_dir):
            filepath = os.path.join(self.output_dir, filename)
            if os.path.isfile(filepath):
                file_modified = datetime.utcfromtimestamp(os.path.getmtime(filepath))
                file_age = now - file_modified
                if file_age.total_seconds() > max_age_hours * 3600:
                    try:
                        os.remove(filepath)
                        deleted_count += 1
                    except OSError:
                        pass
                        
        return deleted_count
