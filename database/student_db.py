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

#===============================================================================
#student dashboard
#======================================================================================

# get_student_dashboard(user_id)      -> Basic student information
# get_student_attendance(user_id)     -> Teacher module se
# get_student_results(user_id)        -> Teacher module se
# get_today_classes(user_id)          -> Teacher/Admin module se
# get_student_assignments(user_id)    -> Teacher module se
# get_student_notices(user_id)        -> Admin/Teacher module se

from database.db import get_connection


def get_student_dashboard(user_id):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            SELECT

                sr.student_name,
                sr.enrollment_number,
                sr.roll_number,
                sr.department,
                sr.program_name,
                sr.semester,
                sr.session,
                sr.email,
                sr.mobile_number,
                sr.profile_photo

            FROM student_registration sr
            INNER JOIN users u
                    ON u.id = sr.user_id

            WHERE u.id = %s

        """, (user_id,))

        student = cur.fetchone()

        if student is None:
            return None

        return {

            "name": student[0],
            "enrollment": student[1],
            "roll_no": student[2],
            "department": student[3],
            "program": student[4],
            "semester": student[5],
            "session": student[6],
            "email": student[7],
            "mobile": student[8],
            "photo": student[9]

        }

    except Exception as e:

        print(e)
        return None

    finally:

        cur.close()
        conn.close()




from database.db import get_connection
import streamlit as st


def get_student_attendance():

    conn = get_connection()
    cur = conn.cursor()

    student_id = st.session_state.student_id

    query = """
        SELECT

            a.attendance_date,
            c.course_code,
            c.course_name,
            a.status,
            t.teacher_name,
            COALESCE(a.remarks,'')

        FROM attendance a

        INNER JOIN courses c
            ON a.course_id = c.course_id

        LEFT JOIN teachers t
            ON a.marked_by = t.teacher_id

        WHERE
            a.student_id = %s

        ORDER BY
            a.attendance_date DESC,
            c.course_name;
    """

    cur.execute(query, (student_id,))

    attendance = cur.fetchall()

    cur.close()
    conn.close()

    return attendance

def get_students_by_course(course_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            s.student_id,
            s.student_name,
            s.enrollment_number
        FROM students s
        JOIN student_courses sc
        ON s.student_id = sc.student_id
        WHERE sc.course_id = %s
    """,(course_id,))

    students = cur.fetchall()

    cur.close()
    conn.close()

    return students

def get_student_attendance_summary(student_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            COUNT(*) FILTER(WHERE status='Present'),

            COUNT(*) FILTER(WHERE status='Absent'),

            COUNT(*)

        FROM attendance

        WHERE student_id=%s

    """,(student_id,))

    present, absent, total = cur.fetchone()

    cur.close()
    conn.close()

    present = present or 0
    absent = absent or 0
    total = total or 0

    percentage = 0

    if total > 0:
        percentage = round((present/total)*100,2)

    return {

        "present":present,
        "absent":absent,
        "total":total,
        "percentage":percentage

    }

def get_student_attendance_history(student_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            a.attendance_date,
            c.course_name,
            a.status
        FROM attendance a

        INNER JOIN courses c
            ON a.course_id = c.course_id

        WHERE
            a.student_id = %s

        ORDER BY
            a.attendance_date DESC,
            c.course_name

        LIMIT 5
    """, (student_id,))

    records = cur.fetchall()

    cur.close()
    conn.close()

    return records

from datetime import date

def get_today_attendance(student_id):

    conn=get_connection()
    cur=conn.cursor()

    cur.execute("""

        SELECT

            c.course_name,
            a.status

        FROM attendance a

        JOIN courses c

        ON a.course_id=c.course_id

        WHERE

            student_id=%s

            AND attendance_date=%s

    """,(student_id,date.today()))

    data=cur.fetchall()

    cur.close()
    conn.close()

    return data

# ==========================================================
# FUTURE MODULES
# These functions will be connected after Teacher/Admin
# dashboard is completed.
# ==========================================================


# def get_student_attendance(user_id):
#
#     """
#     Teacher will update attendance.
#
#     Returns:
#         Overall attendance
#         Subject-wise attendance
#     """
#
#     pass


# def get_student_results(user_id):
#
#     """
#     Teacher will upload internal marks,
#     practical marks and semester results.
#     """
#
#     pass


# def get_today_classes(user_id):
#
#     """
#     Timetable generated by Admin.
#
#     Teacher can also update extra classes.
#     """
#
#     pass


# def get_student_assignments(user_id):
#
#     """
#     Teacher uploads assignments.
#
#     Student can only view/download.
#     """
#
#     pass


# def get_student_notices(user_id):
#
#     """
#     Notices uploaded by
#     Admin / Teacher.
#     """
#
#     pass


# def get_student_messages(user_id):
#
#     """
#     Messaging system between
#     Teacher ↔ Student.
#     """
#
#     pass


# def get_student_documents(user_id):
#
#     """
#     Uploaded documents
#
#     Admit Card
#     Fee Receipt
#     ID Card
#     Marksheet
#     Certificates
#     """
#
#     pass
