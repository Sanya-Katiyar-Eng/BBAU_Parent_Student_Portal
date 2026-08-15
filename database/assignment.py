from database.db import get_connection


def add_assignment(
    course_id,
    title,
    description,
    due_date,
    uploaded_file,
    teacher_id,
    work_type="Assignment"
):
    """
    Teacher ke dwara Assignment, Homework ya Project
    database me save karta hai.
    """

    file_path = None

    # ------------------------------------------------------
    # File handling
    # ------------------------------------------------------

    if uploaded_file is not None:

        file_path = uploaded_file.name

        # Actual file saving baad me add kar sakte hain.
        # Abhi database me filename/path store hoga.


    # ------------------------------------------------------
    # Database Insert
    # ------------------------------------------------------

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO assignments
            (
                teacher_id,
                course_id,
                title,
                description,
                due_date,
                file_path,
                work_type
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                teacher_id,
                course_id,
                title,
                description,
                due_date,
                file_path,
                work_type
            )
        )

        conn.commit()

        return True

    except Exception as e:

        conn.rollback()

        print(
            "ADD ASSIGNMENT ERROR:",
            e
        )

        return False

    finally:

        cursor.close()
        conn.close()





















def get_teacher_assignments(teacher_id):
    """
    Given teacher_id ke assignments, homework aur projects
    database se fetch karta hai.
    """

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                a.assignment_id,
                a.title,
                a.description,
                a.work_type,
                a.due_date,
                a.file_path,
                a.created_at,
                c.course_name
            FROM assignments a
            JOIN courses c
                ON a.course_id = c.course_id
            WHERE a.teacher_id = %s
            ORDER BY a.created_at DESC
            """,
            (teacher_id,)
        )

        rows = cursor.fetchall()

        assignments = []

        for row in rows:

            assignments.append({
                "Assignment ID": row[0],
                "Title": row[1],
                "Description": row[2],
                "Type": row[3],
                "Due Date": row[4],
                "File": row[5],
                "Created At": row[6],
                "Course": row[7]
            })

        return assignments

    except Exception as e:

        print(
            "GET TEACHER ASSIGNMENTS ERROR:",
            e
        )

        return []

    finally:

        cursor.close()
        conn.close()







#Update........................................
def update_assignment(
    assignment_id,
    title,
    description,
    due_date,
    uploaded_file=None,
    work_type="Assignment"
):
    """
    Existing assignment, homework ya project ko update karta hai.
    """

    conn = get_connection()

    try:

        cursor = conn.cursor()

        # --------------------------------------------------
        # File
        # --------------------------------------------------

        file_path = None

        if uploaded_file is not None:
            file_path = uploaded_file.name


        # --------------------------------------------------
        # Update with new file
        # --------------------------------------------------

        if uploaded_file is not None:

            cursor.execute(
                """
                UPDATE assignments
                SET
                    title = %s,
                    description = %s,
                    due_date = %s,
                    file_path = %s,
                    work_type = %s
                WHERE assignment_id = %s
                """,
                (
                    title,
                    description,
                    due_date,
                    file_path,
                    work_type,
                    assignment_id
                )
            )

        # --------------------------------------------------
        # Update without changing file
        # --------------------------------------------------

        else:

            cursor.execute(
                """
                UPDATE assignments
                SET
                    title = %s,
                    description = %s,
                    due_date = %s,
                    work_type = %s
                WHERE assignment_id = %s
                """,
                (
                    title,
                    description,
                    due_date,
                    work_type,
                    assignment_id
                )
            )


        conn.commit()

        return cursor.rowcount > 0


    except Exception as e:

        conn.rollback()

        print(
            "UPDATE ASSIGNMENT ERROR:",
            e
        )

        return False


    finally:

        cursor.close()
        conn.close()









#delete assignment
def delete_assignment(assignment_id):
    """
    Assignment, Homework ya Project ko
    assignment_id ke basis par delete karta hai.
    """

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM assignments
            WHERE assignment_id = %s
            """,
            (assignment_id,)
        )

        conn.commit()

        return cursor.rowcount > 0

    except Exception as e:

        conn.rollback()

        print(
            "DELETE ASSIGNMENT ERROR:",
            e
        )

        return False

    finally:

        cursor.close()
        conn.close()







#add notice
def add_notice(
    course_id,
    title,
    description,
    notice_type,
    expiry_date,
    file_path,
    created_by
):
    """
    Teacher ke dwara create kiya gaya notice
    database me save karta hai.
    """

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO notices
            (
                course_id,
                title,
                description,
                notice_type,
                expiry_date,
                file_path,
                created_by
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                course_id,
                title,
                description,
                notice_type,
                expiry_date,
                file_path,
                created_by
            )
        )

        conn.commit()

        return True

    except Exception as e:

        conn.rollback()

        print(
            "ADD NOTICE ERROR:",
            e
        )

        return False

    finally:

        cursor.close()
        conn.close()


