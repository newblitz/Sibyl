#!/usr/bin/env python3
"""
Quick Email Test - No user input required
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

def quick_test():
    """Quick email test"""
    print("🔧 Quick Email Test")
    print("=" * 30)
    
    # Use a test email (you can change this)
    test_email = "sinprateek165@gmail.com"
    
    print(f"📧 Sending test email to {test_email}...")
    print(f"📧 Using backend: {settings.EMAIL_BACKEND}")
    
    try:
        result = send_mail(
            subject='Test Email from Euphoria',
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
    quick_test()
