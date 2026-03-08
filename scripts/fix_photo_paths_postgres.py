"""
Fix photo file paths in PostgreSQL database
"""
import psycopg2
import os

print("🔧 Fixing photo file paths...")
print()

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="postgres",
        database="drishyamitra"
    )
    cur = conn.cursor()
    
    # Get all photos
    cur.execute('SELECT id, filepath FROM photos')
    photos = cur.fetchall()
    
    print(f"Found {len(photos)} photos in database")
    print()
    
    fixed = 0
    for photo_id, filepath in photos:
        # Check if file exists
        if not os.path.exists(filepath):
            # Try with backend/ prefix
            new_path = os.path.join('backend', filepath)
            if os.path.exists(new_path):
                print(f"✅ Fixing: {filepath} → {new_path}")
                cur.execute('UPDATE photos SET filepath = %s WHERE id = %s', (new_path, photo_id))
                fixed += 1
            else:
                print(f"❌ Not found: {filepath}")
    
    conn.commit()
    
    print()
    print(f"✅ Fixed {fixed} photo paths")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
