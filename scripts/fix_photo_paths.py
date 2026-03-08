"""Fix photo paths in database"""
import sys
import os
sys.path.insert(0, 'backend')

from app import create_app
from models import db, Photo

app = create_app()

with app.app_context():
    photos = Photo.query.all()
    
    print(f"📝 Checking {len(photos)} photos...")
    
    fixed = 0
    for photo in photos:
        print(f"\nPhoto {photo.id}: {photo.filepath}")
        
        # Check if file exists
        if not os.path.exists(photo.filepath):
            # Try with backend/ prefix
            new_path = os.path.join('backend', photo.filepath)
            if os.path.exists(new_path):
                print(f"  ✅ Fixed: {new_path}")
                photo.filepath = new_path
                fixed += 1
            else:
                print(f"  ❌ Not found at: {new_path}")
        else:
            print(f"  ✅ Path OK")
    
    if fixed > 0:
        db.session.commit()
        print(f"\n✅ Fixed {fixed} photo paths")
    else:
        print(f"\n✅ All paths are correct")
