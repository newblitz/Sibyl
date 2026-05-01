#!/usr/bin/env python
"""
Script to populate the database with 10 dummy counsellor/psychologist records.
This script creates:
1. CustomUser records with user_type='Counsellor'
2. Psychologist records linked to the CustomUser
3. AdditionalPsycDetails records linked to the Psychologist
"""

import os
import sys
import django
from datetime import date, timedelta
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prutha.settings')
django.setup()

from loging.models import CustomUser
from CounsellorIntern.models import Psychologist, AdditionalPsycDetails

def create_dummy_counsellors():
    """Create 10 dummy counsellor records"""
    
    # Sample data for counsellors
    counsellor_data = [
        {
            'username': 'dr_smith',
            'email': 'dr.smith@euphoria.com',
            'first_name': 'Sarah',
            'last_name': 'Smith',
            'fname': 'Sarah',
            'middle_name': 'Elizabeth',
            'lname': 'Smith',
            'gender': 'female',
            'phone': '9876543210',
            'DOB': date(1985, 3, 15),
            'address': '123 Wellness Street, Mumbai, Maharashtra',
            'RCI_no': 'RCI123456',
            'experience': 8,
            'license_date': date(2015, 6, 1)
        },
        {
            'username': 'dr_johnson',
            'email': 'dr.johnson@euphoria.com',
            'first_name': 'Michael',
            'last_name': 'Johnson',
            'fname': 'Michael',
            'middle_name': 'David',
            'lname': 'Johnson',
            'gender': 'male',
            'phone': '9876543211',
            'DOB': date(1982, 7, 22),
            'address': '456 Mind Care Avenue, Delhi, NCR',
            'RCI_no': 'RCI123457',
            'experience': 12,
            'license_date': date(2011, 8, 15)
        },
        {
            'username': 'dr_williams',
            'email': 'dr.williams@euphoria.com',
            'first_name': 'Emily',
            'last_name': 'Williams',
            'fname': 'Emily',
            'middle_name': 'Grace',
            'lname': 'Williams',
            'gender': 'female',
            'phone': '9876543212',
            'DOB': date(1988, 11, 8),
            'address': '789 Healing Lane, Bangalore, Karnataka',
            'RCI_no': 'RCI123458',
            'experience': 6,
            'license_date': date(2017, 3, 20)
        },
        {
            'username': 'dr_brown',
            'email': 'dr.brown@euphoria.com',
            'first_name': 'David',
            'last_name': 'Brown',
            'fname': 'David',
            'middle_name': 'Robert',
            'lname': 'Brown',
            'gender': 'male',
            'phone': '9876543213',
            'DOB': date(1980, 1, 30),
            'address': '321 Therapy Road, Chennai, Tamil Nadu',
            'RCI_no': 'RCI123459',
            'experience': 15,
            'license_date': date(2008, 12, 10)
        },
        {
            'username': 'dr_davis',
            'email': 'dr.davis@euphoria.com',
            'first_name': 'Jessica',
            'last_name': 'Davis',
            'fname': 'Jessica',
            'middle_name': 'Marie',
            'lname': 'Davis',
            'gender': 'female',
            'phone': '9876543214',
            'DOB': date(1987, 5, 12),
            'address': '654 Counseling Center, Pune, Maharashtra',
            'RCI_no': 'RCI123460',
            'experience': 9,
            'license_date': date(2014, 9, 5)
        },
        {
            'username': 'dr_miller',
            'email': 'dr.miller@euphoria.com',
            'first_name': 'Christopher',
            'last_name': 'Miller',
            'fname': 'Christopher',
            'middle_name': 'James',
            'lname': 'Miller',
            'gender': 'male',
            'phone': '9876543215',
            'DOB': date(1983, 9, 18),
            'address': '987 Mental Health Plaza, Hyderabad, Telangana',
            'RCI_no': 'RCI123461',
            'experience': 11,
            'license_date': date(2012, 4, 12)
        },
        {
            'username': 'dr_wilson',
            'email': 'dr.wilson@euphoria.com',
            'first_name': 'Amanda',
            'last_name': 'Wilson',
            'fname': 'Amanda',
            'middle_name': 'Rose',
            'lname': 'Wilson',
            'gender': 'female',
            'phone': '9876543216',
            'DOB': date(1986, 12, 3),
            'address': '147 Wellness Way, Kolkata, West Bengal',
            'RCI_no': 'RCI123462',
            'experience': 7,
            'license_date': date(2016, 7, 8)
        },
        {
            'username': 'dr_moore',
            'email': 'dr.moore@euphoria.com',
            'first_name': 'Robert',
            'last_name': 'Moore',
            'fname': 'Robert',
            'middle_name': 'Thomas',
            'lname': 'Moore',
            'gender': 'male',
            'phone': '9876543217',
            'DOB': date(1981, 4, 25),
            'address': '258 Therapy Terrace, Ahmedabad, Gujarat',
            'RCI_no': 'RCI123463',
            'experience': 13,
            'license_date': date(2010, 11, 22)
        },
        {
            'username': 'dr_taylor',
            'email': 'dr.taylor@euphoria.com',
            'first_name': 'Lisa',
            'last_name': 'Taylor',
            'fname': 'Lisa',
            'middle_name': 'Ann',
            'lname': 'Taylor',
            'gender': 'female',
            'phone': '9876543218',
            'DOB': date(1989, 8, 14),
            'address': '369 Counseling Corner, Jaipur, Rajasthan',
            'RCI_no': 'RCI123464',
            'experience': 5,
            'license_date': date(2018, 2, 14)
        },
        {
            'username': 'dr_anderson',
            'email': 'dr.anderson@euphoria.com',
            'first_name': 'James',
            'last_name': 'Anderson',
            'fname': 'James',
            'middle_name': 'William',
            'lname': 'Anderson',
            'gender': 'male',
            'phone': '9876543219',
            'DOB': date(1984, 6, 7),
            'address': '741 Mental Wellness Drive, Kochi, Kerala',
            'RCI_no': 'RCI123465',
            'experience': 10,
            'license_date': date(2013, 5, 30)
        }
    ]
    
    created_count = 0
    
    for data in counsellor_data:
        try:
            # Check if user already exists
            if CustomUser.objects.filter(username=data['username']).exists():
                print(f"User {data['username']} already exists, skipping...")
                continue
            
            # Create CustomUser
            user = CustomUser.objects.create_user(
                username=data['username'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password='counsellor123',  # Default password
                user_type='Counsellor',
                email_verified=True  # Mark as verified for counsellors
            )
            
            # Create Psychologist record
            psychologist = Psychologist.objects.create(
                fname=data['fname'],
                middle_name=data['middle_name'],
                lname=data['lname'],
                email=data['email'],
                gender=data['gender'],
                phone=data['phone'],
                DOB=data['DOB'],
                address=data['address'],
                Auth_id=user
            )
            
            # Create AdditionalPsycDetails record
            additional_details = AdditionalPsycDetails.objects.create(
                RCI_no=data['RCI_no'],
                Experiance=data['experience'],
                Issue_date_of_license=data['license_date'],
                psychologist=psychologist
            )
            
            created_count += 1
            print(f"✅ Created counsellor: Dr. {data['fname']} {data['lname']} (RCI: {data['RCI_no']})")
            
        except Exception as e:
            print(f"❌ Error creating counsellor {data['username']}: {str(e)}")
            continue
    
    print(f"\n🎉 Successfully created {created_count} counsellor records!")
    print(f"📧 All counsellors have email_verified=True and user_type='Counsellor'")
    print(f"🔑 Default password for all counsellors: 'counsellor123'")

if __name__ == '__main__':
    print("🚀 Starting to populate database with dummy counsellors...")
    create_dummy_counsellors()
    print("✨ Database population completed!")
