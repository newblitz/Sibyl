#!/usr/bin/env python3
"""
Test script for Gmail Google Meet integration
Run this after sharing your Gmail calendar with the service account
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

def test_gmail_meet():
    print('='*60)
    print('GMAIL GOOGLE MEET INTEGRATION TEST')
    print('='*60)
    print('Gmail Account: singprateek165@gmail.com')
    print('Service Account: euphoria-meet-integration@subtle-osprey-403915.iam.gserviceaccount.com')
    
    # Test meet link generation
    start_time = datetime(2025, 10, 15, 10, 0)
    end_time = start_time + timedelta(minutes=50)
    attendees = ['singprateek165@gmail.com', 'patient@example.com']
    
    print('\n🔄 Testing meet link generation...')
    
    try:
        meet_link = create_google_meet_link(
            summary='Test Therapy Session - Gmail Integration',
            start_time=start_time,
            end_time=end_time,
            attendees_emails=attendees
        )
        
        if meet_link:
            print(f'\n✅ SUCCESS! Genuine meet link generated: {meet_link}')
            print('🎉 Gmail Google Meet integration is working!')
            print('\n📝 What this means:')
            print('   ✅ Service account has access to your Gmail calendar')
            print('   ✅ Google Meet API is working')
            print('   ✅ Genuine meet links can be generated')
            print('   ✅ Appointments can be approved with genuine meet links')
            return True
        else:
            print('\n❌ No meet link generated')
            print('\n📝 This means:')
            print('   ❌ Service account still needs calendar access')
            print('   ❌ Or Google Meet API is not enabled')
            return False
            
    except Exception as e:
        print(f'\n❌ Error during testing: {e}')
        print('\n📝 Possible issues:')
        print('   1. Calendar not shared with service account')
        print('   2. Google Meet API not enabled')
        print('   3. Service account permissions issue')
        return False

if __name__ == '__main__':
    success = test_gmail_meet()
    
    if success:
        print('\n' + '='*60)
        print('✅ READY FOR APPOINTMENT APPROVAL TESTING')
        print('='*60)
        print('1. Login as counsellor: dr_johnson / counsellor123')
        print('2. Go to pending approvals')
        print('3. Approve an appointment')
        print('4. Check console for genuine meet link generation')
        print('5. Patient should receive email with genuine meet link')
    else:
        print('\n' + '='*60)
        print('❌ SETUP INCOMPLETE')
        print('='*60)
        print('Please complete these steps:')
        print('1. Go to https://calendar.google.com/')
        print('2. Login with: singprateek165@gmail.com')
        print('3. Share your calendar with: euphoria-meet-integration@subtle-osprey-403915.iam.gserviceaccount.com')
        print('4. Set permission to "Make changes to events"')
        print('5. Run this test again')
