"""Reset all faces to unlabeled"""
import sys
sys.path.insert(0, 'backend')

from app import create_app
from models import db, Face, Person, PhotoPersonMap

app = create_app()

with app.app_context():
    # Delete all photo-person mappings
    PhotoPersonMap.query.delete()
    
    # Reset all faces to unlabeled
    faces = Face.query.all()
    for face in faces:
        face.person_id = None
    
    # Delete all persons
    Person.query.delete()
    
    db.session.commit()
    
    print(f"✅ Reset {len(faces)} faces to unlabeled")
    print(f"🎉 Go to http://localhost:3000/label-faces to start labeling!")
