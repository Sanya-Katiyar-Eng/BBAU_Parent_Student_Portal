from database.db import get_connection


def add_student(user_data, student_data):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
        INSERT INTO users(name,email,password,role)
        VALUES(%s,%s,%s,%s)
        RETURNING id
        """,
        (
            user_data["name"],
            user_data["email"],
            user_data["password"],
            "Student"
        ))

        user_id = cur.fetchone()[0]

        cur.execute("""
        INSERT INTO students(

            student_id,
            enrollment_no,
            roll_no,
            department,
            semester,
            gender,
            dob,
            phone,
            parent_email,
            address,
            photo

        )

        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

        """,

        (

            user_id,
            student_data["enrollment_no"],
            student_data["roll_no"],
            student_data["department"],
            student_data["semester"],
            student_data["gender"],
            student_data["dob"],
            student_data["phone"],
            student_data["parent_email"],
            student_data["address"],
            student_data["photo"]

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