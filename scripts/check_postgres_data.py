import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="postgres",
        database="drishyamitra"
    )
    cur = conn.cursor()
    
    print("📊 Checking PostgreSQL database: drishyamitra")
    print()
    
    # Get all tables
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    tables = [row[0] for row in cur.fetchall()]
    
    if not tables:
        print("❌ No tables found in database!")
    else:
        print(f"✅ Found {len(tables)} tables:")
        print()
        
        for table in tables:
            cur.execute(f'SELECT COUNT(*) FROM "{table}"')
            count = cur.fetchone()[0]
            print(f"  📦 {table}: {count} rows")
            
            # Show sample data for non-empty tables
            if count > 0:
                cur.execute(f'SELECT * FROM "{table}" LIMIT 3')
                rows = cur.fetchall()
                if rows:
                    # Get column names
                    cur.execute(f"""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = '{table}'
                        ORDER BY ordinal_position
                    """)
                    columns = [row[0] for row in cur.fetchall()]
                    print(f"      Columns: {', '.join(columns[:5])}...")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
