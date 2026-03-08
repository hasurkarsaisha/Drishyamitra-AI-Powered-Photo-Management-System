"""Test face detection on a single photo"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app
from models import db, Photo
from services.face_recognition import FaceRecognitionService

app = create_app()

with app.app_context():
    # Get first photo
    photo = Photo.query.first()
    if not photo:
        print("No photos found")
        sys.exit(1)
    
    print(f"Testing photo: {photo.filename}")
    print(f"Path: {photo.filepath}")
    print(f"Exists: {os.path.exists(photo.filepath)}")
    print()
    
    face_service = FaceRecognitionService()
    
    if not face_service.deepface_available:
        print("❌ DeepFace not available!")
        sys.exit(1)
    
    print("Detecting faces...")
    faces = face_service.detect_and_extract_faces(photo.filepath)
    print(f"✅ Found {len(faces)} faces!")
    
    for i, face in enumerate(faces, 1):
        print(f"  Face {i}: confidence={face['confidence']:.2f}, bbox={face['bbox']}")
