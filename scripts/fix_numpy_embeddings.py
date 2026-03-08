"""
Fix numpy embedding compatibility issue by removing face data
"""
import psycopg2

print("🔧 Fixing numpy embedding compatibility...")
print("⚠️  This will delete face detection data (photos and people will remain)")
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
    
    # Delete all faces (they have embeddings that can't be loaded)
    print("Deleting face records...")
    cur.execute('DELETE FROM faces')
    faces_deleted = cur.rowcount
    print(f"  ✅ Deleted {faces_deleted} face records")
    
    # Clear reference embeddings from people table (set to NULL is allowed here)
    print("Clearing people reference embeddings...")
    cur.execute('UPDATE people SET reference_embedding = NULL WHERE reference_embedding IS NOT NULL')
    people_updated = cur.rowcount
    print(f"  ✅ Cleared {people_updated} people reference embeddings")
    
    conn.commit()
    
    print()
    print("✅ Done! Face data cleared.")
    print()
    print("📝 Your photos and people names are still there!")
    print("📝 Next steps:")
    print("  1. Restart the backend (it should work now)")
    print("  2. Re-upload photos to regenerate face detections")
    print("  OR run: python reprocess_all_photos.py")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
