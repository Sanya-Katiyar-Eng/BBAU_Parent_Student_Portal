import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn





"""import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL =", DATABASE_URL)

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("SELECT current_database();")
print("Database:", cur.fetchone())

cur.execute(""
SELECT table_name
FROM information_schema.tables
WHERE table_schema='public';
"")
print("Tables:", cur.fetchall())

cur.close()
conn.close()"""