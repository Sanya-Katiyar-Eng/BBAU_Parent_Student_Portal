
from database.db import get_connection
from werkzeug.security import generate_password_hash


def add_teacher(
    teacher_name,
    employee_id,
    department,
    designation,
    qualification,
    phone,
    email,
    gender,
    date_of_birth,
    address,
    city,
    state,
    pincode,
    aadhar_number,
    specialization,
    university,
    passing_year,
    experience,
    joining_date,
    employment_type,
    username,
    password,
    photo=None
):
    """
    Add new teacher with login account.

    Returns:
        True  -> Success
        False -> Failed
    """

    conn = get_connection()
    cur = conn.cursor()

    try:

        # ===============================
        # Hash Password
        # ===============================

        hashed_password = generate_password_hash(password)

        # ===============================
        # Create Login Account
        # ===============================

        cur.execute("""
            INSERT INTO users
            (
                login_username,
                password,
                role,
                first_login,
                account_status
            )
            VALUES
            (
                %s,
                %s,
                'teacher',
                FALSE,
                'Active'
            )
            RETURNING id
        """,
        (
            teacher_name,
            hashed_password
        ))

        teacher_id = cur.fetchone()[0]

        # ===============================
        # Teacher Details
        # ===============================

        cur.execute("""
            INSERT INTO teachers
            (
                teacher_id,
                teacher_name,
                employee_id,
                department,
                designation,
                qualification,
                phone,
                email,
                gender,
                date_of_birth,
                address,
                city,
                state,
                pincode,
                aadhar_number,
                specialization,
                university,
                passing_year,
                experience,
                joining_date,
                employment_type,
                photo,
                status
            )
            VALUES
            (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,'Active'
            )
        """,
        (
            teacher_id,
            teacher_name,
            employee_id,
            department,
            designation,
            qualification,
            phone,
            email,
            gender,
            date_of_birth,
            address,
            city,
            state,
            pincode,
            aadhar_number,
            specialization,
            university,
            passing_year,
            experience,
            joining_date,
            employment_type,
            photo
        ))

        conn.commit()

        return True

    except Exception as e:

        conn.rollback()

        print("Teacher Add Error :", e)

        return False

    finally:

        cur.close()
        conn.close()

#=========================================================================
#get all teacher
#=========================================================================
def get_all_teachers():

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            SELECT
                teacher_id,
                teacher_name,
                employee_id,
                department,
                designation,
                phone,
                email,
                status
            FROM teachers
            ORDER BY teacher_name
        """)

        return cur.fetchall()

    finally:
        cur.close()
        conn.close()
#================================================================
#update teacher
#========================================================================================
from database.db import get_connection


def update_teacher(
    teacher_id,
    teacher_name,
    employee_id,
    department,
    designation,
    email,
    mobile,
    qualification,
    experience,
    gender,
    address
):
    """
    Updates teacher information.

    Args:
        teacher_id (int)

    Returns:
        bool
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE teacher_registration
            SET
                teacher_name = %s,
                employee_id = %s,
                department = %s,
                designation = %s,
                email = %s,
                mobile = %s,
                qualification = %s,
                experience = %s,
                gender = %s,
                address = %s
            WHERE teacher_id = %s
        """, (
            teacher_name,
            employee_id,
            department,
            designation,
            email,
            mobile,
            qualification,
            experience,
            gender,
            address,
            teacher_id
        ))

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print("Error:", e)
        return False

    finally:
        cur.close()
        conn.close()

#=======================================================================================================================
#delete teacher
#================================================================================================================================
from database.db import get_connection


def delete_teacher(teacher_id):
    """
    Deletes a teacher and associated login.

    Args:
        teacher_id (int)

    Returns:
        bool
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        # Get user_id linked to teacher
        cur.execute("""
            SELECT user_id
            FROM teacher_registration
            WHERE teacher_id = %s
        """, (teacher_id,))

        result = cur.fetchone()

        if result is None:
            return False

        user_id = result[0]

        # Delete teacher details
        cur.execute("""
            DELETE FROM teacher_registration
            WHERE teacher_id = %s
        """, (teacher_id,))

        # Delete login account
        cur.execute("""
            DELETE FROM users
            WHERE id = %s
        """, (user_id,))

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print("Error:", e)
        return False

    finally:
        cur.close()
        conn.close()
success = delete_teacher(1)

if success:
    print("Teacher deleted successfully.")
else:
    print("Teacher not found or delete failed.")
