from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.chat_service import ChatService

chat_bp = Blueprint('chat', __name__)
chat_service = ChatService()

@chat_bp.route('/query', methods=['POST'])
@jwt_required()
def chat_query():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data or not data.get('message'):
        return jsonify({'error': 'Message is required'}), 400
    
    message = data['message']
    
    parsed_data = chat_service.parse_query(message, user_id)
    result = chat_service.execute_query(parsed_data, user_id)
    
    chat_service.log_chat(user_id, message, result, parsed_data['intent'])
    
    return jsonify(result), 200

@chat_bp.route('/history', methods=['GET'])
@jwt_required()
def chat_history():
    user_id = int(get_jwt_identity())
    
    from models import ChatLog
    logs = ChatLog.query.filter_by(user_id=user_id).order_by(
        ChatLog.created_at.desc()
    ).limit(50).all()
    
    return jsonify({
        'history': [{
            'id': log.id,
            'message': log.message,
            'response': log.response,
            'intent': log.intent,
            'timestamp': log.created_at.isoformat()
        } for log in logs]
    }), 200

@chat_bp.route('/history', methods=['DELETE'])
@jwt_required()
def clear_chat_history():
    user_id = int(get_jwt_identity())
    
    from models import ChatLog, db
    try:
        # Delete all chat logs for this user
        ChatLog.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Chat history cleared successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
