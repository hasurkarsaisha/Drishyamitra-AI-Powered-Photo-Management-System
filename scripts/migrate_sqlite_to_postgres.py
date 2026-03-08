"""
Migrate data from SQLite to PostgreSQL
"""
import sqlite3
import psycopg2
from psycopg2.extras import execute_values
import sys

print("🔄 Migrating data from SQLite to PostgreSQL...")
print()

# SQLite connection
sqlite_db = "backend/instance/drishyamitra.db"
try:
    sqlite_conn = sqlite3.connect(sqlite_db)
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cur = sqlite_conn.cursor()
    print(f"✅ Connected to SQLite: {sqlite_db}")
except Exception as e:
    print(f"❌ Error connecting to SQLite: {e}")
    sys.exit(1)

# PostgreSQL connection
try:
    pg_conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="postgres",
        database="drishyamitra"
    )
    pg_cur = pg_conn.cursor()
    print(f"✅ Connected to PostgreSQL: drishyamitra")
    print()
except Exception as e:
    print(f"❌ Error connecting to PostgreSQL: {e}")
    print("Make sure PostgreSQL is running and database exists!")
    sys.exit(1)

# Tables to migrate (in order due to foreign keys)
tables = [
    'user',
    'person', 
    'photo',
    'face',
    'photo_person_map',
    'delivery_history'
]

try:
    # Clear existing data in PostgreSQL (in reverse order)
    print("🗑️  Clearing existing PostgreSQL data...")
    for table in reversed(tables):
        try:
            pg_cur.execute(f'TRUNCATE TABLE "{table}" CASCADE')
            print(f"  Cleared: {table}")
        except Exception as e:
            print(f"  Warning: Could not clear {table}: {e}")
    pg_conn.commit()
    print()
    
    # Migrate each table
    for table in tables:
        print(f"📦 Migrating table: {table}")
        
        # Get all rows from SQLite
        sqlite_cur.execute(f'SELECT * FROM "{table}"')
        rows = sqlite_cur.fetchall()
        
        if not rows:
            print(f"  ⚠️  No data in {table}")
            continue
        
        # Get column names
        columns = [description[0] for description in sqlite_cur.description]
        
        # Prepare INSERT statement
        cols_str = ', '.join([f'"{col}"' for col in columns])
        placeholders = ', '.join(['%s'] * len(columns))
        insert_sql = f'INSERT INTO "{table}" ({cols_str}) VALUES ({placeholders})'
        
        # Convert rows to tuples
        data = [tuple(row) for row in rows]
        
        # Insert data
        try:
            execute_values(pg_cur, insert_sql, data, page_size=100)
            pg_conn.commit()
            print(f"  ✅ Migrated {len(rows)} rows")
        except Exception as e:
            print(f"  ❌ Error migrating {table}: {e}")
            pg_conn.rollback()
            continue
    
    print()
    print("🎉 Migration completed!")
    print()
    
    # Show summary
    print("📊 Summary:")
    for table in tables:
        pg_cur.execute(f'SELECT COUNT(*) FROM "{table}"')
        count = pg_cur.fetchone()[0]
        print(f"  {table}: {count} rows")
    
    # Reset sequences for auto-increment columns
    print()
    print("🔧 Resetting sequences...")
    for table in tables:
        try:
            pg_cur.execute(f"""
                SELECT setval(pg_get_serial_sequence('"{table}"', 'id'), 
                       COALESCE((SELECT MAX(id) FROM "{table}"), 1), 
                       true)
            """)
            print(f"  ✅ Reset sequence for {table}")
        except Exception as e:
            print(f"  ⚠️  No sequence for {table} (might not have id column)")
    
    pg_conn.commit()
    
except Exception as e:
    print(f"❌ Migration failed: {e}")
    pg_conn.rollback()
    sys.exit(1)
finally:
    sqlite_conn.close()
    pg_conn.close()

print()
print("✨ All done! You can now use PostgreSQL with your existing data.")
