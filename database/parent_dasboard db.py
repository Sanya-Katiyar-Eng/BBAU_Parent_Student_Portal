from database.db import get_connection
def get_parent_student(user_id):

    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT
            s.student_name,
            s.enrollment_no,
            s.course,
            s.semester,
            s.department
        FROM users u
        JOIN parents p
            ON u.id = p.user_id
        JOIN students s
            ON p.student_id = s.id
        WHERE u.id = %s
          AND u.role = 'parent';
    """

    cur.execute(query, (user_id,))
    student = cur.fetchone()

    cur.close()
    conn.close()

    return student