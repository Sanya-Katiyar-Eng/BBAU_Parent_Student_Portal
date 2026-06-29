from database.db import get_connection
def login_user(email, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT role FROM users WHERE email=%s AND password=%s",
        (email, password)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        return user[0]   # role
    return None
"""conn = get_connection()
cur = conn.cursor()

cur.execute("SELECT * FROM users")

print(cur.fetchall())"""



"""from database.db import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';
"")

print(cur.fetchall())

cur.close()
conn.close()"""