"""
Unlabel all faces in a photo
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app
from models import db, Photo, Face, PhotoPersonMap

app = create_app()

def unlabel_photo(photo_id):
    """Unlabel all faces in a photo"""
    with app.app_context():
        photo = Photo.query.get(photo_id)
        if not photo:
            print(f"❌ Photo {photo_id} not found")
            return
        
        print(f"\n📸 Photo: {photo.filename} (ID: {photo.id})")
        
        faces = Face.query.filter_by(photo_id=photo_id).all()
        print(f"   Found {len(faces)} faces")
        
        # Unlabel all faces
        for face in faces:
            if face.person_id:
                from models import Person
                person = Person.query.get(face.person_id)
                print(f"   Unlabeling face {face.id} (was: {person.name if person else 'Unknown'})")
                face.person_id = None
        
        # Delete all photo-person mappings for this photo
        mappings = PhotoPersonMap.query.filter_by(photo_id=photo_id).all()
        for mapping in mappings:
            db.session.delete(mapping)
        
        db.session.commit()
        
        print(f"\n✅ All faces unlabeled! Ready to relabel correctly.")

if __name__ == '__main__':
    photo_id = int(input("Enter photo ID to unlabel: "))
    unlabel_photo(photo_id)
