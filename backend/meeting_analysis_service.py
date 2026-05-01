"""
Meeting Analysis Service
Handles the complete pipeline: Audio → Sarvam Transcript → Gemini Summary → Database Storage
"""

import asyncio
import os
import json
import tempfile
import shutil
from typing import Optional, Dict, Any
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

# Import Sarvam transcription service
from sarvam_speech_to_transcript import SarvamSpeechToTranscript

# Import Gemini AI (Google's Generative AI)
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ Google Generative AI not installed. Install with: pip install google-generativeai")

# Import Django models
from CounsellorIntern.models import Dailylog_Counserllor_patient, MeetingSummary

class MeetingAnalysisService:
    """
    Service class to handle complete meeting analysis pipeline
    """
    
    def __init__(self):
        self.sarvam_api_key = getattr(settings, 'SARVAM_API_KEY', os.getenv('SARVAM_API_KEY'))
        self.gemini_api_key = getattr(settings, 'GEMINI_API_KEY', os.getenv('GEMINI_API_KEY'))
        
        # Initialize Gemini if available
        if GEMINI_AVAILABLE and self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.gemini_model = None
    
    async def process_meeting_audio(self, audio_file: UploadedFile, session_id: int) -> Dict[str, Any]:
        """
        Complete pipeline: Process audio file and generate meeting summary
        
        Args:
            audio_file: Uploaded audio file
            session_id: ID of the Dailylog_Counserllor_patient session
            
        Returns:
            Dict containing processing results and status
        """
        try:
            # Step 1: Validate session exists
            session = await self._get_session(session_id)
            if not session:
                return {
                    'success': False,
                    'error': 'Session not found',
                    'session_id': session_id
                }
            
            # Step 2: Save audio file temporarily
            temp_file_path = await self._save_temp_audio(audio_file)
            if not temp_file_path:
                return {
                    'success': False,
                    'error': 'Failed to save audio file',
                    'session_id': session_id
                }
            
            # Step 3: Get transcript from Sarvam
            transcript_result = await self._get_transcript(temp_file_path)
            
            # Clean up temp file
            self._cleanup_temp_file(temp_file_path)
            
            if not transcript_result:
                return {
                    'success': False,
                    'error': 'Failed to generate transcript',
                    'session_id': session_id
                }
            
            # Step 4: Generate summary using Gemini
            summary_data = await self._generate_summary(transcript_result)
            
            # Step 5: Store in database
            meeting_summary = await self._store_summary(session, transcript_result, summary_data)
            
            return {
                'success': True,
                'session_id': session_id,
                'transcript': transcript_result.get('full_text', ''),
                'summary': summary_data.get('summary', ''),
                'key_points': summary_data.get('key_points', []),
                'sentiment': summary_data.get('sentiment_analysis', {}),
                'recommendations': summary_data.get('recommendations', ''),
                'meeting_summary_id': meeting_summary.id if meeting_summary else None
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Processing failed: {str(e)}',
                'session_id': session_id
            }
    
    async def _get_session(self, session_id: int) -> Optional[Dailylog_Counserllor_patient]:
        """Get session from database"""
        try:
            return Dailylog_Counserllor_patient.objects.get(id=session_id)
        except Dailylog_Counserllor_patient.DoesNotExist:
            return None
    
    async def _save_temp_audio(self, audio_file: UploadedFile) -> Optional[str]:
        """Save uploaded audio file temporarily"""
        try:
            # Create temporary directory
            temp_dir = tempfile.mkdtemp()
            temp_file_path = os.path.join(temp_dir, audio_file.name)
            
            # Save file
            with open(temp_file_path, 'wb') as temp_file:
                for chunk in audio_file.chunks():
                    temp_file.write(chunk)
            
            return temp_file_path
            
        except Exception as e:
            print(f"Error saving temp audio: {e}")
            return None
    
    def _cleanup_temp_file(self, file_path: str):
        """Clean up temporary file and directory"""
        try:
            if os.path.exists(file_path):
                temp_dir = os.path.dirname(file_path)
                shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"Error cleaning up temp file: {e}")
    
    async def _get_transcript(self, audio_path: str) -> Optional[Dict[str, Any]]:
        """Get transcript from Sarvam API"""
        try:
            if not self.sarvam_api_key or self.sarvam_api_key == 'YOUR_API_KEY':
                print("⚠️ Sarvam API key not configured")
                return None
            
            # Initialize Sarvam service
            stt_service = SarvamSpeechToTranscript(self.sarvam_api_key)
            
            # Get transcript
            result = await stt_service.transcribe_audio(
                audio_path=audio_path,
                language_code="en-IN",
                model="saarika:v2.5",
                with_timestamps=True,
                with_diarization=True,
                num_speakers=2
            )
            
            return result
            
        except Exception as e:
            print(f"Error getting transcript: {e}")
            return None
    
    async def _generate_summary(self, transcript_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary using Gemini AI"""
        try:
            if not self.gemini_model:
                # Fallback: Simple text processing if Gemini not available
                return self._fallback_summary(transcript_data)
            
            full_text = transcript_data.get('full_text', '')
            if not full_text:
                return self._fallback_summary(transcript_data)
            
            # Create prompt for Gemini
            prompt = self._create_analysis_prompt(full_text)
            
            # Generate response
            response = await self._call_gemini_async(prompt)
            
            # Parse response
            return self._parse_gemini_response(response)
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return self._fallback_summary(transcript_data)
    
    def _create_analysis_prompt(self, transcript: str) -> str:
        """Create prompt for Gemini analysis"""
        return f"""
        Please analyze the following counselling session transcript and provide a comprehensive summary:

        TRANSCRIPT:
        {transcript}

        Please provide your analysis in the following JSON format:
        {{
            "summary": "A comprehensive summary of the session (2-3 paragraphs)",
            "key_points": [
                "Key point 1",
                "Key point 2",
                "Key point 3"
            ],
            "sentiment_analysis": {{
                "overall_sentiment": "positive/negative/neutral",
                "patient_sentiment": "positive/negative/neutral",
                "counsellor_sentiment": "positive/negative/neutral",
                "confidence_score": 0.85
            }},
            "recommendations": "Specific recommendations for follow-up care or next steps"
        }}

        Focus on:
        1. Patient's main concerns and issues
        2. Counsellor's approach and techniques used
        3. Progress made during the session
        4. Emotional state and sentiment of both parties
        5. Actionable recommendations for future sessions
        """
    
    async def _call_gemini_async(self, prompt: str) -> str:
        """Call Gemini API asynchronously"""
        try:
            # Run the synchronous call in a thread pool
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.gemini_model.generate_content(prompt)
            )
            return response.text
        except Exception as e:
            print(f"Error calling Gemini: {e}")
            return ""
    
    def _parse_gemini_response(self, response: str) -> Dict[str, Any]:
        """Parse Gemini response and extract structured data"""
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                # Fallback if no JSON found
                return self._fallback_summary({'full_text': response})
        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            return self._fallback_summary({'full_text': response})
    
    def _fallback_summary(self, transcript_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback summary when AI services are not available"""
        full_text = transcript_data.get('full_text', '')
        
        # Simple text processing
        sentences = full_text.split('.')
        key_sentences = sentences[:3] if len(sentences) >= 3 else sentences
        
        return {
            'summary': f"Session transcript: {full_text[:500]}{'...' if len(full_text) > 500 else ''}",
            'key_points': key_sentences,
            'sentiment_analysis': {
                'overall_sentiment': 'neutral',
                'patient_sentiment': 'neutral',
                'counsellor_sentiment': 'neutral',
                'confidence_score': 0.5
            },
            'recommendations': 'Review transcript for detailed analysis'
        }
    
    async def _store_summary(self, session: Dailylog_Counserllor_patient, 
                           transcript_data: Dict[str, Any], 
                           summary_data: Dict[str, Any]) -> Optional[MeetingSummary]:
        """Store meeting summary in database"""
        try:
            # Check if summary already exists
            existing_summary = MeetingSummary.objects.filter(session=session).first()
            
            if existing_summary:
                # Update existing summary
                existing_summary.transcript = transcript_data.get('full_text', '')
                existing_summary.summary = summary_data.get('summary', '')
                existing_summary.key_points = summary_data.get('key_points', [])
                existing_summary.sentiment_analysis = summary_data.get('sentiment_analysis', {})
                existing_summary.recommendations = summary_data.get('recommendations', '')
                existing_summary.save()
                return existing_summary
            else:
                # Create new summary
                meeting_summary = MeetingSummary.objects.create(
                    session=session,
                    transcript=transcript_data.get('full_text', ''),
                    summary=summary_data.get('summary', ''),
                    key_points=summary_data.get('key_points', []),
                    sentiment_analysis=summary_data.get('sentiment_analysis', {}),
                    recommendations=summary_data.get('recommendations', '')
                )
                return meeting_summary
                
        except Exception as e:
            print(f"Error storing summary: {e}")
            return None

# Convenience functions for easy integration
async def analyze_meeting_audio(audio_file: UploadedFile, session_id: int) -> Dict[str, Any]:
    """
    Convenience function to analyze meeting audio
    
    Args:
        audio_file: Uploaded audio file
        session_id: ID of the counselling session
        
    Returns:
        Dict with analysis results
    """
    service = MeetingAnalysisService()
    return await service.process_meeting_audio(audio_file, session_id)

def get_session_summary(session_id: int) -> Optional[Dict[str, Any]]:
    """
    Get existing summary for a session
    
    Args:
        session_id: ID of the counselling session
        
    Returns:
        Dict with summary data or None if not found
    """
    try:
        session = Dailylog_Counserllor_patient.objects.get(id=session_id)
        summary = getattr(session, 'summary', None)
        
        if summary:
            return {
                'id': summary.id,
                'transcript': summary.transcript,
                'summary': summary.summary,
                'key_points': summary.key_points,
                'sentiment_analysis': summary.sentiment_analysis,
                'recommendations': summary.recommendations,
                'created_at': summary.created_at,
                'updated_at': summary.updated_at
            }
        return None
        
    except Dailylog_Counserllor_patient.DoesNotExist:
        return None
