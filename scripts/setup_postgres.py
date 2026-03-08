import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

print("🔧 Setting up PostgreSQL database...")

# Connect to PostgreSQL server (default postgres database)
try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="postgres",
        database="postgres"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Check if database exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname='drishyamitra'")
    exists = cursor.fetchone()
    
    if exists:
        print("✅ Database 'drishyamitra' already exists")
    else:
        # Create database
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier('drishyamitra')
        ))
        print("✅ Database 'drishyamitra' created successfully")
    
    cursor.close()
    conn.close()
    
    print("\n🔄 Now initializing tables...")
    
    # Connect to the new database and create tables
    import sys
    sys.path.insert(0, 'backend')
    from app import create_app
    app = create_app()
    
    with app.app_context():
        from models import db
        db.create_all()
        print("✅ All tables created successfully!")
    
    print("\n✨ PostgreSQL setup complete!")
    print("📊 Database: postgresql://postgres:***@localhost:5432/drishyamitra")
    
except psycopg2.OperationalError as e:
    print(f"❌ Error connecting to PostgreSQL: {e}")
    print("\n💡 Make sure:")
    print("  1. PostgreSQL is installed and running")
    print("  2. Username is 'postgres' and password is 'postgres'")
    print("  3. PostgreSQL is listening on localhost:5432")
except Exception as e:
    print(f"❌ Error: {e}")
