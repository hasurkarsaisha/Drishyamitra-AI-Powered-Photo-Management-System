from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Face, Photo, Person, PhotoPersonMap
from services.face_recognition import FaceRecognitionService
import os

faces_bp = Blueprint('faces', __name__)
face_service = FaceRecognitionService()

@faces_bp.route('/people', methods=['GET'])
@jwt_required()
def get_people():
    """Get all people with photo counts and avatar info"""
    user_id = int(get_jwt_identity())
    
    # Get all people for this user
    people = Person.query.filter_by(user_id=user_id).all()
    
    # Get photo counts and first face for each person
    people_data = []
    for person in people:
        # Get first face of this person (for avatar)
        first_face = Face.query.filter_by(person_id=person.id).first()
        
        # Count photos
        photo_count = PhotoPersonMap.query.filter_by(person_id=person.id).count()
        
        people_data.append({
            'id': person.id,
            'name': person.name,
            'photo_count': photo_count,
            'avatar_face_id': first_face.id if first_face else None
        })
    
    print(f"📊 Found {len(people_data)} people for user {user_id}")
    
    return jsonify({'people': people_data}), 200

@faces_bp.route('/unlabeled', methods=['GET'])
@jwt_required()
def get_unlabeled_faces():
    user_id = int(get_jwt_identity())
    
    unlabeled_faces = Face.query.join(Photo).filter(
        Photo.user_id == user_id,
        Face.person_id.is_(None)
    ).limit(50).all()
    
    print(f"📊 Found {len(unlabeled_faces)} unlabeled faces for user {user_id}")
    
    # Get suggested matches for each face
    faces_with_suggestions = []
    for face in unlabeled_faces:
        suggestion = face_service.find_matching_person(face.embedding, user_id)
        
        face_data = {
            'id': face.id,
            'photo_id': face.photo_id,
            'bbox': face.bbox,
            'confidence': face.confidence
        }
        
        if suggestion:
            face_data['suggested_person'] = {
                'id': suggestion.id,
                'name': suggestion.name
            }
            print(f"  Face {face.id}: Suggested {suggestion.name}")
        else:
            print(f"  Face {face.id}: No suggestion")
        
        faces_with_suggestions.append(face_data)
    
    return jsonify({'unlabeled_faces': faces_with_suggestions}), 200

@faces_bp.route('/<int:face_id>/crop', methods=['GET'])
@jwt_required()
def get_face_crop(face_id):
    """Get cropped face image"""
    user_id = int(get_jwt_identity())
    
    face = Face.query.get(face_id)
    if not face:
        return jsonify({'error': 'Face not found'}), 404
    
    photo = Photo.query.get(face.photo_id)
    if photo.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get photo path
    filepath = photo.filepath
    if filepath.startswith('backend\\') or filepath.startswith('backend/'):
        filepath = filepath.replace('backend\\', '', 1).replace('backend/', '', 1)
    if not os.path.isabs(filepath):
        filepath = os.path.abspath(filepath)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'Photo file not found'}), 404
    
    # Parse bbox
    try:
        from PIL import Image
        import io
        
        bbox_parts = face.bbox.split(',')
        x, y, w, h = map(int, bbox_parts)
        
        # Open image and crop
        img = Image.open(filepath)
        
        # Add padding
        padding = 20
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(img.width, x + w + padding)
        y2 = min(img.height, y + h + padding)
        
        cropped = img.crop((x1, y1, x2, y2))
        
        # Convert to bytes
        img_io = io.BytesIO()
        cropped.save(img_io, 'JPEG', quality=95)
        img_io.seek(0)
        
        from flask import send_file
        return send_file(img_io, mimetype='image/jpeg')
        
    except Exception as e:
        print(f"Error cropping face: {e}")
        return jsonify({'error': 'Failed to crop face'}), 500

@faces_bp.route('/label', methods=['POST'])
@jwt_required()
def label_face():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data or not data.get('face_id') or not data.get('person_name'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    face_id = data['face_id']
    person_name = data['person_name']
    
    print(f"\n🏷️  Labeling face {face_id} as '{person_name}'")
    
    face = Face.query.get(face_id)
    if not face:
        print(f"  ❌ Face {face_id} not found")
        return jsonify({'error': 'Face not found'}), 404
    
    photo = Photo.query.get(face.photo_id)
    if photo.user_id != user_id:
        print(f"  ❌ Unauthorized")
        return jsonify({'error': 'Unauthorized'}), 403
    
    print(f"  Face bbox: {face.bbox}")
    print(f"  Photo: {photo.filename}")
    
    success = face_service.label_face(face_id, person_name, user_id)
    
    if success:
        print(f"  ✅ Successfully labeled")
        return jsonify({'message': 'Face labeled successfully'}), 200
    else:
        print(f"  ❌ Failed to label")
        return jsonify({'error': 'Failed to label face'}), 500

@faces_bp.route('/<int:face_id>', methods=['DELETE'])
@jwt_required()
def delete_face(face_id):
    """Delete a face (for 'Not a Face' button)"""
    user_id = int(get_jwt_identity())
    
    face = Face.query.get(face_id)
    if not face:
        return jsonify({'error': 'Face not found'}), 404
    
    photo = Photo.query.get(face.photo_id)
    if photo.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(face)
    db.session.commit()
    
    return jsonify({'message': 'Face deleted successfully'}), 200
