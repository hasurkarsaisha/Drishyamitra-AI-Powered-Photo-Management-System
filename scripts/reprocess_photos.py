"""
Reprocess existing photos to detect faces with DeepFace
"""
import sys
sys.path.insert(0, 'backend')

from app import create_app
from models import db, Photo
from services.face_recognition import FaceRecognitionService

app = create_app()

with app.app_context():
    # Get all unprocessed or processed photos
    photos = Photo.query.all()
    
    print(f"🔍 Found {len(photos)} photos to process")
    
    face_service = FaceRecognitionService()
    
    total_faces = 0
    for i, photo in enumerate(photos, 1):
        print(f"\n[{i}/{len(photos)}] Processing: {photo.filename}")
        
        # Reset processed flag
        photo.processed = False
        db.session.commit()
        
        # Process photo
        faces_count = face_service.process_photo(photo, photo.user_id)
        total_faces += faces_count
        
        print(f"  ✅ Detected {faces_count} face(s)")
    
    print(f"\n🎉 Complete! Detected {total_faces} faces in {len(photos)} photos")
