"""
API routes for TTS Service
"""
from flask import Blueprint, request, jsonify, send_file
from src.services.tts_service import TTSService
from config.settings import Config
import os

api_bp = Blueprint('api', __name__)
tts_service = TTSService()

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": Config.SERVICE_NAME,
        "version": Config.VERSION
    }), 200

@api_bp.route('/synthesize', methods=['POST'])
def synthesize():
    """
    Convert text to speech
    
    Request JSON:
        {
            "text": "Turn left at the next intersection",
            "language": "en",  # optional
            "speed": 1.0       # optional
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                "success": False,
                "error": "Missing required field: text"
            }), 400
            
        text = data['text']
        language = data.get('language', Config.DEFAULT_LANGUAGE)
        speed = data.get('speed', Config.DEFAULT_SPEED)
        
        # Synthesize speech
        result = tts_service.synthesize(text, language, speed)
        
        # Build response
        response = {
            "success": True,
            "audio_url": f"/api/tts/audio/{result['filename']}",
            "filename": result['filename'],
            "language": result['language'],
            "text_length": result['text_length'],
            "file_size": result['file_size'],
            "created_at": result['created_at']
        }
        
        return jsonify(response), 201
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except RuntimeError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500

@api_bp.route('/audio/<filename>', methods=['GET'])
def get_audio(filename):
    """
    Retrieve generated audio file
    """
    try:
        filepath = tts_service.get_audio_path(filename)
        
        if not os.path.exists(filepath):
            return jsonify({
                "success": False,
                "error": "Audio file not found"
            }), 404
            
        return send_file(filepath, mimetype='audio/mpeg')
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Failed to retrieve audio file"
        }), 500

@api_bp.route('/languages', methods=['GET'])
def get_languages():
    """Get list of supported languages"""
    return jsonify({
        "success": True,
        "languages": Config.ALLOWED_LANGUAGES,
        "default": Config.DEFAULT_LANGUAGE
    }), 200

@api_bp.route('/cleanup', methods=['POST'])
def cleanup():
    """Clean up old audio files"""
    try:
        data = request.get_json() or {}
        max_age_hours = data.get('max_age_hours', 24)
        
        deleted_count = tts_service.cleanup_old_files(max_age_hours)
        
        return jsonify({
            "success": True,
            "deleted_count": deleted_count,
            "max_age_hours": max_age_hours
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Cleanup failed"
        }), 500
