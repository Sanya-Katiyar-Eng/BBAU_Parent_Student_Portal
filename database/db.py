import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL EXISTS:", bool(DATABASE_URL))
print("DATABASE HOST:", DATABASE_URL.split("@")[1].split("/")[0] if DATABASE_URL else "NONE")  

def get_connection():

    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured")

    return psycopg2.connect(
        DATABASE_URL,
        sslmode="require",
        connect_timeout=10,
        keepalives=1,
        keepalives_idle=30,
        keepalives_interval=10,
        keepalives_count=5
    )



