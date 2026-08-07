from database.db import get_connection




def create_parent_from_student(student_id):

    conn = get_connection()
    cur = conn.cursor()

    try:

        # Student data fetch

        cur.execute(
            """
            SELECT
                student_id,
                father_name,
                mother_name,
                phone,
                email,
                address,
                occupation

            FROM students

            WHERE student_id=%s
            """,
            (student_id,)
        )


        student = cur.fetchone()


        if not student:
            return False



        # check already parent exists

        cur.execute(
            """
            SELECT parent_id
            FROM parents
            WHERE student_id=%s
            """,
            (student_id,)
        )


        existing = cur.fetchone()


        if existing:
            return True



        # Insert parent


        cur.execute(
            """
            INSERT INTO parents
            (
                student_id,
                father_name,
                mother_name,
                phone,
                email,
                address,
                occupation,
                status
            )

            VALUES
            (%s,%s,%s,%s,%s,%s,%s,'Active')

            """,

            (
                student[0],
                student[1],
                student[2],
                student[3],
                student[4],
                student[5],
                student[6]
            )
        )


        conn.commit()


        return True



    except Exception as e:

        conn.rollback()

        print("Parent Auto Create Error:",e)

        return False


    finally:

        cur.close()
        conn.close()  































        
def get_students_for_dropdown():
    """
    Returns active students for Parent Registration dropdown.
    Format:
    [
        (student_id, "Enrollment No - Student Name")
    ]
    """

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            SELECT
                student_id,
                enrollment_no,
                student_name
            FROM students
            WHERE account_status = 'Active'
            ORDER BY enrollment_no;
        """)


        students = cur.fetchall()


        dropdown_data = []


        for student in students:

            student_id = student[0]

            enrollment = student[1]

            name = student[2]


            dropdown_data.append(
                (
                    student_id,
                    f"{enrollment} - {name}"
                )
            )


        return dropdown_data



    except Exception as e:

        print("Student Dropdown Error:", e)

        return []



    finally:

        cur.close()

        conn.close()

#===========================================================================================================
#Student by ID
#===================================================================================================================
from database.db import get_connection


def get_student_by_id(student_id):
    """
    Returns complete details of a student using student_id.
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT
                student_id,
                enrollment_no,
                full_name,
                department,
                semester,
                gender,
                dob,
                phone,
                email,
                address,
                account_status
            FROM students
            WHERE student_id = %s;
        """, (student_id,))

        student = cur.fetchone()

        return student

    except Exception as e:
        print("Error:", e)
        return None

    finally:
        cur.close()
        conn.close()


#+========================================================================================
#search by keyword
#=========================================================================================================================
from database.db import get_connection


def search_student(keyword):
    """
    Search students by Enrollment No or Student Name.
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        search = f"%{keyword}%"

        cur.execute("""
            SELECT
                student_id,
                enrollment_no,
                full_name,
                department,
                semester
            FROM students
            WHERE
                enrollment_no ILIKE %s
                OR full_name ILIKE %s
            ORDER BY enrollment_no;
        """, (search, search))

        students = cur.fetchall()

        return students

    except Exception as e:
        print("Error:", e)
        return []

    finally:
        cur.close()
        conn.close()

#=================================================================================================
#  Add parent
# =================================================================================================

from database.db import get_connection


