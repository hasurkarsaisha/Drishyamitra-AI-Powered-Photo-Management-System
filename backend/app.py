import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure CORS to allow frontend domain
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    
    # Build list of allowed origins
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]
    
    # Add production frontend URL if set
    if frontend_url and frontend_url not in allowed_origins:
        allowed_origins.append(frontend_url)
    
    # Also allow any vercel.app domain for this project
    allowed_origins.append("https://laughing-waddle-snowy.vercel.app")
    
    CORS(app, 
         resources={r"/*": {"origins": allowed_origins}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )
    
    db.init_app(app)
    jwt = JWTManager(app)
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        print("DEBUG: JWT token expired")
        print(f"  Header: {jwt_header}")
        print(f"  Payload: {jwt_payload}")
        return jsonify({'error': 'Token has expired'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print(f"DEBUG: Invalid JWT token")
        print(f"  Error: {error}")
        return jsonify({'error': f'Invalid token: {str(error)}'}), 422
    
    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        print(f"DEBUG: No JWT token provided")
        print(f"  Error: {error}")
        return jsonify({'error': f'Missing authorization token: {str(error)}'}), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        print("DEBUG: JWT token revoked")
        return jsonify({'error': 'Token has been revoked'}), 401
    
    # Add root route
    @app.route('/')
    def index():
        return {
            'message': 'Drishyamitra API',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'auth': '/auth/login, /auth/register, /auth/me',
                'photos': '/photos/upload, /photos/search, /photos/<id>',
                'faces': '/faces/unlabeled, /faces/label',
                'chat': '/chat/query, /chat/history',
                'delivery': '/deliver/email, /deliver/whatsapp, /deliver/history'
            },
            'frontend': 'http://localhost:3000'
        }
    
    from routes.auth import auth_bp
    from routes.photos import photos_bp
    from routes.faces import faces_bp
    from routes.chat import chat_bp
    from routes.delivery import delivery_bp
    from routes.bulk_upload import bulk_upload_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(photos_bp, url_prefix='/photos')
    app.register_blueprint(faces_bp, url_prefix='/faces')
    app.register_blueprint(chat_bp, url_prefix='/chat')
    app.register_blueprint(delivery_bp, url_prefix='/deliver')
    app.register_blueprint(bulk_upload_bp, url_prefix='/bulk')
    
    with app.app_context():
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
