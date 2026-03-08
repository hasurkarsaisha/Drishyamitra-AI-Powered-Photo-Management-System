"""Add reference embeddings to existing people"""
import sys
sys.path.insert(0, 'backend')

from sqlalchemy import text

# First add the column
from config import Config
import psycopg2

conn = psycopg2.connect(Config.SQLALCHEMY_DATABASE_URI.replace('postgresql://', 'postgresql://'))
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE people ADD COLUMN IF NOT EXISTS reference_embedding BYTEA")
    conn.commit()
    print("✅ Added reference_embedding column")
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()

cursor.close()
conn.close()

# Now populate the data
from app import create_app
from models import db, Person, Face

app = create_app()

with app.app_context():
    # Populate reference embeddings for existing people
    people = Person.query.all()
    
    print(f"\n📊 Updating {len(people)} people with reference embeddings...")
    
    for person in people:
        if person.reference_embedding is None:
            # Get first labeled face for this person
            face = Face.query.filter_by(person_id=person.id).first()
            if face and face.embedding is not None:
                person.reference_embedding = face.embedding
                print(f"  ✅ {person.name}: Added reference embedding")
    
    db.session.commit()
    
    print(f"\n🎉 Done! People can now be recognized even after deleting photos")
