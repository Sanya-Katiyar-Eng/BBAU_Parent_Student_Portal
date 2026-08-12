import streamlit as st
from database.dashboard_db import (
    get_student_attendance,
    get_student_attendance_percentage
)
from database.parent_db import (
    get_child_attendance_summary,
    get_child_today_attendance,
    get_child_attendance_history
)
# ===========================
# Database Functions
# (Abhi sirf import kar rahe hain)
# ===========================

from database.parent_db import (
    get_parent_dashboard,
    get_parent_profile,
    get_student_attendance,
    get_student_results,
    get_student_assignments,
    get_parent_notices,
    get_student_timetable
)

import pandas as pd
import streamlit as st


def attendance_view():

    st.divider()
    student_id = st.session_state.user_id

    attendance = get_student_attendance()


    if not attendance:
        st.info("No attendance available.")
        return

    total = len(attendance)

    present = sum(
        1
        for row in attendance
        if row[3] == "Present"
    )

    absent = total - present

    percentage = get_student_attendance_percentage(student_id)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Classes", total)
    c2.metric("Present", present)
    c3.metric("Absent", absent)
    c4.metric("Attendance", f"{percentage}%")

    st.divider()

    df = pd.DataFrame(
        attendance,
        columns=[
            "Date",
            "Course Code",
            "Course",
            "Status",
            "Teacher",
            "Remarks"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
def parent_home():

    # ==========================
    # Session State Initialize
    # ==========================
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "role" not in st.session_state:
        st.session_state.role = None

    if "parent_id" not in st.session_state:
        st.session_state.parent_id = None

    if "student_id" not in st.session_state:
        st.session_state.student_id = None

    # Login check
    if not st.session_state.logged_in or st.session_state.role != "parent":
        st.error("Please login first.")
        st.stop()

    student_id = st.session_state.get("student_id")
    parent_id = st.session_state.get("parent_id")

    if parent_id is None or student_id is None:
        st.error("Parent session not found. Please login again.")
        st.stop()

    st.sidebar.title("👨‍👩‍👧 Parent Portal")

    menu = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "👤 Student Profile",
            "📅 Attendance",
            "📊 Results",
            "📝 Assignments",
            "📢 Notices",
            "📖 Timetable",
            "🚪 Logout"
        ]
    )

    if menu == "🏠 Dashboard":
        parent_dashboard(parent_id)

    elif menu == "👤 Student Profile":
        parent_profile()

    elif menu == "📅 Attendance":
        parent_attendance()

    elif menu == "📊 Results":
        parent_results(student_id)

    elif menu == "📝 Assignments":
        parent_assignments(student_id)

    elif menu == "📢 Notices":
        parent_notices()

    elif menu == "📖 Timetable":
        parent_timetable(student_id)

    elif menu == "🚪 Logout":
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.parent_id = None
        st.session_state.student_id = None
        st.rerun()
def parent_dashboard(parent_id):

    st.title("🏠 Parent Dashboard")

    # Database se data fetch
    dashboard = get_parent_dashboard(parent_id)

    # Agar parent record nahi mila
    if not dashboard:
        st.error("Parent record not found.")
        return

    # Data unpack
    (
        student_id,
        student_name,
        enrollment,
        department,
        semester,
        roll_no,
        student_status,
        account_status,
        father_name,
        mother_name,
        phone,
        email
    ) = dashboard

    st.success(f"Welcome, {father_name}")

    st.divider()

    # Student Details
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Student Name", student_name)
        st.metric("Enrollment No", enrollment)
        st.metric("Roll No", roll_no)

    with col2:
        st.metric("Department", department)
        st.metric("Semester", semester)
        st.metric("Status", student_status)

    st.divider()

    # Parent Details
    st.subheader("👨‍👩‍👧 Parent Information")

    st.write(f"**Father Name:** {father_name}")
    st.write(f"**Mother Name:** {mother_name}")
    st.write(f"**Phone:** {phone}")
    st.write(f"**Email:** {email}")
