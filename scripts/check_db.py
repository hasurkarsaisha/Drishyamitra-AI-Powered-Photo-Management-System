import sqlite3

conn = sqlite3.connect('backend/instance/drishyamitra.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("📊 Database Tables:")
for table in tables:
    print(f"  - {table[0]}")

print("\n📈 Database Statistics:")

# Count users
cursor.execute("SELECT COUNT(*) FROM users")
users = cursor.fetchone()[0]
print(f"  Users: {users}")

# Count photos
cursor.execute("SELECT COUNT(*) FROM photos")
photos = cursor.fetchone()[0]
print(f"  Photos: {photos}")

# Count people
cursor.execute("SELECT COUNT(*) FROM people")
people = cursor.fetchone()[0]
print(f"  People: {people}")

# Count faces
cursor.execute("SELECT COUNT(*) FROM face")
faces = cursor.fetchone()[0]
print(f"  Faces: {faces}")

# Get user details
if users > 0:
    print("\n👤 Registered Users:")
    cursor.execute("SELECT id, username, email, created_at FROM user")
    for user in cursor.fetchall():
        print(f"  - ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Created: {user[3]}")

conn.close()
print("\n✅ Database check complete!")
