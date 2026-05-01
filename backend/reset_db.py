#!/usr/bin/env python3
"""
Database Reset Script
Use this if you need to reset the database completely
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

def reset_database():
    """Reset the database by deleting and recreating it"""
    print("⚠️  WARNING: This will delete all data in your database!")
    confirm = input("Type 'YES' to confirm: ")
    
    if confirm != 'YES':
        print("❌ Database reset cancelled")
        return
    
    # Delete the database file
    db_path = Path('db.sqlite3')
    if db_path.exists():
        db_path.unlink()
        print("✅ Database file deleted")
    
    # Run migrations
    print("🔄 Running migrations...")
    os.system('python manage.py migrate')
    
    # Create superuser
    print("👤 Creating superuser...")
    os.system('python manage.py createsuperuser')
    
    print("✅ Database reset complete!")

if __name__ == "__main__":
    reset_database()
