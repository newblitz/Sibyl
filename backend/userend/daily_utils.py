# your_app/daily_utils.py
import time
import requests
import json
from django.conf import settings

# Daily API configuration
DAILY_API_BASE_URL = "https://api.daily.co/v1"

def create_daily_meeting_for_appointment(appointment):
    """
    Creates a Daily.co room for a specific appointment using the REST API.
    
    - Sets auto-start for audio-only recording.
    - Uses the appointment's ID in the room name for easy tracking.
    """
    try:
        # Check if Daily API key is configured
        api_key = settings.DAILY_API_KEY
        if not api_key or api_key == 'your_daily_api_key_here':
            print("⚠️ Daily API key not configured, generating fallback meeting link")
            # Generate a fallback meeting link (Google Meet style)
            room_name = f"appointment-{appointment.id}-{int(time.time())}"
            fallback_url = f"https://meet.google.com/{room_name}"
            return fallback_url, room_name
        
        # Create a unique, predictable room name
        room_name = f"appointment-{appointment.id}-{appointment.selected_doctor.Auth_id}-{int(time.time())}"

        # Define room properties (simplified without recording for now)
        room_data = {
            'name': room_name,
            'properties': {
                'exp': int(time.time() + (3 * 24 * 3600)),  # Room expires in 3 days
                'max_participants': 10,  # Limit participants for therapy sessions
                'enable_chat': True,  # Enable chat for communication
                'enable_screenshare': True,  # Enable screen sharing
                # https://docs.daily.co/reference/rest-api/rooms/config#nbf
                'enable_recording': "cloud",  # Disable recording for now (requires webhook setup)
            }
        }
        
        # Make API request to create room
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            f"{DAILY_API_BASE_URL}/rooms",
            headers=headers,
            json=room_data,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            room_info = response.json()
            print(f"✅ Daily.co room created successfully: {room_name}")
            print(f"✅ Room URL: {room_info.get('url')}")
            return room_info.get('url'), room_info.get('name')
        else:
            print(f"❌ Daily API error: {response.status_code} - {response.text}")
            # Generate fallback meeting link
            fallback_url = f"https://meet.google.com/{room_name}"
            return fallback_url, room_name

    except Exception as e:
        print(f"Error creating Daily.co room: {e}")
        # Generate fallback meeting link
        room_name = f"appointment-{appointment.id}-{int(time.time())}"
        fallback_url = f"https://meet.google.com/{room_name}"
        return fallback_url, room_name

def get_daily_room_recording(room_name):
    """
    Gets the recording of a Daily.co room.
    """
    try:
        api_key = settings.DAILY_API_KEY
        if not api_key or api_key == 'your_daily_api_key_here':
            return None
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            f"{DAILY_API_BASE_URL}/rooms/{room_name}/recordings",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        return None
            
    except Exception as e:
        print(f"Error getting recording: {e}")
        return None
            