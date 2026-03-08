from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.delivery_service import DeliveryService

delivery_bp = Blueprint('delivery', __name__)

def get_delivery_service():
    """Get or create delivery service with current app context"""
    if not hasattr(current_app, 'delivery_service'):
        current_app.delivery_service = DeliveryService(current_app)
    return current_app.delivery_service

@delivery_bp.route('/email', methods=['POST'])
@jwt_required()
def send_email():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data or not data.get('recipient') or not data.get('photo_ids'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    recipient = data['recipient']
    photo_ids = data['photo_ids']
    subject = data.get('subject', 'Your Photos from Drishyamitra')
    
    delivery_service = get_delivery_service()
    result = delivery_service.send_email(recipient, photo_ids, user_id, subject)
    
    return jsonify(result), 200 if result['success'] else 500

@delivery_bp.route('/whatsapp', methods=['POST'])
@jwt_required()
def send_whatsapp():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data or not data.get('recipient') or not data.get('photo_ids'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    recipient = data['recipient']
    photo_ids = data['photo_ids']
    
    delivery_service = get_delivery_service()
    result = delivery_service.send_whatsapp(recipient, photo_ids, user_id)
    
    return jsonify(result), 200 if result['success'] else 500

@delivery_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    user_id = int(get_jwt_identity())
    delivery_service = get_delivery_service()
    history = delivery_service.get_delivery_history(user_id)
    
    return jsonify({'history': history}), 200