def parent_profile():

    st.title("👨‍👩‍👧 Parent & Student Profile")
    st.write("Session User ID :", st.session_state.user_id)

    if "parent_id" in st.session_state:
        st.write("Parent ID :", st.session_state.parent_id)

    if "student_id" in st.session_state:
        st.write("Student ID :", st.session_state.student_id)

    profile = get_parent_profile()

    if not profile:
        st.error("Profile not found.")
        return

    (
        parent_id,
        student_id,
        father_name,
        mother_name,
        occupation,
        parent_phone,
        parent_email,
        parent_address,
        student_name,
        roll_no,
        enrollment,
        department,
        semester,
        gender,
        dob,
        blood_group,
        student_email,
        student_phone,
        student_address,
        city,
        state,
        pincode,
        photo,
        student_status,
        account_status
    ) = profile

    # ==========================
    # Student Information
    # ==========================

    st.subheader("🎓 Student Information")
    st.divider()

    col1, col2 = st.columns([1,3])

    with col1:

        if photo:
            st.image(photo, width=180)
        else:
            if gender and gender.lower() == "female":
                st.image(
            "https://avatar.iran.liara.run/public/girl?username=student",
            width=180
        )
            else:
                st.image(
            "https://avatar.iran.liara.run/public/boy?username=student",
            width=180
        )
    with col2:

        st.markdown(f"### {student_name}")

        c1, c2 = st.columns(2)

        with c1:
            st.write("**Enrollment No:**", enrollment)
            st.write("**Roll No:**", roll_no)
            st.write("**Department:**", department)
            st.write("**Semester:**", semester)
            st.write("**Gender:**", gender)
            st.write("**Blood Group:**", blood_group)

        with c2:
            st.write("**Date of Birth:**", dob)
            st.write("**Email:**", student_email)
            st.write("**Phone:**", student_phone)
            st.write("**Status:**", student_status)
            st.write("**Account:**", account_status)

    st.info(
        f"📍 {student_address}, {city}, {state} - {pincode}"
    )

    # ==========================
    # Parent Information
    # ==========================

    st.subheader("👨‍👩‍👧 Parent Information")
    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        st.write("**Father Name:**", father_name)
        st.write("**Mother Name:**", mother_name)
        st.write("**Occupation:**", occupation)

    with c2:

        st.write("**Mobile:**", parent_phone)
        st.write("**Email:**", parent_email)

    st.info(f"🏠 {parent_address}")














def parent_attendance():

    # Get child/student ID from session
    student_id = st.session_state.get("student_id")

    if not student_id:
        st.error("Student information not found.")
        return

    # =========================
    # Attendance Summary
    # =========================

    summary = get_child_attendance_summary(student_id)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Present", summary["present"])

    with c2:
        st.metric("Absent", summary["absent"])

    with c3:
        st.metric("Total", summary["total"])

    with c4:
        st.metric(
            "Attendance %",
            f"{summary['percentage']}%"
        )

    st.divider()

    # =========================
    # Today's Attendance
    # =========================

    st.subheader("Today's Attendance")

    today = get_child_today_attendance(student_id)

    if today:

        for row in today:

            if row[1] == "Present":
                st.success(
                    f"🟢 {row[0]} : Present"
                )
            else:
                st.error(
                    f"🔴 {row[0]} : Absent"
                )

    else:
        st.info(
            "Attendance not marked today."
        )

    st.divider()

    # =========================
    # Attendance History
    # =========================

    st.subheader("📋 Attendance History")

    history = get_child_attendance_history(student_id)

    if history:

        for attendance_date, course_name, status in history:

            formatted_date = attendance_date.strftime(
                "%d %b %Y"
            )
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{course_name}**")
                st.caption(f"📅 {formatted_date}")
            with col2:
                if status == "Present":
                    st.success("🟢 Present")
                else:
                    st.error("🔴 Absent")
            st.divider()
    else:
        st.info("No attendance history found.")











def parent_results():

    st.title(" Results")

    result = get_student_results()

    st.dataframe(result)

















def parent_assignments():

    st.title(" Assignments")

    assignments = get_student_assignments()

    st.dataframe(assignments)


















def parent_notices():

    st.title(" Notices")

    notices = get_parent_notices()

    st.dataframe(notices)
















def parent_timetable():

    st.title(" Timetable")

    timetable = get_student_timetable()

    st.dataframe(timetable)

# ===========================
# Parent Home
# ===========================

def parent_home():

    st.sidebar.title(" Parent Portal")

    menu = st.sidebar.radio(
        "Navigation",
        [
            " Dashboard",
            " Student Profile",
            " Attendance",
            " Results",
            " Assignments",
            " Notices",
            " Timetable",
            " Logout"
        ]
    )

    student_id = st.session_state.student_id
    parent_id = st.session_state.parent_id

    if menu == " Dashboard":
        parent_dashboard(parent_id)

    elif menu == " Student Profile":
        parent_profile()

    elif menu == " Attendance":
        parent_attendance()

    elif menu == " Results":
        parent_results()

    elif menu == " Assignments":
        parent_assignments()

    elif menu == " Notices":
        parent_notices()

    elif menu == " Timetable":
        parent_timetable()

    elif menu == " Logout":

        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.parent_id = None
        st.session_state.student_id = None

        st.rerun()