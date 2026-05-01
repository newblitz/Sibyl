"""
Configuration file for Meeting Analysis Service
Set up your API keys and configuration here
"""

import os
from django.conf import settings

# API Keys Configuration
# Set these as environment variables or in your Django settings

# Sarvam API Key for Speech-to-Text
SARVAM_API_KEY = os.getenv('SARVAM_API_KEY', 'YOUR_SARVAM_API_KEY_HERE')

# Google Gemini API Key for AI Summary Generation
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_GEMINI_API_KEY_HERE')

# Configuration Settings
MEETING_ANALYSIS_CONFIG = {
    # Sarvam Speech-to-Text settings
    'sarvam': {
        'language_code': 'en-IN',
        'model': 'saarika:v2.5',
        'with_timestamps': True,
        'with_diarization': True,
        'num_speakers': 2,
        'max_file_size': 100 * 1024 * 1024,  # 100MB
        'allowed_extensions': ['.mp3', '.wav', '.m4a', '.flac', '.ogg']
    },
    
    # Gemini AI settings
    'gemini': {
        'model': 'gemini-1.5-flash',
        'max_tokens': 4000,
        'temperature': 0.7
    },
    
    # Processing settings
    'processing': {
        'temp_dir_prefix': 'meeting_analysis_',
        'cleanup_temp_files': True,
        'timeout_seconds': 300  # 5 minutes
    }
}

def get_sarvam_config():
    """Get Sarvam configuration"""
    return MEETING_ANALYSIS_CONFIG['sarvam']

def get_gemini_config():
    """Get Gemini configuration"""
    return MEETING_ANALYSIS_CONFIG['gemini']

def get_processing_config():
    """Get processing configuration"""
    return MEETING_ANALYSIS_CONFIG['processing']

def validate_api_keys():
    """Validate that API keys are configured"""
    issues = []
    
    if not SARVAM_API_KEY or SARVAM_API_KEY == 'YOUR_SARVAM_API_KEY_HERE':
        issues.append("SARVAM_API_KEY not configured")
    
    if not GEMINI_API_KEY or GEMINI_API_KEY == 'YOUR_GEMINI_API_KEY_HERE':
        issues.append("GEMINI_API_KEY not configured")
    
    return issues

def print_setup_instructions():
    """Print setup instructions for API keys"""
    print("🔧 Meeting Analysis Service Setup")
    print("=" * 50)
    print()
    print("1. Sarvam API Key Setup:")
    print("   - Visit: https://sarvam.ai/")
    print("   - Sign up and get your API key")
    print("   - Set environment variable:")
    print("     export SARVAM_API_KEY='your_sarvam_api_key_here'")
    print()
    print("2. Google Gemini API Key Setup:")
    print("   - Visit: https://makersuite.google.com/app/apikey")
    print("   - Create a new API key")
    print("   - Set environment variable:")
    print("     export GEMINI_API_KEY='your_gemini_api_key_here'")
    print()
    print("3. Django Settings (alternative to environment variables):")
    print("   Add to your settings.py:")
    print("   SARVAM_API_KEY = 'your_sarvam_api_key_here'")
    print("   GEMINI_API_KEY = 'your_gemini_api_key_here'")
    print()
    print("4. Test the setup:")
    print("   python test_meeting_analysis.py")
    print()

if __name__ == "__main__":
    print_setup_instructions()
    
    # Validate configuration
    issues = validate_api_keys()
    if issues:
        print("⚠️  Configuration Issues:")
        for issue in issues:
            print(f"   - {issue}")
        print()
        print("Please fix these issues before using the service.")
    else:
        print("✅ Configuration looks good!")
        print("You can now use the Meeting Analysis Service.")
