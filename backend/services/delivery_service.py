import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from models import db, DeliveryHistory, Photo

try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    GMAIL_AVAILABLE = True
except ImportError:
    GMAIL_AVAILABLE = False

class DeliveryService:
    def __init__(self, app=None):
        self.gmail_creds = None
        self.gmail_service = None
        self.app = app
        
        if not GMAIL_AVAILABLE:
            print("⚠️  Gmail API not configured. Email delivery is disabled.")
            print("   To enable: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        elif app:
            self._init_gmail(app)
    
    def _init_gmail(self, app):
        """Initialize Gmail with app config"""
        client_id = app.config.get('GMAIL_CLIENT_ID')
        client_secret = app.config.get('GMAIL_CLIENT_SECRET')
        refresh_token = app.config.get('GMAIL_REFRESH_TOKEN')
        
        if client_id and client_secret and refresh_token:
            try:
                self.gmail_creds = Credentials(
                    None,
                    refresh_token=refresh_token,
                    token_uri='https://oauth2.googleapis.com/token',
                    client_id=client_id,
                    client_secret=client_secret
                )
                self.gmail_service = build('gmail', 'v1', credentials=self.gmail_creds)
                print("✅ Gmail API configured successfully!")
            except Exception as e:
                print(f"⚠️  Gmail API initialization failed: {e}")
        else:
            print("⚠️  Gmail credentials not found in .env file")
    
    def send_email(self, recipient, photo_ids, user_id, subject="Your Photos from Drishyamitra"):
        """Send photos via Gmail"""
        if not self.gmail_service:
            print(f"📧 Email delivery requested to {recipient} with {len(photo_ids)} photos")
            print("   Gmail API not configured.")
            self._log_delivery(user_id, 'email', recipient, photo_ids, 'failed')
            return {
                'success': False,
                'message': 'Gmail API not configured. Check your .env file.'
            }
        
        try:
            # Get photos
            photos = Photo.query.filter(Photo.id.in_(photo_ids)).all()
            
            # Create message
            message = MIMEMultipart()
            message['to'] = recipient
            message['subject'] = subject
            
            # Email body
            body = f"Hello!\n\nHere are {len(photos)} photos from Drishyamitra.\n\nEnjoy!"
            message.attach(MIMEText(body, 'plain'))
            
            # Attach photos
            for photo in photos:
                if os.path.exists(photo.filepath):
                    with open(photo.filepath, 'rb') as f:
                        img = MIMEImage(f.read())
                        img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(photo.filepath))
                        message.attach(img)
            
            # Send
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            send_message = {'raw': raw_message}
            
            result = self.gmail_service.users().messages().send(
                userId='me',
                body=send_message
            ).execute()
            
            self._log_delivery(user_id, 'email', recipient, photo_ids, 'sent')
            
            print(f"✅ Email sent successfully to {recipient}")
            return {
                'success': True,
                'message': f'Email sent successfully to {recipient}',
                'message_id': result['id']
            }
            
        except Exception as e:
            print(f"❌ Email delivery failed: {e}")
            self._log_delivery(user_id, 'email', recipient, photo_ids, 'failed')
            return {
                'success': False,
                'message': f'Email delivery failed: {str(e)}'
            }
    
    def send_whatsapp(self, recipient, photo_ids, user_id):
        """Send photos via WhatsApp (placeholder - requires WhatsApp Web API setup)"""
        try:
            photos = Photo.query.filter(Photo.id.in_(photo_ids)).all()
            photo_paths = [p.filepath for p in photos if os.path.exists(p.filepath)]
            
            self._log_delivery(user_id, 'whatsapp', recipient, photo_ids, 'pending')
            
            return {
                'success': True,
                'message': f'WhatsApp delivery queued for {len(photo_paths)} photos',
                'note': 'WhatsApp integration requires additional setup'
            }
        
        except Exception as e:
            self._log_delivery(user_id, 'whatsapp', recipient, photo_ids, 'failed')
            return {'success': False, 'message': f'WhatsApp failed: {str(e)}'}
    
    def _log_delivery(self, user_id, delivery_type, recipient, photo_ids, status):
        """Log delivery history"""
        delivery = DeliveryHistory(
            user_id=user_id,
            delivery_type=delivery_type,
            recipient=recipient,
            photo_ids=','.join(map(str, photo_ids)),
            status=status
        )
        db.session.add(delivery)
        db.session.commit()
    
    def get_delivery_history(self, user_id):
        """Get delivery history for user"""
        deliveries = DeliveryHistory.query.filter_by(user_id=user_id).order_by(
            DeliveryHistory.created_at.desc()
        ).limit(50).all()
        
        return [{
            'id': d.id,
            'type': d.delivery_type,
            'recipient': d.recipient,
            'photo_count': len(d.photo_ids.split(',')) if d.photo_ids else 0,
            'status': d.status,
            'date': d.created_at.isoformat()
        } for d in deliveries]
