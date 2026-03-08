from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    photos = db.relationship('Photo', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Photo(db.Model):
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    processed = db.Column(db.Boolean, default=False)
    
    faces = db.relationship('Face', backref='photo', lazy=True, cascade='all, delete-orphan')
    person_maps = db.relationship('PhotoPersonMap', backref='photo_ref', lazy=True, cascade='all, delete-orphan')

class Person(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reference_embedding = db.Column(db.PickleType, nullable=True)  # Keep one embedding for recognition
    
    faces = db.relationship('Face', backref='person', lazy=True)
    photo_maps = db.relationship('PhotoPersonMap', backref='person_ref', lazy=True, cascade='all, delete-orphan')

class Face(db.Model):
    __tablename__ = 'faces'
    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    embedding = db.Column(db.PickleType, nullable=False)
    bbox = db.Column(db.String(100))
    confidence = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PhotoPersonMap(db.Model):
    __tablename__ = 'photo_person_map'
    __table_args__ = (
        db.UniqueConstraint('photo_id', 'person_id', name='unique_photo_person'),
    )
    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id', ondelete='CASCADE'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id', ondelete='CASCADE'), nullable=False)

class DeliveryHistory(db.Model):
    __tablename__ = 'delivery_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    delivery_type = db.Column(db.String(20), nullable=False)
    recipient = db.Column(db.String(255), nullable=False)
    photo_ids = db.Column(db.String(500))
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChatLog(db.Model):
    __tablename__ = 'chat_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text)
    intent = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
