"""Check people and their photos"""
import sys
sys.path.insert(0, 'backend')

from app import create_app
from models import db, Person, Photo, PhotoPersonMap, Face

app = create_app()

with app.app_context():
    people = Person.query.all()
    
    print("👥 People and their photos:\n")
    
    for person in people:
        print(f"Person: {person.name} (ID: {person.id})")
        
        # Get all photo mappings
        mappings = PhotoPersonMap.query.filter_by(person_id=person.id).all()
        print(f"  Photo mappings: {len(mappings)}")
        
        # Get unique photos
        photo_ids = set(pm.photo_id for pm in mappings)
        print(f"  Unique photos: {len(photo_ids)}")
        
        for photo_id in photo_ids:
            photo = Photo.query.get(photo_id)
            if photo:
                # Count faces of this person in this photo
                faces = Face.query.filter_by(photo_id=photo_id, person_id=person.id).all()
                print(f"    - {photo.filename}: {len(faces)} face(s) of {person.name}")
        
        print()
