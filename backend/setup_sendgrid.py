#!/usr/bin/env python3
"""
SendGrid Setup Script for MindEase
This script helps you test your SendGrid configuration
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

from loging.email_service import email_service

def test_sendgrid_config():
    """Test SendGrid configuration"""
    print("🔧 Testing SendGrid Configuration")
    print("=" * 50)
    
    # Check API key
    api_key = os.environ.get("SENDGRID_API_KEY")
    if not api_key or api_key == "your_sendgrid_api_key_here":
        print("❌ SENDGRID_API_KEY not set!")
        print("\nTo set your SendGrid API key:")
        print("1. Get your API key from https://sendgrid.com")
        print("2. Run: export SENDGRID_API_KEY='your_actual_api_key_here'")
        print("3. Or add it to your environment variables")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Check from email
    from_email = os.environ.get("DEFAULT_FROM_EMAIL", "euphoriafulfillment@gmail.com")
    print(f"✅ From Email: {from_email}")
    
    # Test email sending
    test_email = input("\nEnter a test email address (or press Enter to skip): ").strip()
    if test_email:
        print(f"\n📧 Sending test email to {test_email}...")
        success = email_service.send_verification_email(test_email, "123456")
        if success:
            print("✅ Test email sent successfully!")
        else:
            print("❌ Failed to send test email")
    else:
        print("⏭️  Skipping email test")
    
    return True

def show_instructions():
    """Show setup instructions"""
    print("\n📋 SendGrid Setup Instructions")
    print("=" * 50)
    print("1. Go to https://sendgrid.com and create an account")
    print("2. Navigate to Settings → API Keys")
    print("3. Click 'Create API Key'")
    print("4. Choose 'Restricted Access' and give it 'Mail Send' permissions")
    print("5. Copy the API key (starts with 'SG.')")
    print("6. Set the environment variable:")
    print("   export SENDGRID_API_KEY='your_actual_api_key_here'")
    print("7. Optionally set your from email:")
    print("   export DEFAULT_FROM_EMAIL='your-email@domain.com'")
    print("\n💡 Make sure your from email is verified in SendGrid!")

if __name__ == "__main__":
    print("🚀 MindEase SendGrid Setup")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        show_instructions()
    else:
        test_sendgrid_config()
        show_instructions()
