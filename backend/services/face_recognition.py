import os
import numpy as np
from models import db, Face, Person, PhotoPersonMap

class FaceRecognitionService:
    def __init__(self):
        self.model_name = "Facenet512"
        self.detector_backend = "retinaface"  # Better for difficult cases
        self.distance_metric = "cosine"
        self.threshold = 0.50  # More lenient for different angles/lighting
        self.deepface_available = False
        
        # Try to import DeepFace
        try:
            # Initialize tensorflow first to avoid __version__ AttributeError
            import tensorflow as tf
            # Suppress tensorflow warnings
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
            tf.get_logger().setLevel('ERROR')
            
            from deepface import DeepFace
            self.DeepFace = DeepFace
            self.deepface_available = True
            print("✅ DeepFace loaded successfully!")
        except ImportError as e:
            print(f"⚠️  DeepFace not available. Face detection disabled.")
            print(f"   Error: {e}")
            print("   Install with: pip install deepface tf-keras")
        except Exception as e:
            print(f"⚠️  Error loading DeepFace: {e}")
            print("   Face detection disabled.")
    
    def detect_and_extract_faces(self, image_path):
        """Detect faces and extract embeddings using DeepFace"""
        if not self.deepface_available:
            return []
        
        try:
            # Make sure path is absolute
            if not os.path.isabs(image_path):
                image_path = os.path.abspath(image_path)
            
            if not os.path.exists(image_path):
                print(f"Error: Image file not found: {image_path}")
                return []
            
            # Detect faces and extract embeddings
            faces = self.DeepFace.extract_faces(
                img_path=image_path,
                detector_backend=self.detector_backend,
                enforce_detection=False,
                align=True
            )
            
            results = []
            for face_data in faces:
                # More lenient threshold for group photos
                if face_data['confidence'] < 0.50:  # Lowered from 0.70
                    continue
                
                facial_area = face_data['facial_area']
                w = facial_area['w']
                h = facial_area['h']
                
                # Filter out very small detections (likely noise)
                if w < 20 or h < 20:
                    continue
                
                # Filter out extremely large detections (likely full body/background)
                if w > 800 or h > 800:
                    continue
                
                # Get embedding
                embedding = self.DeepFace.represent(
                    img_path=image_path,
                    model_name=self.model_name,
                    detector_backend=self.detector_backend,
                    enforce_detection=False
                )
                
                if embedding and len(embedding) > 0:
                    bbox = f"{facial_area['x']},{facial_area['y']},{w},{h}"
                    
                    results.append({
                        'embedding': np.array(embedding[0]['embedding']),
                        'bbox': bbox,
                        'confidence': face_data['confidence']
                    })
            
            # Remove duplicate detections (same face detected multiple times)
            results = self._remove_duplicate_faces(results)
            
            return results
            
        except Exception as e:
            print(f"Error detecting faces: {e}")
            return []
    
    def _remove_duplicate_faces(self, faces):
        """Remove duplicate face detections based on bbox overlap and embedding similarity"""
        if len(faces) <= 1:
            return faces
        
        unique_faces = []
        
        for face in faces:
            is_duplicate = False
            
            for existing_face in unique_faces:
                # Check bbox overlap
                bbox1 = [float(x) for x in face['bbox'].split(',')]
                bbox2 = [float(x) for x in existing_face['bbox'].split(',')]
                
                # Calculate IoU (Intersection over Union)
                x1_min, y1_min, w1, h1 = bbox1
                x2_min, y2_min, w2, h2 = bbox2
                
                x1_max, y1_max = x1_min + w1, y1_min + h1
                x2_max, y2_max = x2_min + w2, y2_min + h2
                
                # Calculate intersection
                x_inter_min = max(x1_min, x2_min)
                y_inter_min = max(y1_min, y2_min)
                x_inter_max = min(x1_max, x2_max)
                y_inter_max = min(y1_max, y2_max)
                
                if x_inter_max > x_inter_min and y_inter_max > y_inter_min:
                    inter_area = (x_inter_max - x_inter_min) * (y_inter_max - y_inter_min)
                    bbox1_area = w1 * h1
                    bbox2_area = w2 * h2
                    union_area = bbox1_area + bbox2_area - inter_area
                    iou = inter_area / union_area if union_area > 0 else 0
                    
                    # If bboxes overlap significantly (IoU > 0.5), check embedding similarity
                    if iou > 0.5:
                        distance = self._cosine_distance(face['embedding'], existing_face['embedding'])
                        # If embeddings are very similar (distance < 0.1), it's a duplicate
                        if distance < 0.1:
                            is_duplicate = True
                            break
            
            if not is_duplicate:
                unique_faces.append(face)
        
        print(f"  Removed {len(faces) - len(unique_faces)} duplicate detections")
        return unique_faces
    
    def find_matching_person(self, embedding, user_id, exclude_person_ids=None):
        """Find matching person by comparing embeddings, excluding already matched people"""
        if not self.deepface_available:
            return None
        
        if exclude_person_ids is None:
            exclude_person_ids = set()
        
        # Get ALL labeled faces (not just reference embeddings)
        # This allows matching across different angles/lighting
        known_faces = db.session.query(Face, Person).join(
            Person, Face.person_id == Person.id
        ).filter(
            Person.user_id == user_id,
            Face.person_id.isnot(None),
            Face.embedding.isnot(None),
            ~Person.id.in_(exclude_person_ids) if exclude_person_ids else True
        ).all()
        
        best_match = None
        best_distance = float('inf')
        
        print(f"  🔍 Checking {len(known_faces)} labeled faces (excluding {len(exclude_person_ids)} people)...")
        
        # Check against ALL labeled faces for each person
        person_distances = {}  # Track best distance per person
        
        for face, person in known_faces:
            distance = self._cosine_distance(embedding, face.embedding)
            
            # Track the best (minimum) distance for each person
            if person.id not in person_distances or distance < person_distances[person.id]:
                person_distances[person.id] = distance
        
        # Find the person with the best match
        for person_id, distance in person_distances.items():
            person = Person.query.get(person_id)
            print(f"    - {person.name}: best distance = {distance:.4f} (threshold = {self.threshold})")
            
            if distance < self.threshold and distance < best_distance:
                best_distance = distance
                best_match = person
                print(f"      ✅ New best match!")
        
        if best_match:
            print(f"  ✅ MATCHED to {best_match.name} (distance: {best_distance:.4f})")
        else:
            print(f"  ❌ NO MATCH FOUND (best distance: {best_distance:.4f})")
        
        return best_match
    
    def _cosine_distance(self, emb1, emb2):
        """Calculate cosine distance between embeddings"""
        return 1 - np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    
    def process_photo(self, photo, user_id):
        """Process photo for face detection and recognition"""
        if not self.deepface_available:
            photo.processed = True
            db.session.commit()
            print(f"⚠️  Photo {photo.id} marked as processed (DeepFace not available)")
            return 0
        
        try:
            faces_data = self.detect_and_extract_faces(photo.filepath)
            
            # Track which people have already been matched in this photo
            matched_people_ids = set()
            
            for face_data in faces_data:
                # Try to find matching person, excluding already matched people
                matching_person = self.find_matching_person(
                    face_data['embedding'], 
                    user_id,
                    exclude_person_ids=matched_people_ids
                )
                
                if matching_person:
                    print(f"  ✅ Matched face to: {matching_person.name}")
                    matched_people_ids.add(matching_person.id)  # Mark as used
                else:
                    print(f"  ❓ No match found - will need labeling")
                
                # Create face record
                face = Face(
                    photo_id=photo.id,
                    person_id=matching_person.id if matching_person else None,
                    embedding=face_data['embedding'],
                    bbox=face_data['bbox'],
                    confidence=face_data['confidence']
                )
                db.session.add(face)
                
                # Create photo-person mapping if person identified
                if matching_person:
                    # Check if mapping already exists
                    existing_map = PhotoPersonMap.query.filter_by(
                        photo_id=photo.id,
                        person_id=matching_person.id
                    ).first()
                    
                    if not existing_map:
                        photo_person_map = PhotoPersonMap(
                            photo_id=photo.id,
                            person_id=matching_person.id
                        )
                        db.session.add(photo_person_map)
            
            photo.processed = True
            db.session.commit()
            
            matched_count = len(matched_people_ids)
            unlabeled_count = len(faces_data) - matched_count
            print(f"✅ Photo {photo.id} processed: {len(faces_data)} faces detected ({matched_count} matched, {unlabeled_count} unlabeled)")
            return len(faces_data)
            
        except Exception as e:
            print(f"❌ Error processing photo {photo.id}: {e}")
            photo.processed = True
            db.session.commit()
            return 0
    
    def label_face(self, face_id, person_name, user_id):
        """Label an unknown face with a person name"""
        face = Face.query.get(face_id)
        if not face:
            return False
        
        person = Person.query.filter_by(name=person_name, user_id=user_id).first()
        if not person:
            person = Person(name=person_name, user_id=user_id)
            db.session.add(person)
            db.session.flush()
        
        # Save reference embedding if person doesn't have one
        if person.reference_embedding is None and face.embedding is not None:
            person.reference_embedding = face.embedding
        
        face.person_id = person.id
        
        # Check if mapping already exists
        existing_map = PhotoPersonMap.query.filter_by(
            photo_id=face.photo_id,
            person_id=person.id
        ).first()
        
        if not existing_map:
            photo_person_map = PhotoPersonMap(
                photo_id=face.photo_id,
                person_id=person.id
            )
            db.session.add(photo_person_map)
        
        db.session.commit()
        
        return True
        db.session.commit()
        
        return True
