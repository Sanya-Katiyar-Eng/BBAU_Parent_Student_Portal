import streamlit as st
import streamlit.components.v1 as components
from database.db import get_connection
from database.notification_db import save_fcm_token
from database.dashboard_db import (
    get_student_attendance,
    get_student_attendance_percentage
)
from database.assignment import get_student_assignments,get_student_notices
from database.parent_db import (
    get_child_attendance_summary,
    get_child_today_attendance,
    get_child_attendance_history
)
# ===========================
# Database Functions
# (Abhi sirf import kar rahe hain)
# ===========================
from database.student_db import get_student_timetable
from database.parent_db import (
    get_parent_dashboard,
    get_parent_profile,
    get_student_attendance,
    get_student_results,


)

import pandas as pd



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

    


# ==========================================================
# PARENT HOME
# ==========================================================




def parent_home():

    # ==========================================================
    # SESSION INITIALIZATION
    # ==========================================================

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "role" not in st.session_state:
        st.session_state.role = None

    if "parent_id" not in st.session_state:
        st.session_state.parent_id = None

    if "student_id" not in st.session_state:
        st.session_state.student_id = None


    # ==========================================================
    # LOGIN CHECK
    # ==========================================================

    if not st.session_state.logged_in:
        st.error("Please login first.")
        st.stop()

    if st.session_state.role != "parent":
        st.error("You do not have permission to access this page.")
        st.stop()


    # ==========================================================
    # SESSION DATA
    # ==========================================================

    parent_id = st.session_state.get("parent_id")
    student_id = st.session_state.get("student_id")


    if parent_id is None or student_id is None:

        st.error("Parent session not found.")

        if st.button("Login Again"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.parent_id = None
            st.session_state.student_id = None
            st.rerun()

        st.stop()


    # ==========================================================
    # SIDEBAR
    # ==========================================================

    st.sidebar.title("BBAU")

    st.sidebar.caption(
        "Student & Parent Management"
    )

    st.sidebar.divider()


    menu = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Student Profile",
            "Attendance",
            "Assignments",
            "Timetable",
            "Logout"
        ],
        key="parent_navigation"
    )


    st.sidebar.divider()

    st.sidebar.caption(
        "BBAU Student Management System"
    )


    # ==========================================================
    # ROUTING
    # ==========================================================

    if menu == "Dashboard":

        parent_dashboard(parent_id)


    elif menu == "Student Profile":

        parent_profile()


    elif menu == "Attendance":

        parent_attendance()




    elif menu == "Assignments":

        parent_assignments(student_id)




    elif menu == "Timetable":
        from dashboard.student import student_timetable
        student_timetable()


    elif menu == "Logout":

        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.parent_id = None
        st.session_state.student_id = None

        st.rerun()






# ==========================================================
# PARENT DASHBOARD
# ==========================================================


               






