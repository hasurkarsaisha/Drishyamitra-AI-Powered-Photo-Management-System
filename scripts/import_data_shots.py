#!/usr/bin/env python
"""
Quick import script for data-shots folder
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Change to backend directory
os.chdir(os.path.join(os.path.dirname(__file__), 'backend'))

# Import the bulk import function
from bulk_import import bulk_import

# Configuration
FOLDER_PATH = r"D:\Drishyamitra\data-shots"
API_URL = "http://localhost:5000"

def main():
    print("\n" + "="*60)
    print("  Quick Import: data-shots folder")
    print("="*60 + "\n")
    
    # Get credentials
    username = input("Enter your username: ").strip()
    
    from getpass import getpass
    password = getpass("Enter your password: ")
    
    print(f"\n📁 Importing from: {FOLDER_PATH}")
    print(f"👤 User: {username}")
    print(f"🌐 API: {API_URL}\n")
    
    confirm = input("Continue? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled")
        return
    
    # Import
    success = bulk_import(FOLDER_PATH, username, password, API_URL)
    
    if success:
        print("\n✅ Import complete! Check your gallery at http://localhost:3000")
    else:
        print("\n❌ Import failed. Check the errors above.")

if __name__ == "__main__":
    main()