def get_teacher_notices(created_by):

    """
    Logged-in teacher ke published notices
    database se fetch karta hai.
    """

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                n.notice_id,
                n.title,
                n.description,
                n.notice_type,
                n.expiry_date,
                n.file_path,
                n.created_at,
                c.course_name
            FROM notices n

            LEFT JOIN courses c
                ON n.course_id = c.course_id

            WHERE n.created_by = %s

            ORDER BY n.created_at DESC
            """,
            (created_by,)
        )

        rows = cursor.fetchall()

        notices = []

        for row in rows:

            notices.append({

                "notice_id": row[0],

                "title": row[1],

                "message": row[2],

                "notice_type": row[3],

                "expiry_date": row[4],

                "file_path": row[5],

                "created_at": row[6],

                "course": row[7]

            })

        return notices

    except Exception as e:

        print(
            "GET TEACHER NOTICES ERROR:",
            e
        )

        return []

    finally:

        cursor.close()
        conn.close()







## update notice
def update_notice(
    notice_id,
    course_id,
    title,
    description,
    notice_type,
    expiry_date,
    file_path=None
):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        # --------------------------------------------------
        # File ke saath update
        # --------------------------------------------------

        if file_path is not None:

            cursor.execute(
                """
                UPDATE notices
                SET
                    course_id = %s,
                    title = %s,
                    description = %s,
                    notice_type = %s,
                    expiry_date = %s,
                    file_path = %s
                WHERE notice_id = %s
                """,
                (
                    course_id,
                    title,
                    description,
                    notice_type,
                    expiry_date,
                    file_path,
                    notice_id
                )
            )

        # --------------------------------------------------
        # File change nahi karna
        # --------------------------------------------------

        else:

            cursor.execute(
                """
                UPDATE notices
                SET
                    course_id = %s,
                    title = %s,
                    description = %s,
                    notice_type = %s,
                    expiry_date = %s
                WHERE notice_id = %s
                """,
                (
                    course_id,
                    title,
                    description,
                    notice_type,
                    expiry_date,
                    notice_id
                )
            )

        conn.commit()

        return cursor.rowcount > 0

    except Exception as e:

        conn.rollback()

        print(
            "UPDATE NOTICE ERROR:",
            e
        )

        return False

    finally:

        cursor.close()
        conn.close()






#delet notice.........................
def delete_notice(notice_id):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM notices
            WHERE notice_id = %s
            """,
            (notice_id,)
        )

        conn.commit()

        return cursor.rowcount > 0

    except Exception as e:

        conn.rollback()

        print(
            "DELETE NOTICE ERROR:",
            e
        )

        return False

    finally:

        cursor.close()
        conn.close()







#student assingment
def get_student_assignments(student_id):

    conn = get_connection()

    try:

        cur = conn.cursor()

        # 1. Student check
        cur.execute("""
            SELECT
                student_id,
                student_name,
                department,
                semester
            FROM students
            WHERE student_id = %s
        """, (student_id,))

        student = cur.fetchone()

        print("STUDENT:", student)

        if not student:
            print("❌ STUDENT NOT FOUND")
            return []

        # 2. Assignment check
        cur.execute("""
            SELECT
                assignment_id,
                teacher_id,
                course_id,
                title,
                description,
                due_date,
                file_path,
                created_at,
                work_type
            FROM assignments
            ORDER BY created_at DESC
        """)

        assignment_rows = cur.fetchall()

        print(
            "TOTAL ASSIGNMENTS:",
            len(assignment_rows)
        )

        for row in assignment_rows:
            print("ASSIGNMENT:", row)

        # 3. Student ke department/semester ke courses
        cur.execute("""
            SELECT
                course_id,
                course_code,
                course_name,
                department,
                semester,
                teacher_id
            FROM courses
            WHERE department = %s
            AND semester = %s
        """, (
            student[2],
            student[3]
        ))

        courses = cur.fetchall()

        print(
            "STUDENT COURSES:",
            courses
        )

        # 4. Final assignment query
        cur.execute("""
            SELECT
                a.assignment_id,
                a.title,
                a.description,
                a.due_date,
                a.file_path,
                a.work_type,
                a.created_at,

                c.course_id,
                c.course_code,
                c.course_name,

                t.teacher_id,
                t.teacher_name

            FROM assignments a

            JOIN courses c
                ON a.course_id = c.course_id

            LEFT JOIN teachers t
                ON a.teacher_id = t.teacher_id

            WHERE c.department = %s
            AND c.semester = %s

            ORDER BY
                a.due_date ASC NULLS LAST,
                a.created_at DESC
        """, (
            student[2],
            student[3]
        ))

        rows = cur.fetchall()

        print(
            "FINAL ASSIGNMENTS:",
            rows
        )

        assignments = []

        for row in rows:

            assignments.append({

                "Assignment ID": row[0],

                "Title": row[1],

                "Description": row[2],

                "Due Date": row[3],

                "File": row[4],

                "Type": row[5],

                "Created At": row[6],

                "Course ID": row[7],

                "Course Code": row[8],

                "Course": row[9],

                "Teacher ID": row[10],

                "Teacher": (
                    row[11]
                    if row[11]
                    else "Teacher"
                )
            })

        print(
            "RETURNING:",
            len(assignments),
            "assignments"
        )

        return assignments

    except Exception as e:

        print(
            "GET ASSIGNMENTS ERROR:",
            repr(e)
        )

        return []

    finally:

        try:
            cur.close()
        except:
            pass

        conn.close()































## student notice
def get_student_notices(student_id):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                n.notice_id,
                n.title,
                n.description,
                n.notice_type,
                n.expiry_date,
                n.file_path,
                n.created_at,
                c.course_name
            FROM notices n

            INNER JOIN courses c
                ON n.course_id = c.course_id

            INNER JOIN students s
                ON LOWER(s.department) = LOWER(c.department)
                AND s.semester = c.semester

            WHERE s.student_id = %s

            AND (
                n.expiry_date IS NULL
                OR n.expiry_date >= CURRENT_DATE
            )

            ORDER BY n.created_at DESC
            """,
            (student_id,)
        )

        rows = cursor.fetchall()

        notices = []

        for row in rows:

            notices.append({

                "Notice ID": row[0],

                "Title": row[1],

                "Description": row[2],

                "Type": row[3],

                "Expiry Date": row[4],

                "File": row[5],

                "Created At": row[6],

                "Course": row[7]

            })

        return notices

    except Exception as e:

        print(
            "GET STUDENT NOTICES ERROR:",
            e
        )

        return []

    finally:

        cursor.close()
        conn.close()