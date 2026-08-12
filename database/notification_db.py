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

