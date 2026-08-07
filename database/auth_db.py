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
                login_username,
                password,
                role,
                first_login,
                account_status
            FROM users
            WHERE
                LOWER(login_username)=LOWER(%s)
                AND LOWER(role)=LOWER(%s)
        """, (
            login_username,
            role
        ))

        user = cur.fetchone()

        if user is None:
            return {
                "success": False,
                "message": "User not found."
            }

        user_id = user[0]
        email = user[1]
        db_password = user[2]
        db_role = user[3]
        first_login = user[4]
        account_status = user[5]

        if account_status.lower() != "active":
            return {
                "success": False,
                "message": "Account is inactive."
            }

        if first_login:
            return {
                "success": False,
                "first_login": True,
                "user_id": user_id,
                "email": email,
                "message": "Activate your account."
            }

        if db_password == password:
            password_valid = True
        else:
            password_valid = check_password_hash(db_password, password)

        if not password_valid:
            return {
                "success": False,
                "message": "Invalid Password."
            }
        parent_id = None
        student_id = None
        if db_role.lower() == "parent":

            cur.execute("""
        SELECT parent_id, student_id
        FROM parents
        WHERE parent_id = %s
    """, (user_id,))

            parent = cur.fetchone()

            if parent:
                parent_id = parent[0]
                student_id = parent[1]


        return {
            "success": True,
            "user_id": user_id,
            "role": db_role,
            "email": email,
            "first_login": False,
            "parent_id": parent_id,
            "student_id": student_id
}

    finally:
        cur.close()
        conn.close()















        
            
            

        

            
def verify_password(entered_password, saved_password):
    try:
        return check_password_hash(saved_password, entered_password)
    except Exception:
        return saved_password == entered_password           

