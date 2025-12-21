"""
Example usage of TTS Service API
"""
import requests
import json

# Base URL for the TTS service
BASE_URL = "http://localhost:5001/api/tts"

def test_health():
    """Test health check"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_languages():
    """Test get supported languages"""
    print("Getting supported languages...")
    response = requests.get(f"{BASE_URL}/languages")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_synthesize():
    """Test text-to-speech synthesis"""
    print("Synthesizing speech...")
    
    data = {
        "text": "Turn left at the next intersection in 500 meters",
        "language": "en",
        "speed": 1.0
    }
    
    response = requests.post(f"{BASE_URL}/synthesize", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        # Try to download the audio file
        audio_url = result['audio_url']
        print(f"\nDownloading audio from: {BASE_URL.replace('/api/tts', '')}{audio_url}")
        audio_response = requests.get(f"{BASE_URL.replace('/api/tts', '')}{audio_url}")
        
        if audio_response.status_code == 200:
            filename = f"test_output_{result['filename']}"
            with open(filename, 'wb') as f:
                f.write(audio_response.content)
            print(f"Audio saved to: {filename}")
    else:
        print(f"Error: {response.json()}\n")

def test_cleanup():
    """Test cleanup of old files"""
    print("Testing cleanup...")
    
    data = {
        "max_age_hours": 1
    }
    
    response = requests.post(f"{BASE_URL}/cleanup", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

if __name__ == "__main__":
    print("TTS Service API Example Usage\n")
    print("=" * 50 + "\n")
    
    try:
        test_health()
        test_languages()
        test_synthesize()
        test_cleanup()
        
        print("=" * 50)
        print("All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to TTS service.")
        print("Make sure the service is running on http://localhost:5001")
    except Exception as e:
        print(f"Error: {e}")
