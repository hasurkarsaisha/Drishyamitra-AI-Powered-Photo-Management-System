"""
Reset a person's reference embedding and unlabel all their faces
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app
from models import db, Person, Face, PhotoPersonMap

app = create_app()

def reset_person(person_name, user_id=1):
    """Reset a person's reference embedding and unlabel their faces"""
    with app.app_context():
        person = Person.query.filter_by(name=person_name, user_id=user_id).first()
        
        if not person:
            print(f"❌ Person '{person_name}' not found")
            return
        
        print(f"\n🔄 Resetting: {person_name} (ID: {person.id})")
        
        # Count faces
        faces = Face.query.filter_by(person_id=person.id).all()
        print(f"   Found {len(faces)} faces labeled as {person_name}")
        
        # Delete reference embedding
        if person.reference_embedding is not None:
            person.reference_embedding = None
            print(f"   ✅ Deleted reference embedding")
        
        # Unlabel all faces
        for face in faces:
            print(f"   Unlabeling face {face.id}")
            face.person_id = None
        
        # Delete photo-person mappings
        mappings = PhotoPersonMap.query.filter_by(person_id=person.id).all()
        for mapping in mappings:
            db.session.delete(mapping)
        print(f"   Deleted {len(mappings)} photo-person mappings")
        
        # Delete the person
        db.session.delete(person)
        
        db.session.commit()
        
        print(f"\n✅ Reset complete!")
        print(f"   {len(faces)} faces are now unlabeled")
        print(f"   Person '{person_name}' deleted")
        print(f"   You can now relabel these faces correctly")

if __name__ == '__main__':
    reset_person("Ayush")
