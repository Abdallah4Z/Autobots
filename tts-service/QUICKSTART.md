# TTS Service Quick Start Guide

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- (Optional) Docker and Docker Compose for containerized deployment

## Installation

### Option 1: Local Installation

1. Navigate to the tts-service directory:
```bash
cd tts-service
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the service:
```bash
python src/app.py
```

The service will start on `http://localhost:5001`

### Option 2: Docker Deployment

1. Navigate to the tts-service directory:
```bash
cd tts-service
```

2. Build and run with Docker Compose:
```bash
docker-compose up --build
```

The service will start on `http://localhost:5001`

## Testing the Service

### Using the Example Script

Run the example usage script to test all endpoints:
```bash
python example_usage.py
```

### Using curl

Test the health endpoint:
```bash
curl http://localhost:5001/api/tts/health
```

Synthesize speech:
```bash
curl -X POST http://localhost:5001/api/tts/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, this is a test", "language": "en"}'
```

### Running Tests

Run the unit tests:
```bash
pytest tests/
```

Or with verbose output:
```bash
pytest tests/ -v
```

## Configuration

Edit `config/settings.py` to customize:
- **PORT**: Service port (default: 5001)
- **HOST**: Service host (default: 0.0.0.0)
- **DEFAULT_LANGUAGE**: Default language for TTS (default: en)
- **MAX_TEXT_LENGTH**: Maximum text length (default: 5000)
- **ALLOWED_LANGUAGES**: Supported languages list

Environment variables:
- `TTS_PORT`: Override default port
- `TTS_HOST`: Override default host
- `TTS_DEBUG`: Enable debug mode (true/false)

## Integration with Autobots

The TTS service is designed to integrate seamlessly with the Autobots Transportation Network Analysis System:

1. **Navigation Announcements**: Convert turn-by-turn directions to audio
2. **Traffic Alerts**: Provide audio notifications for traffic conditions
3. **Emergency Routing**: Voice instructions for emergency vehicle routing
4. **Accessibility**: Make the system accessible for visually impaired users

To integrate, make HTTP requests from your frontend or backend to the TTS service API endpoints.

## Troubleshooting

### Import Errors
If you get import errors, make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

### Port Already in Use
If port 5001 is already in use, change the port in `config/settings.py` or set the `TTS_PORT` environment variable:
```bash
export TTS_PORT=5002
python src/app.py
```

### Audio Files Not Generated
Ensure you have internet connectivity, as gTTS requires internet access to Google's text-to-speech service.

## API Documentation

See the [README.md](README.md) file for complete API documentation including:
- Available endpoints
- Request/response formats
- Error handling
- Example requests

## Support

For issues or questions, please refer to the main Autobots repository documentation or create an issue on GitHub.
