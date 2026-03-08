import psycopg2

print("🔍 Checking PostgreSQL database...")

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="postgres",
        database="drishyamitra"
    )
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    tables = cursor.fetchall()
    
    print("\n📊 Database Tables:")
    for table in tables:
        print(f"  - {table[0]}")
    
    print("\n📈 Database Statistics:")
    
    # Count records in each table
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  {table_name}: {count} records")
    
    # Get user details if any
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    if user_count > 0:
        print("\n👤 Registered Users:")
        cursor.execute("SELECT id, username, email, created_at FROM users")
        for user in cursor.fetchall():
            print(f"  - ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Created: {user[3]}")
    else:
        print("\n👤 No users registered yet")
    
    cursor.close()
    conn.close()
    
    print("\n✅ PostgreSQL database is ready!")
    print("🌐 Backend: http://localhost:5000")
    print("🎨 Frontend: http://localhost:3000")
    
except Exception as e:
    print(f"❌ Error: {e}")
