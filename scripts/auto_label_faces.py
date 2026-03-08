"""
Script to automatically label faces using existing reference embeddings
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app
from models import db, Face, Person, PhotoPersonMap
from services.face_recognition import FaceRecognitionService

app = create_app()

def auto_label_faces(user_id=1):
    """Auto-label all unlabeled faces using reference embeddings"""
    with app.app_context():
        face_service = FaceRecognitionService()
        
        # Get all unlabeled faces
        unlabeled_faces = Face.query.join(
            Face.photo
        ).filter(
            Face.person_id.is_(None),
            Face.photo.has(user_id=user_id)
        ).all()
        
        print(f"\n📊 Found {len(unlabeled_faces)} unlabeled faces")
        
        # Get all people with reference embeddings
        people = Person.query.filter(
            Person.user_id == user_id,
            Person.reference_embedding.isnot(None)
        ).all()
        
        print(f"📊 Found {len(people)} people with reference embeddings:")
        for person in people:
            print(f"  - {person.name}")
        
        print("\n🔄 Starting auto-labeling...\n")
        
        matched = 0
        unmatched = 0
        
        for face in unlabeled_faces:
            print(f"Face {face.id} (photo {face.photo_id}):")
            
            # Try to find match
            matching_person = face_service.find_matching_person(face.embedding, user_id)
            
            if matching_person:
                # Update face
                face.person_id = matching_person.id
                
                # Create photo-person mapping if doesn't exist
                existing_map = PhotoPersonMap.query.filter_by(
                    photo_id=face.photo_id,
                    person_id=matching_person.id
                ).first()
                
                if not existing_map:
                    photo_person_map = PhotoPersonMap(
                        photo_id=face.photo_id,
                        person_id=matching_person.id
                    )
                    db.session.add(photo_person_map)
                
                matched += 1
                print(f"  ✅ Labeled as {matching_person.name}\n")
            else:
                unmatched += 1
                print(f"  ❌ No match found\n")
        
        db.session.commit()
        
        print(f"\n✅ Auto-labeling complete!")
        print(f"   Matched: {matched}")
        print(f"   Unmatched: {unmatched}")

if __name__ == '__main__':
    auto_label_faces()
