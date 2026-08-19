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
from werkzeug.security import generate_password_hash
##############################
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

        # ==========================================================
        # 1. UPDATE STUDENT
        # ==========================================================

        cur.execute("""
            UPDATE students
            SET
                student_name = %s,
                dob = %s,
                gender = %s,
                blood_group = %s,
                email = %s,
                phone = %s,
                address = %s,
                city = %s,
                state = %s,
                pincode = %s,
                registration_status = 'Completed',
                updated_at = CURRENT_TIMESTAMP
            WHERE student_id = %s
        """, (
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

        # ==========================================================
        # GET STUDENT ROLL NUMBER
        # ==========================================================

        cur.execute("""
            SELECT roll_no
            FROM students
            WHERE student_id = %s
        """, (student_id,))

        student_data = cur.fetchone()

        if not student_data:
            raise Exception("Student not found.")

        roll_no = student_data[0]

        # ==========================================================
        # 2. CHECK PARENT LINKED TO THIS STUDENT
        # ==========================================================

        cur.execute("""
            SELECT parent_id
            FROM parents
            WHERE student_id = %s
        """, (student_id,))

        student_parent = cur.fetchone()

        # ==========================================================
        # CASE 1:
        # Parent already linked with this student
        # ==========================================================

        if student_parent:

            parent_id = student_parent[0]

            # Check if this roll number belongs to another user
            cur.execute("""
                SELECT id
                FROM users
                WHERE login_username = %s
                AND id != %s
            """, (
                roll_no,
                parent_id
            ))

            roll_taken = cur.fetchone()

            if roll_taken:

                raise Exception(
                    f"Roll number {roll_no} "
                    f"is already used by another account."
                )

            # Update parent login username = roll number
            cur.execute("""
                UPDATE users
                SET
                    login_username = %s,
                    role = 'parent',
                    account_status = 'active'
                WHERE id = %s
            """, (
                roll_no,
                parent_id
            ))

            # Update parent information
            cur.execute("""
                UPDATE parents
                SET
                    father_name = %s,
                    mother_name = %s,
                    phone = %s,
                    email = %s,
                    occupation = %s,
                    address = %s
                WHERE parent_id = %s
            """, (
                father_name,
                mother_name,
                parent_phone,
                parent_email,
                occupation,
                address,
                parent_id
            ))

        # ==========================================================
        # CASE 2:
        # This student has no parent linked,
        # but parent login already exists
        # ==========================================================

        else:

            # Search parent user using student roll number
            cur.execute("""
                SELECT id
                FROM users
                WHERE login_username = %s
            """, (roll_no,))

            existing_user = cur.fetchone()

            if existing_user:

                parent_id = existing_user[0]

                # Check whether this parent already has
                # a parent profile
                cur.execute("""
                    SELECT
                        parent_id,
                        student_id
                    FROM parents
                    WHERE parent_id = %s
                """, (parent_id,))

                existing_parent = cur.fetchone()

                # --------------------------------------------------
                # Existing parent profile found
                # --------------------------------------------------

                if existing_parent:

                    existing_student_id = existing_parent[1]

                    # Parent belongs to same student
                    if existing_student_id == student_id:

                        cur.execute("""
                            UPDATE parents
                            SET
                                father_name = %s,
                                mother_name = %s,
                                phone = %s,
                                email = %s,
                                occupation = %s,
                                address = %s
                            WHERE parent_id = %s
                        """, (
                            father_name,
                            mother_name,
                            parent_phone,
                            parent_email,
                            occupation,
                            address,
                            parent_id
                        ))

                    # Parent belongs to another student
                    else:

                        raise Exception(
                            f"Roll number {roll_no} "
                            f"is already linked with another student."
                        )

                # --------------------------------------------------
                # User exists but parent profile does not exist
                # --------------------------------------------------

                else:

                    cur.execute("""
                        UPDATE users
                        SET
                            role = 'parent',
                            account_status = 'active'
                        WHERE id = %s
                    """, (parent_id,))

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
                    """, (
                        parent_id,
                        student_id,
                        father_name,
                        mother_name,
                        parent_phone,
                        parent_email,
                        occupation,
                        address
                    ))

            # ======================================================
            # CASE 3:
            # Parent user does NOT exist → create new parent
            # ======================================================

            else:

                hashed_password = generate_password_hash(
                    "Parent@123"
                )

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
                        'parent',
                        TRUE,
                        'active'
                    )
                    RETURNING id
                """, (
                    roll_no,
                    hashed_password
                ))

                parent_id = cur.fetchone()[0]

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
                """, (
                    parent_id,
                    student_id,
                    father_name,
                    mother_name,
                    parent_phone,
                    parent_email,
                    occupation,
                    address
                ))

        # ==========================================================
        # 3. COMMIT
        # ==========================================================

        conn.commit()

        print("PROFILE UPDATED SUCCESSFULLY")

        return True

    except Exception as e:

        conn.rollback()

        print("=" * 60)
        print("PROFILE UPDATE ERROR:", repr(e))
        print("=" * 60)

        raise

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

    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT
                a.attendance_id,
                a.student_id,
                a.course_id,
                c.course_name,
                a.attendance_date,
                a.status,
                a.remarks
            FROM attendance a

            INNER JOIN courses c
                ON a.course_id = c.course_id

            WHERE a.student_id = %s
            AND a.attendance_date = CURRENT_DATE

            ORDER BY c.course_name
        """, (student_id,))

        rows = cur.fetchall()

        print("TODAY ATTENDANCE:", rows)

        attendance = []

        for row in rows:

            attendance.append({
                "attendance_id": row[0],
                "student_id": row[1],
                "course_id": row[2],
                "course_name": row[3],
                "attendance_date": row[4],
                "status": row[5],
                "remarks": row[6]
            })

        return attendance

    except Exception as e:

        print(
            "GET TODAY ATTENDANCE ERROR:",
            repr(e)
        )

        return []

    finally:

        try:
            cur.close()
        except:
            pass

        conn.close()







