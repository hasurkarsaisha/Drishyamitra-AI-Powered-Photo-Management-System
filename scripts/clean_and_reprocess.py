"""Clean bad detections and reprocess with stricter filters"""
import sys
sys.path.insert(0, 'backend')

from app import create_app
from models import db, Face, Person, PhotoPersonMap, Photo
from services.face_recognition import FaceRecognitionService

app = create_app()

with app.app_context():
    print("🧹 Cleaning up...")
    
    # Delete all existing data
    PhotoPersonMap.query.delete()
    Face.query.delete()
    Person.query.delete()
    
    # Reset all photos to unprocessed
    photos = Photo.query.all()
    for photo in photos:
        photo.processed = False
    
    db.session.commit()
    
    print(f"✅ Cleaned up. Now reprocessing {len(photos)} photos with stricter filters...")
    
    face_service = FaceRecognitionService()
    
    total_faces = 0
    for i, photo in enumerate(photos, 1):
        print(f"\n[{i}/{len(photos)}] Processing: {photo.filename}")
        faces_count = face_service.process_photo(photo, photo.user_id)
        total_faces += faces_count
        print(f"  ✅ Detected {faces_count} face(s)")
    
    print(f"\n🎉 Complete! Detected {total_faces} high-quality faces")
    print(f"Go to http://localhost:3000/label-faces to label them!")
