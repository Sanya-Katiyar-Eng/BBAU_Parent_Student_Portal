from database.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash


# ==========================================================
# Get User By Username & Role
# ==========================================================

def get_user(login_username, role):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            SELECT
                id,
                login_username,
                password,
                role,
                first_login,
                account_status
            FROM users
            WHERE login_username=%s
            AND role=%s
        """,
        (
            login_username,
            role.lower()
        ))

        return cur.fetchone()

    finally:

        cur.close()
        conn.close()


# ==========================================================
# Verify Student Before First Login
# ==========================================================

def verify_student(enrollment_no, roll_no):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            SELECT
                u.id
            FROM users u
            JOIN students s
            ON u.id=s.student_id

            WHERE

                u.login_username=%s
                AND s.roll_no=%s
                AND u.role='student'
        """,
        (
            enrollment_no,
            roll_no
        ))

        return cur.fetchone()

    finally:

        cur.close()
        conn.close()


# ==========================================================
# Create First Password
# ==========================================================

def create_password(user_id, new_password):

    conn = get_connection()
    cur = conn.cursor()

    try:

        hashed_password = generate_password_hash(new_password)

        cur.execute("""
            UPDATE users

            SET

                password=%s,
                first_login=FALSE,
                updated_at=CURRENT_TIMESTAMP

            WHERE id=%s
        """,
        (
            hashed_password,
            user_id
        ))

        conn.commit()

        return True

    except:

        conn.rollback()

        return False

    finally:

        cur.close()
        conn.close()


# ==========================================================
# Verify Login Password
# ==========================================================

from werkzeug.security import check_password_hash

def verify_login(login_username, password, role):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            SELECT
                id,
                password,
                role,
                first_login,
                account_status
            FROM users
            WHERE
                login_username = %s
                AND role = %s
        """, (
            login_username,
            role.lower()
        ))

        user = cur.fetchone()

        if user is None:
            return {
                "success": False,
                "message": "User not found."
            }

        user_id = user[0]
        db_password = user[1]
        db_role = user[2]
        first_login = user[3]
        account_status = user[4]

        # Account Status Check
        if account_status.lower() != "active":
            return {
                "success": False,
                "message": "Account is inactive."
            }

        # First Login
        if first_login:
            return {
                "success": False,
                "first_login": True,
                "user_id": user_id,
                "message": "Activate your account."
            }

        # Password Verification
        if not check_password_hash(db_password, password):
            return {
                "success": False,
                "message": "Invalid Password."
            }

        # Login Success
        return {
            "success": True,
            "user_id": user_id,
            "role": db_role,
            "first_login": False
        }

    finally:
        cur.close()
        conn.close()
            
            

        

            
            

def verify_password(entered_password, saved_password):

    return check_password_hash(
        saved_password,
        entered_password
    )