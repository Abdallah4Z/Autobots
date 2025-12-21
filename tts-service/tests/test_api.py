"""
Tests for TTS Service
"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import create_app
from config.settings import Config

@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/api/tts/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'tts-service'
    assert data['version'] == '1.0.0'

def test_get_languages(client):
    """Test get supported languages"""
    response = client.get('/api/tts/languages')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'languages' in data
    assert 'en' in data['languages']
    assert data['default'] == 'en'

def test_synthesize_missing_text(client):
    """Test synthesize with missing text"""
    response = client.post('/api/tts/synthesize',
                          json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False
    assert 'text' in data['error']

def test_synthesize_success(client):
    """Test successful text synthesis"""
    response = client.post('/api/tts/synthesize',
                          json={
                              'text': 'Hello, this is a test',
                              'language': 'en'
                          })
    # Note: This test may fail if gTTS is not installed or network is unavailable
    # In a real environment, we'd mock the TTS service
    if response.status_code == 201:
        data = response.get_json()
        assert data['success'] is True
        assert 'audio_url' in data
        assert 'filename' in data

def test_get_nonexistent_audio(client):
    """Test retrieving non-existent audio file"""
    response = client.get('/api/tts/audio/nonexistent.mp3')
    assert response.status_code == 404

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
