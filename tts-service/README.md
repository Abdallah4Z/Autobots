# TTS Service

Text-to-Speech microservice for the Autobots Transportation Network Analysis System.

## Overview

The TTS Service provides text-to-speech capabilities for the Autobots system, enabling audio navigation announcements, alerts, and accessibility features.

## Features

- Convert text to speech audio
- Support for multiple languages
- Configurable voice parameters (speed, pitch, volume)
- RESTful API endpoints
- Integration-ready with the main Autobots application

## Prerequisites

- Python 3.7+
- Flask
- gTTS (Google Text-to-Speech) or pyttsx3

## Installation

```bash
cd tts-service
pip install -r requirements.txt
```

## Running the Service

```bash
python src/app.py
```

The service will start on `http://localhost:5001` by default.

## API Endpoints

### POST /api/tts/synthesize
Convert text to speech.

**Request Body:**
```json
{
  "text": "Turn left at the next intersection",
  "language": "en",
  "speed": 1.0
}
```

**Response:**
```json
{
  "success": true,
  "audio_url": "/api/tts/audio/abc123.mp3",
  "duration": 2.5
}
```

### GET /api/tts/health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "tts-service",
  "version": "1.0.0"
}
```

## Configuration

Edit `config/settings.py` to customize:
- Port number
- Audio output directory
- Default language
- Voice parameters

## Integration with Autobots

The TTS service can be integrated with the main Autobots application to provide:
- Turn-by-turn navigation announcements
- Traffic alert notifications
- Emergency vehicle routing instructions
- Public transport announcements

## License

See the main project LICENSE file.
