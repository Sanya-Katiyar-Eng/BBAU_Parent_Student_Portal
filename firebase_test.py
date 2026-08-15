import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate(
    "bbau-student-parent-portal-firebase-adminsdk-fbsvc-bc468310ea.json"
)

firebase_admin.initialize_app(cred)

FCM_TOKEN = "duzU5rjdHvBR4Tabbd-otf:APA91bHg0cWu6V6hh79ke3tfmMas4no_pin8tZ5QuPQsKWE-4sNxFAF7rrAAlHq-dr0eXs0H5jOh6eg0cDTHomV3bBVQZg6CzJyVqeeSjllJV_qYb6yVz9o"

message = messaging.Message(
    notification=messaging.Notification(
        title="BBAU Attendance",
        body="Test notification successfully received! 🔔"
    ),
    token=FCM_TOKEN,
)

response = messaging.send(message)

print("Notification sent successfully!")
print("Message ID:", response)