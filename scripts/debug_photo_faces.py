"""
Debug faces in a specific photo
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app
from models import db, Photo, Face, Person

app = create_app()

def debug_photo(photo_id):
    """Debug faces in a photo"""
    with app.app_context():
        photo = Photo.query.get(photo_id)
        if not photo:
            print(f"Photo {photo_id} not found")
            return
        
        print(f"\n📸 Photo: {photo.filename} (ID: {photo.id})")
        print(f"   Path: {photo.filepath}")
        
        faces = Face.query.filter_by(photo_id=photo_id).all()
        print(f"\n👤 Faces detected: {len(faces)}")
        
        for i, face in enumerate(faces, 1):
            person_name = "UNLABELED"
            if face.person_id:
                person = Person.query.get(face.person_id)
                if person:
                    person_name = person.name
            
            print(f"\n  Face {i} (ID: {face.id}):")
            print(f"    Person: {person_name}")
            print(f"    BBox: {face.bbox}")
            print(f"    Confidence: {face.confidence:.2f}")

if __name__ == '__main__':
    # Test with a photo that has multiple people
    photo_id = int(input("Enter photo ID to debug: "))
    debug_photo(photo_id)
