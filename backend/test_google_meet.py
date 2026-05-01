#!/usr/bin/env python3
"""
Test script to verify Google Meet integration
Run this after setting up service account credentials
"""

import os
import sys
import django

# Setup Django
sys.path.append('/Users/prateekmac/Desktop/project x/prutha')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prutha.settings')
django.setup()

from Counsellordashboard.views import create_google_meet_link
from datetime import datetime, timedelta

def test_google_meet():
    print('='*60)
    print('GOOGLE MEET INTEGRATION TEST')
    print('='*60)
    
    # Check if service account file exists
    service_account_file = '/Users/prateekmac/Desktop/project x/prutha/service_account.json'
    
    if not os.path.exists(service_account_file):
        print('❌ Service account file not found')
        return False
    
    print('✅ Service account file found')
    
    # Check file content
    with open(service_account_file, 'r') as f:
        content = f.read()
        
    if '"type": "service_account"' in content:
        print('✅ Service account format detected')
    else:
        print('❌ Not a service account file (might be web OAuth)')
        return False
    
    if 'client_email' in content and 'private_key' in content:
        print('✅ Required fields present')
    else:
        print('❌ Missing required fields')
        return False
    
    # Test meet link generation
    try:
        start_time = datetime(2025, 10, 15, 10, 0)
        end_time = start_time + timedelta(minutes=50)
        attendees = ['test@example.com', 'patient@example.com']
        
        print('\n🔄 Testing meet link generation...')
        meet_link = create_google_meet_link(
            summary='Test Therapy Session',
            start_time=start_time,
            end_time=end_time,
            attendees_emails=attendees
        )
        
        if meet_link:
            print(f'✅ SUCCESS! Meet link generated: {meet_link}')
            print('🎉 Google Meet integration is working!')
            return True
        else:
            print('❌ Meet link generation failed')
            return False
            
    except Exception as e:
        print(f'❌ Error during testing: {e}')
        return False

if __name__ == '__main__':
    success = test_google_meet()
    
    if success:
        print('\n' + '='*60)
        print('✅ READY TO TEST APPOINTMENT APPROVAL')
        print('='*60)
        print('1. Login as counsellor: dr_johnson / counsellor123')
        print('2. Go to pending approvals')
        print('3. Approve an appointment')
        print('4. Check console for meet link generation')
        print('5. Patient should receive email with meet link')
    else:
        print('\n' + '='*60)
        print('❌ SETUP INCOMPLETE')
        print('='*60)
        print('Please follow the steps in GOOGLE_MEET_SETUP.md')
        print('You need to create a Service Account, not use Web OAuth credentials')
