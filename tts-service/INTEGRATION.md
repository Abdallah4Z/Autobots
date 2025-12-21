# TTS Service Integration Guide

## Overview

This document describes how to integrate the TTS (Text-to-Speech) service with the Autobots Transportation Network Analysis System.

## Architecture

```
┌─────────────────────┐
│   Frontend (React)  │
│   Port: 5173        │
└──────────┬──────────┘
           │
           │ HTTP Requests
           │
┌──────────▼──────────┐      ┌─────────────────────┐
│   Backend (Flask)   │◄─────┤  TTS Service        │
│   Port: 5000        │      │  Port: 5001         │
└─────────────────────┘      └─────────────────────┘
```

## Integration Points

### 1. Navigation Announcements

**Use Case**: Provide audio turn-by-turn directions to users.

**Example Integration** (Backend - Python):

```python
import requests

def get_navigation_audio(instruction):
    """Convert navigation instruction to audio"""
    tts_url = "http://localhost:5001/api/tts/synthesize"
    
    payload = {
        "text": instruction,
        "language": "en",
        "speed": 1.0
    }
    
    response = requests.post(tts_url, json=payload)
    
    if response.status_code == 201:
        result = response.json()
        return result['audio_url']
    else:
        return None

# Usage
instruction = "Turn left at the next intersection in 500 meters"
audio_url = get_navigation_audio(instruction)
```

**Example Integration** (Frontend - JavaScript/TypeScript):

```typescript
async function synthesizeSpeech(text: string, language: string = 'en') {
  const response = await fetch('http://localhost:5001/api/tts/synthesize', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      text,
      language,
      speed: 1.0
    })
  });
  
  if (response.ok) {
    const data = await response.json();
    return data.audio_url;
  }
  
  return null;
}

// Usage
const audioUrl = await synthesizeSpeech('Turn left at the next intersection');
const audio = new Audio(`http://localhost:5001${audioUrl}`);
audio.play();
```

### 2. Traffic Alerts

**Use Case**: Audio notifications for traffic conditions.

**Example**:

```python
def generate_traffic_alert(location, severity, description):
    """Generate audio alert for traffic conditions"""
    if severity == "high":
        text = f"Warning! Heavy traffic detected at {location}. {description}"
    elif severity == "medium":
        text = f"Moderate traffic at {location}. {description}"
    else:
        text = f"Traffic update: {location}. {description}"
    
    return get_navigation_audio(text)
```

### 3. Emergency Vehicle Routing

**Use Case**: Voice instructions for emergency services.

**Example**:

```python
def emergency_routing_audio(route_info):
    """Generate audio for emergency routing"""
    emergency_type = route_info['emergency_type']
    distance = route_info['distance']
    eta = route_info['eta']
    
    text = f"{emergency_type} routing: Proceed {distance} meters. Estimated time: {eta} minutes."
    
    payload = {
        "text": text,
        "language": "en",
        "speed": 1.2  # Faster speech for emergency
    }
    
    response = requests.post("http://localhost:5001/api/tts/synthesize", json=payload)
    return response.json()
```

### 4. Multi-Language Support

**Example** for supporting multiple languages:

```python
# Language mapping based on user preference
LANGUAGE_MAP = {
    'en': 'en',  # English
    'es': 'es',  # Spanish
    'fr': 'fr',  # French
    'ar': 'ar',  # Arabic (for Cairo users)
    'de': 'de',  # German
}

def get_user_language_audio(text, user_language='en'):
    """Generate audio in user's preferred language"""
    language_code = LANGUAGE_MAP.get(user_language, 'en')
    
    payload = {
        "text": text,
        "language": language_code,
        "speed": 1.0
    }
    
    response = requests.post("http://localhost:5001/api/tts/synthesize", json=payload)
    return response.json()
```

## Backend Integration Example

Add TTS support to the existing Autobots backend:

**backend/src/app/services/tts_client.py**:

```python
"""TTS Service Client for Autobots Backend"""
import requests
from typing import Optional, Dict

