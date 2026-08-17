import os
import streamlit as st
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)


def get_database_url():

    # Streamlit Cloud
    try:
        return st.secrets["DATABASE_URL"]
    except Exception:
        pass

    # Local .env
    return os.getenv("DATABASE_URL")


DATABASE_URL = get_database_url()


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