def add_parent(parent_data):
    conn = get_connection()
    cur = conn.cursor()

    try:
        # -------------------------------
        # Check Student Exists
        # -------------------------------
        cur.execute("""
            SELECT student_id
            FROM students
            WHERE student_id = %s;
        """, (parent_data["student_id"],))

        if cur.fetchone() is None:
            return False, "Student not found."

        # -------------------------------
        # Check Duplicate Phone
        # -------------------------------
        cur.execute("""
            SELECT 1
            FROM parents
            WHERE phone = %s;
        """, (parent_data["phone"],))

        if cur.fetchone():
            return False, "Phone number already exists."

        # -------------------------------
        # Check Duplicate Email
        # -------------------------------
        cur.execute("""
            SELECT 1
            FROM parents
            WHERE email = %s;
        """, (parent_data["email"],))

        if cur.fetchone():
            return False, "Email already exists."

        # -------------------------------
        # Insert Parent
        # -------------------------------
        cur.execute("""
            INSERT INTO parents (
                student_id,
                parent_name,
                relation,
                occupation,
                phone,
                email,
                address,
                photo,
                status,
                created_at
            )
            VALUES (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,NOW()
            )
            RETURNING parent_id;
        """, (
            parent_data["student_id"],
            parent_data["parent_name"],
            parent_data["relation"],
            parent_data["occupation"],
            parent_data["phone"],
            parent_data["email"],
            parent_data["address"],
            parent_data["photo"],
            "Active"
        ))

        parent_id = cur.fetchone()[0]

        # -------------------------------
        # Create Login Account
        # -------------------------------
        cur.execute("""
            INSERT INTO users (
                login_username,
                password,
                role,
                first_login,
                account_status
            )
            VALUES (%s,%s,%s,%s,%s);
        """, (
            parent_data["phone"],          # Username
            parent_data["password"],       # Temporary Password
            "parent",
            True,
            "Active"
        ))

        conn.commit()

        return True, parent_id

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        cur.close()
        conn.close()



#============================================================================================================
# get all parent
#==============================================================
def get_all_parents():
    """
    Returns all parents with student details.
    """

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            SELECT

                p.parent_id,

                p.father_name,

                p.mother_name,

                p.phone,

                p.email,

                p.occupation,

                p.status,

                p.student_id,

                s.enrollment_no,

                s.student_name,

                s.department,

                s.semester


            FROM parents p


            INNER JOIN students s

            ON p.student_id = s.student_id


            ORDER BY p.parent_id DESC;

        """)


        parents = cur.fetchall()

        return parents


    except Exception as e:

        print("Get Parents Error:",e)

        return []


    finally:

        cur.close()

        conn.close()

 
#=================================================================================================
# get_parent_by_id(parent_id)
#=============================================================================================================
def get_parent_by_id(parent_id):

    conn=get_connection()
    cur=conn.cursor()


    try:

        cur.execute("""
        SELECT

        p.parent_id,
        p.student_id,
        p.father_name,
        p.mother_name,
        p.occupation,
        p.phone,
        p.email,
        p.address,
        p.status,
        p.created_at,


        s.enrollment_no,
        s.student_name,
        s.department,
        s.semester


        FROM parents p


        JOIN students s

        ON p.student_id=s.student_id


        WHERE p.parent_id=%s

        """,(parent_id,))


        return cur.fetchone()


    except Exception as e:

        print(e)

        return None


    finally:

        cur.close()
        conn.close()
#=====================================================================================================================
# update_parent(parent_id, parent_data)
#===========================================================================================================
from database.db import get_connection


def update_parent(parent_id, parent_data):
    """
    Update parent details.
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        # Check duplicate phone
        cur.execute("""
            SELECT 1
            FROM parents
            WHERE phone = %s
            AND parent_id != %s;
        """, (parent_data["phone"], parent_id))

        if cur.fetchone():
            return False, "Phone number already exists."

        # Check duplicate email
        cur.execute("""
            SELECT 1
            FROM parents
            WHERE email = %s
            AND parent_id != %s;
        """, (parent_data["email"], parent_id))

        if cur.fetchone():
            return False, "Email already exists."

        # Update parent
        cur.execute("""
            UPDATE parents
            SET
                parent_name = %s,
                relation = %s,
                occupation = %s,
                phone = %s,
                email = %s,
                address = %s,
                photo = %s,
                status = %s
            WHERE parent_id = %s;
        """, (
            parent_data["parent_name"],
            parent_data["relation"],
            parent_data["occupation"],
            parent_data["phone"],
            parent_data["email"],
            parent_data["address"],
            parent_data["photo"],
            parent_data["status"],
            parent_id
        ))

        # Update username in users table
        cur.execute("""
            UPDATE users
            SET login_username = %s
            WHERE role = 'parent'
            AND login_username = %s;
        """, (
            parent_data["phone"],
            parent_data["old_phone"]
        ))

        conn.commit()

        return True, "Parent updated successfully."

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        cur.close()
        conn.close()


