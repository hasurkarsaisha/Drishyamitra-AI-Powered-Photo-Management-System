"""
Label all unlabeled faces
"""
import sys
sys.path.insert(0, 'backend')

from app import create_app
from models import db, Face, Person, PhotoPersonMap, Photo

app = create_app()

with app.app_context():
    # Get all unlabeled faces
    unlabeled = Face.query.filter(Face.person_id.is_(None)).all()
    
    print(f"🔍 Found {len(unlabeled)} unlabeled faces")
    
    if len(unlabeled) == 0:
        print("✅ All faces are already labeled!")
        exit(0)
    
    # Group by user
    user_faces = {}
    for face in unlabeled:
        photo = Photo.query.get(face.photo_id)
        if photo.user_id not in user_faces:
            user_faces[photo.user_id] = []
        user_faces[photo.user_id].append((face, photo))
    
    for user_id, faces_list in user_faces.items():
        print(f"\n👤 User {user_id}: {len(faces_list)} unlabeled faces")
        print("Enter person names (or press Enter to skip):")
        
        for i, (face, photo) in enumerate(faces_list, 1):
            print(f"\n[{i}/{len(faces_list)}] Photo: {photo.filename}")
            print(f"  Face ID: {face.id}, Confidence: {face.confidence:.2f}")
            
            name = input("  Person name (or Enter to skip): ").strip()
            
            if name:
                # Find or create person
                person = Person.query.filter_by(name=name, user_id=user_id).first()
                if not person:
                    person = Person(name=name, user_id=user_id)
                    db.session.add(person)
                    db.session.flush()
                    print(f"  ✅ Created new person: {name}")
                
                # Label face
                face.person_id = person.id
                
                # Create photo-person mapping
                existing_map = PhotoPersonMap.query.filter_by(
                    photo_id=photo.id,
                    person_id=person.id
                ).first()
                
                if not existing_map:
                    photo_person_map = PhotoPersonMap(
                        photo_id=photo.id,
                        person_id=person.id
                    )
                    db.session.add(photo_person_map)
                
                print(f"  ✅ Labeled as: {name}")
    
    db.session.commit()
    print(f"\n🎉 Done! Check the People page to see labeled faces.")