def parent_dashboard(parent_id):

    # ==========================================================
    # PAGE STYLE
    # ==========================================================

    st.markdown("""
    <style>

    .dashboard-welcome {
        padding: 24px 28px;
        border-radius: 18px;
        margin-bottom: 24px;
        background: linear-gradient(
            135deg,
            rgba(67, 97, 238, 0.12),
            rgba(76, 201, 240, 0.10)
        );
        border: 1px solid rgba(67, 97, 238, 0.15);
        animation: fadeSlide 0.6s ease;
    }

    .welcome-title {
        font-size: 30px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .welcome-subtitle {
        font-size: 14px;
        opacity: 0.70;
    }

    .section-heading {
        font-size: 21px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 14px;
        animation: fadeSlide 0.7s ease;
    }

    .info-label {
        font-size: 11px;
        font-weight: 600;
        opacity: 0.60;
        letter-spacing: 0.7px;
        text-transform: uppercase;
    }

    .info-value {
        font-size: 19px;
        font-weight: 650;
        margin-top: 5px;
    }

    .quick-card {
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(128,128,128,0.18);
        transition: all 0.3s ease;
        min-height: 120px;
    }

    .quick-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.10);
    }

    .quick-title {
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .quick-text {
        font-size: 12px;
        opacity: 0.65;
    }

    .work-card {
        padding: 18px;
        border-radius: 15px;
        border: 1px solid rgba(128,128,128,0.18);
        margin-bottom: 12px;
        transition: all 0.3s ease;
    }

    .work-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    }

    .work-title {
        font-size: 17px;
        font-weight: 700;
    }

    .work-meta {
        font-size: 12px;
        opacity: 0.65;
        margin-top: 5px;
    }

    .notice-card {
        padding: 18px;
        border-radius: 15px;
        border: 1px solid rgba(128,128,128,0.18);
        margin-bottom: 12px;
        transition: all 0.3s ease;
    }

    .notice-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    }

    .notice-title {
        font-size: 17px;
        font-weight: 700;
    }

    .notice-meta {
        font-size: 12px;
        opacity: 0.65;
        margin-top: 5px;
    }

    @keyframes fadeSlide {

        from {
            opacity: 0;
            transform: translateY(12px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }

    }

    </style>
    """, unsafe_allow_html=True)


    # ==========================================================
    # GET PARENT + STUDENT DATA
    # ==========================================================

    dashboard = get_parent_dashboard(parent_id)


    if not dashboard:

        st.error(
            "Parent record not found."
        )

        return


    # ==========================================================
    # UNPACK DATABASE DATA
    # ==========================================================

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


    # ==========================================================
    # WELCOME
    # ==========================================================

    st.markdown(
        f"""
        <div class="dashboard-welcome">

            <div class="welcome-title">
                Welcome, {father_name}
            </div>

            <div class="welcome-subtitle">
                Parent Portal • Student Academic Dashboard
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ==========================================================
    # STUDENT OVERVIEW
    # ==========================================================

    st.markdown(
        '<div class="section-heading">Student Overview</div>',
        unsafe_allow_html=True
    )


    # ----------------------------------------------------------
    # ROW 1
    # ----------------------------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        with st.container(border=True):

            st.markdown(
                '<div class="info-label">Student Name</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="info-value">{student_name}</div>',
                unsafe_allow_html=True
            )


    with col2:

        with st.container(border=True):

            st.markdown(
                '<div class="info-label">Enrollment Number</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="info-value">{enrollment}</div>',
                unsafe_allow_html=True
            )


    with col3:

        with st.container(border=True):

            st.markdown(
                '<div class="info-label">Roll Number</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="info-value">{roll_no}</div>',
                unsafe_allow_html=True
            )


    # ----------------------------------------------------------
    # ROW 2
    # ----------------------------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        with st.container(border=True):

            st.markdown(
                '<div class="info-label">Department</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="info-value">{department}</div>',
                unsafe_allow_html=True
            )


    with col2:

        with st.container(border=True):

            st.markdown(
                '<div class="info-label">Semester</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="info-value">{semester}</div>',
                unsafe_allow_html=True
            )


    with col3:

        with st.container(border=True):

            st.markdown(
                '<div class="info-label">Student Status</div>',
                unsafe_allow_html=True
            )

            if str(student_status).lower() == "active":

                st.success(
                    "Active"
                )

            else:

                st.warning(
                    str(student_status)
                )


    # ==========================================================
    # PARENT INFORMATION
    # ==========================================================

    st.markdown(
        '<div class="section-heading">Parent Information</div>',
        unsafe_allow_html=True
    )


    parent_col1, parent_col2 = st.columns(2)


    with parent_col1:

        with st.container(border=True):

            st.subheader(
                "Father"
            )

            st.caption(
                "Father Name"
            )

            st.write(
                father_name
            )

            st.divider()

            st.caption(
                "Phone Number"
            )

            st.write(
                phone
            )


    with parent_col2:

        with st.container(border=True):

            st.subheader(
                "Mother"
            )

            st.caption(
                "Mother Name"
            )

            st.write(
                mother_name
            )

            st.divider()

            st.caption(
                "Email Address"
            )

            st.write(
                email
            )


    # ==========================================================
    # QUICK ACCESS
    # ==========================================================

    st.markdown(
        '<div class="section-heading">Quick Access</div>',
        unsafe_allow_html=True
    )


    q1, q2, q3, q4 = st.columns(4)


    with q1:

        with st.container(border=True):

            st.markdown(
                """
                <div class="quick-card">

                    <div class="quick-title">
                        Attendance
                    </div>

                    <div class="quick-text">
                        View student attendance
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    with q2:

        with st.container(border=True):

            st.markdown(
                """
                <div class="quick-card">

                    <div class="quick-title">
                        Results
                    </div>

                    <div class="quick-text">
                        Check academic results
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    with q3:

        with st.container(border=True):

            st.markdown(
                """
                <div class="quick-card">

                    <div class="quick-title">
                        Assignments
                    </div>

                    <div class="quick-text">
                        View academic work
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    with q4:

        with st.container(border=True):

            st.markdown(
                """
                <div class="quick-card">

                    <div class="quick-title">
                        Notices
                    </div>

                    <div class="quick-text">
                        View latest notices
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    # ==========================================================
    # RECENT ASSIGNMENTS / HOMEWORK / PROJECTS
    # ==========================================================

    st.markdown(
        '<div class="section-heading">Recent Academic Work</div>',
        unsafe_allow_html=True
    )


    try:

        academic_work = get_student_assignments(
            student_id
        )

    except Exception:

        academic_work = []


    if academic_work:

        # latest 5
        academic_work = academic_work[:5]


        for work in academic_work:

            with st.container(border=True):

                st.markdown(
                    f"""
                    <div class="work-card">

                        <div class="work-title">
                            {work.get("title", "Untitled")}
                        </div>

                        <div class="work-meta">
                            Course: {work.get("course", "N/A")}
                            &nbsp; • &nbsp;
                            Type: {work.get("type", "Assignment")}
                        </div>

                        <div style="margin-top:10px;">
                            {work.get("description", "No description provided.")}
                        </div>

                        <div class="work-meta">
                            Due Date:
                            {work.get("due_date", "Not specified")}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

    else:

        st.info(
            "No academic work has been published for this student yet."
        )


    # ==========================================================
    # RECENT NOTICES
    # ==========================================================

    st.markdown(
        '<div class="section-heading">Latest Notices</div>',
        unsafe_allow_html=True
    )


    try:

        student_notices = get_student_notices(
            student_id
        )

    except Exception:

        student_notices = []


    if student_notices:

        student_notices = student_notices[:5]


        for notice in student_notices:

            with st.container(border=True):

                st.markdown(
                    f"""
                    <div class="notice-card">

                        <div class="notice-title">
                            {notice.get("title", "Notice")}
                        </div>

                        <div class="notice-meta">
                            {notice.get("notice_type", "General Notice")}
                            &nbsp; • &nbsp;
                            {notice.get("course", "General")}
                        </div>

                        <div style="margin-top:10px;">
                            {notice.get("message", "No message available.")}
                        </div>

                        <div class="notice-meta">
                            Expiry:
                            {notice.get("expiry_date", "Not specified")}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

    else:

        st.info(
            "No notices have been published for this student yet."
        )          













def parent_profile():

    # ==========================================================
    # PAGE STYLE
    # ==========================================================

    st.markdown("""
    <style>

    .profile-header {
        padding: 24px 28px;
        border-radius: 18px;
        margin-bottom: 25px;
        background: linear-gradient(
            135deg,
            rgba(67, 97, 238, 0.12),
            rgba(76, 201, 240, 0.10)
        );
        border: 1px solid rgba(67, 97, 238, 0.15);
        animation: profileFade 0.6s ease;
    }

    .profile-title {
        font-size: 30px;
        font-weight: 750;
        margin-bottom: 5px;
    }

    .profile-subtitle {
        font-size: 14px;
        opacity: 0.65;
    }

    .section-title {
        font-size: 21px;
        font-weight: 700;
        margin-top: 24px;
        margin-bottom: 14px;
    }

    .student-name {
        font-size: 28px;
        font-weight: 750;
        margin-bottom: 12px;
    }

    .info-label {
        font-size: 11px;
        font-weight: 650;
        opacity: 0.58;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        margin-bottom: 3px;
    }

    .info-value {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 14px;
    }

    .profile-card {
        padding: 22px;
        border-radius: 17px;
        border: 1px solid rgba(128,128,128,0.18);
        transition: all 0.3s ease;
        animation: cardFade 0.7s ease;
    }

    .profile-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 28px rgba(0,0,0,0.09);
    }

    .address-card {
        padding: 16px 20px;
        border-radius: 14px;
        border: 1px solid rgba(128,128,128,0.15);
        margin-top: 15px;
        font-size: 14px;
        opacity: 0.85;
    }

    .status-active {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        background: rgba(40,167,69,0.12);
        color: #198754;
        font-size: 13px;
        font-weight: 650;
    }

    @keyframes profileFade {

        from {
            opacity: 0;
            transform: translateY(12px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }

    }

    @keyframes cardFade {

        from {
            opacity: 0;
            transform: translateY(8px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }

    }

    </style>
    """, unsafe_allow_html=True)


    # ==========================================================
    # GET PROFILE DATA
    # ==========================================================

    profile = get_parent_profile()


    if not profile:

        st.error(
            "Profile information could not be found."
        )

        return


    # ==========================================================
    # UNPACK DATABASE DATA
    # ==========================================================

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


    # ==========================================================
    # HEADER
    # ==========================================================

    st.markdown(
        """
        <div class="profile-header">

            <div class="profile-title">
                Parent & Student Profile
            </div>

            <div class="profile-subtitle">
                View student academic information and parent details
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ==========================================================
    # STUDENT INFORMATION
    # ==========================================================

    st.markdown(
        '<div class="section-title">Student Information</div>',
        unsafe_allow_html=True
    )


    # ==========================================================
    # STUDENT PROFILE CARD
    # ==========================================================

    with st.container(border=True):

        photo_col, info_col = st.columns(
            [1, 3]
        )


        # ------------------------------------------------------
        # PHOTO
        # ------------------------------------------------------

        with photo_col:

            if photo:

                st.image(
                    photo,
                    width=180
                )

            else:

                if (
                    gender
                    and str(gender).lower() == "female"
                ):

                    st.image(
                        "https://avatar.iran.liara.run/public/girl?username=student",
                        width=180
                    )

                else:

                    st.image(
                        "https://avatar.iran.liara.run/public/boy?username=student",
                        width=180
                    )


        # ------------------------------------------------------
        # STUDENT BASIC INFORMATION
        # ------------------------------------------------------

        with info_col:

            st.markdown(
                f"""
                <div class="student-name">
                    {student_name}
                </div>
                """,
                unsafe_allow_html=True
            )


            c1, c2 = st.columns(2)


            # --------------------------------------------------
            # COLUMN 1
            # --------------------------------------------------

            with c1:

                st.markdown(
                    f"""
                    <div class="info-label">
                        Enrollment Number
                    </div>

                    <div class="info-value">
                        {enrollment}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                st.markdown(
                    f"""
                    <div class="info-label">
                        Roll Number
                    </div>

                    <div class="info-value">
                        {roll_no}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                st.markdown(
                    f"""
                    <div class="info-label">
                        Department
                    </div>

                    <div class="info-value">
                        {department}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                st.markdown(
                    f"""
                    <div class="info-label">
                        Semester
                    </div>

                    <div class="info-value">
                        {semester}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # --------------------------------------------------
            # COLUMN 2
            # --------------------------------------------------

            with c2:

                st.markdown(
                    f"""
                    <div class="info-label">
                        Gender
                    </div>

                    <div class="info-value">
                        {gender}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                st.markdown(
                    f"""
                    <div class="info-label">
                        Date of Birth
                    </div>

                    <div class="info-value">
                        {dob}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                st.markdown(
                    f"""
                    <div class="info-label">
                        Blood Group
                    </div>

                    <div class="info-value">
                        {blood_group}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                st.markdown(
                    f"""
                    <div class="info-label">
                        Student Status
                    </div>

                    <div class="info-value">
                        {student_status}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


    # ==========================================================
    # STUDENT CONTACT
    # ==========================================================

    st.markdown(
        '<div class="section-title">Student Contact Information</div>',
        unsafe_allow_html=True
    )


    contact_col1, contact_col2 = st.columns(2)


    with contact_col1:

        with st.container(border=True):

            st.markdown(
                f"""
                <div class="info-label">
                    Email Address
                </div>

                <div class="info-value">
                    {student_email}
                </div>
                """,
                unsafe_allow_html=True
            )


    with contact_col2:

        with st.container(border=True):

            st.markdown(
                f"""
                <div class="info-label">
                    Phone Number
                </div>

                <div class="info-value">
                    {student_phone}
                </div>
                """,
                unsafe_allow_html=True
            )


    # ==========================================================
    # STUDENT ADDRESS
    # ==========================================================

    student_full_address = (
        f"{student_address}, "
        f"{city}, "
        f"{state} - "
        f"{pincode}"
    )


    st.markdown(
        f"""
        <div class="address-card">
            Student Address<br>
            <strong>{student_full_address}</strong>
        </div>
        """,
        unsafe_allow_html=True
    )


    # ==========================================================
    # PARENT INFORMATION
    # ==========================================================

    st.markdown(
        '<div class="section-title">Parent Information</div>',
        unsafe_allow_html=True
    )


    parent_col1, parent_col2 = st.columns(2)


    # ==========================================================
    # FATHER / MOTHER
    # ==========================================================

    with parent_col1:

        with st.container(border=True):

            st.subheader(
                "Father Information"
            )

            st.markdown(
                f"""
                <div class="info-label">
                    Father Name
                </div>

                <div class="info-value">
                    {father_name}
                </div>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                f"""
                <div class="info-label">
                    Occupation
                </div>

                <div class="info-value">
                    {occupation}
                </div>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                f"""
                <div class="info-label">
                    Mobile Number
                </div>

                <div class="info-value">
                    {parent_phone}
                </div>
                """,
                unsafe_allow_html=True
            )


    # ==========================================================
    # MOTHER / EMAIL
    # ==========================================================

    with parent_col2:

        with st.container(border=True):

            st.subheader(
                "Mother Information"
            )

            st.markdown(
                f"""
                <div class="info-label">
                    Mother Name
                </div>

                <div class="info-value">
                    {mother_name}
                </div>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                f"""
                <div class="info-label">
                    Parent Email
                </div>

                <div class="info-value">
                    {parent_email}
                </div>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                f"""
                <div class="info-label">
                    Account Status
                </div>

                <div class="info-value">
                    {account_status}
                </div>
                """,
                unsafe_allow_html=True
            )


    # ==========================================================
    # PARENT ADDRESS
    # ==========================================================

    st.markdown(
        f"""
        <div class="address-card">
            Parent Address<br>
            <strong>{parent_address}</strong>
        </div>
        """,
        unsafe_allow_html=True
    )














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














import time
from datetime import datetime, date
import streamlit as st

def parent_assignments(student_id):

    # =========================================================
    # CUSTOM CSS: SINGLE CLEAN DASHBOARD VIEW (NO DUPLICATION / NO EMOJIS)
    # =========================================================
    st.markdown("""
        <style>
        /* Smooth Slide-up Entrance Animation */
        @keyframes singleViewFade {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .single-assign-container {
            animation: singleViewFade 0.35s ease-out;
        }

        /* Top Overview Strip */
        .summary-strip {
            background: #1e293b;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 8px;
            padding: 14px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .summary-label {
            color: #94a3b8;
            font-size: 0.82rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .summary-count {
            color: #38bdf8;
            font-size: 1.5rem;
            font-weight: 700;
        }

        /* Single Modern Card */
        .work-card {
            background: #1e293b;
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-left: 3px solid #3b82f6;
            border-radius: 8px;
            padding: 16px 20px;
            margin-bottom: 12px;
            transition: all 0.25s ease-in-out;
        }

        .work-card:hover {
            transform: translateY(-2px);
            border-left-color: #38bdf8;
            border-color: rgba(56, 189, 248, 0.3);
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35);
        }

        .tag-pill {
            background: rgba(59, 130, 246, 0.15);
            color: #60a5fa;
            border: 1px solid rgba(59, 130, 246, 0.3);
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            display: inline-block;
        }

        .due-pill {
            background: rgba(245, 158, 11, 0.12);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.25);
            padding: 3px 10px;
            border-radius: 5px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
        }

        .work-title-text {
            color: #f8fafc;
            font-size: 1.05rem;
            font-weight: 700;
            margin-top: 4px;
        }

        .work-sub-text {
            color: #cbd5e1;
            font-size: 0.88rem;
            margin-top: 2px;
        }

        .work-desc-box {
            color: #94a3b8;
            font-size: 0.85rem;
            margin-top: 10px;
            padding-top: 8px;
            border-top: 1px dashed rgba(255, 255, 255, 0.08);
        }
        </style>
    """, unsafe_allow_html=True)

    # =========================================================
    # LOAD DATA
    # =========================================================
    with st.spinner("Loading academic work..."):
        time.sleep(0.1)
        try:
            assignments = get_student_assignments(student_id)
        except Exception as e:
            st.error("Unable to load assignments.")
            st.exception(e)
            return

    # Header
    st.title("Academic Work")
    st.caption("Assignments, homework and projects assigned to the student")
    st.divider()

    # Empty Check
    if not assignments:
        st.info("No assignments, homework or projects have been assigned yet.")
        return

    # =========================================================
    # SINGLE SUMMARY STRIP (Replaces duplicate Overview section)
    # =========================================================
    total_assignments = len(assignments)

    summary_html = f"""<div class='summary-strip'>
<div>
<div class='summary-label'>Total Assigned Tasks</div>
<div style='color: #64748b; font-size: 0.8rem;'>Pending / Ongoing Work</div>
</div>
<div class='summary-count'>{total_assignments}</div>
</div>"""
    st.markdown(summary_html, unsafe_allow_html=True)

    # =========================================================
    # ASSIGNMENT DISPLAY (RENDER ONCE ONLY)
    # =========================================================
    st.markdown("<div class='single-assign-container'>", unsafe_allow_html=True)

    for assignment in assignments:
        assignment_id = assignment.get("Assignment ID", "N/A")
        title = assignment.get("Title", "Untitled Assignment")
        description = assignment.get("Description", "No instructions provided.")
        work_type = assignment.get("Type", "Assignment")
        course = assignment.get("Course", "Unknown Course")
        teacher = assignment.get("Teacher", "Teacher")
        due_date = assignment.get("Due Date")
        file_path = assignment.get("File")

        # Format Date
        if due_date:
            if isinstance(due_date, (datetime, date)):
                due_display = due_date.strftime("%d %b %Y")
            else:
                due_display = str(due_date)
        else:
            due_display = "No Deadline"

        # Card Output
        card_html = f"""<div class='work-card'>
<div style='display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;'>
<div>
<span class='tag-pill'>{work_type}</span>
<div class='work-title-text'>{title}</div>
<div class='work-sub-text'>Course: <b>{course}</b></div>
</div>
<div style='text-align: right;'>
<div class='due-pill'>Due: {due_display}</div>
<div style='color: #64748b; font-size: 0.8rem; margin-top: 4px;'>Teacher: {teacher}</div>
</div>
</div>
<div class='work-desc-box'>{description}</div>
</div>"""

        st.markdown(card_html, unsafe_allow_html=True)

        # Attachment Check
        if file_path:
            if str(file_path).startswith("http://") or str(file_path).startswith("https://"):
                st.link_button("View Attached Reference", file_path, use_container_width=False)
            else:
                st.caption(f"Attachment: {file_path}")

        st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)











    # =========================================================
    # HELPER FUNCTIONS
    # =========================================================

    def get_value(data, key, default=""):

        try:
            value = data.get(key, default)

            if value is None:
                return default

            return value

        except Exception:
            return default

    def format_date(value):

        if not value:
            return "No deadline"

        try:

            if isinstance(value, (datetime, date)):
                return value.strftime("%d %B %Y")

            value = str(value)

            try:
                return datetime.strptime(
                    value[:10],
                    "%Y-%m-%d"
                ).strftime("%d %B %Y")

            except:
                return value

        except:
            return str(value)

    def is_completed(assignment):

        status = str(
            get_value(
                assignment,
                "Status",
                ""
            )
        ).lower().strip()

        return status in [
            "completed",
            "complete",
            "submitted",
            "done"
        ]

    # =========================================================
    # CALCULATE SUMMARY
    # =========================================================

    total_work = len(assignments)

    completed_work = sum(
        1
        for assignment in assignments
        if is_completed(assignment)
    )

    pending_work = total_work - completed_work

    # =========================================================
    # SUMMARY
    # =========================================================

    st.subheader("Overview")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📚 Total Work",
            total_work
        )

    with col2:

        st.metric(
            "⏳ Pending",
            pending_work
        )

    with col3:

        st.metric(
            "✅ Completed",
            completed_work
        )

    st.divider()

    # =========================================================
    # FILTER
    # =========================================================

    st.subheader("Academic Work")

    filter_option = st.selectbox(
        "Filter assignments",
        [
            "All",
            "Pending",
            "Completed"
        ],
        key="parent_assignment_filter"
    )

    # =========================================================
    # FILTER DATA
    # =========================================================

    filtered_assignments = []

    for assignment in assignments:

        completed = is_completed(assignment)

        if filter_option == "Pending" and completed:
            continue

        if filter_option == "Completed" and not completed:
            continue

        filtered_assignments.append(assignment)

    # =========================================================
    # NO FILTER RESULT
    # =========================================================

    if not filtered_assignments:

        st.info(
            f"No {filter_option.lower()} academic work found."
        )

        return

    # =========================================================
    # ASSIGNMENT CARDS
    # =========================================================

    for index, assignment in enumerate(
        filtered_assignments,
        start=1
    ):

        assignment_id = get_value(
            assignment,
            "Assignment ID",
            index
        )

        work_type = get_value(
            assignment,
            "Type",
            "Assignment"
        )

        title = get_value(
            assignment,
            "Title",
            "Untitled Assignment"
        )

        description = get_value(
            assignment,
            "Description",
            "No instructions provided."
        )

        course = get_value(
            assignment,
            "Course",
            "Not specified"
        )

        teacher = get_value(
            assignment,
            "Teacher",
            "Not specified"
        )

        due_date = get_value(
            assignment,
            "Due Date",
            ""
        )

        file_name = get_value(
            assignment,
            "File",
            ""
        )

        status = get_value(
            assignment,
            "Status",
            ""
        )

        completed = is_completed(assignment)

        # =====================================================
        # EXPANDER = NATIVE STREAMLIT CARD-LIKE UI
        # =====================================================

        status_icon = "✅" if completed else "⏳"

        with st.expander(
            f"{status_icon}  {title}",
            expanded=False
        ):

            # -------------------------------------------------
            # TOP INFORMATION
            # -------------------------------------------------

            col1, col2 = st.columns(2)

            with col1:

                st.write("**Type**")
                st.write(work_type)

                st.write("**Course**")
                st.write(course)

                st.write("**Assigned By**")
                st.write(teacher)

            with col2:

                st.write("**Status**")

                if completed:
                    st.success(
                        "Completed"
                    )
                else:
                    st.warning(
                        "Pending"
                    )

                st.write("**Submission Deadline**")

                if due_date:
                    st.write(
                        f"📅 {format_date(due_date)}"
                    )
                else:
                    st.write(
                        "No deadline"
                    )

            st.divider()

            # -------------------------------------------------
            # DESCRIPTION
            # -------------------------------------------------

            st.write("### 📝 Instructions")

            if description:

                st.write(
                    description
                )

            else:

                st.caption(
                    "No instructions provided."
                )

            st.divider()

            # -------------------------------------------------
            # ATTACHMENT
            # -------------------------------------------------

            st.write("### 📎 Attachment")

            if file_name:

                st.write(
                    f"**File:** `{file_name}`"
                )

                file_path = str(file_name)

                # ---------------------------------------------
                # URL
                # ---------------------------------------------

                if (
                    file_path.startswith("http://")
                    or
                    file_path.startswith("https://")
                ):

                    st.link_button(
                        "🔗 Open Attachment",
                        file_path,
                        use_container_width=True
                    )

                # ---------------------------------------------
                # LOCAL FILE
                # ---------------------------------------------

                else:

                    import os

                    if os.path.exists(file_path):

                        try:

                            with open(
                                file_path,
                                "rb"
                            ) as file:

                                file_data = file.read()

                            st.download_button(
                                "⬇️ Download Attachment",
                                data=file_data,
                                file_name=os.path.basename(
                                    file_path
                                ),
                                key=(
                                    f"download_"
                                    f"{assignment_id}_"
                                    f"{index}"
                                ),
                                use_container_width=True
                            )

                        except Exception as e:

                            st.error(
                                "Unable to open attachment."
                            )

                    else:

                        st.warning(
                            "Attachment is recorded but "
                            "the file is not available."
                        )

            else:

                st.caption(
                    "No attachment was provided."
                )

            st.divider()

            # -------------------------------------------------
            # ASSIGNMENT ID
            # -------------------------------------------------

            st.caption(
                f"Assignment ID: {assignment_id}"
            )

    # =========================================================
    # FOOTER INFORMATION
    # =========================================================

    st.divider()

    st.caption(
        f"Showing {len(filtered_assignments)} "
        f"of {total_work} academic work items."
    )














def parent_notices():

    # ==========================================================
    # PROFESSIONAL NOTICE PAGE STYLE
    # ==========================================================

    st.markdown("""
    <style>

    .notice-header {
        padding: 10px 0 24px 0;
        animation: noticeFadeDown 0.7s ease-out;
    }

    .notice-title {
        font-size: 32px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 6px;
    }

    .notice-subtitle {
        font-size: 15px;
        opacity: 0.65;
    }

    .notice-card {
        padding: 22px 24px;
        border-radius: 16px;
        border: 1px solid rgba(128,128,128,0.18);
        margin-bottom: 16px;
        animation: noticeFadeUp 0.55s ease-out;
        transition: all 0.3s ease;
    }

    .notice-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.10);
        border-color: rgba(128,128,128,0.35);
    }

    .notice-type {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        opacity: 0.55;
        margin-bottom: 8px;
    }

    .notice-heading {
        font-size: 21px;
        font-weight: 650;
        margin-bottom: 10px;
    }

    .notice-description {
        font-size: 14px;
        line-height: 1.7;
        opacity: 0.72;
        margin-bottom: 16px;
    }

    .notice-meta {
        font-size: 13px;
        opacity: 0.62;
        margin-top: 6px;
    }

    .notice-expiry {
        padding: 12px 16px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.18);
        text-align: center;
        transition: all 0.25s ease;
    }

    .notice-expiry:hover {
        transform: scale(1.03);
    }

    .expiry-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.55;
    }

    .expiry-value {
        font-size: 14px;
        font-weight: 600;
        margin-top: 5px;
    }

    @keyframes noticeFadeDown {

        from {
            opacity: 0;
            transform: translateY(-15px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }

    }

    @keyframes noticeFadeUp {

        from {
            opacity: 0;
            transform: translateY(18px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }

    }

    </style>
    """, unsafe_allow_html=True)


    # ==========================================================
    # SESSION CHECK
    # ==========================================================

    student_id = st.session_state.get(
        "student_id"
    )


    if student_id is None:

        st.error(
            "Student information not available. Please login again."
        )

        st.stop()


    # ==========================================================
    # HEADER
    # ==========================================================

    st.markdown("""
    <div class="notice-header">

        <div class="notice-title">
            Notices
        </div>

        <div class="notice-subtitle">
            Important announcements and academic updates
        </div>

    </div>
    """, unsafe_allow_html=True)


    # ==========================================================
    # FETCH NOTICES
    # ==========================================================

    notices = get_student_notices(
        student_id
    )


    # ==========================================================
    # EMPTY STATE
    # ==========================================================

    if not notices:

        st.info(
            "No new notices are available at the moment."
        )

        return


    # ==========================================================
    # SUMMARY
    # ==========================================================

    total_notices = len(notices)


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Available Notices",
            total_notices
        )


    with col2:

        st.metric(
            "Latest Update",
            "Available"
        )


    st.write("")


    # ==========================================================
    # NOTICE LIST
    # ==========================================================

    for notice in notices:

        notice_id = notice["Notice ID"]

        title = notice["Title"]

        description = (
            notice["Description"]
            if notice["Description"]
            else "No additional information provided."
        )

        notice_type = (
            notice["Type"]
            if notice["Type"]
            else "General Notice"
        )

        course = (
            notice["Course"]
            if notice["Course"]
            else "General"
        )

        expiry_date = notice["Expiry Date"]

        created_at = notice["Created At"]

        file_path = notice["File"]


        # ======================================================
        # NOTICE CARD
        # ======================================================

        st.markdown(
            f"""
            <div class="notice-card">

                <div class="notice-type">
                    {notice_type}
                </div>

                <div class="notice-heading">
                    {title}
                </div>

                <div class="notice-description">
                    {description}
                </div>

                <div class="notice-meta">
                    Course: <b>{course}</b>
                </div>

                <div class="notice-meta">
                    Published: <b>{created_at}</b>
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # ======================================================
        # EXPIRY + ATTACHMENT
        # ======================================================

        col1, col2 = st.columns(
            [2, 1]
        )


        with col1:

            expiry_text = (
                str(expiry_date)
                if expiry_date
                else "No expiry date"
            )

            st.markdown(
                f"""
                <div class="notice-expiry">

                    <div class="expiry-label">
                        Notice Valid Until
                    </div>

                    <div class="expiry-value">
                        {expiry_text}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        with col2:

            if file_path:

                st.write("")

                st.button(
                    "View Attachment",
                    key=f"notice_file_{notice_id}",
                    use_container_width=True
                )


        st.write("")

















