import sqlite3

conn = sqlite3.connect('backend/instance/drishyamitra.db')
cur = conn.cursor()
cur.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = [row[0] for row in cur.fetchall()]

print("Tables in SQLite database:")
for table in tables:
    cur.execute(f'SELECT COUNT(*) FROM "{table}"')
    count = cur.fetchone()[0]
    print(f"  {table}: {count} rows")

conn.close()
