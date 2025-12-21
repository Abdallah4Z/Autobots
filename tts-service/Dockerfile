FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create audio output directory
RUN mkdir -p audio_output

# Expose port
EXPOSE 5001

# Set environment variables
ENV TTS_PORT=5001
ENV TTS_HOST=0.0.0.0

# Run the application
CMD ["python", "src/app.py"]
