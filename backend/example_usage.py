#!/usr/bin/env python3
"""
Example usage of the Meeting Analysis Service
This script demonstrates how to use the API endpoints
"""

import requests
import json
import os

def example_analyze_meeting():
    """Example of how to analyze a meeting audio file"""
    
    print("🎤 Example: Analyze Meeting Audio")
    print("=" * 50)
    
    # API endpoint
    api_url = "http://127.0.0.1:8000/api/analyze-meeting/"
    
    # Example data
    session_id = 1  # Replace with actual session ID from your database
    audio_file_path = "sample_meeting.mp3"  # Replace with actual audio file
    
    # Check if file exists
    if not os.path.exists(audio_file_path):
        print(f"❌ Audio file not found: {audio_file_path}")
        print("   Please provide a valid audio file path")
        return
    
    try:
        # Prepare the request
        with open(audio_file_path, 'rb') as audio_file:
            files = {
                'audio_file': (os.path.basename(audio_file_path), audio_file, 'audio/mpeg')
            }
            data = {
                'session_id': session_id
            }
            
            print(f"📤 Uploading: {audio_file_path}")
            print(f"📋 Session ID: {session_id}")
            print("⏳ Processing...")
            
            # Make the request
            response = requests.post(api_url, files=files, data=data, timeout=300)
            
            # Handle response
            if response.status_code == 200:
                result = response.json()
                
                if result.get('success'):
                    print("\n✅ Analysis completed!")
                    print(f"📝 Transcript: {result.get('transcript', '')[:200]}...")
                    print(f"📄 Summary: {result.get('summary', '')[:200]}...")
                    print(f"🎯 Key Points: {len(result.get('key_points', []))} points")
                    print(f"💾 Summary ID: {result.get('meeting_summary_id')}")
                else:
                    print(f"❌ Analysis failed: {result.get('error')}")
            else:
                print(f"❌ HTTP Error {response.status_code}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

def example_get_summary():
    """Example of how to get an existing meeting summary"""
    
    print("\n📋 Example: Get Meeting Summary")
    print("=" * 50)
    
    session_id = 1  # Replace with actual session ID
    
    api_url = f"http://127.0.0.1:8000/api/meeting-summary/{session_id}/"
    
    try:
        print(f"📤 Getting summary for session: {session_id}")
        
        response = requests.get(api_url, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                data = result.get('data', {})
                print("✅ Summary retrieved!")
                print(f"📅 Created: {data.get('created_at')}")
                print(f"📝 Summary: {data.get('summary', '')[:200]}...")
                print(f"🎯 Key Points: {len(data.get('key_points', []))} points")
            else:
                print(f"❌ Failed: {result.get('error')}")
        else:
            print(f"❌ HTTP Error {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def show_curl_examples():
    """Show curl command examples"""
    
    print("\n🌐 cURL Examples")
    print("=" * 50)
    
    print("1. Analyze Meeting Audio:")
    print("""
curl -X POST http://127.0.0.1:8000/api/analyze-meeting/ \\
     -F "audio_file=@meeting.mp3" \\
     -F "session_id=1"
""")
    
    print("2. Get Meeting Summary:")
    print("""
curl http://127.0.0.1:8000/api/meeting-summary/1/
""")
    
    print("3. With authentication (if required):")
    print("""
curl -X POST http://127.0.0.1:8000/api/analyze-meeting/ \\
     -H "Authorization: Bearer your_token" \\
     -F "audio_file=@meeting.mp3" \\
     -F "session_id=1"
""")

def show_javascript_example():
    """Show JavaScript/Fetch example"""
    
    print("\n🟨 JavaScript Example")
    print("=" * 50)
    
    print("""
// HTML
<input type="file" id="audioFile" accept="audio/*">
<input type="number" id="sessionId" placeholder="Session ID">
<button onclick="analyzeMeeting()">Analyze Meeting</button>

// JavaScript
async function analyzeMeeting() {
    const audioFile = document.getElementById('audioFile').files[0];
    const sessionId = document.getElementById('sessionId').value;
    
    if (!audioFile || !sessionId) {
        alert('Please select an audio file and enter session ID');
        return;
    }
    
    const formData = new FormData();
    formData.append('audio_file', audioFile);
    formData.append('session_id', sessionId);
    
    try {
        const response = await fetch('/api/analyze-meeting/', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            console.log('Transcript:', result.transcript);
            console.log('Summary:', result.summary);
            console.log('Key Points:', result.key_points);
        } else {
            console.error('Error:', result.error);
        }
    } catch (error) {
        console.error('Request failed:', error);
    }
}
""")

def show_python_requests_example():
    """Show Python requests example"""
    
    print("\n🐍 Python Requests Example")
    print("=" * 50)
    
    print("""
import requests

def analyze_meeting_audio(audio_file_path, session_id):
    url = "http://127.0.0.1:8000/api/analyze-meeting/"
    
    with open(audio_file_path, 'rb') as audio_file:
        files = {'audio_file': audio_file}
        data = {'session_id': session_id}
        
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                return result
            else:
                print(f"Error: {result.get('error')}")
        else:
            print(f"HTTP Error: {response.status_code}")
    
    return None

# Usage
result = analyze_meeting_audio('meeting.mp3', 1)
if result:
    print(f"Summary: {result['summary']}")
    print(f"Key Points: {result['key_points']}")
""")

def main():
    """Main function"""
    
    print("🎤 Meeting Analysis Service - Usage Examples")
    print("=" * 60)
    
    # Show examples
    show_curl_examples()
    show_javascript_example()
    show_python_requests_example()
    
    # Interactive examples (uncomment to test)
    # example_analyze_meeting()
    # example_get_summary()
    
    print("\n💡 Tips:")
    print("   - Make sure your Django server is running")
    print("   - Set up your API keys (SARVAM_API_KEY and GEMINI_API_KEY)")
    print("   - Use valid session IDs from your database")
    print("   - Audio files should be clear with minimal background noise")
    print("   - Supported formats: MP3, WAV, M4A, FLAC, OGG")
    print("   - Maximum file size: 100MB")

if __name__ == "__main__":
    main()
