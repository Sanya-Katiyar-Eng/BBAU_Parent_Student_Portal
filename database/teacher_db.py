
from database.db import get_connection
from werkzeug.security import generate_password_hash
import streamlit as st
from database.db import *
from auth.login import normalize_text
from psycopg2.extras import RealDictCursor
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
            normalize_text(username),
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
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s
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
    photo,
    "Active"
))

        conn.commit()

        return True

    except Exception as e:
        conn.rollback()
        raise e

    finally:

        cur.close()
        conn.close()




















def get_teacher_dashboard(teacher_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM teachers
        WHERE teacher_id=%s
        """,
        (teacher_id,)
    )

    data = cur.fetchone()

    cur.close()
    conn.close()

    return data



















from database.db import get_connection


def get_teacher_courses(teacher_id):

    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT
            course_id,
            course_code,
            course_name,
            department,
            semester,
            credits

        FROM courses

        WHERE
            teacher_id = %s

        ORDER BY
            semester,
            course_name;
    """

    cur.execute(query, (teacher_id,))

    courses = cur.fetchall()

    cur.close()
    conn.close()

    return courses












#=========================================================================
#get all teacher
#=========================================================================
from database.db import get_connection


def get_teacher_courses(teacher_id):

    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT

            tc.course_id,
            c.course_code,
            c.course_name,
            c.semester,
            c.department,
            c.credits

        FROM teacher_courses tc

        INNER JOIN courses c
            ON tc.course_id = c.course_id

        WHERE
            tc.teacher_id = %s
            AND tc.status = 'Active'

        ORDER BY
            c.semester,
            c.course_name;
    """

    cur.execute(query, (teacher_id,))

    courses = cur.fetchall()

    cur.close()
    conn.close()

    return courses
#================================================================
#update teacher
#=========================================================================================================================
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





def get_teacher_dashboard(user_id):

    conn = get_connection()
    cur = conn.cursor()

    dashboard = {
        "teacher_name": "",
        "employee_id": "",
        "department": "",
        "students": 0,
        "courses": 0,
        "attendance": 0,
        "results": 0
    }

    try:

        # -------------------------------
        # Teacher Information
        # -------------------------------
        cur.execute("""
            SELECT
                teacher_name,
                employee_id,
                department
            FROM teachers
            WHERE teacher_id = %s
        """, (user_id,))

        teacher = cur.fetchone()

        if teacher:

            dashboard["teacher_name"] = teacher[0]
            dashboard["employee_id"] = teacher[1]
            dashboard["department"] = teacher[2]

        # -------------------------------
        # Total Students
        # -------------------------------
        cur.execute("""
            SELECT COUNT(*)
            FROM students
        """)

        dashboard["students"] = cur.fetchone()[0]

        # -------------------------------
        # Total Courses
        # -------------------------------
        cur.execute("""
            SELECT COUNT(*)
            FROM courses
        """)

        dashboard["courses"] = cur.fetchone()[0]

        # -------------------------------
        # Today's Attendance
        # -------------------------------
        cur.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE attendance_date = CURRENT_DATE
        """)

        dashboard["attendance"] = cur.fetchone()[0]

        # -------------------------------
        # Pending Results
        # -------------------------------
        dashboard["results"] = 0

    except Exception as e:

        print(e)

    finally:

        cur.close()
        conn.close()

    return dashboard


#=============================================================================
#home page

#----------------------------------------------------
#





















def get_teacher_students(teacher_id):

    conn = get_connection()
    cur = conn.cursor()

    try:

        # Teacher department
        cur.execute("""
            SELECT department
            FROM teachers
            WHERE teacher_id = %s
        """, (teacher_id,))

        teacher = cur.fetchone()

        if teacher is None:
            return []

        department = teacher[0].strip()

        # Department Mapping
        department_map = {
            "CS": "Computer Science",
            "IT": "Information Technology",
            "BCA": "BCA",
            "MCA": "MCA"
        }

        department = department_map.get(department, department)

        # Students
        cur.execute("""
            SELECT
                student_id,
                roll_no,
                student_name,
                department,
                semester,
                enrollment_no,
                gender,
                status
            FROM students
            WHERE department = %s
            ORDER BY roll_no
        """, (department,))

        return cur.fetchall()

    except Exception as e:
        print("Student Fetch Error:", e)
        return []

    finally:
        cur.close()
        conn.close()











