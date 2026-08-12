
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()


def send_attendance_sms(phone, student_name, course_name, status):

    try:

        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        twilio_number = os.getenv("TWILIO_NUMBER")

        print("SID loaded:", bool(account_sid))
        print("TOKEN loaded:", bool(auth_token))
        print("NUMBER loaded:", bool(twilio_number))

        if not account_sid:
            print("TWILIO_ACCOUNT_SID missing")
            return False

        if not auth_token:
            print("TWILIO_AUTH_TOKEN missing")
            return False

        if not twilio_number:
            print("TWILIO_NUMBER missing")
            return False

        if not phone:
            print("Parent phone missing")
            return False

        phone = str(phone).strip()

        if not phone.startswith("+91"):
            phone = "+91" + phone

        if status.lower() == "present":

            message_text = (
                f"Dear Parent, your child {student_name} "
                f"was present in today's {course_name} class."
            )

        else:

            message_text = (
                f"Dear Parent, your child {student_name} "
                f"was absent in today's {course_name} class."
            )

        client = Client(
            account_sid,
            auth_token
        )

        message = client.messages.create(
            body=message_text,
            from_=twilio_number,
            to=phone
        )

        print("SMS SENT:", message.sid)

        return True

    except Exception as e:

        print("SMS ERROR:", e)

        return False