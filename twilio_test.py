import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_NUMBER")

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+917905639342",
    from_=twilio_number,
    body="sms_appointment_reminders"
)

print("SMS SID:", message.sid)
print("SMS STATUS:", message.status)