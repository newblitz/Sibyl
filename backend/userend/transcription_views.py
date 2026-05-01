"""
API endpoints for meeting analysis service
"""

import asyncio
import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

# Import the meeting analysis service
from meeting_analysis_service import analyze_meeting_audio, get_session_summary

@csrf_exempt
@require_http_methods(["POST"])
def analyze_meeting(request):
    """
    API endpoint to analyze meeting audio and generate summary
    
    Expected POST data:
    - audio_file: Audio file (MP3, WAV, M4A, FLAC, OGG)
    - session_id: ID of the Dailylog_Counserllor_patient session
    
    Returns:
    - JSON response with analysis results
    """
    try:
        # Get audio file and session ID
        audio_file = request.FILES.get('audio_file')
        session_id = request.POST.get('session_id')
        
        if not audio_file:
            return JsonResponse({
                'success': False,
                'error': 'No audio file provided'
            }, status=400)
        
        if not session_id:
            return JsonResponse({
                'success': False,
                'error': 'No session ID provided'
            }, status=400)
        
        try:
            session_id = int(session_id)
        except ValueError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid session ID'
            }, status=400)
        
        # Validate file type
        allowed_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg']
        file_extension = os.path.splitext(audio_file.name)[1].lower()
        
        if file_extension not in allowed_extensions:
            return JsonResponse({
                'success': False,
                'error': f'Unsupported file type. Allowed: {", ".join(allowed_extensions)}'
            }, status=400)
        
        # Validate file size (100MB limit)
        if audio_file.size > 100 * 1024 * 1024:
            return JsonResponse({
                'success': False,
                'error': 'File size too large. Maximum 100MB allowed.'
            }, status=400)
        
        # Process the audio analysis
        result = asyncio.run(analyze_meeting_audio(audio_file, session_id))
        
        if result['success']:
            return JsonResponse(result)
        else:
            return JsonResponse(result, status=500)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)

@require_http_methods(["GET"])
def get_meeting_summary(request, session_id):
    """
    API endpoint to get existing meeting summary
    
    Args:
        session_id: ID of the counselling session
        
    Returns:
        JSON response with summary data
    """
    try:
        session_id = int(session_id)
        summary_data = get_session_summary(session_id)
        
        if summary_data:
            return JsonResponse({
                'success': True,
                'data': summary_data
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'No summary found for this session'
            }, status=404)
            
    except ValueError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid session ID'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)