def search_teacher_students(teacher_id, search_text):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT
                s.student_id,
                s.roll_no,
                s.name,
                s.department,
                s.semester,
                s.enrollment_no,
                s.gender,
                s.status

            FROM students s

            JOIN teachers t
            ON s.department = t.department

            WHERE 
                t.teacher_id = %s
                AND
                (
                    s.name ILIKE %s
                    OR s.roll_no ILIKE %s
                    OR s.enrollment_no ILIKE %s
                )

            ORDER BY
                s.roll_no

        """, (
            teacher_id,
            f"%{search_text}%",
            f"%{search_text}%",
            f"%{search_text}%"
        ))

        students = cur.fetchall()

        return students

    except Exception as e:
        print("Student Search Error:", e)
        return []

    finally:
        cur.close()
        conn.close()























def filter_teacher_students(
        teacher_id,
        semester=None,
        gender=None,
        status=None
    ):

    conn = get_connection()
    cur = conn.cursor()

    try:

        query = """
            SELECT
                s.student_id,
                s.roll_no,
                s.name,
                s.department,
                s.semester,
                s.enrollment_no,
                s.gender,
                s.status

            FROM students s

            JOIN teachers t
            ON s.department = t.department

            WHERE
                t.teacher_id = %s
        """

        params = [teacher_id]


        if semester:
            query += """
                AND s.semester = %s
            """
            params.append(semester)


        if gender:
            query += """
                AND s.gender = %s
            """
            params.append(gender)


        if status:
            query += """
                AND s.status = %s
            """
            params.append(status)


        query += """
            ORDER BY s.roll_no
        """


        cur.execute(query, tuple(params))

        students = cur.fetchall()

        return students


    except Exception as e:
        print("Student Filter Error:", e)
        return []


    finally:
        cur.close()
        conn.close()


from database.db import get_connection

from database.db import get_connection


def save_attendance(
        course_id,
        attendance_date,
        teacher_id,
        attendance_data
):

    conn = get_connection()
    cur = conn.cursor()

    try:

        for student in attendance_data:

            student_id = student["student_id"]
            status = student["status"]

            # Check Existing Attendance
            cur.execute("""
                SELECT attendance_id
                FROM attendance
                WHERE
                    student_id=%s
                    AND course_id=%s
                    AND attendance_date=%s
            """,(
                student_id,
                course_id,
                attendance_date
            ))

            record = cur.fetchone()

            # -----------------------------
            # Update Existing Attendance
            # -----------------------------
            if record:

                cur.execute("""
                    UPDATE attendance
                    SET
                        status=%s,
                        marked_by=%s
                    WHERE attendance_id=%s
                """,(
                    status,
                    teacher_id,
                    record[0]
                ))

            # -----------------------------
            # Insert New Attendance
            # -----------------------------
            else:

                cur.execute("""
                    INSERT INTO attendance(

                        student_id,
                        course_id,
                        attendance_date,
                        status,
                        marked_by

                    )

                    VALUES(
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )

                """,(

                    student_id,
                    course_id,
                    attendance_date,
                    status,
                    teacher_id

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





def get_students_by_course(course_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            s.student_id,
            s.student_name,
            s.enrollment_no,
            s.roll_no,
            s.department,
            s.semester,
            s.status

        FROM students s

        INNER JOIN student_courses sc
            ON s.student_id = sc.student_id

        WHERE
            sc.course_id = %s
            AND s.status = 'Active'
            AND s.account_status = 'Active'

        ORDER BY s.roll_no
    """, (course_id,))

    students = cur.fetchall()

    cur.close()
    conn.close()

    return students




























