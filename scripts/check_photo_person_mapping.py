"""
Check photo-person mappings to understand duplicate appearances
"""
import sys
import os
from collections import defaultdict

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app
from models import db, Photo, Person, PhotoPersonMap, Face

app = create_app()

def check_mappings(user_id=1):
    """Check photo-person mappings"""
    with app.app_context():
        # Get all photos
        photos = Photo.query.filter_by(user_id=user_id).all()
        print(f"\n📊 Total photos: {len(photos)}")
        
        # Check each photo's people
        print("\n📸 Photos with multiple people:")
        for photo in photos:
            people_in_photo = PhotoPersonMap.query.filter_by(photo_id=photo.id).all()
            if len(people_in_photo) > 1:
                people_names = []
                for mapping in people_in_photo:
                    person = Person.query.get(mapping.person_id)
                    if person:
                        people_names.append(person.name)
                print(f"  Photo {photo.id} ({photo.filename}): {len(people_in_photo)} people - {', '.join(people_names)}")
        
        # Check for duplicate mappings (same photo-person pair multiple times)
        print("\n🔍 Checking for duplicate mappings...")
        mappings = PhotoPersonMap.query.join(Photo).filter(Photo.user_id == user_id).all()
        
        mapping_counts = defaultdict(int)
        for mapping in mappings:
            key = (mapping.photo_id, mapping.person_id)
            mapping_counts[key] += 1
        
        duplicates = {k: v for k, v in mapping_counts.items() if v > 1}
        
        if duplicates:
            print(f"⚠️  Found {len(duplicates)} duplicate mappings:")
            for (photo_id, person_id), count in duplicates.items():
                photo = Photo.query.get(photo_id)
                person = Person.query.get(person_id)
                print(f"  Photo {photo_id} ({photo.filename}) → {person.name}: {count} times")
        else:
            print("✅ No duplicate mappings found")
        
        # Show people with their photo counts
        print("\n👥 People and their photos:")
        people = Person.query.filter_by(user_id=user_id).all()
        for person in people:
            photo_count = PhotoPersonMap.query.filter_by(person_id=person.id).count()
            face_count = Face.query.filter_by(person_id=person.id).count()
            print(f"  {person.name}: {photo_count} photos, {face_count} faces")

if __name__ == '__main__':
    check_mappings()
