
import socketio
from aiohttp import web

from database.db import get_connection


# ==========================================
# Socket.IO Server
# ==========================================

sio = socketio.AsyncServer(
    async_mode="aiohttp",
    cors_allowed_origins="*"
)

app = web.Application()

sio.attach(app)


# ==========================================
# Parent Connected
# ==========================================

@sio.event
async def connect(sid, environ):

    print("Client connected:", sid)


# ==========================================
# Parent Disconnected
# ==========================================

@sio.event
async def disconnect(sid):

    print("Client disconnected:", sid)


# ==========================================
# Parent Join Room
# ==========================================

@sio.event
async def join_parent(sid, data):

    parent_id = data.get("parent_id")

    if not parent_id:
        return

    room = f"parent_{parent_id}"

    await sio.enter_room(
        sid,
        room
    )

    print(
        f"Parent {parent_id} joined room"
    )


# ==========================================
# TEST NOTIFICATION
# ==========================================

@sio.event
async def test_notification(sid, data):

    parent_id = data.get("parent_id")

    if not parent_id:
        return

    room = f"parent_{parent_id}"

    await sio.emit(
        "notification",
        {
            "title": "BBAU Portal",
            "message":
                "Socket.IO notification working successfully 🔔"
        },
        room=room
    )

    print(
        f"Test notification sent to parent {parent_id}"
    )


# ==========================================
# ATTENDANCE NOTIFICATION
# ==========================================

async def attendance_notification(request):

    try:

        data = await request.json()

        student_id = data.get("student_id")
        student_name = data.get("student_name")
        course_name = data.get("course_name")
        status = data.get("status")
        attendance_date = data.get("attendance_date")

        if not student_id:

            return web.json_response(
                {
                    "success": False,
                    "message": "student_id missing"
                },
                status=400
            )


        # ======================================
        # Get Parent ID from Database
        # ======================================

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT parent_id
            FROM parents
            WHERE student_id = %s
            LIMIT 1
            """,
            (student_id,)
        )

        result = cur.fetchone()

        cur.close()
        conn.close()


        if not result:

            print(
                f"No parent found for student {student_id}"
            )

            return web.json_response(
                {
                    "success": False,
                    "message": "Parent not found"
                },
                status=404
            )


        parent_id = result[0]

        room = f"parent_{parent_id}"


        # ======================================
        # Notification Message
        # ======================================

        message = (
            f"{student_name} was marked "
            f"{status} in {course_name} "
            f"on {attendance_date}."
        )


        # ======================================
        # Send Socket.IO Notification
        # ======================================

        await sio.emit(
            "notification",
            {
                "title": "Attendance Update 🔔",
                "message": message
            },
            room=room
        )


        print(
            f"Attendance notification sent "
            f"to parent {parent_id}"
        )


        return web.json_response(
            {
                "success": True,
                "parent_id": parent_id
            }
        )


    except Exception as e:

        print(
            "Attendance notification error:",
            e
        )

        return web.json_response(
            {
                "success": False,
                "message": str(e)
            },
            status=500
        )


# ==========================================
# HTTP Route
# ==========================================

app.router.add_post(
    "/attendance-notification",
    attendance_notification
)


# ==========================================
# Run Server
# ==========================================

if __name__ == "__main__":

    print(
        "Socket.IO server running "
        "on http://localhost:5000"
    )

    web.run_app(
        app,
        host="0.0.0.0",
        port=5000
    )


















