"""
Reprocess all photos with updated detection settings
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app
from models import db, Photo, Face, PhotoPersonMap
from services.face_recognition import FaceRecognitionService

app = create_app()

def reprocess_all(user_id=1):
    """Reprocess all photos"""
    with app.app_context():
        photos = Photo.query.filter_by(user_id=user_id).all()
        
        print(f"\n📸 Found {len(photos)} photos to reprocess")
        print("This will delete all existing face detections and re-detect with new settings")
        
        confirm = input("\nContinue? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Cancelled")
            return
        
        face_service = FaceRecognitionService()
        
        total_old_faces = 0
        total_new_faces = 0
        
        for i, photo in enumerate(photos, 1):
            print(f"\n[{i}/{len(photos)}] {photo.filename}")
            
            # Delete old faces
            old_faces = Face.query.filter_by(photo_id=photo.id).all()
            total_old_faces += len(old_faces)
            for face in old_faces:
                db.session.delete(face)
            
            # Delete old mappings
            old_mappings = PhotoPersonMap.query.filter_by(photo_id=photo.id).all()
            for mapping in old_mappings:
                db.session.delete(mapping)
            
            db.session.commit()
            
            # Mark as unprocessed
            photo.processed = False
            db.session.commit()
            
            # Reprocess
            face_count = face_service.process_photo(photo, user_id)
            total_new_faces += face_count
            print(f"  Old: {len(old_faces)} faces → New: {face_count} faces")
        
        print(f"\n✅ Reprocessing complete!")
        print(f"   Total old faces: {total_old_faces}")
        print(f"   Total new faces: {total_new_faces}")
        print(f"   Difference: {total_new_faces - total_old_faces:+d}")

if __name__ == '__main__':
    reprocess_all()
