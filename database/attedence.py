from database.db import get_connection
def get_parent_phone_by_student(student_id):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT phone
            FROM parents
            WHERE student_id = %s
            LIMIT 1
        """, (student_id,))

        result = cur.fetchone()

        if result:
            phone = result[0]

            if phone:
                phone = str(phone).strip()

                # India country code add karein
                if not phone.startswith("+91"):
                    phone = "+91" + phone

                return phone

        return None

    except Exception as e:
        print("Error fetching parent phone:", e)
        return None

    finally:
        cur.close()
        conn.close()






def get_student_attendance_last_5_days(student_id):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT
                a.attendance_date,
                c.course_code,
                c.course_name,
                a.status,
                COALESCE(a.remarks, '')
            FROM attendance a

            INNER JOIN courses c
                ON a.course_id = c.course_id

            WHERE a.student_id = %s
              AND a.attendance_date >= CURRENT_DATE - INTERVAL '4 days'

            ORDER BY
                a.attendance_date DESC,
                c.course_code
        """, (student_id,))

        rows = cur.fetchall()

        attendance = []

        for row in rows:
            attendance.append({
                "date": row[0],
                "course_code": row[1],
                "course_name": row[2],
                "status": row[3],
                "remarks": row[4]
            })

        return attendance

    except Exception as e:
        print("Error fetching student attendance:", e)
        return []

    finally:
        cur.close()
        conn.close()



def get__last_5_days(parent_id):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT
                a.attendance_date,
                c.course_code,
                c.course_name,
                a.status,
                COALESCE(a.remarks, ''),
                s.student_name
            FROM attendance a

            INNER JOIN courses c
                ON a.course_id = c.course_id

            INNER JOIN students s
                ON a.student_id = s.student_id

            INNER JOIN parents p
                ON a.student_id = p.student_id

            WHERE p.parent_id = %s
              AND a.attendance_date >= CURRENT_DATE - INTERVAL '4 days'

            ORDER BY
                a.attendance_date DESC,
                c.course_code
        """, (parent_id,))

        rows = cur.fetchall()

        attendance = []

        for row in rows:
            attendance.append({
                "date": row[0],
                "course_code": row[1],
                "course_name": row[2],
                "status": row[3],
                "remarks": row[4],
                "student_name": row[5]
            })

        return attendance

    except Exception as e:
        print("Error fetching parent attendance:", e)
        return []

    finally:
        cur.close()
        conn.close()



