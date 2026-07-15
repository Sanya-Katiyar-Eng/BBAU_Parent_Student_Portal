
from database.db import get_connection
from werkzeug.security import generate_password_hash
import streamlit as st
from auth.login import normalize_text

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
                %s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,'Active'
            )
        """,
        (
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
    teacher_name,
    employee_id,
    department,
    designation,
    email,
    phone,
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
            UPDATE teachers
            SET
                teacher_name = %s,
                employee_id = %s,
                department = %s,
                designation = %s,
                email = %s,
                phone = %s,
                qualification = %s,
                experience = %s,
                gender = %s,
                address = %s
            WHERE teacher_name = %s
        """, (
            teacher_name,
            employee_id,
            department,
            designation,
            email,
            phone,
            qualification,
            experience,
            gender,
            address,
            teacher_name
        ))

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        st.error(f"Database Error: {e}")
        print("Error:", e)
        
        return False

    finally:
        cur.close()
        conn.close()

#=======================================================================================================================
#delete teacher
#================================================================================================================================
from database.db import get_connection

def delete_teacher(teacher_name, employee_id):

    conn = get_connection()
    cur = conn.cursor()

    try:
        # Check teacher exists
        cur.execute("""
            SELECT teacher_name
            FROM teachers
            WHERE teacher_name=%s
            AND employee_id=%s
        """, (teacher_name, employee_id))

        if cur.fetchone() is None:
            return False

        # Delete from teachers
        cur.execute("""
            DELETE FROM teachers
            WHERE teacher_name=%s
            AND employee_id=%s
        """, (teacher_name, employee_id))

        # Delete from users
        cur.execute("""
            DELETE FROM users
            WHERE login_username = %s
              AND role = 'teacher'
        """, (teacher_name,))

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        st.error(f"Database Error: {e}")
        print(e)
        return False

    finally:
        cur.close()
        conn.close()

#=====================================================================================
# search teacher
#=====================================================================================================
def search_teachers(name="", employee_id=""):

    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT
        teacher_name,
        employee_id,
        department,
        designation,
        phone,
        email
    FROM teachers
    WHERE 1=1
    """

    values = []

    if name:
        query += " AND teacher_name ILIKE %s"
        values.append(f"%{name}%")

    if employee_id:
        query += " AND employee_id ILIKE %s"
        values.append(f"%{employee_id}%")

    cur.execute(query, values)

    teachers = cur.fetchall()

    cur.close()
    conn.close()

    return teachers