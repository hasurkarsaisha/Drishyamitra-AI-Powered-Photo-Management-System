import os
from flask import Blueprint, request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import db, Photo, Person, PhotoPersonMap
from services.face_recognition import FaceRecognitionService
from config import Config

photos_bp = Blueprint('photos', __name__)
face_service = FaceRecognitionService()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@photos_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_photo():
    try:
        user_id = int(get_jwt_identity())
        
        print(f"DEBUG: user_id = {user_id}")
        print(f"DEBUG: request.files = {request.files}")
        print(f"DEBUG: request.form = {request.form}")
        
        if 'file' not in request.files:
            print("DEBUG: No 'file' in request.files")
            return jsonify({'error': 'No file provided'}), 400
    except Exception as e:
        print(f"Error in upload_photo: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 422
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    filename = secure_filename(file.filename)
    user_folder = os.path.join(Config.UPLOAD_FOLDER, str(user_id))
    os.makedirs(user_folder, exist_ok=True)
    
    filepath = os.path.join(user_folder, filename)
    counter = 1
    while os.path.exists(filepath):
        name, ext = os.path.splitext(filename)
        filepath = os.path.join(user_folder, f"{name}_{counter}{ext}")
        counter += 1
    
    file.save(filepath)
    
    photo = Photo(user_id=user_id, filename=os.path.basename(filepath), filepath=filepath)
    db.session.add(photo)
    db.session.commit()
    
    try:
        face_count = face_service.process_photo(photo, user_id)
        return jsonify({
            'message': 'Photo uploaded successfully',
            'photo_id': photo.id,
            'faces_detected': face_count
        }), 201
    except Exception as e:
        return jsonify({
            'message': 'Photo uploaded but processing failed',
            'photo_id': photo.id,
            'error': str(e)
        }), 201

@photos_bp.route('/search', methods=['GET'])
@jwt_required()
def search_photos():
    try:
        user_id = int(get_jwt_identity())
        person_name = request.args.get('person')
        
        query = Photo.query.filter_by(user_id=user_id)
    except Exception as e:
        print(f"Error in search_photos: {e}")
        return jsonify({'error': str(e)}), 422
    
    if person_name:
        person = Person.query.filter_by(name=person_name, user_id=user_id).first()
        if person:
            photo_ids = [pm.photo_id for pm in person.photo_maps]
            query = query.filter(Photo.id.in_(photo_ids))
    
    photos = query.order_by(Photo.upload_date.desc()).all()
    
    return jsonify({
        'photos': [{
            'id': p.id,
            'filename': p.filename,
            'upload_date': p.upload_date.isoformat(),
            'processed': p.processed
        } for p in photos]
    }), 200

@photos_bp.route('/<int:photo_id>', methods=['GET'])
@jwt_required()
def get_photo(photo_id):
    user_id = int(get_jwt_identity())
    photo = Photo.query.filter_by(id=photo_id, user_id=user_id).first()
    
    if not photo:
        return jsonify({'error': 'Photo not found'}), 404
    
    # Handle path - remove 'backend/' prefix if present since we're already in backend dir
    filepath = photo.filepath
    if filepath.startswith('backend\\') or filepath.startswith('backend/'):
        filepath = filepath.replace('backend\\', '', 1).replace('backend/', '', 1)
    
    # Make absolute from current directory
    if not os.path.isabs(filepath):
        filepath = os.path.abspath(filepath)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'Photo file not found on disk'}), 404
    
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    
    return send_from_directory(directory, filename)

@photos_bp.route('/<int:photo_id>', methods=['DELETE'])
@jwt_required()
def delete_photo(photo_id):
    """Delete a photo and its file"""
    user_id = int(get_jwt_identity())
    photo = Photo.query.filter_by(id=photo_id, user_id=user_id).first()
    
    if not photo:
        return jsonify({'error': 'Photo not found'}), 404
    
    # Delete file from disk
    filepath = photo.filepath
    if filepath.startswith('backend\\') or filepath.startswith('backend/'):
        filepath = filepath.replace('backend\\', '', 1).replace('backend/', '', 1)
    if not os.path.isabs(filepath):
        filepath = os.path.abspath(filepath)
    
    if os.path.exists(filepath):
        os.remove(filepath)
    
    # Delete from database (cascade will delete faces and mappings)
    db.session.delete(photo)
    db.session.commit()
    
    return jsonify({'message': 'Photo deleted successfully'}), 200

@photos_bp.route('/people', methods=['GET'])
@jwt_required()
def get_people():
    user_id = int(get_jwt_identity())
    people = Person.query.filter_by(user_id=user_id).all()
    
    result = []
    for person in people:
        photo_count = len(person.photo_maps)
        result.append({
            'id': person.id,
            'name': person.name,
            'photo_count': photo_count
        })
    
    return jsonify({'people': result}), 200

@photos_bp.route('/people/<int:person_id>/photos', methods=['GET'])
@jwt_required()
def get_person_photos(person_id):
    user_id = int(get_jwt_identity())
    person = Person.query.filter_by(id=person_id, user_id=user_id).first()
    
    if not person:
        return jsonify({'error': 'Person not found'}), 404
    
    photos = [Photo.query.get(pm.photo_id) for pm in person.photo_maps]
    
    return jsonify({
        'person': person.name,
        'photos': [{
            'id': p.id,
            'filename': p.filename,
            'upload_date': p.upload_date.isoformat()
        } for p in photos if p]
    }), 200

@photos_bp.route('/<int:photo_id>/faces', methods=['GET'])
@jwt_required()
def get_photo_faces(photo_id):
    """Get all faces detected in a specific photo"""
    user_id = int(get_jwt_identity())
    photo = Photo.query.filter_by(id=photo_id, user_id=user_id).first()
    
    if not photo:
        return jsonify({'error': 'Photo not found'}), 404
    
    from models import Face
    # Order by ID to ensure consistent ordering
    faces = Face.query.filter_by(photo_id=photo_id).order_by(Face.id).all()
    
    print(f"\n📸 Photo {photo_id}: Found {len(faces)} faces")
    
    result = []
    for face in faces:
        face_data = {
            'id': face.id,
            'bbox': face.bbox,
            'confidence': face.confidence,
            'person_name': None
        }
        
        if face.person_id:
            person = Person.query.get(face.person_id)
            if person:
                face_data['person_name'] = person.name
                print(f"  Face {face.id}: {person.name} at {face.bbox}")
        else:
            print(f"  Face {face.id}: UNLABELED at {face.bbox}")
            # Get suggestion for unlabeled face
            suggestion = face_service.find_matching_person(face.embedding, user_id)
            if suggestion:
                face_data['suggested_person'] = {
                    'id': suggestion.id,
                    'name': suggestion.name
                }
                print(f"    Suggestion: {suggestion.name}")
        
        result.append(face_data)
    
    return jsonify({'faces': result}), 200
