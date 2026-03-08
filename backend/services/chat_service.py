import os
import re
from datetime import datetime, timedelta
from groq import Groq
from models import db, Photo, Person, PhotoPersonMap, ChatLog

class ChatService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.model = "llama-3.1-8b-instant"  # Updated model
        self.conversation_context = {}  # Store context per user
    
    def parse_query(self, message, user_id):
        """Parse user message and extract intent"""
        # Get conversation context for this user
        context = self.conversation_context.get(user_id, {})
        last_person = context.get('last_person')
        last_photos = context.get('last_photos')
        
        # Build context-aware prompt
        context_info = ""
        if last_person:
            context_info = f"\n\nConversation context:\n- Last person mentioned: {last_person}"
            if last_photos:
                context_info += f"\n- Last search returned {len(last_photos)} photos"
        
        prompt = f"""You are an AI assistant for a photo management system. Analyze this user query:

User query: "{message}"{context_info}

Important context rules:
- If user says "this photos", "these photos", "them", use the last search results
- If user says "her", "him", "his", "their" referring to a person, use the last person mentioned
- If user says "send", "mail", "email" with context, it's an EMAIL intent

Determine the intent:
1. CHAT - greeting/casual (hi, hello, hey, how are you)
2. SEARCH - find photos (show photos, find pictures)
3. GROUP - group photos (group photos, photos with multiple people)
4. SOLO - solo photos (photos of just X alone, solo photos of X)
5. STATS - statistics (how many photos, photo count, statistics)
6. EMAIL - send/mail/email photos (mail photos, send photos, email photos to someone)
7. WHATSAPP - send via WhatsApp

For EMAIL/WHATSAPP requests:
- Extract person name from phrases like "photos of X", "X's photos", "X photos"
- If user says "this/these photos" or "them", use CONTEXT_PHOTOS
- If user says "her/him/his/their", use CONTEXT_PERSON
- Extract recipient email address (format: name@domain.com)

If SEARCH/GROUP/SOLO/EMAIL/WHATSAPP, extract:
- Person name(s) - can be multiple separated by "and" or ","
- Time period (as days_ago number)
- Recipient email/phone if mentioned

Respond in this exact format:
INTENT: <CHAT or SEARCH or GROUP or SOLO or STATS or EMAIL or WHATSAPP>
PERSON: <name(s) or CONTEXT_PERSON or none>
DAYS_AGO: <number or none>
RECIPIENT: <email/phone or none>
USE_CONTEXT_PHOTOS: <yes or no>
RESPONSE: <if CHAT, write a friendly response>"""

        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.7,
                max_tokens=300
            )
            
            result = response.choices[0].message.content
            return self._extract_parsed_data(result)
        except Exception as e:
            print(f"Groq API error: {str(e)}")
            return self._fallback_parse(message)
    
    def _extract_parsed_data(self, response):
        """Extract structured data from Groq response"""
        data = {
            'intent': 'chat',
            'person': None,
            'days_ago': None,
            'recipient': None,
            'chat_response': None,
            'use_context_photos': False
        }
        
        lines = response.strip().split('\n')
        for line in lines:
            if line.startswith('INTENT:'):
                intent = line.split(':', 1)[1].strip().lower()
                data['intent'] = intent
            elif line.startswith('PERSON:'):
                person = line.split(':', 1)[1].strip()
                data['person'] = person if person.lower() not in ['none', ''] else None
            elif line.startswith('DAYS_AGO:'):
                days = line.split(':', 1)[1].strip()
                data['days_ago'] = int(days) if days.lower() != 'none' and days.isdigit() else None
            elif line.startswith('RECIPIENT:'):
                recipient = line.split(':', 1)[1].strip()
                data['recipient'] = recipient if recipient.lower() != 'none' else None
            elif line.startswith('USE_CONTEXT_PHOTOS:'):
                use_context = line.split(':', 1)[1].strip().lower()
                data['use_context_photos'] = use_context == 'yes'
            elif line.startswith('RESPONSE:'):
                data['chat_response'] = line.split(':', 1)[1].strip()
        
        return data
    
    def _fallback_parse(self, message):
        """Fallback parsing if Groq fails"""
        message_lower = message.lower()
        
        # Check for greetings
        greetings = ['hi', 'hello', 'hey', 'sup', 'yo', 'howdy']
        if any(greeting in message_lower.split() for greeting in greetings):
            return {
                'intent': 'chat',
                'person': None,
                'days_ago': None,
                'recipient': None,
                'chat_response': "Hey! 👋 I'm your photo assistant. I can help you find photos, organize them, or send them to people. What would you like to do?",
                'use_context_photos': False
            }
        
        # Check for context references (this, these, them, those)
        context_words = ['this', 'these', 'them', 'those', 'that']
        uses_context = any(word in message_lower.split() for word in context_words)
        
        # Check for email/send intent
        intent = 'search'
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', message)
        
        if ('email' in message_lower or 'mail' in message_lower or 'send' in message_lower):
            intent = 'email'
            # If using context words, use context photos
            if uses_context:
                return {
                    'intent': 'email',
                    'person': 'CONTEXT_PERSON',
                    'days_ago': None,
                    'recipient': email_match.group(0) if email_match else None,
                    'chat_response': None,
                    'use_context_photos': True
                }
        elif 'whatsapp' in message_lower:
            intent = 'whatsapp'
            if uses_context:
                return {
                    'intent': 'whatsapp',
                    'person': 'CONTEXT_PERSON',
                    'days_ago': None,
                    'recipient': email_match.group(0) if email_match else None,
                    'chat_response': None,
                    'use_context_photos': True
                }
        
        # Extract person name - look for "photos of X" or "X photos" or "X's photos"
        person_match = re.search(r'photos?\s+of\s+(\w+)', message_lower)
        if not person_match:
            person_match = re.search(r'(\w+)\'?s?\s+photos?', message_lower)
        if not person_match and not uses_context:
            person_match = re.search(r'photos?\s+(\w+)', message_lower)
        
        person_name = person_match.group(1) if person_match else None
        
        # Don't use context words as person names
        if person_name in context_words:
            person_name = 'CONTEXT_PERSON' if uses_context else None
        
        recipient = email_match.group(0) if email_match else None
        
        return {
            'intent': intent,
            'person': person_name,
            'days_ago': None,
            'recipient': recipient,
            'chat_response': None,
            'use_context_photos': uses_context
        }
    
    def execute_query(self, parsed_data, user_id):
        """Execute the parsed query and return results"""
        intent = parsed_data['intent']
        
        # Handle context references
        context = self.conversation_context.get(user_id, {})
        
        # Replace CONTEXT_PERSON with actual person name
        if parsed_data['person'] == 'CONTEXT_PERSON' and context.get('last_person'):
            parsed_data['person'] = context['last_person']
        
        # Use context photos if requested OR if it's an email/whatsapp with context
        if parsed_data.get('use_context_photos') and context.get('last_photos'):
            # For email/whatsapp with context photos
            if intent in ['email', 'whatsapp']:
                return self._handle_context_delivery(parsed_data, user_id, context)
        
        # If email/whatsapp intent but no explicit person and we have context, use context
        if intent in ['email', 'whatsapp'] and not parsed_data['person'] and context.get('last_photos'):
            return self._handle_context_delivery(parsed_data, user_id, context)
        
        if intent == 'chat':
            return {
                'success': True,
                'message': parsed_data.get('chat_response') or "Hello! I'm your photo assistant. Ask me to find photos or just chat!",
                'intent': 'chat'
            }
        elif intent == 'search':
            result = self._search_photos(parsed_data, user_id)
            # Store context
            if result['success'] and result.get('photos'):
                self._update_context(user_id, parsed_data.get('person'), result['photos'])
            return result
        elif intent == 'group':
            return self._search_group_photos(user_id)
        elif intent == 'solo':
            return self._search_solo_photos(parsed_data, user_id)
        elif intent == 'stats':
            return self._get_stats(user_id)
        elif intent == 'email':
            return self._prepare_email_delivery(parsed_data, user_id)
        elif intent == 'whatsapp':
            return self._prepare_whatsapp_delivery(parsed_data, user_id)
        else:
            return {'success': False, 'message': 'I can help you find photos, send them via email/WhatsApp, or just chat!'}
    
    def _update_context(self, user_id, person, photos):
        """Update conversation context for user"""
        if user_id not in self.conversation_context:
            self.conversation_context[user_id] = {}
        
        if person:
            self.conversation_context[user_id]['last_person'] = person
        if photos:
            self.conversation_context[user_id]['last_photos'] = photos
    
    def _handle_context_delivery(self, parsed_data, user_id, context):
        """Handle delivery using context photos"""
        photos = context.get('last_photos', [])
        person = context.get('last_person', 'these')
        
        if not photos:
            return {
                'success': False,
                'message': "I don't have any photos from our previous conversation. Please search for photos first."
            }
        
        if not parsed_data['recipient']:
            return {
                'success': True,
                'action': 'email_ask_recipient',
                'photos': photos,
                'count': len(photos),
                'message': f"I'll send {len(photos)} photo{'s' if len(photos) != 1 else ''} of {person}. What email address should I use?"
            }
        
        # Actually send the email
        from services.delivery_service import DeliveryService
        from flask import current_app
        
        delivery_service = DeliveryService(current_app)
        
        photo_ids = [p['id'] for p in photos]
        result = delivery_service.send_email(
            recipient=parsed_data['recipient'],
            photo_ids=photo_ids,
            user_id=user_id
        )
        
        if result['success']:
            return {
                'success': True,
                'message': f"✅ Successfully sent {len(photos)} photo{'s' if len(photos) != 1 else ''} of {person} to {parsed_data['recipient']}!"
            }
        else:
            error_msg = result.get('error') or result.get('message') or 'Unknown error'
            return {
                'success': False,
                'message': f"❌ Failed to send email: {error_msg}"
            }
    
    def _search_group_photos(self, user_id):
        """Find photos with 3 or more people"""
        from sqlalchemy import func
        
        # Count people per photo
        photo_person_counts = db.session.query(
            PhotoPersonMap.photo_id,
            func.count(PhotoPersonMap.person_id).label('person_count')
        ).join(Photo).filter(
            Photo.user_id == user_id
        ).group_by(PhotoPersonMap.photo_id).having(
            func.count(PhotoPersonMap.person_id) >= 3
        ).all()
        
        photo_ids = [ppc.photo_id for ppc in photo_person_counts]
        
        if not photo_ids:
            return {'success': False, 'message': 'No group photos found (need 3+ people)'}
        
        photos = Photo.query.filter(Photo.id.in_(photo_ids)).order_by(Photo.upload_date.desc()).all()
        
        return {
            'success': True,
            'photos': [{'id': p.id, 'filename': p.filename, 'date': p.upload_date.isoformat()} for p in photos],
            'count': len(photos),
            'message': f"Found {len(photos)} group photo{'s' if len(photos) != 1 else ''} (3+ people)"
        }
    
    def _search_solo_photos(self, parsed_data, user_id):
        """Find photos with only one specific person"""
        if not parsed_data['person']:
            return {'success': False, 'message': 'Please specify whose solo photos you want'}
        
        # Case-insensitive person search
        all_people = Person.query.filter_by(user_id=user_id).all()
        person = next((p for p in all_people if p.name.lower() == parsed_data['person'].lower()), None)
        
        if not person:
            return {'success': False, 'message': f"Person '{parsed_data['person']}' not found"}
        
        # Find photos where this person appears AND only 1 person total
        from sqlalchemy import func
        
        solo_photo_ids = db.session.query(
            PhotoPersonMap.photo_id
        ).join(Photo).filter(
            Photo.user_id == user_id
        ).group_by(PhotoPersonMap.photo_id).having(
            func.count(PhotoPersonMap.person_id) == 1
        ).all()
        
        solo_photo_ids = [pid[0] for pid in solo_photo_ids]
        
        # Filter to only this person's photos
        person_photo_ids = {pm.photo_id for pm in person.photo_maps}
        final_photo_ids = set(solo_photo_ids) & person_photo_ids
        
        if not final_photo_ids:
            return {'success': False, 'message': f"No solo photos of {person.name} found"}
        
        photos = Photo.query.filter(Photo.id.in_(final_photo_ids)).order_by(Photo.upload_date.desc()).all()
        
        return {
            'success': True,
            'photos': [{'id': p.id, 'filename': p.filename, 'date': p.upload_date.isoformat()} for p in photos],
            'count': len(photos),
            'message': f"Found {len(photos)} solo photo{'s' if len(photos) != 1 else ''} of {person.name}"
        }
    
    def _get_stats(self, user_id):
        """Get photo statistics"""
        total_photos = Photo.query.filter_by(user_id=user_id).count()
        total_people = Person.query.filter_by(user_id=user_id).count()
        
        # Most photographed person
        from sqlalchemy import func
        top_person = db.session.query(
            Person.name,
            func.count(PhotoPersonMap.photo_id).label('photo_count')
        ).join(PhotoPersonMap).filter(
            Person.user_id == user_id
        ).group_by(Person.id).order_by(
            func.count(PhotoPersonMap.photo_id).desc()
        ).first()
        
        stats_message = f"📊 Your Photo Stats:\n\n"
        stats_message += f"• Total photos: {total_photos}\n"
        stats_message += f"• People recognized: {total_people}\n"
        if top_person:
            stats_message += f"• Most photographed: {top_person.name} ({top_person.photo_count} photos)"
        
        return {
            'success': True,
            'message': stats_message,
            'intent': 'stats'
        }
    
    def _search_photos(self, parsed_data, user_id):
        """Search photos based on criteria"""
        query = Photo.query.filter_by(user_id=user_id)
        
        # Handle multiple people search (e.g., "Ayush and Aditya")
        if parsed_data['person']:
            # Split by "and" or "," to get multiple names
            import re
            person_names = re.split(r'\s+and\s+|,\s*', parsed_data['person'])
            person_names = [name.strip() for name in person_names if name.strip()]
            
            if len(person_names) > 1:
                # Find photos with ALL these people (case-insensitive)
                people = Person.query.filter(
                    Person.user_id == user_id
                ).all()
                
                # Case-insensitive matching
                matched_people = []
                for name in person_names:
                    matched = next((p for p in people if p.name.lower() == name.lower()), None)
                    if matched:
                        matched_people.append(matched)
                
                if len(matched_people) != len(person_names):
                    found_names = {p.name.lower() for p in matched_people}
                    missing = [name for name in person_names if name.lower() not in found_names]
                    return {'success': False, 'message': f"Person(s) not found: {', '.join(missing)}"}
                
                # Get photos that have ALL these people
                photo_ids_sets = []
                for person in matched_people:
                    photo_ids = {pm.photo_id for pm in person.photo_maps}
                    photo_ids_sets.append(photo_ids)
                
                # Intersection - photos with ALL people
                common_photo_ids = set.intersection(*photo_ids_sets) if photo_ids_sets else set()
                
                if not common_photo_ids:
                    names_str = " and ".join([p.name for p in matched_people])
                    return {'success': False, 'message': f"No photos found with {names_str} together"}
                
                query = query.filter(Photo.id.in_(common_photo_ids))
            else:
                # Single person search (case-insensitive)
                person = Person.query.filter(
                    Person.user_id == user_id
                ).all()
                
                # Case-insensitive matching
                matched_person = next((p for p in person if p.name.lower() == person_names[0].lower()), None)
                
                if matched_person:
                    photo_ids = [pm.photo_id for pm in matched_person.photo_maps]
                    query = query.filter(Photo.id.in_(photo_ids))
                else:
                    return {'success': False, 'message': f"Person '{person_names[0]}' not found"}
        
        if parsed_data['days_ago']:
            date_threshold = datetime.utcnow() - timedelta(days=parsed_data['days_ago'])
            query = query.filter(Photo.upload_date >= date_threshold)
        
        photos = query.order_by(Photo.upload_date.desc()).all()
        
        result = {
            'success': True,
            'photos': [{'id': p.id, 'filename': p.filename, 'date': p.upload_date.isoformat()} for p in photos],
            'count': len(photos),
            'message': f"Found {len(photos)} photo{'s' if len(photos) != 1 else ''}"
        }
        
        # Store context
        if parsed_data['person']:
            self._update_context(user_id, parsed_data['person'], result['photos'])
        
        return result
    
    def _prepare_email_delivery(self, parsed_data, user_id):
        """Prepare photos for email delivery"""
        # Check if we should use context
        context = self.conversation_context.get(user_id, {})
        
        # If we have context photos and no specific person mentioned, use context
        if context.get('last_photos') and not parsed_data.get('person'):
            return self._handle_context_delivery(parsed_data, user_id, context)
        
        # Otherwise do a new search
        search_result = self._search_photos(parsed_data, user_id)
        
        if not search_result['success']:
            return search_result
        
        # Check if recipient email is provided
        if not parsed_data['recipient']:
            return {
                'success': True,
                'action': 'email_ask_recipient',
                'photos': search_result['photos'],
                'count': search_result['count'],
                'message': f"I found {search_result['count']} photo{'s' if search_result['count'] != 1 else ''}. What email address should I send them to?"
            }
        
        # Actually send the email
        from services.delivery_service import DeliveryService
        from flask import current_app
        
        delivery_service = DeliveryService(current_app)
        
        photo_ids = [p['id'] for p in search_result['photos']]
        result = delivery_service.send_email(
            recipient=parsed_data['recipient'],
            photo_ids=photo_ids,
            user_id=user_id
        )
        
        if result['success']:
            return {
                'success': True,
                'message': f"✅ Successfully sent {search_result['count']} photo{'s' if search_result['count'] != 1 else ''} to {parsed_data['recipient']}!"
            }
        else:
            error_msg = result.get('error') or result.get('message') or 'Unknown error'
            return {
                'success': False,
                'message': f"❌ Failed to send email: {error_msg}"
            }
    
    def _prepare_whatsapp_delivery(self, parsed_data, user_id):
        """Prepare photos for WhatsApp delivery"""
        search_result = self._search_photos(parsed_data, user_id)
        
        if not search_result['success']:
            return search_result
        
        return {
            'success': True,
            'action': 'whatsapp',
            'photos': search_result['photos'],
            'recipient': parsed_data['recipient'],
            'message': f"Ready to send {search_result['count']} photos via WhatsApp"
        }
    
    def log_chat(self, user_id, message, response, intent):
        """Log chat interaction"""
        chat_log = ChatLog(
            user_id=user_id,
            message=message,
            response=str(response),
            intent=intent
        )
        db.session.add(chat_log)
        db.session.commit()