def get_teacher_courses(teacher_id):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            SELECT
                course_id,
                course_code,
                course_name,
                department,
                semester,
                credits
            FROM courses
            WHERE teacher_id = %s
            ORDER BY semester, course_name
        """, (teacher_id,))

        courses = cur.fetchall()

        return courses

    except Exception as e:

        print(f"Database Error: {e}")
        return []

    finally:

        cur.close()
        conn.close()
























def get_attendance(
        teacher_id,
        course_id=None,
        attendance_date=None
    ):

    conn = get_connection()
    cur = conn.cursor()

    try:

        query = """
            SELECT
                a.attendance_id,
                a.student_id,
                s.roll_no,
                s.name,
                c.course_name,
                a.attendance_date,
                a.status

            FROM attendance a

            JOIN students s
            ON a.student_id = s.student_id

            JOIN courses c
            ON a.course_id = c.course_id

            WHERE
                a.teacher_id = %s
        """

        params = [teacher_id]


        if course_id:
            query += """
                AND a.course_id = %s
            """
            params.append(course_id)


        if attendance_date:
            query += """
                AND a.attendance_date = %s
            """
            params.append(attendance_date)


        query += """
            ORDER BY
                a.attendance_date DESC,
                s.roll_no
        """


        cur.execute(
            query,
            tuple(params)
        )

        attendance = cur.fetchall()

        return attendance


    except Exception as e:
        print("Attendance Fetch Error:", e)
        return []


    finally:
        cur.close()
        conn.close()





from database.db import get_connection

def get_all_teachers():
    conn = get_connection()
    cur = conn.cursor()

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
        ORDER BY teacher_name;
    """)

    teachers = cur.fetchall()

    cur.close()
    conn.close()

    return teachers







def update_attendance(
        attendance_id,
        status
    ):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            UPDATE attendance

            SET
                status = %s

            WHERE
                attendance_id = %s

        """, (
            status,
            attendance_id
        ))


        conn.commit()

        return True


    except Exception as e:
        conn.rollback()
        print("Attendance Update Error:", e)
        return False


    finally:
        cur.close()
        conn.close()











def save_result(
        teacher_id,
        course_id,
        student_id,
        marks,
        grade
    ):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            INSERT INTO results
            (
                teacher_id,
                course_id,
                student_id,
                marks,
                grade
            )

            VALUES
            (%s, %s, %s, %s, %s)

        """, (
            teacher_id,
            course_id,
            student_id,
            marks,
            grade
        ))


        conn.commit()

        return True


    except Exception as e:
        conn.rollback()
        print("Result Save Error:", e)
        return False


    finally:
        cur.close()
        conn.close()






















def get_results(
        teacher_id,
        course_id=None,
        student_id=None
    ):

    conn = get_connection()
    cur = conn.cursor()

    try:

        query = """
            SELECT
                r.result_id,
                r.student_id,
                s.roll_no,
                s.name,
                c.course_name,
                r.marks,
                r.grade,
                r.created_at

            FROM results r

            JOIN students s
            ON r.student_id = s.student_id

            JOIN courses c
            ON r.course_id = c.course_id

            WHERE
                r.teacher_id = %s
        """

        params = [teacher_id]


        if course_id:
            query += """
                AND r.course_id = %s
            """
            params.append(course_id)


        if student_id:
            query += """
                AND r.student_id = %s
            """
            params.append(student_id)


        query += """
            ORDER BY
                s.roll_no
        """


        cur.execute(
            query,
            tuple(params)
        )


        results = cur.fetchall()

        return results


    except Exception as e:
        print("Result Fetch Error:", e)
        return []


    finally:
        cur.close()
        conn.close()


































