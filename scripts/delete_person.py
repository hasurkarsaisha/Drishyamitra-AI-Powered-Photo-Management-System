"""
Delete a person and all their data
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app
from models import db, Person, Face, PhotoPersonMap

app = create_app()

def delete_person(person_name, user_id=1):
    """Delete a person and all their associations"""
    with app.app_context():
        person = Person.query.filter_by(name=person_name, user_id=user_id).first()
        
        if not person:
            print(f"❌ Person '{person_name}' not found")
            return
        
        print(f"\n🗑️  Deleting person: {person_name} (ID: {person.id})")
        
        # Count what will be deleted
        faces = Face.query.filter_by(person_id=person.id).all()
        mappings = PhotoPersonMap.query.filter_by(person_id=person.id).all()
        
        print(f"   - {len(faces)} face labels will be removed (faces will become unlabeled)")
        print(f"   - {len(mappings)} photo-person mappings will be deleted")
        print(f"   - Reference embedding will be deleted")
        
        # Unlabel all faces (set person_id to None instead of deleting)
        for face in faces:
            print(f"     Unlabeling face {face.id}")
            face.person_id = None
        
        # Delete mappings
        for mapping in mappings:
            db.session.delete(mapping)
        
        # Delete person
        db.session.delete(person)
        db.session.commit()
        
        print(f"\n✅ Person '{person_name}' deleted successfully!")
        print(f"   {len(faces)} faces are now unlabeled and ready to be relabeled")

if __name__ == '__main__':
    delete_person("Ayush Mestri")
