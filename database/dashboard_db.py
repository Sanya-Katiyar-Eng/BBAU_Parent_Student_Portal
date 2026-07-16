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


def get_recent_activity():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT action, module, created_at
        FROM activity_logs
        ORDER BY created_at DESC
        LIMIT 10
    """)

    activity = cur.fetchall()

    cur.close()
    conn.close()

    return activity


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