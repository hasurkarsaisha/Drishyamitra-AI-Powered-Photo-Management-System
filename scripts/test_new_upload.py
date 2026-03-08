"""
Test uploading a new photo to see if faces are auto-matched
"""
import sys
import os
import shutil

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app
from models import db, Face, Person, Photo
from services.face_recognition import FaceRecognitionService

app = create_app()

def test_upload(source_photo_path, user_id=1):
    """Simulate uploading a photo"""
    with app.app_context():
        face_service = FaceRecognitionService()
        
        # Copy photo to upload folder
        from config import Config
        user_folder = os.path.join(Config.UPLOAD_FOLDER, str(user_id))
        os.makedirs(user_folder, exist_ok=True)
        
        filename = os.path.basename(source_photo_path)
        dest_path = os.path.join(user_folder, f"test_{filename}")
        
        print(f"\n📤 Simulating upload of: {filename}")
        print(f"   Source: {source_photo_path}")
        print(f"   Dest: {dest_path}")
        
        if not os.path.exists(source_photo_path):
            print(f"❌ Source file not found!")
            return
        
        shutil.copy2(source_photo_path, dest_path)
        
        # Create photo record
        photo = Photo(
            user_id=user_id,
            filename=filename,
            filepath=dest_path
        )
        db.session.add(photo)
        db.session.flush()
        
        print(f"✅ Photo record created: ID {photo.id}")
        
        # Process for faces
        print(f"\n🔍 Processing for faces...")
        face_count = face_service.process_photo(photo, user_id)
        
        print(f"\n✅ Processing complete!")
        print(f"   Faces detected: {face_count}")
        
        # Check results
        faces = Face.query.filter_by(photo_id=photo.id).all()
        labeled = [f for f in faces if f.person_id is not None]
        unlabeled = [f for f in faces if f.person_id is None]
        
        print(f"\n📊 RESULTS:")
        print(f"   Total faces: {len(faces)}")
        print(f"   Auto-labeled: {len(labeled)}")
        print(f"   Need labeling: {len(unlabeled)}")
        
        if labeled:
            print(f"\n✅ AUTO-LABELED FACES:")
            for face in labeled:
                person = Person.query.get(face.person_id)
                print(f"   - {person.name}")
        
        if unlabeled:
            print(f"\n❓ UNLABELED FACES:")
            for face in unlabeled:
                print(f"   - Face {face.id} (confidence: {face.confidence:.2f})")

if __name__ == '__main__':
    # Test with one of the existing photos
    test_photo = "Data-shots/IMG_2920.JPG"
    if os.path.exists(test_photo):
        test_upload(test_photo)
    else:
        print(f"Test photo not found: {test_photo}")
        print("Available photos in Data-shots:")
        if os.path.exists("Data-shots"):
            for f in os.listdir("Data-shots")[:5]:
                print(f"  - {f}")
