#!/usr/bin/env python3
"""
Test Email Configuration Script
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prutha.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email_configuration():
    """Test the email configuration"""
    print("🔧 Testing Email Configuration")
    print("=" * 50)
    
    # Check settings
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"SENDGRID_API_KEY: {'Set' if settings.SENDGRID_API_KEY and settings.SENDGRID_API_KEY != 'your_sendgrid_api_key_here' else 'Not Set'}")
    
    # Test email sending
    test_email = input("\nEnter a test email address: ").strip()
    if not test_email:
        print("No email provided, skipping test")
        return
    
    print(f"\n📧 Sending test email to {test_email}...")
    
    try:
        result = send_mail(
            subject='Test Email from MindEase',
            message='This is a test email to verify SendGrid configuration.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_email],
            html_message='<h1>Test Email</h1><p>This is a test email to verify SendGrid configuration.</p>',
            fail_silently=False
        )
        
        if result:
            print("✅ Test email sent successfully!")
            print("Check your inbox (and spam folder) for the test email.")
        else:
            print("❌ Failed to send test email")
            
    except Exception as e:
        print(f"❌ Error sending test email: {str(e)}")

if __name__ == "__main__":
    test_email_configuration()
