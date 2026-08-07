from database.db import get_connection


def get_dashboard_counts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM students")
    total_students = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM teachers")
    total_teachers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM parents")
    total_parents = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {
        "students": total_students,
        "teachers": total_teachers,
        "parents": total_parents
    }
from database.db import get_connection

def get_all_courses():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT course_id, course_name
        FROM courses
        ORDER BY course_name
    """)

    courses = cur.fetchall()

    cur.close()
    conn.close()

    return courses
from database.db import get_connection


def assign_student_to_course(student_id, course_id):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            INSERT INTO student_courses
            (student_id, course_id)
            VALUES (%s,%s)
        """,
        (student_id, course_id))


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
            s.enrollment_no

        FROM students s

        INNER JOIN student_courses sc
        ON s.student_id = sc.student_id

        WHERE sc.course_id = %s

    """, (course_id,))


    students = cur.fetchall()

    cur.close()
    conn.close()

    return students

def get_students_by_department():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT department, COUNT(*)
        FROM students
        GROUP BY department
        ORDER BY department
    """)

    data = cur.fetchall()

    cur.close()
    conn.close()

    return data




def get_students_by_gender():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT gender, COUNT(*)
        FROM students
        GROUP BY gender
        ORDER BY gender;
    """)

    data = cur.fetchall()

    cur.close()
    conn.close()

    return data



def get_monthly_registration():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            TO_CHAR(created_at,'Mon') AS month,
            COUNT(*)
        FROM students
        GROUP BY
            EXTRACT(MONTH FROM created_at),
            TO_CHAR(created_at,'Mon')
        ORDER BY
            EXTRACT(MONTH FROM created_at);
    """)

    data = cur.fetchall()

    cur.close()
    conn.close()

    return data


def get_all_students():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            student_id,
            student_name,
            enrollment_no
        FROM students
        ORDER BY student_name
    """)

    students = cur.fetchall()

    cur.close()
    conn.close()

    return students

def get_all_teachers():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            teacher_id,
            teacher_name,
            email,
            specialization
        FROM teachers
        ORDER BY teacher_name
    """)

    teachers = cur.fetchall()

    cur.close()
    conn.close()

    return teachers

def get_recent_activity():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            activity,
            created_at
        FROM activity_logs
        ORDER BY created_at DESC
        LIMIT 10
    """)

    data = cur.fetchall()

    cur.close()
    conn.close()

    return data




#..............................................................
#Save attendance
#....................................................................
def save_attendance(course_id, attendance_date, teacher_id, attendance_data):

    conn = get_connection()
    cur = conn.cursor()

    try:

        for student in attendance_data:

            # Check if attendance already exists
            cur.execute("""
                SELECT attendance_id
                FROM attendance
                WHERE student_id=%s
                AND course_id=%s
                AND attendance_date=%s
            """, (
                student["student_id"],
                course_id,
                attendance_date
            ))

            exists = cur.fetchone()

            if exists:

                cur.execute("""
                    UPDATE attendance
                    SET
                        status=%s,
                        marked_by=%s
                    WHERE attendance_id=%s
                """, (
                    student["status"],
                    teacher_id,
                    exists[0]
                ))

            else:

                cur.execute("""
                    INSERT INTO attendance
                    (
                        student_id,
                        course_id,
                        attendance_date,
                        status,
                        marked_by
                    )
                    VALUES(%s,%s,%s,%s,%s)
                """, (

                    student["student_id"],
                    course_id,
                    attendance_date,
                    student["status"],
                    teacher_id

                ))

        conn.commit()
        return True

    except Exception as e:

        print(e)
        conn.rollback()
        return False

    finally:

        cur.close()
        conn.close()


#...........................................................
#parent dashboard ke liye attendence
#..................................................................
def get_student_attendance(student_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            COUNT(*) FILTER
            (WHERE status='Present'),

            COUNT(*)

        FROM attendance

        WHERE student_id=%s

    """,(student_id,))

    present,total = cur.fetchone()

    cur.close()
    conn.close()

    if total==0:
        return 0

    return round((present/total)*100,2)

#........................................
#Attendance history
#.............................................
def get_attendance_history(student_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            c.course_name,
            attendance_date,
            status

        FROM attendance a

        JOIN courses c

        ON a.course_id=c.course_id

        WHERE student_id=%s

        ORDER BY attendance_date DESC

    """,(student_id,))

    data=cur.fetchall()

    cur.close()
    conn.close()

    return data

#.................................................................\
#parent mobile number

def get_parent_mobile(student_id):

    conn=get_connection()
    cur=conn.cursor()

    cur.execute("""

        SELECT phone

        FROM parents

        WHERE student_id=%s

    """,(student_id,))

    row=cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return row[0]

    return None

#..............................................................
def get_student_attendance_percentage(student_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT

            COUNT(*) FILTER (WHERE status='Present'),
            COUNT(*)

        FROM attendance

        WHERE student_id=%s

    """,(student_id,))

    present,total = cur.fetchone()

    cur.close()
    conn.close()

    if total == 0:
        return 0

    return round((present/total)*100,2)



def get_parent_details(student_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            p.phone,
            p.email,
            s.student_name

        FROM parents p

        JOIN students s

        ON p.student_id = s.student_id

        WHERE p.student_id=%s

    """,(student_id,))

    data = cur.fetchone()

    cur.close()
    conn.close()

    return data