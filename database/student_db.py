from database.db import get_connection
import streamlit as st
from werkzeug.security import generate_password_hash
def add_student(
    roll_no,
    enrollment_no,
    department,
    semester
):
    temp_password = f"BBAU@{enrollment_no}"

    hashed_password = generate_password_hash(temp_password)
    conn = get_connection()
    cur = conn.cursor()

    try:
         
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
    'student',
    TRUE,
    'Active'
)
RETURNING id
""",
(
    enrollment_no,
    hashed_password
))

        user_id = cur.fetchone()[0]
        print(user_id)


        cur.execute("""
            INSERT INTO students
            (   student_id,
                roll_no,
                enrollment_no,
                department,
                semester,
                registration_status,
                account_status
            )

            VALUES
            (
                %s,%s,%s,%s,%s,'Pending','Active'
            )
        """,
        (
            user_id, 
            roll_no,
            enrollment_no,
            department,
            semester,
        ))

        conn.commit()

        return True

    except Exception as e:
        conn.rollback()
        st.error(f"Database Error: {e}")
        return False

    finally:

        cur.close()
        conn.close()




#-----------------------------------------------------------
# View student
#-------------------------------------------


from database.db import get_connection

def get_all_students(search="", department="All", semester="All",
                     registration="All", account="All"):

    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT
        s.student_id,
        s.enrollment_no,
        s.roll_no,
        COALESCE(p.full_name,'Not Completed') AS student_name,
        s.department,
        s.semester,
        s.registration_status,
        s.account_status
    FROM students s
    LEFT JOIN student_profiles p
    ON s.student_id=p.student_id
    WHERE 1=1
    """

    values = []

    if search:
        query += """
        AND (
            LOWER(s.enrollment_no) LIKE LOWER(%s)
            OR LOWER(s.roll_no) LIKE LOWER(%s)
            OR LOWER(COALESCE(p.full_name,'')) LIKE LOWER(%s)
        )
        """
        values.extend([f"%{search}%", f"%{search}%", f"%{search}%"])

    if department != "All":
        query += " AND s.department=%s"
        values.append(department)

    if semester != "All":
        query += " AND s.semester=%s"
        values.append(str(semester))

    if registration != "All":
        query += " AND s.registration_status=%s"
        values.append(registration)

    if account != "All":
        query += " AND s.account_status=%s"
        values.append(account)

    query += " ORDER BY s.student_id DESC"

    cur.execute(query, values)

    data = cur.fetchall()

    cur.close()
    conn.close()

    return data


#====================================================

def get_student_dashboard_counts():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            COUNT(*) AS total_students,

            COUNT(*) FILTER (
                WHERE registration_status='Completed'
            ) AS completed,

            COUNT(*) FILTER (
                WHERE registration_status='Pending'
            ) AS pending,

            COUNT(*) FILTER (
                WHERE account_status='Active'
            ) AS active

        FROM students;
    """)

    data = cur.fetchone()

    cur.close()
    conn.close()

    return data

#===================================================
#delete student
#-------------------------------------------------------------------------
def delete_student(enrollment_no):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            SELECT student_id
            FROM students
            WHERE enrollment_no=%s
        """, (enrollment_no,))
        row = cur.fetchone()
        if row is None:
            return False
        user_id = row[0]
        cur.execute("""
            DELETE FROM students
            WHERE student_id=%s
        """, (user_id,))
        cur.execute("""
            DELETE FROM users
            WHERE id=%s
        """, (user_id,))


        conn.commit()

        return True
    except Exception as e:
        conn.rollback()
        st.error(f"Database Error: {e}")
        return False
    finally:

        cur.close()
        conn.close()
    

def get_student_by_enrollment(enrollment_no):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            s.student_id,
            s.enrollment_no,
            s.roll_no,
            COALESCE(p.full_name,'Not Completed'),
            s.department,
            s.semester,
            s.registration_status,
            s.account_status

        FROM students s

        LEFT JOIN student_profiles p
        ON s.student_id = p.student_id

        WHERE s.enrollment_no=%s
    """,(enrollment_no,))

    student = cur.fetchone()

    cur.close()
    conn.close()

    return student


#==================================================================================
#registration
#====================================================================================
def get_registration_status(student_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT registration_status
        FROM students
        WHERE student_id=%s
    """, (student_id,))

    result = cur.fetchone()

    cur.close()
    conn.close()

    if result:
        return result[0]

    return None













#================================================================================================================
#submit all form info
#============================================================================================
from database.db import get_connection

def save_student_profile(

    student_id,

    student_name,
    dob,
    gender,
    blood_group,
    email,
    phone,
    address,
    city,
    state,
    pincode,

    father_name,
    mother_name,
    parent_phone,
    parent_email,
    occupation

):

    conn = get_connection()
    cur = conn.cursor()

    try:

        # ============================
        # Update Student
        # ============================

        cur.execute("""

        UPDATE students

        SET

        student_name=%s,
        dob=%s,
        gender=%s,
        blood_group=%s,
        email=%s,
        phone=%s,
        address=%s,
        city=%s,
        state=%s,
        pincode=%s,

        registration_status='Completed',
        updated_at=CURRENT_TIMESTAMP

        WHERE student_id=%s

        """,

        (

        student_name,
        dob,
        gender,
        blood_group,
        email,
        phone,
        address,
        city,
        state,
        pincode,

        student_id

        ))

        # ============================
        # Parent Login
        # ============================

        cur.execute("""

        INSERT INTO users
        (

        login_username,
        password,
        role

        )

        VALUES

        (

        %s,
        %s,
        'parent'

        )

        RETURNING id

        """,

        (

        parent_phone,
        "Parent@123"

        ))

        parent_id = cur.fetchone()[0]

        # ============================
        # Parent Table
        # ============================

        cur.execute("""

        INSERT INTO parents
        (

        parent_id,
        student_id,
        father_name,
        mother_name,
        phone,
        email,
        occupation,
        address

        )

        VALUES

        (

        %s,%s,%s,%s,%s,%s,%s,%s

        )

        """,

        (

        parent_id,
        student_id,
        father_name,
        mother_name,
        parent_phone,
        parent_email,
        occupation,
        address

        ))

        conn.commit()

        return True

    except Exception as e:

        conn.rollback()

        print(e)

        return False

    finally:

        cur.close()
        conn.close()