#=================================================================================================
#delete_parent(parent_id)

#=============================================================================================================

from database.db import get_connection


def delete_parent(parent_id):
    """
    Soft delete parent by changing status to Inactive.
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        # Parent inactive
        cur.execute("""
            UPDATE parents
            SET status = 'Inactive'
            WHERE parent_id = %s;
        """, (parent_id,))

        # Disable parent login
        cur.execute("""
            UPDATE users
            SET account_status = 'Inactive'
            WHERE login_username = (
                SELECT phone
                FROM parents
                WHERE parent_id = %s
            );
        """, (parent_id,))

        conn.commit()

        return True, "Parent deleted successfully."

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        cur.close()
        conn.close()
#=====================================================================================================================
#search_parent(keyword)
#===========================================================================================================

from database.db import get_connection


def search_parent(keyword):
    """
    Search parent by parent name, student name,
    enrollment number, phone or email.
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        search = f"%{keyword}%"

        cur.execute("""
            SELECT
                p.parent_id,
                p.parent_name,
                p.relation,
                p.phone,
                p.email,
                p.occupation,
                p.status,

                s.student_id,
                s.enrollment_no,
                s.full_name,
                s.department,
                s.semester

            FROM parents p
            INNER JOIN students s
                ON p.student_id = s.student_id

            WHERE
                p.parent_name ILIKE %s
                OR p.phone ILIKE %s
                OR p.email ILIKE %s
                OR s.full_name ILIKE %s
                OR s.enrollment_no ILIKE %s

            ORDER BY p.parent_name;
        """, (
            search,
            search,
            search,
            search,
            search
        ))

        parents = cur.fetchall()

        return parents

    except Exception as e:
        print("Error:", e)
        return []

    finally:
        cur.close()
        conn.close()

#=================================================================================================
#filter_parents(department, semester, relation)
#=============================================================================================================

from database.db import get_connection