def get_student_timetable(student_id):

    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        query = """
            SELECT
                t.timetable_id,
                t.day_name,
                t.start_time,
                t.end_time,
                t.room_no,
                t.semester,
                c.course_code,
                c.course_name,
                c.department,
                te.teacher_name

            FROM timetable t

            INNER JOIN courses c
                ON t.course_id = c.course_id

            LEFT JOIN teachers te
                ON t.teacher_id = te.teacher_id

            WHERE t.semester = (
                SELECT CAST(semester AS INTEGER)
                FROM students
                WHERE student_id = %s
            )

            AND t.status = 'Scheduled'

            ORDER BY
                CASE t.day_name
                    WHEN 'Monday' THEN 1
                    WHEN 'Tuesday' THEN 2
                    WHEN 'Wednesday' THEN 3
                    WHEN 'Thursday' THEN 4
                    WHEN 'Friday' THEN 5
                    WHEN 'Saturday' THEN 6
                    WHEN 'Sunday' THEN 7
                    ELSE 8
                END,
                t.start_time
        """

        cur.execute(query, (student_id,))

        rows = cur.fetchall()

        print("================================")
        print("STUDENT TIMETABLE DEBUG")
        print("STUDENT ID:", student_id)
        print("TIMETABLE ROWS:", rows)
        print("ROW COUNT:", len(rows))
        print("================================")

        return rows

    except Exception as e:

        print("Student Timetable Error:", e)

        return []

    finally:

        if cur:
            cur.close()

        if conn:
            conn.close()













def get_student_courses(student_id):

    conn = get_connection()

    try:

        cur = conn.cursor()

        cur.execute("""
            SELECT
                c.course_id,
                c.course_code,
                c.course_name,
                c.department,
                c.semester,
                c.teacher_id,
                c.credits,
                t.teacher_name

            FROM student_courses sc

            INNER JOIN courses c
                ON sc.course_id = c.course_id

            LEFT JOIN teachers t
                ON c.teacher_id = t.teacher_id

            WHERE sc.student_id = %s

            ORDER BY c.semester, c.course_code
        """, (student_id,))

        rows = cur.fetchall()

        courses = []

        for row in rows:

            courses.append({
                "Course ID": row[0],
                "Course Code": row[1],
                "Course Name": row[2],
                "Department": row[3],
                "Semester": row[4],
                "Teacher ID": row[5],
                "Credits": row[6],
                "Teacher": row[7] or "Not Assigned"
            })

        return courses

    except Exception as e:

        print(
            "GET STUDENT COURSES ERROR:",
            e
        )

        return []

    finally:

        cur.close()
        conn.close()




