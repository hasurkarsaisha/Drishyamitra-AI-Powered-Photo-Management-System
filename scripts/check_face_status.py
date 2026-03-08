"""
Check the current status of faces in the database
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app
from models import db, Face, Person, Photo, PhotoPersonMap

app = create_app()

def check_status(user_id=1):
    """Check face and photo status"""
    with app.app_context():
        # Get all faces
        all_faces = Face.query.join(Photo).filter(Photo.user_id == user_id).all()
        labeled_faces = [f for f in all_faces if f.person_id is not None]
        unlabeled_faces = [f for f in all_faces if f.person_id is None]
        
        print(f"\n📊 FACE STATUS:")
        print(f"   Total faces: {len(all_faces)}")
        print(f"   Labeled: {len(labeled_faces)}")
        print(f"   Unlabeled: {len(unlabeled_faces)}")
        
        # Get all people
        people = Person.query.filter_by(user_id=user_id).all()
        print(f"\n👥 PEOPLE ({len(people)} total):")
        for person in people:
            face_count = Face.query.filter_by(person_id=person.id).count()
            photo_count = PhotoPersonMap.query.filter_by(person_id=person.id).count()
            has_ref = "✅" if person.reference_embedding is not None else "❌"
            print(f"   {person.name}: {face_count} faces, {photo_count} photos, ref_emb: {has_ref}")
        
        # Get all photos
        photos = Photo.query.filter_by(user_id=user_id).all()
        processed = [p for p in photos if p.processed]
        unprocessed = [p for p in photos if not p.processed]
        
        print(f"\n📷 PHOTOS:")
        print(f"   Total: {len(photos)}")
        print(f"   Processed: {len(processed)}")
        print(f"   Unprocessed: {len(unprocessed)}")
        
        # Show recent photos with face counts
        print(f"\n📸 RECENT PHOTOS:")
        recent = Photo.query.filter_by(user_id=user_id).order_by(Photo.upload_date.desc()).limit(10).all()
        for photo in recent:
            face_count = Face.query.filter_by(photo_id=photo.id).count()
            labeled_count = Face.query.filter(Face.photo_id == photo.id, Face.person_id.isnot(None)).count()
            print(f"   Photo {photo.id}: {face_count} faces ({labeled_count} labeled) - {photo.filename}")

if __name__ == '__main__':
    check_status()
