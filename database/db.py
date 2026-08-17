import os
import streamlit as st
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)
DATABASE_URL = st.secrets.get("DATABASE_URL", os.getenv("DATABASE_URL"))
#DATABASE_URL = os.getenv("DATABASE_URL")

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



