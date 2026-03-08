"""
Check for duplicate photos in the database
"""
import sys
import os
from collections import defaultdict

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app
from models import db, Photo

app = create_app()

def check_duplicates(user_id=1):
    """Check for duplicate photos"""
    with app.app_context():
        photos = Photo.query.filter_by(user_id=user_id).all()
        
        print(f"\n📊 Total photos: {len(photos)}")
        
        # Group by filename
        by_filename = defaultdict(list)
        for photo in photos:
            by_filename[photo.filename].append(photo)
        
        # Find duplicates
        duplicates = {k: v for k, v in by_filename.items() if len(v) > 1}
        
        if duplicates:
            print(f"\n⚠️  Found {len(duplicates)} duplicate filenames:")
            for filename, photo_list in duplicates.items():
                print(f"\n  {filename}:")
                for photo in photo_list:
                    print(f"    - ID: {photo.id}, Path: {photo.filepath}")
        else:
            print("\n✅ No duplicate filenames found")
        
        # Check for duplicate file paths
        by_filepath = defaultdict(list)
        for photo in photos:
            by_filepath[photo.filepath].append(photo)
        
        path_duplicates = {k: v for k, v in by_filepath.items() if len(v) > 1}
        
        if path_duplicates:
            print(f"\n⚠️  Found {len(path_duplicates)} duplicate file paths:")
            for filepath, photo_list in path_duplicates.items():
                print(f"\n  {filepath}:")
                for photo in photo_list:
                    print(f"    - ID: {photo.id}, Filename: {photo.filename}")
        else:
            print("\n✅ No duplicate file paths found")

if __name__ == '__main__':
    check_duplicates()
