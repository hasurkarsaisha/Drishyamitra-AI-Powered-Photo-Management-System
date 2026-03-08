"""Check which photos have faces detected"""
import sys
sys.path.insert(0, 'backend')

from app import create_app
from models import db, Photo, Face

app = create_app()

with app.app_context():
    photos = Photo.query.order_by(Photo.id).all()
    
    print("📊 Face Detection Summary:\n")
    
    for photo in photos:
        faces = Face.query.filter_by(photo_id=photo.id).all()
        print(f"Photo {photo.id}: {photo.filename}")
        print(f"  Faces detected: {len(faces)}")
        if faces:
            for face in faces:
                print(f"    - Face {face.id}: confidence {face.confidence:.2%}")
        print()
