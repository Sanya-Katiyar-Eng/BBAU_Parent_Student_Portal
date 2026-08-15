from database.db import get_connection
import streamlit as st
from dotenv import load_dotenv
from twilio.rest import Client
import os

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")

client = Client(
    TWILIO_SID,
    TWILIO_TOKEN
)
import os
def send_parent_email(parent_email, student_name, course_name, attendance_date):

    print("="*50)
    print("EMAIL SENT")
    print(parent_email)
    print(student_name)
    print(course_name)
    print(attendance_date)
    print("="*50)

    return True

from database.db import get_connection


def save_fcm_token(parent_id, student_id, fcm_token):

    conn = get_connection()
    cur = conn.cursor()

    query = """
        INSERT INTO fcm_tokens
        (
            parent_id,
            student_id,
            fcm_token,
            updated_at
        )
        VALUES
        (
            %s,
            %s,
            %s,
            CURRENT_TIMESTAMP
        )

        ON CONFLICT (fcm_token)
        DO UPDATE SET

            parent_id = EXCLUDED.parent_id,

            student_id = EXCLUDED.student_id,

            updated_at = CURRENT_TIMESTAMP
    """

    cur.execute(
        query,
        (
            parent_id,
            student_id,
            fcm_token
        )
    )

    conn.commit()

    cur.close()
    conn.close()