import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import db, Photo
from services.face_recognition import FaceRecognitionService
from config import Config

bulk_upload_bp = Blueprint('bulk_upload', __name__)
face_service = FaceRecognitionService()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@bulk_upload_bp.route('/import-folder', methods=['POST'])
@jwt_required()
def import_folder():
    """Import all photos from a specified folder path"""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data or not data.get('folder_path'):
        return jsonify({'error': 'Folder path is required'}), 400
    
    folder_path = data['folder_path']
    
    if not os.path.exists(folder_path):
        return jsonify({'error': 'Folder path does not exist'}), 400
    
    if not os.path.isdir(folder_path):
        return jsonify({'error': 'Path is not a directory'}), 400
    
    # Get all image files from folder
    imported = []
    skipped = []
    errors = []
    
    for filename in os.listdir(folder_path):
        if not allowed_file(filename):
            skipped.append(filename)
            continue
        
        try:
            source_path = os.path.join(folder_path, filename)
            
            # Create user folder
            user_folder = os.path.join(Config.UPLOAD_FOLDER, str(user_id))
            os.makedirs(user_folder, exist_ok=True)
            
            # Generate unique filename
            safe_filename = secure_filename(filename)
            dest_path = os.path.join(user_folder, safe_filename)
            
            counter = 1
            while os.path.exists(dest_path):
                name, ext = os.path.splitext(safe_filename)
                dest_path = os.path.join(user_folder, f"{name}_{counter}{ext}")
                counter += 1
            
            # Copy file
            import shutil
            shutil.copy2(source_path, dest_path)
            
            # Create database entry
            photo = Photo(
                user_id=user_id,
                filename=os.path.basename(dest_path),
                filepath=dest_path
            )
            db.session.add(photo)
            db.session.flush()
            
            # Process for face recognition
            try:
                face_count = face_service.process_photo(photo, user_id)
                imported.append({
                    'filename': filename,
                    'photo_id': photo.id,
                    'faces_detected': face_count
                })
            except Exception as e:
                imported.append({
                    'filename': filename,
                    'photo_id': photo.id,
                    'faces_detected': 0,
                    'note': 'Face detection failed'
                })
            
        except Exception as e:
            errors.append({
                'filename': filename,
                'error': str(e)
            })
    
    db.session.commit()
    
    return jsonify({
        'message': 'Bulk import completed',
        'imported': len(imported),
        'skipped': len(skipped),
        'errors': len(errors),
        'details': {
            'imported': imported,
            'skipped': skipped,
            'errors': errors
        }
    }), 200

@bulk_upload_bp.route('/upload-multiple', methods=['POST'])
@jwt_required()
def upload_multiple():
    """Upload multiple files at once"""
    try:
        user_id = int(get_jwt_identity())
        
        print(f"DEBUG: user_id = {user_id}")
        print(f"DEBUG: request.files = {request.files}")
        print(f"DEBUG: request.form = {request.form}")
        
        if 'files' not in request.files:
            print("DEBUG: No 'files' in request.files")
            return jsonify({'error': 'No files provided'}), 400
    except Exception as e:
        print(f"Error in upload_multiple: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 422
    
    files = request.files.getlist('files')
    
    if not files:
        return jsonify({'error': 'No files selected'}), 400
    
    imported = []
    skipped = []
    errors = []
    
    for file in files:
        if file.filename == '':
            skipped.append({'filename': 'empty', 'reason': 'No filename'})
            continue
        
        if not allowed_file(file.filename):
            skipped.append({'filename': file.filename, 'reason': 'Invalid file type'})
            continue
        
        try:
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
            db.session.flush()
            
            try:
                face_count = face_service.process_photo(photo, user_id)
                imported.append({
                    'filename': file.filename,
                    'photo_id': photo.id,
                    'faces_detected': face_count
                })
            except Exception as e:
                imported.append({
                    'filename': file.filename,
                    'photo_id': photo.id,
                    'faces_detected': 0
                })
        
        except Exception as e:
            errors.append({
                'filename': file.filename,
                'error': str(e)
            })
    
    db.session.commit()
    
    total_faces = sum(item.get('faces_detected', 0) for item in imported)
    
    return jsonify({
        'message': 'Multiple upload completed',
        'imported': len(imported),
        'skipped': len(skipped),
        'errors': len(errors),
        'total_faces': total_faces,
        'details': {
            'imported': imported,
            'skipped': skipped,
            'errors': errors
        }
    }), 200