def get_student_profile(student_id):

    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT
            s.student_id,
            s.student_name,
            s.dob,
            s.gender,
            s.blood_group,
            s.email,
            s.phone,
            s.address,
            s.city,
            s.state,
            s.pincode,
            s.enrollment_no,
            s.roll_no,
            s.department,
            s.semester,
            s.photo,

            p.father_name,
            p.mother_name,
            p.phone AS parent_phone,
            p.email AS parent_email

        FROM students s

        LEFT JOIN parents p
            ON s.student_id = p.student_id

        WHERE s.student_id = %s
    """

    cur.execute(query, (student_id,))

    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return None

    columns = [desc[0] for desc in cur.description]

    profile = dict(zip(columns, row))

    cur.close()
    conn.close()

    return profile






def get_student_dashboard_summary(student_id):

    conn = get_connection()
    cur = conn.cursor()

    # -----------------------------
    # 1. ATTENDANCE
    # -----------------------------

    cur.execute("""
        SELECT
            COUNT(*) AS total_classes,
            COUNT(*) FILTER (
                WHERE status = 'Present'
            ) AS present_classes
        FROM attendance
        WHERE student_id = %s
    """, (student_id,))

    attendance_row = cur.fetchone()

    total_classes = attendance_row[0] or 0
    present_classes = attendance_row[1] or 0

    if total_classes > 0:
        attendance = round(
            (present_classes / total_classes) * 100,
            2
        )
    else:
        attendance = 0


    # -----------------------------
    # 2. ENROLLED COURSES
    # -----------------------------

    cur.execute("""
        SELECT COUNT(DISTINCT course_id)
        FROM student_courses
        WHERE student_id = %s
    """, (student_id,))

    courses = cur.fetchone()[0] or 0


    # -----------------------------
    # 3. CGPA
    # -----------------------------

    # Results table me abhi data nahi hai
    cgpa = 0


    # -----------------------------
    # 4. PENDING ASSIGNMENTS
    # -----------------------------

    # Assignment module abhi complete nahi hai
    pending_assignments = 0


    # -----------------------------
    # CLOSE CONNECTION
    # -----------------------------

    cur.close()
    conn.close()


    return {
        "attendance": attendance,
        "cgpa": float(cgpa),
        "courses": int(courses),
        "pending_assignments": int(pending_assignments)
    }





















def get_student_today_classes(student_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            c.course_name,
            t.teacher_name,
            tt.start_time,
            tt.end_time
        FROM timetable tt

        JOIN courses c
            ON tt.course_id = c.course_id

        LEFT JOIN teachers t
            ON c.teacher_id = t.teacher_id

        WHERE tt.class_date = CURRENT_DATE

        ORDER BY tt.start_time
    """, ())

    rows = cur.fetchall()

    cur.close()
    conn.close()

    classes = []

    for row in rows:
        classes.append({
            "course_name": row[0],
            "teacher_name": row[1] or "Faculty",
            "start_time": row[2],
            "end_time": row[3]
        })

    return classes












'''def get_student_notices(student_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            notice_id,
            title,
            description,
            notice_date
        FROM notices
        WHERE status = 'Published'
        ORDER BY notice_date DESC
        LIMIT 5
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    notices = []

    for row in rows:

        notices.append({
            "notice_id": row[0],
            "title": row[1],
            "description": row[2],
            "notice_date": row[3]
        })

    return notices'''













def get_student_today_attendance(student_id):

    conn = get_connection()

    try:

        cur = conn.cursor()

        cur.execute("""
            SELECT
                a.attendance_id,
                a.student_id,
                a.course_id,
                c.course_name,
                a.attendance_date,
                a.status,
                a.remarks
            FROM attendance a

            INNER JOIN courses c
                ON a.course_id = c.course_id

            WHERE a.student_id = %s
            AND a.attendance_date = CURRENT_DATE

            ORDER BY c.course_name
        """, (student_id,))

        rows = cur.fetchall()

        print(
            "STUDENT TODAY ATTENDANCE:",
            rows
        )

        attendance = []

        for row in rows:

            attendance.append({

                "attendance_id": row[0],

                "student_id": row[1],

                "course_id": row[2],

                "course_name": row[3],

                "attendance_date": row[4],

                "status": row[5],

                "remarks": row[6]

            })

        return attendance

    except Exception as e:

        print(
            "GET STUDENT TODAY ATTENDANCE ERROR:",
            repr(e)
        )

        return []

    finally:

        try:
            cur.close()
        except:
            pass

        conn.close()







