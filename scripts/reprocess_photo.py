"""
Reprocess a specific photo to detect all faces
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app
from models import db, Photo, Face, PhotoPersonMap
from services.face_recognition import FaceRecognitionService

app = create_app()

def reprocess_photo(photo_id):
    """Reprocess a photo - delete old faces and detect again"""
    with app.app_context():
        photo = Photo.query.get(photo_id)
        if not photo:
            print(f"❌ Photo {photo_id} not found")
            return
        
        print(f"\n📸 Reprocessing: {photo.filename} (ID: {photo.id})")
        
        # Delete old faces
        old_faces = Face.query.filter_by(photo_id=photo_id).all()
        print(f"   Deleting {len(old_faces)} old face detections...")
        for face in old_faces:
            db.session.delete(face)
        
        # Delete old mappings for this photo
        old_mappings = PhotoPersonMap.query.filter_by(photo_id=photo_id).all()
        print(f"   Deleting {len(old_mappings)} old photo-person mappings...")
        for mapping in old_mappings:
            db.session.delete(mapping)
        
        db.session.commit()
        
        # Mark as unprocessed
        photo.processed = False
        db.session.commit()
        
        # Reprocess
        print(f"\n🔍 Detecting faces...")
        face_service = FaceRecognitionService()
        face_count = face_service.process_photo(photo, photo.user_id)
        
        print(f"\n✅ Reprocessing complete!")
        print(f"   Detected: {face_count} faces")
        
        # Show results
        new_faces = Face.query.filter_by(photo_id=photo_id).all()
        labeled = [f for f in new_faces if f.person_id is not None]
        unlabeled = [f for f in new_faces if f.person_id is None]
        
        print(f"   Labeled: {len(labeled)}")
        print(f"   Unlabeled: {len(unlabeled)}")

if __name__ == '__main__':
    photo_id = int(input("Enter photo ID to reprocess: "))
    reprocess_photo(photo_id)
