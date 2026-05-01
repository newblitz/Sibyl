#!/usr/bin/env python3
"""
Test script for Meeting Analysis API
Demonstrates how to use the audio → transcript → summary pipeline
"""

import requests
import json
import os

def test_meeting_analysis_api():
    """Test the meeting analysis API endpoint"""
    
    print("🎤 Meeting Analysis API Test")
    print("=" * 50)
    
    # API endpoint
    api_url = "http://127.0.0.1:8000/api/analyze-meeting/"
    
    # Test data
    session_id = 1  # Replace with actual session ID
    audio_file_path = input("Enter path to audio file (or press Enter to skip): ").strip()
    
    if not audio_file_path:
        print("⏭️  Skipping file upload test")
        return
    
    if not os.path.exists(audio_file_path):
        print(f"❌ Audio file not found: {audio_file_path}")
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
            
            print(f"📤 Uploading audio file: {audio_file_path}")
            print(f"📋 Session ID: {session_id}")
            print("⏳ Processing... (this may take a few minutes)")
            
            # Make the request
            response = requests.post(api_url, files=files, data=data, timeout=300)
            
            # Handle response
            if response.status_code == 200:
                result = response.json()
                
                if result.get('success'):
                    print("\n✅ Analysis completed successfully!")
                    print("\n📝 TRANSCRIPT:")
                    print("-" * 40)
                    print(result.get('transcript', 'No transcript available'))
                    
                    print("\n📄 SUMMARY:")
                    print("-" * 40)
                    print(result.get('summary', 'No summary available'))
                    
                    print("\n🎯 KEY POINTS:")
                    print("-" * 40)
                    for i, point in enumerate(result.get('key_points', []), 1):
                        print(f"{i}. {point}")
                    
                    print("\n😊 SENTIMENT ANALYSIS:")
                    print("-" * 40)
                    sentiment = result.get('sentiment', {})
                    print(f"Overall: {sentiment.get('overall_sentiment', 'N/A')}")
                    print(f"Patient: {sentiment.get('patient_sentiment', 'N/A')}")
                    print(f"Counsellor: {sentiment.get('counsellor_sentiment', 'N/A')}")
                    print(f"Confidence: {sentiment.get('confidence_score', 'N/A')}")
                    
                    print("\n💡 RECOMMENDATIONS:")
                    print("-" * 40)
                    print(result.get('recommendations', 'No recommendations available'))
                    
                    print(f"\n💾 Summary ID: {result.get('meeting_summary_id')}")
                    
                else:
                    print(f"❌ Analysis failed: {result.get('error')}")
            else:
                print(f"❌ HTTP Error {response.status_code}: {response.text}")
                
    except requests.exceptions.Timeout:
        print("⏰ Request timed out. The analysis might still be processing.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_get_summary_api():
    """Test the get summary API endpoint"""
    
    print("\n📋 Get Summary API Test")
    print("=" * 50)
    
    session_id = input("Enter session ID to get summary (or press Enter to skip): ").strip()
    
    if not session_id:
        print("⏭️  Skipping get summary test")
        return
    
    try:
        session_id = int(session_id)
    except ValueError:
        print("❌ Invalid session ID")
        return
    
    api_url = f"http://127.0.0.1:8000/api/meeting-summary/{session_id}/"
    
    try:
        print(f"📤 Getting summary for session ID: {session_id}")
        
        response = requests.get(api_url, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                data = result.get('data', {})
                print("\n✅ Summary retrieved successfully!")
                print(f"📅 Created: {data.get('created_at')}")
                print(f"📝 Summary: {data.get('summary', 'No summary available')}")
                print(f"🎯 Key Points: {len(data.get('key_points', []))} points")
            else:
                print(f"❌ Failed to get summary: {result.get('error')}")
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def show_api_usage():
    """Show API usage examples"""
    
    print("\n📚 API USAGE EXAMPLES")
    print("=" * 50)
    
    print("""
1. Analyze Meeting Audio:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/analyze-meeting/ \\
        -F "audio_file=@meeting.mp3" \\
        -F "session_id=1"
   ```

2. Get Meeting Summary:
   ```bash
   curl http://127.0.0.1:8000/api/meeting-summary/1/
   ```

3. Python Requests:
   ```python
   import requests
   
   # Analyze audio
   with open('audio.mp3', 'rb') as f:
       response = requests.post(
           'http://127.0.0.1:8000/api/analyze-meeting/',
           files={'audio_file': f},
           data={'session_id': 1}
       )
   
   # Get summary
   response = requests.get('http://127.0.0.1:8000/api/meeting-summary/1/')
   ```

4. JavaScript/Fetch:
   ```javascript
   const formData = new FormData();
   formData.append('audio_file', audioFile);
   formData.append('session_id', '1');
   
   fetch('/api/analyze-meeting/', {
       method: 'POST',
       body: formData
   })
   .then(response => response.json())
   .then(data => console.log(data));
   ```

5. Required Environment Variables:
   ```bash
   export SARVAM_API_KEY="your_sarvam_api_key"
   export GEMINI_API_KEY="your_gemini_api_key"
   ```

6. Supported Audio Formats:
   - MP3, WAV, M4A, FLAC, OGG
   - Maximum file size: 100MB
   - Recommended: Clear audio with minimal background noise
   """)

def main():
    """Main function"""
    
    print("🎤 Meeting Analysis API Test Suite")
    print("=" * 60)
    
    # Show usage examples
    show_api_usage()
    
    # Test analyze meeting API
    test_meeting_analysis_api()
    
    # Test get summary API
    test_get_summary_api()
    
    print("\n✅ Test completed!")
    print("\n💡 Tips:")
    print("   - Make sure your Django server is running on http://127.0.0.1:8000")
    print("   - Ensure you have valid session IDs in your database")
    print("   - Set up your API keys (SARVAM_API_KEY and GEMINI_API_KEY)")
    print("   - For best results, use clear audio with distinct speakers")

if __name__ == "__main__":
    main()
