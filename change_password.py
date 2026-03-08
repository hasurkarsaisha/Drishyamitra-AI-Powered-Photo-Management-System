"""
Change user password
"""
import sys
sys.path.insert(0, 'backend')

from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def change_password(username, new_password):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        
        if not user:
            print(f"❌ User '{username}' not found!")
            return
        
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        
        print(f"✅ Password changed successfully for user '{username}'!")
        print(f"   New password: {new_password}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python change_password.py <username> <new_password>")
        print("Example: python change_password.py ayush newpassword123")
    else:
        username = sys.argv[1]
        new_password = sys.argv[2]
        change_password(username, new_password)
