"""
Fix photos 21 and 22 to detect all faces
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app
from models import db, Photo, Face, PhotoPersonMap
from services.face_recognition import FaceRecognitionService

app = create_app()

def fix_photos():
    """Reprocess photos 21 and 22"""
    with app.app_context():
        face_service = FaceRecognitionService()
        
        for photo_id in [21, 22]:
            photo = Photo.query.get(photo_id)
            if not photo:
                print(f"❌ Photo {photo_id} not found")
                continue
            
            print(f"\n📸 Reprocessing: {photo.filename} (ID: {photo.id})")
            
            # Delete old faces
            old_faces = Face.query.filter_by(photo_id=photo_id).all()
            print(f"   Deleting {len(old_faces)} old face detections...")
            for face in old_faces:
                db.session.delete(face)
            
            # Delete old mappings
            old_mappings = PhotoPersonMap.query.filter_by(photo_id=photo_id).all()
            print(f"   Deleting {len(old_mappings)} old mappings...")
            for mapping in old_mappings:
                db.session.delete(mapping)
            
            db.session.commit()
            
            # Mark as unprocessed
            photo.processed = False
            db.session.commit()
            
            # Reprocess
            print(f"   Detecting faces with new settings...")
            face_count = face_service.process_photo(photo, photo.user_id)
            
            print(f"   ✅ Detected: {face_count} faces")

if __name__ == '__main__':
    fix_photos()