def update_result(
        result_id,
        marks,
        grade
    ):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            UPDATE results

            SET
                marks = %s,
                grade = %s

            WHERE
                result_id = %s

        """, (
            marks,
            grade,
            result_id
        ))


        conn.commit()

        return True


    except Exception as e:
        conn.rollback()
        print("Result Update Error:", e)
        return False


    finally:
        cur.close()
        conn.close()

















def get_assignments(
        teacher_id,
        course_id=None
    ):

    conn = get_connection()
    cur = conn.cursor()

    try:

        query = """
            SELECT
                a.assignment_id,
                a.course_id,
                c.course_name,
                a.title,
                a.description,
                a.due_date,
                a.created_at

            FROM assignments a

            JOIN courses c
            ON a.course_id = c.course_id

            WHERE
                a.teacher_id = %s
        """

        params = [teacher_id]


        if course_id:
            query += """
                AND a.course_id = %s
            """
            params.append(course_id)


        query += """
            ORDER BY
                a.created_at DESC
        """


        cur.execute(
            query,
            tuple(params)
        )


        assignments = cur.fetchall()

        return assignments


    except Exception as e:
        print("Assignment Fetch Error:", e)
        return []


    finally:
        cur.close()
        conn.close()

































from psycopg2.extras import RealDictCursor
def get_teacher_profile(teacher_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)


    try:
        cur.execute("""
            SELECT
                teacher_id,
                employee_id,
                department,
                designation,
                qualification,
                date_of_birth,
                experience,
                joining_date,
                employment_type,
                gender,
                phone,
                photo,
                status,
                created_at,
                university,
                address,
                teacher_name,
                email
            FROM teachers
            WHERE teacher_id = %s
        """, (teacher_id,))

        return cur.fetchone()
    except Exception as e:
        print("Teacher profile Error",e)
        return None

    finally:
        cur.close()
        conn.close()











def update_teacher_profile(
        teacher_id,
        phone,
        qualification,
        photo
    ):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            UPDATE teachers

            SET
                phone = %s,
                qualification = %s,
                photo = %s,
                updated_at = CURRENT_TIMESTAMP

            WHERE
                teacher_id = %s

        """, (
            phone,
            qualification,
            photo,
            teacher_id
        ))


        conn.commit()

        return True


    except Exception as e:
        conn.rollback()
        print("Teacher Profile Update Error:", e)
        return False


    finally:
        cur.close()
        conn.close() 


















def update_teacher_password(
        teacher_id,
        new_password
    ):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            UPDATE users

            SET
                password = %s,
                first_login = FALSE,
                updated_at = CURRENT_TIMESTAMP

            WHERE
                id = (
                    SELECT parent_id
                    FROM teachers
                    WHERE teacher_id = %s
                )

        """, (
            new_password,
            teacher_id
        ))


        conn.commit()

        return True


    except Exception as e:
        conn.rollback()
        print("Password Update Error:", e)
        return False


    finally:
        cur.close()
        conn.close()






















def get_student_by_id(student_id):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            SELECT
                student_id,
                roll_no,
                name,
                department,
                semester,
                enrollment_no,
                gender,
                status,
                photo
            FROM students
            WHERE student_id = %s
        """, (student_id,))

        row = cur.fetchone()

        if row:
            return {
                "student_id": row[0],
                "roll_no": row[1],
                "name": row[2],
                "department": row[3],
                "semester": row[4],
                "enrollment_no": row[5],
                "gender": row[6],
                "status": row[7],
                "photo": row[8]
            }

        return None


    except Exception as e:
        print("Student Fetch Error:", e)
        return None


    finally:
        cur.close()
        conn.close()














        from datetime import datetime, timedelta



def get_today_classes(teacher_id):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            SELECT
                c.course_name,
                c.semester,
                t.day_name,
                t.start_time,
                t.end_time,
                t.room_no

            FROM timetable t

            JOIN courses c
            ON t.course_id = c.course_id

            WHERE t.teacher_id = %s

            ORDER BY t.start_time
        """, (teacher_id,))

        return cur.fetchall()

    except Exception as e:
        print("Timetable Error:", e)
        return []

    finally:
        cur.close()
        conn.close()








from database.db import get_connection
def assign_course(teacher_id, course_id, semester, session):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO teacher_courses
        (teacher_id, course_id, semester, session)
        VALUES (%s,%s,%s,%s)
        ON CONFLICT DO NOTHING
    """, (teacher_id, course_id, semester, session))

    conn.commit()
    cur.close()
    conn.close()











