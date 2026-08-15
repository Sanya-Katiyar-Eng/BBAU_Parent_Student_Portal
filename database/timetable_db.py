

from database.db import get_connection


# =========================================================
# ADD CLASS
# =========================================================
def add_class_schedule(
    teacher_id,
    course_id,
    class_date,
    day_name,
    start_time,
    end_time,
    room_no,
    semester
):

    conn = None

    try:

        from datetime import date

        if class_date < date.today():
            return False, "Past date par class schedule nahi kar sakte."

        if start_time >= end_time:
            return False, "End time, start time ke baad hona chahiye."

        conn = get_connection()
        cur = conn.cursor()

        query = """
            INSERT INTO timetable
            (
                teacher_id,
                course_id,
                class_date,
                day_name,
                start_time,
                end_time,
                room_no,
                semester,
                status
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                'Scheduled'
            )
        """

        cur.execute(
            query,
            (
                teacher_id,       # IMPORTANT
                course_id,        # IMPORTANT
                class_date,
                day_name,
                start_time,
                end_time,
                room_no,
                semester
            )
        )

        conn.commit()

        return True, "Class scheduled successfully."

    except Exception as e:

        if conn:
            conn.rollback()

        print("ADD CLASS ERROR:", e)

        return False, str(e)

    finally:

        if conn:
            conn.close()

# =========================================================
# UPDATE CLASS
# =========================================================

def update_class_schedule(
    timetable_id,
    teacher_id,
    course_id,
    day_name,
    start_time,
    end_time,
    room_no,
    semester
):

    conn = None
    cur = None

    try:

        conn = get_connection()
        cur = conn.cursor()

        if start_time >= end_time:
            return False, "End time must be after start time."

        cur.execute(
            """
            UPDATE timetable
            SET
                course_id = %s,
                day_name = %s,
                start_time = %s,
                end_time = %s,
                room_no = %s,
                semester = %s
            WHERE timetable_id = %s
              AND teacher_id = %s
            """,
            (
                course_id,
                day_name,
                start_time,
                end_time,
                room_no,
                semester,
                timetable_id,
                teacher_id
            )
        )

        if cur.rowcount == 0:

            conn.rollback()

            return False, "Class not found."

        conn.commit()

        return True, "Class updated successfully."

    except Exception as e:

        if conn:
            conn.rollback()

        print("Update Timetable Error:", e)

        return False, f"Database Error: {e}"

    finally:

        if cur:
            cur.close()

        if conn:
            conn.close()


# =========================================================
# DELETE CLASS
# =========================================================









def delete_class_schedule(timetable_id, teacher_id):

    conn = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        query = """
            DELETE FROM timetable
            WHERE timetable_id = %s
              AND teacher_id = %s
        """

        cur.execute(
            query,
            (timetable_id, teacher_id)
        )

        if cur.rowcount == 0:
            conn.rollback()
            return False, "Class not found or you are not allowed to delete it."

        conn.commit()

        return True, "Class deleted successfully."

    except Exception as e:

        if conn:
            conn.rollback()

        print("DELETE CLASS ERROR:", e)

        return False, str(e)

    finally:

        if conn:
            conn.close()



























# =========================================================
# GET ACTUAL TEACHER ID
# =========================================================

def get_actual_teacher_id(user_id):

    conn = None
    cur = None

    try:

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT teacher_id
            FROM teachers
            WHERE teacher_id = %s
            """,
            (user_id,)
        )

        result = cur.fetchone()

        if result:
            return result[0]

        return None

    except Exception as e:

        print("Actual Teacher ID Error:", e)

        return None

    finally:

        if cur:
            cur.close()

        if conn:
            conn.close()


# =========================================================
# GET COURSES FOR TEACHER
# =========================================================

def get_schedule_courses(teacher_id):

    conn = None
    cur = None

    try:

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                course_id,
                course_code,
                course_name,
                department,
                semester
            FROM courses
            WHERE teacher_id = %s
            ORDER BY semester, course_name
            """,
            (teacher_id,)
        )

        rows = cur.fetchall()

        courses = []

        for row in rows:

            courses.append({
                "Course ID": row[0],
                "Course Code": row[1],
                "Course Name": row[2],
                "Department": row[3],
                "Semester": row[4]
            })

        return courses

    except Exception as e:

        print("Schedule Courses Error:", e)

        return []

    finally:

        if cur:
            cur.close()

        if conn:
            conn.close()


def get_teacher_timetable(teacher_id):

    conn = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        query = """
            SELECT
                t.timetable_id,
                t.class_date,
                t.day_name,
                t.start_time,
                t.end_time,
                t.room_no,
                t.semester,
                t.course_id,
                c.course_name,
                c.course_code
            FROM timetable t
            INNER JOIN courses c
                ON t.course_id = c.course_id
            WHERE t.teacher_id = %s
              AND t.status = 'Scheduled'
            ORDER BY
                t.class_date ASC NULLS LAST,
                t.start_time ASC
        """

        cur.execute(query, (teacher_id,))
        rows = cur.fetchall()
        print("DEBUG TEACHER ID:", teacher_id)
        print("TEACHER TIMETABLE DATA:", rows)

        return rows

    except Exception as e:

        print("GET TEACHER TIMETABLE ERROR:", e)

        return []

    finally:

        if conn:
            conn.close()















def get_student_class_schedule(student_id):

    conn = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        query = """
            SELECT
                t.timetable_id,
                t.class_date,
                t.day_name,
                t.start_time,
                t.end_time,
                t.room_no,
                t.semester,
                t.course_id,
                c.course_name,
                c.course_code
            FROM timetable t
            JOIN students s
                ON t.semester = s.semester::integer
            JOIN courses c
                ON t.course_id = c.course_id
            WHERE s.student_id = %s
              AND t.status = 'Scheduled'
            ORDER BY
                t.class_date ASC,
                t.start_time ASC
        """

        cur.execute(query, (student_id,))

        rows = cur.fetchall()

        print("DEBUG STUDENT ID:", student_id)
        print("STUDENT CLASS SCHEDULE:", rows)

        cur.close()

        return rows

    except Exception as e:

        print("GET STUDENT CLASS SCHEDULE ERROR:", e)

        return []

    finally:

        if conn:
            conn.close()
