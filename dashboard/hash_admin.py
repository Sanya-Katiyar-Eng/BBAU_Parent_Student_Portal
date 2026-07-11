from werkzeug.security import generate_password_hash
from database.db import get_connection

conn = get_connection()
cur = conn.cursor()

hashed_password = generate_password_hash("sanya@2008")

cur.execute("""
UPDATE users
SET password=%s
WHERE login_username=%s
""",
(
    hashed_password,
    "sanyakatiyar01@gmail.com"
))

conn.commit()

cur.close()
conn.close()

print("Admin password updated successfully.")