def get_teacher_courses(teacher_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            course_id,
            course_name,
            department,
            semester,
            credits
        FROM courses
        WHERE teacher_id = %s
        ORDER BY semester
    """, (teacher_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    courses = []

    for row in rows:
        courses.append({
            "Course ID": row[0],
            "Course Name": row[1],
            "Department": row[2],
            "Semester": f"Semester {row[3]}",
            "Credits": row[4]
        })

    return courses


   














def get_result_progress(teacher_department):

    conn=get_connection()
    cur=conn.cursor()

    cur.execute("""

    SELECT
    semester,
    COUNT(student_id)

    FROM students

    WHERE department=%s

    GROUP BY semester

    ORDER BY semester

    """,(teacher_department,))

    total=cur.fetchall()


    progress=[]

    for sem,total_students in total:

        cur.execute("""

        SELECT COUNT(DISTINCT student_id)

        FROM results

        WHERE semester=%s

        """,(sem,))

        uploaded=cur.fetchone()[0]

        progress.append({
            "semester":sem,
            "uploaded":uploaded,
            "remaining":total_students-uploaded
        })

    conn.close()

    return progress

















def get_assignment_progress(teacher_id):

    conn=get_connection()
    cur=conn.cursor()

    cur.execute("""

    SELECT
    course_name,
    semester,
    due_date

    FROM assignments

    WHERE teacher_id=%s

    ORDER BY due_date DESC

    LIMIT 5

    """,(teacher_id,))

    data=cur.fetchall()

    conn.close()

    return data




















def get_attendance_by_date(course_id, attendance_date):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            a.attendance_id,
            s.enrollment_no,
            s.student_name,
            a.status

        FROM attendance a

        JOIN students s
        ON a.student_id = s.student_id

        WHERE
            a.course_id=%s
            AND a.attendance_date=%s

        ORDER BY s.roll_no
    """, (course_id, attendance_date))

    data = cur.fetchall()

    cur.close()
    conn.close()

    return data


def get_attendance_for_edit(course_id, attendance_date):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            a.attendance_id,
            s.student_id,
            s.enrollment_no,
            s.student_name,
            a.status

        FROM attendance a

        JOIN students s

        ON a.student_id=s.student_id

        WHERE

            a.course_id=%s

            AND a.attendance_date=%s

        ORDER BY s.roll_no

    """,(course_id,attendance_date))

    data=cur.fetchall()

    cur.close()
    conn.close()

    return data


def update_attendance(attendance_id,status):

    conn=get_connection()
    cur=conn.cursor()

    try:

        cur.execute("""

            UPDATE attendance

            SET status=%s

            WHERE attendance_id=%s

        """,(status,attendance_id))

        conn.commit()

        return True

    except Exception as e:

        print(e)

        conn.rollback()

        return False

    finally:

        cur.close()
        conn.close()

def get_attendance_analytics(course_id, attendance_date):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            COUNT(*) FILTER(WHERE status='Present'),

            COUNT(*) FILTER(WHERE status='Absent'),

            COUNT(*)

        FROM attendance

        WHERE
            course_id=%s
            AND attendance_date=%s

    """,(course_id,attendance_date))

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
def export_attendance(course_id, attendance_date):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            s.roll_no,
            s.enrollment_no,
            s.student_name,
            c.course_name,
            a.attendance_date,
            a.status

        FROM attendance a

        JOIN students s
            ON a.student_id=s.student_id

        JOIN courses c
            ON a.course_id=c.course_id

        WHERE

            a.course_id=%s

            AND a.attendance_date=%s

        ORDER BY s.roll_no

    """,(course_id,attendance_date))

    data=cur.fetchall()

    columns=[

        "Roll No",
        "Enrollment No",
        "Student Name",
        "Course",
        "Date",
        "Status"

    ]

    cur.close()
    conn.close()

    return data,columns









from database.db import get_connection


def get_teacher_statistics():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            COUNT(*) AS total_teachers,
            COUNT(*) FILTER (WHERE LOWER(status) = 'active') AS active_teachers,
            COUNT(*) FILTER (WHERE LOWER(status) = 'inactive') AS inactive_teachers,
            COUNT(DISTINCT department) AS total_departments
        FROM teachers;
    """)

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result











