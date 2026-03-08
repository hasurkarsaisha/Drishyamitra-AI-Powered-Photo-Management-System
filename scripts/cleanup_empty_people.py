"""
Clean up people with no faces
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app
from models import db, Person, Face, PhotoPersonMap

app = create_app()

def cleanup_empty_people(user_id=1):
    """Remove people who have no faces"""
    with app.app_context():
        people = Person.query.filter_by(user_id=user_id).all()
        
        to_delete = []
        for person in people:
            face_count = Face.query.filter_by(person_id=person.id).count()
            if face_count == 0:
                to_delete.append(person)
        
        if to_delete:
            print(f"\n🗑️  Found {len(to_delete)} people with no faces:")
            for person in to_delete:
                print(f"   - {person.name}")
                # Delete mappings
                mappings = PhotoPersonMap.query.filter_by(person_id=person.id).all()
                for mapping in mappings:
                    db.session.delete(mapping)
                # Delete person
                db.session.delete(person)
            
            db.session.commit()
            print(f"\n✅ Cleaned up {len(to_delete)} empty people")
        else:
            print("\n✅ No empty people to clean up")

if __name__ == '__main__':
    cleanup_empty_people()
