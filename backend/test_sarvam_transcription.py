#!/usr/bin/env python3
"""
Test script for Sarvam Speech-to-Transcript integration
"""

import asyncio
import os
from sarvam_speech_to_transcript import SarvamSpeechToTranscript, quick_transcribe

async def test_transcription():
    """Test the transcription functionality"""
    
    print("🎵 Sarvam Speech-to-Transcript Test")
    print("=" * 50)
    
    # Check if API key is set
    api_key = os.getenv("SARVAM_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY":
        print("⚠️  Please set your SARVAM_API_KEY environment variable")
        print("   Example: export SARVAM_API_KEY='your_actual_api_key_here'")
        return
    
    # Get audio file path from user
    audio_path = input("\n📁 Enter the path to your audio file: ").strip()
    
    if not audio_path:
        print("❌ No audio file path provided")
        return
    
    if not os.path.exists(audio_path):
        print(f"❌ Audio file not found: {audio_path}")
        return
    
    print(f"\n🎵 Processing: {audio_path}")
    print("⏳ This may take a few minutes depending on file size...")
    
    try:
        # Method 1: Using the class directly
        print("\n🔧 Method 1: Using SarvamSpeechToTranscript class")
        stt_service = SarvamSpeechToTranscript(api_key)
        
        result = await stt_service.transcribe_audio(
            audio_path=audio_path,
            language_code="en-IN",
            model="saarika:v2.5",
            with_timestamps=True,
            with_diarization=True,
            num_speakers=2
        )
        
        if result:
            print("\n✅ Transcription completed successfully!")
            stt_service.print_transcription_summary(result)
            
            # Save to file
            output_file = f"transcription_{os.path.basename(audio_path)}.json"
            import json
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Results saved to: {output_file}")
        else:
            print("❌ Transcription failed")
            
    except Exception as e:
        print(f"❌ Error during transcription: {e}")

async def test_quick_transcribe():
    """Test the quick transcription function"""
    
    print("\n🚀 Method 2: Using quick_transcribe function")
    
    audio_path = input("📁 Enter audio file path (or press Enter to skip): ").strip()
    
    if not audio_path:
        print("⏭️  Skipping quick test")
        return
    
    if not os.path.exists(audio_path):
        print(f"❌ Audio file not found: {audio_path}")
        return
    
    try:
        result = await quick_transcribe(audio_path)
        
        if result:
            print("✅ Quick transcription completed!")
            print(f"📄 Full text: {result.get('full_text', 'No text found')}")
            print(f"🎯 Speakers: {', '.join(result.get('speakers', []))}")
        else:
            print("❌ Quick transcription failed")
            
    except Exception as e:
        print(f"❌ Error during quick transcription: {e}")

def show_usage_examples():
    """Show usage examples"""
    
    print("\n📚 USAGE EXAMPLES")
    print("=" * 50)
    
    print("""
1. Basic Usage:
   ```python
   from sarvam_speech_to_transcript import quick_transcribe
   
   result = await quick_transcribe("audio.mp3")
   print(result['full_text'])
   ```

2. Advanced Usage:
   ```python
   from sarvam_speech_to_transcript import SarvamSpeechToTranscript
   
   stt = SarvamSpeechToTranscript("your_api_key")
   result = await stt.transcribe_audio(
       "audio.mp3",
       language_code="en-IN",
       num_speakers=3,
       with_timestamps=True
   )
   ```

3. Environment Setup:
   ```bash
   export SARVAM_API_KEY="your_actual_api_key_here"
   python sarvam_speech_to_transcript.py
   ```

4. Supported Audio Formats:
   - MP3, WAV, M4A, FLAC, OGG
   - Maximum file size: 100MB
   - Recommended: Clear audio with minimal background noise
   """)

async def main():
    """Main function"""
    
    print("🎤 Sarvam Speech-to-Transcript Integration Test")
    print("=" * 60)
    
    # Show usage examples
    show_usage_examples()
    
    # Test transcription
    await test_transcription()
    
    # Test quick function
    await test_quick_transcribe()
    
    print("\n✅ Test completed!")
    print("\n💡 Tips:")
    print("   - Make sure your audio file is clear and has minimal background noise")
    print("   - For best results, use audio with distinct speakers")
    print("   - Processing time depends on audio length and quality")

if __name__ == "__main__":
    asyncio.run(main())