def filter_parents(department=None, semester=None, relation=None):
    """
    Filter parents by department, semester and relation.
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        query = """
            SELECT
                p.parent_id,
                p.parent_name,
                p.relation,
                p.phone,
                p.email,
                p.occupation,
                p.status,

                s.student_id,
                s.enrollment_no,
                s.full_name,
                s.department,
                s.semester

            FROM parents p
            INNER JOIN students s
                ON p.student_id = s.student_id

            WHERE 1=1
        """

        values = []

        if department:
            query += " AND s.department = %s"
            values.append(department)

        if semester:
            query += " AND s.semester = %s"
            values.append(semester)

        if relation:
            query += " AND p.relation = %s"
            values.append(relation)

        query += " ORDER BY p.parent_name;"

        cur.execute(query, tuple(values))

        parents = cur.fetchall()

        return parents

    except Exception as e:
        print("Error:", e)
        return []

    finally:
        cur.close()
        conn.close()
#=====================================================================================================================
#check_parent_phone(phone)
#===========================================================================================================
from database.db import get_connection


def check_parent_phone(phone):
    """
    Check if parent phone number already exists.
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT parent_id
            FROM parents
            WHERE phone = %s;
        """, (phone,))

        parent = cur.fetchone()

        if parent:
            return True

        return False

    except Exception as e:
        print("Error:", e)
        return False

    finally:
        cur.close()
        conn.close()


#=================================================================================================
# check_parent_email(email)
#=============================================================================================================
from database.db import get_connection


def check_parent_email(email):
    """
    Check if parent email already exists.
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT parent_id
            FROM parents
            WHERE email = %s;
        """, (email,))

        parent = cur.fetchone()

        if parent:
            return True

        return False

    except Exception as e:
        print("Error:", e)
        return False

    finally:
        cur.close()
        conn.close()

#=====================================================================================================================
# check_student_parent_exists(student_id)
#===========================================================================================================
from database.db import get_connection


def check_student_parent_exists(student_id):
    """
    Check whether a parent is already assigned
    to the given student.
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT parent_id
            FROM parents
            WHERE student_id = %s;
        """, (student_id,))

        parent = cur.fetchone()

        if parent:
            return True

        return False

    except Exception as e:
        print("Error:", e)
        return False

    finally:
        cur.close()
        conn.close()


#=================================================================================================
# create_parent_user(login_username, password)
#=============================================================================================================
from database.db import get_connection


def create_parent_user(login_username, password):
    """
    Create login account for parent.
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO users (
                login_username,
                password,
                role,
                first_login,
                account_status,
                created_at
            )
            VALUES (
                %s,
                %s,
                'parent',
                TRUE,
                'Active',
                NOW()
            );
        """, (
            login_username,
            password
        ))

        conn.commit()

        return True

    except Exception as e:
        conn.rollback()
        print("Error:", e)
        return False

    finally:
        cur.close()
        conn.close()


#=====================================================================================================================
# update_parent_password(parent_id, password)
#===========================================================================================================
from database.db import get_connection


def update_parent_password(parent_id, password):
    """
    Update parent's login password.
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE users
            SET
                password = %s,
                first_login = FALSE
            WHERE
                role = 'parent'
                AND login_username = (
                    SELECT phone
                    FROM parents
                    WHERE parent_id = %s
                );
        """, (
            password,
            parent_id
        ))

        conn.commit()

        if cur.rowcount > 0:
            return True

        return False

    except Exception as e:
        conn.rollback()
        print("Error:", e)
        return False

    finally:
        cur.close()
        conn.close()


#=================================================================================================
#get_parent_login(parent_id)
#=============================================================================================================

from database.db import get_connection


def get_parent_login(parent_id):
    """
    Returns parent login details.
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT
                u.login_username,
                u.password,
                u.role,
                u.first_login,
                u.account_status
            FROM users u
            INNER JOIN parents p
                ON u.login_username = p.phone
            WHERE p.parent_id = %s;
        """, (parent_id,))

        login_data = cur.fetchone()

        return login_data

    except Exception as e:
        print("Error:", e)
        return None

    finally:
        cur.close()
        conn.close()
#=====================================================================================================================
#update_parent_status(parent_id, status)
#===========================================================================================================
from database.db import get_connection


def update_parent_status(parent_id, status):
    """
    Update parent account status.
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        # Update parent status
        cur.execute("""
            UPDATE parents
            SET status = %s
            WHERE parent_id = %s;
        """, (status, parent_id))

        # Update user account status
        cur.execute("""
            UPDATE users
            SET account_status = %s
            WHERE role = 'parent'
            AND login_username = (
                SELECT phone
                FROM parents
                WHERE parent_id = %s
            );
        """, (
            status,
            parent_id
        ))

        conn.commit()

        if cur.rowcount > 0:
            return True

        return False

    except Exception as e:
        conn.rollback()
        print("Error:", e)
        return False

    finally:
        cur.close()
        conn.close()


#=================================================================================================
#count_total_parents()
#=============================================================================================================
from database.db import get_connection


def count_total_parents():
    """
    Returns total number of parents.
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT COUNT(*)
            FROM parents;
        """)

        total = cur.fetchone()[0]

        return total

    except Exception as e:
        print("Error:", e)
        return 0

    finally:
        cur.close()
        conn.close()

#=====================================================================================================================
#count_active_parents()
#===========================================================================================================

from database.db import get_connection


def count_active_parents():
    """
    Returns total number of active parents.
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT COUNT(*)
            FROM parents
            WHERE status = 'Active';
        """)

        total = cur.fetchone()[0]

        return total

    except Exception as e:
        print("Error:", e)
        return 0

    finally:
        cur.close()
        conn.close()

#=================================================================================================
#count_inactive_parents()
#=============================================================================================================
from database.db import get_connection


def count_inactive_parents():
    """
    Returns total number of inactive parents.
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT COUNT(*)
            FROM parents
            WHERE status = 'Inactive';
        """)

        total = cur.fetchone()[0]

        return total

    except Exception as e:
        print("Error:", e)
        return 0

    finally:
        cur.close()
        conn.close()

#=====================================================================================================================
#upload_parent_photo(parent_id, photo_path)
#===========================================================================================================

from database.db import get_connection


