from database.db import get_connection
import streamlit as st

def add_student(
    roll_no,
    enrollment_no,
    department,
    semester,
    password
):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            INSERT INTO students
            (
                roll_no,
                enrollment_no,
                department,
                semester,
                password,
                first_login,
                registration_status,
                account_status
            )

            VALUES
            (
                %s,%s,%s,%s,%s,TRUE,'Pending','Active'
            )
        """,
        (
            roll_no,
            enrollment_no,
            department,
            semester,
            password
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
            DELETE FROM students
            WHERE enrollment_no = %s
        """, (enrollment_no,))

        conn.commit()

        if cur.rowcount > 0:
            return True

        return False

    except Exception as e:
        conn.rollback()
        print(e)
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