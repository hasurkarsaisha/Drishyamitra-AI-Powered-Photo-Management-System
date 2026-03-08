"""
Remove duplicate photo-person mappings
"""
import sys
import os
from collections import defaultdict

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app
from models import db, Photo, PhotoPersonMap

app = create_app()

def fix_duplicates(user_id=1):
    """Remove duplicate mappings"""
    with app.app_context():
        # Get all mappings
        mappings = PhotoPersonMap.query.join(Photo).filter(Photo.user_id == user_id).all()
        
        # Group by (photo_id, person_id)
        seen = set()
        to_delete = []
        
        for mapping in mappings:
            key = (mapping.photo_id, mapping.person_id)
            if key in seen:
                to_delete.append(mapping)
            else:
                seen.add(key)
        
        if to_delete:
            print(f"\n🗑️  Removing {len(to_delete)} duplicate mappings...")
            for mapping in to_delete:
                photo = Photo.query.get(mapping.photo_id)
                from models import Person
                person = Person.query.get(mapping.person_id)
                print(f"  Removing duplicate: Photo {mapping.photo_id} ({photo.filename}) → {person.name}")
                db.session.delete(mapping)
            
            db.session.commit()
            print("\n✅ Duplicates removed!")
        else:
            print("\n✅ No duplicates to remove")

if __name__ == '__main__':
    fix_duplicates()
