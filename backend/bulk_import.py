#!/usr/bin/env python
"""
Bulk Import Script for Drishyamitra
Import all photos from a folder into the database
"""

import os
import sys
import requests
from getpass import getpass

def bulk_import(folder_path, username, password, api_url="http://localhost:5000"):
    """Import all photos from a folder"""
    
    print(f"\n🚀 Drishyamitra Bulk Import Tool\n")
    print(f"{'='*50}")
    
    # Validate folder
    if not os.path.exists(folder_path):
        print(f"❌ Error: Folder '{folder_path}' does not exist")
        return False
    
    if not os.path.isdir(folder_path):
        print(f"❌ Error: '{folder_path}' is not a directory")
        return False
    
    # Count image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif'}
    image_files = [f for f in os.listdir(folder_path) 
                   if os.path.splitext(f.lower())[1] in image_extensions]
    
    if not image_files:
        print(f"❌ No image files found in '{folder_path}'")
        return False
    
    print(f"📁 Folder: {folder_path}")
    print(f"📸 Found {len(image_files)} image files")
    print(f"{'='*50}\n")
    
    # Login
    print("🔐 Logging in...")
    try:
        login_response = requests.post(
            f"{api_url}/auth/login",
            json={"username": username, "password": password}
        )
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.json().get('error', 'Unknown error')}")
            return False
        
        token = login_response.json()['access_token']
        print("✅ Login successful!\n")
        
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False
    
    # Import folder
    print("📤 Importing photos...")
    try:
        import_response = requests.post(
            f"{api_url}/bulk/import-folder",
            json={"folder_path": folder_path},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if import_response.status_code != 200:
            print(f"❌ Import failed: {import_response.json().get('error', 'Unknown error')}")
            return False
        
        result = import_response.json()
        
        print(f"\n{'='*50}")
        print(f"✅ Import completed!")
        print(f"{'='*50}")
        print(f"✅ Imported: {result['imported']} photos")
        print(f"⏭️  Skipped:  {result['skipped']} files")
        print(f"❌ Errors:   {result['errors']} files")
        
        if result['details']['imported']:
            print(f"\n📸 Imported photos:")
            for item in result['details']['imported'][:10]:  # Show first 10
                faces = item.get('faces_detected', 0)
                print(f"   • {item['filename']} (ID: {item['photo_id']}, Faces: {faces})")
            
            if len(result['details']['imported']) > 10:
                print(f"   ... and {len(result['details']['imported']) - 10} more")
        
        if result['details']['skipped']:
            print(f"\n⏭️  Skipped files:")
            for filename in result['details']['skipped'][:5]:
                print(f"   • {filename}")
            if len(result['details']['skipped']) > 5:
                print(f"   ... and {len(result['details']['skipped']) - 5} more")
        
        if result['details']['errors']:
            print(f"\n❌ Errors:")
            for error in result['details']['errors'][:5]:
                print(f"   • {error['filename']}: {error['error']}")
            if len(result['details']['errors']) > 5:
                print(f"   ... and {len(result['details']['errors']) - 5} more")
        
        print(f"\n{'='*50}\n")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main function"""
    print("\n" + "="*50)
    print("  Drishyamitra - Bulk Photo Import Tool")
    print("="*50 + "\n")
    
    # Get folder path
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        folder_path = input("📁 Enter folder path: ").strip()
    
    # Get credentials
    print("\n🔐 Login credentials:")
    username = input("Username: ").strip()
    password = getpass("Password: ")
    
    # Optional: API URL
    api_url = input("\n🌐 API URL (press Enter for http://localhost:5000): ").strip()
    if not api_url:
        api_url = "http://localhost:5000"
    
    # Confirm
    print(f"\n{'='*50}")
    print(f"Ready to import from: {folder_path}")
    print(f"User: {username}")
    print(f"API: {api_url}")
    print(f"{'='*50}")
    
    confirm = input("\n▶️  Continue? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Import cancelled")
        return
    
    # Import
    success = bulk_import(folder_path, username, password, api_url)
    
    if success:
        print("✅ All done! Check your gallery at http://localhost:3000")
    else:
        print("❌ Import failed. Please check the errors above.")

if __name__ == "__main__":
    main()