class TTSClient:
    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url
        self.api_endpoint = f"{base_url}/api/tts"
    
    def synthesize(self, text: str, language: str = "en", speed: float = 1.0) -> Optional[Dict]:
        """Synthesize text to speech"""
        try:
            response = requests.post(
                f"{self.api_endpoint}/synthesize",
                json={
                    "text": text,
                    "language": language,
                    "speed": speed
                },
                timeout=10
            )
            
            if response.status_code == 201:
                return response.json()
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"TTS Service error: {e}")
            return None
    
    def get_audio_url(self, filename: str) -> str:
        """Get full URL for audio file"""
        return f"{self.base_url}/api/tts/audio/{filename}"
    
    def health_check(self) -> bool:
        """Check if TTS service is available"""
        try:
            response = requests.get(f"{self.api_endpoint}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
```

## Frontend Integration Example

**app/src/services/ttsService.ts**:

```typescript
export interface TTSRequest {
  text: string;
  language?: string;
  speed?: number;
}

export interface TTSResponse {
  success: boolean;
  audio_url: string;
  filename: string;
  language: string;
  text_length: number;
  file_size: number;
  created_at: string;
}

class TTSService {
  private baseUrl: string = 'http://localhost:5001/api/tts';
  
  async synthesize(request: TTSRequest): Promise<TTSResponse | null> {
    try {
      const response = await fetch(`${this.baseUrl}/synthesize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: request.text,
          language: request.language || 'en',
          speed: request.speed || 1.0
        })
      });
      
      if (response.ok) {
        return await response.json();
      }
      
      return null;
    } catch (error) {
      console.error('TTS Service error:', error);
      return null;
    }
  }
  
  async playAudio(audioUrl: string): Promise<void> {
    const audio = new Audio(`http://localhost:5001${audioUrl}`);
    await audio.play();
  }
  
  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/health`);
      return response.ok;
    } catch {
      return false;
    }
  }
}

export const ttsService = new TTSService();
```

## React Component Example

```tsx
import React, { useState } from 'react';
import { ttsService } from '../services/ttsService';

export const NavigationWithAudio: React.FC = () => {
  const [isPlaying, setIsPlaying] = useState(false);
  
  const handleSpeak = async (instruction: string) => {
    setIsPlaying(true);
    
    const result = await ttsService.synthesize({
      text: instruction,
      language: 'en',
      speed: 1.0
    });
    
    if (result) {
      await ttsService.playAudio(result.audio_url);
    }
    
    setIsPlaying(false);
  };
  
  return (
    <button 
      onClick={() => handleSpeak('Turn left at the next intersection')}
      disabled={isPlaying}
    >
      🔊 Speak Instruction
    </button>
  );
};
```

## Environment Configuration

### Development

Add to `.env` files:

**Backend (.env)**:
```
TTS_SERVICE_URL=http://localhost:5001
```

**Frontend (.env)**:
```
VITE_TTS_SERVICE_URL=http://localhost:5001
```

### Production

For production deployment, use proper service discovery or load balancer URLs:

```
TTS_SERVICE_URL=https://tts-service.autobots.example.com
```

## Error Handling

Always implement proper error handling:

```python
def safe_tts_synthesize(text, language='en'):
    """Safely synthesize text with fallback"""
    try:
        response = requests.post(
            "http://localhost:5001/api/tts/synthesize",
            json={"text": text, "language": language},
            timeout=10
        )
        
        if response.status_code == 201:
            return response.json()
        else:
            print(f"TTS service error: {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("TTS service is unavailable")
        return None
    except requests.exceptions.Timeout:
        print("TTS service timeout")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

## Performance Considerations

1. **Caching**: Cache frequently used phrases to avoid repeated API calls
2. **Async Processing**: Use async/await patterns to avoid blocking
3. **File Cleanup**: Regularly call the cleanup endpoint to remove old audio files
4. **Rate Limiting**: Implement rate limiting on the client side to avoid overwhelming the service

## Security

1. **CORS**: Configure CORS properly in production
2. **API Keys**: Add API key authentication if needed
3. **Rate Limiting**: Implement rate limiting on the TTS service
4. **Input Validation**: Always validate text input length and content

## Testing Integration

Example test for integration:

```python
def test_tts_integration():
    """Test TTS service integration"""
    # Check if service is available
    health_response = requests.get("http://localhost:5001/api/tts/health")
    assert health_response.status_code == 200
    
    # Test synthesis
    response = requests.post(
        "http://localhost:5001/api/tts/synthesize",
        json={"text": "Test integration", "language": "en"}
    )
    assert response.status_code == 201
    assert response.json()['success'] is True
```

## Deployment

When deploying both services:

1. Start the TTS service first: `docker-compose up tts-service`
2. Configure backend to use TTS service URL
3. Update frontend environment variables
4. Test the integration endpoints

## Monitoring

Monitor TTS service health:

```python
import time

def monitor_tts_service():
    """Monitor TTS service availability"""
    while True:
        try:
            response = requests.get("http://localhost:5001/api/tts/health", timeout=5)
            if response.status_code == 200:
                print("✓ TTS service is healthy")
            else:
                print("✗ TTS service returned non-200 status")
        except:
            print("✗ TTS service is unreachable")
        
        time.sleep(60)  # Check every minute
```

## Support

For integration issues or questions, refer to:
- TTS Service README: `tts-service/README.md`
- TTS Service Quick Start: `tts-service/QUICKSTART.md`
- Main Autobots documentation: `docs/`
