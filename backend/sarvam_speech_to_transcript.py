import asyncio
import os
import json
from pathlib import Path
from sarvamai import AsyncSarvamAI

class SarvamSpeechToTranscript:
    def __init__(self, api_key=None):
        """
        Initialize Sarvam Speech-to-Text client
        
        Args:
            api_key (str): Sarvam API key. If None, will try to get from environment variable SARVAM_API_KEY
        """
        self.api_key = api_key or os.getenv("SARVAM_API_KEY", "YOUR_API_KEY")
        self.client = None
        
    async def initialize_client(self):
        """Initialize the Sarvam AI client"""
        try:
            self.client = AsyncSarvamAI(api_subscription_key=self.api_key)
            print("✅ Sarvam AI client initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize Sarvam AI client: {e}")
            return False
    
    async def transcribe_audio(self, audio_path, language_code="en-IN", model="saarika:v2.5", 
                             with_timestamps=True, with_diarization=True, num_speakers=2):
        """
        Transcribe audio file to text
        
        Args:
            audio_path (str): Path to the audio file
            language_code (str): Language code (default: "en-IN")
            model (str): Model to use (default: "saarika:v2.5")
            with_timestamps (bool): Include timestamps in output
            with_diarization (bool): Enable speaker diarization
            num_speakers (int): Number of speakers to detect
            
        Returns:
            dict: Transcription result with text, timestamps, and speaker info
        """
        if not self.client:
            if not await self.initialize_client():
                return None
        
        try:
            # Validate audio file exists
            if not os.path.exists(audio_path):
                print(f"❌ Audio file not found: {audio_path}")
                return None
            
            print(f"🎵 Processing audio file: {audio_path}")
            
            # Create speech-to-text job
            job = await self.client.speech_to_text_job.create_job(
                language_code=language_code,
                model=model,
                with_timestamps=with_timestamps,
                with_diarization=with_diarization,
                num_speakers=num_speakers
            )
            
            print("📝 Speech-to-text job created")
            
            # Upload audio file
            await job.upload_files(file_paths=[audio_path])
            print("📤 Audio file uploaded")
            
            # Start processing
            await job.start()
            print("🚀 Processing started...")
            
            # Wait for completion
            final_status = await job.wait_until_complete()
            print(f"✅ Processing completed with status: {final_status}")
            
            # Check if job failed
            if await job.is_failed():
                print("❌ Speech-to-text job failed")
                return None
            
            # Download outputs
            output_dir = "./transcript_output"
            os.makedirs(output_dir, exist_ok=True)
            await job.download_outputs(output_dir=output_dir)
            print(f"📁 Output downloaded to: {output_dir}")
            
            # Parse the results
            result = await self._parse_transcription_results(output_dir)
            return result
            
        except Exception as e:
            print(f"❌ Error during transcription: {e}")
            return None
    
    async def _parse_transcription_results(self, output_dir):
        """Parse the transcription results from the output directory"""
        try:
            # Look for JSON files in the output directory
            output_path = Path(output_dir)
            json_files = list(output_path.glob("*.json"))
            
            if not json_files:
                print("❌ No JSON output files found")
                return None
            
            # Read the first JSON file (usually the main result)
            with open(json_files[0], 'r', encoding='utf-8') as f:
                result = json.load(f)
            
            # Extract relevant information
            transcription_data = {
                'full_text': '',
                'segments': [],
                'speakers': [],
                'language': result.get('language', 'unknown'),
                'duration': result.get('duration', 0)
            }
            
            # Extract text segments with timestamps and speakers
            if 'segments' in result:
                for segment in result['segments']:
                    segment_data = {
                        'text': segment.get('text', ''),
                        'start_time': segment.get('start', 0),
                        'end_time': segment.get('end', 0),
                        'speaker': segment.get('speaker', 'unknown')
                    }
                    transcription_data['segments'].append(segment_data)
                    transcription_data['full_text'] += segment_data['text'] + ' '
            
            # Extract unique speakers
            speakers = set(segment.get('speaker', 'unknown') for segment in result.get('segments', []))
            transcription_data['speakers'] = list(speakers)
            
            return transcription_data
            
        except Exception as e:
            print(f"❌ Error parsing transcription results: {e}")
            return None
    
    def print_transcription_summary(self, result):
        """Print a formatted summary of the transcription"""
        if not result:
            print("❌ No transcription result to display")
            return
        
        print("\n" + "="*60)
        print("📝 TRANSCRIPTION SUMMARY")
        print("="*60)
        print(f"Language: {result.get('language', 'Unknown')}")
        print(f"Duration: {result.get('duration', 0):.2f} seconds")
        print(f"Speakers: {', '.join(result.get('speakers', []))}")
        print(f"Segments: {len(result.get('segments', []))}")
        
        print("\n📄 FULL TRANSCRIPT:")
        print("-" * 40)
        print(result.get('full_text', 'No text found'))
        
        if result.get('segments'):
            print("\n🎯 DETAILED SEGMENTS:")
            print("-" * 40)
            for i, segment in enumerate(result['segments'][:10]):  # Show first 10 segments
                print(f"{i+1}. [{segment['start_time']:.2f}s - {segment['end_time']:.2f}s] "
                      f"Speaker {segment['speaker']}: {segment['text']}")
            
            if len(result['segments']) > 10:
                print(f"... and {len(result['segments']) - 10} more segments")

async def main():
    """Main function to demonstrate usage"""
    # Initialize the speech-to-transcript service
    stt_service = SarvamSpeechToTranscript()
    
    # Example usage - replace with your actual audio file path
    audio_file = input("Enter the path to your audio file: ").strip()
    
    if not audio_file:
        print("❌ No audio file path provided")
        return
    
    # Transcribe the audio
    result = await stt_service.transcribe_audio(
        audio_path=audio_file,
        language_code="en-IN",
        model="saarika:v2.5",
        with_timestamps=True,
        with_diarization=True,
        num_speakers=2
    )
    
    if result:
        # Print the results
        stt_service.print_transcription_summary(result)
        
        # Save results to a file
        output_file = "transcription_result.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Full results saved to: {output_file}")
    else:
        print("❌ Transcription failed")

# Convenience function for quick transcription
async def quick_transcribe(audio_path, api_key=None):
    """
    Quick function to transcribe audio and return results
    
    Args:
        audio_path (str): Path to audio file
        api_key (str): Sarvam API key (optional)
        
    Returns:
        dict: Transcription results or None if failed
    """
    stt_service = SarvamSpeechToTranscript(api_key)
    return await stt_service.transcribe_audio(audio_path)

if __name__ == "__main__":
    asyncio.run(main())

# --- Usage Examples ---
# Basic usage:
# result = await quick_transcribe("path/to/audio.mp3")
# 
# With custom settings:
# stt_service = SarvamSpeechToTranscript("your_api_key")
# result = await stt_service.transcribe_audio("audio.mp3", num_speakers=3)
