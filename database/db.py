"""import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(
        DATABASE_URL,
        sslmode="require",
        connect_timeout=10,
        keepalives=1,
        keepalives_idle=30,
        keepalives_interval=10,
        keepalives_count=5
    )"""
import os
from urllib.parse import urlparse
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL")

parsed = urlparse(DATABASE_URL)

print("HOST:", parsed.hostname)
print("USER:", parsed.username)
print("DATABASE:", parsed.path)
print("PASSWORD PRESENT:", bool(parsed.password))
print("PASSWORD LENGTH:", len(parsed.password) if parsed.password else 0)


def get_connection():
    return psycopg2.connect(
        DATABASE_URL,
        sslmode="require",
        connect_timeout=10,
        keepalives=1,
        keepalives_idle=30,
        keepalives_interval=10,
        keepalives_count=5
    )