def upload_parent_photo(parent_id, photo_path):
    """
    Update parent photo.
    """

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE parents
            SET photo = %s
            WHERE parent_id = %s;
        """, (
            photo_path,
            parent_id
        ))

        conn.commit()

        if cur.rowcount > 0:
            return True

        return False

    except Exception as e:
        conn.rollback()
        print("Error:", e)
        return False

    finally:
        cur.close()
        conn.close()

#=================================================================================================
#Prent page db
#=============================================================================================================
from database.db import get_connection


def get_parent_dashboard(parent_id):

    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT
            s.student_id,
            s.student_name,
            s.enrollment_no,
            s.department,
            s.semester,
            s.roll_no,
            s.status,
            s.account_status,

            p.father_name,
            p.mother_name,
            p.phone,
            p.email

        FROM parents p
        INNER JOIN students s
            ON p.student_id = s.student_id

        WHERE p.parent_id = %s
        LIMIT 1;
    """

    cur.execute(query, (parent_id,))
    data = cur.fetchone()

    cur.close()
    conn.close()

    return data

#=====================================================================================================================
#
#===========================================================================================================
from database.db import get_connection
import streamlit as st


def get_parent_profile():

    conn = get_connection()
    cur = conn.cursor()

    user_id = st.session_state.user_id



    # Check parent table
    cur.execute("""
        SELECT *
        FROM parents
        WHERE parent_id = %s
    """, (user_id,))

    parent = cur.fetchone()
    print("Parent Table :", parent)

    # Check student table
    cur.execute("""
        SELECT *
        FROM students
        WHERE student_id = %s
    """, (st.session_state.student_id,))

    student = cur.fetchone()
    print("Student Table :", student)

    # Original Query
    query = """
        SELECT

            p.parent_id,
            p.student_id,

            p.father_name,
            p.mother_name,
            p.occupation,
            p.phone,
            p.email,
            p.address,

            s.student_name,
            s.roll_no,
            s.enrollment_no,
            s.department,
            s.semester,
            s.gender,
            s.dob,
            s.blood_group,
            s.email,
            s.phone,
            s.address,
            s.city,
            s.state,
            s.pincode,
            s.photo,
            s.status,
            s.account_status

        FROM parents p

        INNER JOIN students s
            ON p.student_id = s.student_id

        WHERE p.parent_id = %s
    """

    cur.execute(query, (user_id,))
    profile = cur.fetchone()

    print("Final Query :", profile)

    cur.close()
    conn.close()

    return profile



def get_child_attendance_summary(student_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            COUNT(*) FILTER (WHERE status='Present'),

            COUNT(*) FILTER (WHERE status='Absent'),

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

from datetime import date

def get_child_today_attendance(student_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            c.course_name,
            a.status

        FROM attendance a

        JOIN courses c

        ON c.course_id=a.course_id

        WHERE

            a.student_id=%s

            AND attendance_date=%s

    """,(student_id,date.today()))

    data=cur.fetchall()

    cur.close()
    conn.close()

    return data

def get_child_attendance_history(student_id):

    conn=get_connection()
    cur=conn.cursor()

    cur.execute("""

        SELECT

            attendance_date,
            c.course_name,
            status

        FROM attendance a

        JOIN courses c

        ON c.course_id=a.course_id

        WHERE student_id=%s

        ORDER BY attendance_date DESC

    """,(student_id,))

    data=cur.fetchall()

    cur.close()
    conn.close()

    return data
#=================================================================================================
#
#=============================================================================================================

def get_student_attendance():
    pass
#=====================================================================================================================
#
#===========================================================================================================
def get_student_results():
    pass


#=================================================================================================
#
#=============================================================================================================
def get_student_assignments():
    pass
#=====================================================================================================================
#
#===========================================================================================================
def get_parent_notices():
    pass

#=================================================================================================
#
#=============================================================================================================
def get_student_timetable():
    pass

#=====================================================================================================================
#
#===========================================================================================================



#=================================================================================================
#=============================================================================================================


#=====================================================================================================================
#
#===========================================================================================================



#=================================================================================================
#
#=============================================================================================================


#=====================================================================================================================
#
#===========================================================================================================
