import streamlit as st

import streamlit.components.v1 as components
from database.db import get_connection
from database.notification_db import save_fcm_token
from database.dashboard_db import (
    get_student_attendance,
    get_student_attendance_percentage
)
from database.assignment import get_student_notices,get_student_assignments
from database.parent_db import (
    get_child_attendance_summary,
    get_child_today_attendance,
    get_child_attendance_history
)
# ===========================
# Database Functions
# (Abhi sirf import kar rahe hain)
# ===========================
from database.student_db import get_student_timetable,get_today_attendance
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
            "Profile",
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


    elif menu == "Profile":

        parent_profile()


    elif menu == "Attendance":

        parent_attendance()




    elif menu == "Assignments":
        parent_assignments(st.session_state.user_id)




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

    st.title(
        f"Welcome, {father_name or 'Parent'}"
    )

    st.caption(
        "Parent Portal • Student Academic Dashboard"
    )

    st.divider()


    # ==========================================================
    # QUICK ACCESS
    # ==========================================================

    st.subheader(
        "Quick Access"
    )


    q1, q2, q3, q4 = st.columns(4)


    # ----------------------------------------------------------
    # ATTENDANCE
    # ----------------------------------------------------------

    with q1:

        with st.container(border=True):

            st.markdown(
                "### 📊 Attendance"
            )

            st.caption(
                "View student attendance"
            )


    # ----------------------------------------------------------
    # RESULTS
    # ----------------------------------------------------------

    with q2:

        with st.container(border=True):

            st.markdown(
                "### 📈 Results"
            )

            st.caption(
                "Check academic results"
            )


    # ----------------------------------------------------------
    # ASSIGNMENTS
    # ----------------------------------------------------------

    with q3:

        with st.container(border=True):

            st.markdown(
                "### 📝 Assignments"
            )

            st.caption(
                "View academic work"
            )


    # ----------------------------------------------------------
    # NOTICES
    # ----------------------------------------------------------

    with q4:

        with st.container(border=True):

            st.markdown(
                "### 🔔 Notices"
            )

            st.caption(
                "View latest notices"
            )


    # ==========================================================
    # RECENT ACADEMIC WORK
    # ==========================================================

    st.subheader(
        "Recent Academic Work"
    )


    try:

        academic_work = parent_assignments(
            student_id
        )

    except Exception:

        academic_work = []


    if academic_work:

        # Latest 5
        academic_work = academic_work[:5]


        for work in academic_work:

            title = (
                work.get(
                    "title",
                    "Untitled"
                )
                or "Untitled"
            )

            course = (
                work.get(
                    "course",
                    "N/A"
                )
                or "N/A"
            )

            work_type = (
                work.get(
                    "type",
                    "Assignment"
                )
                or "Assignment"
            )

            due_date = (
                work.get(
                    "due_date",
                    "Not specified"
                )
                or "Not specified"
            )


            # --------------------------------------------------
            # SINGLE LINE CARD
            # --------------------------------------------------

            with st.container(
                border=True
            ):

                col1, col2, col3, col4 = st.columns(
                    [3, 2, 2, 1.5]
                )


                with col1:

                    st.write(
                        f"**{title}**"
                    )


                with col2:

                    st.caption(
                        f"Course: {course}"
                    )


                with col3:

                    st.caption(
                        f"Type: {work_type}"
                    )


                with col4:

                    st.caption(
                        f"Due: {due_date}"
                    )


    else:

        st.info(
            "No academic work has been published for this student yet."
        )


    # ==========================================================
    # LATEST NOTICES
    # ==========================================================

    st.subheader(
        "Latest Notices"
    )


    try:

        student_notices = get_student_notices(
            student_id
        )

    except Exception:

        student_notices = []


    if student_notices:

        # Latest 5
        student_notices = student_notices[:5]


        for notice in student_notices:

            title = (
                notice.get(
                    "title",
                    "Notice"
                )
                or "Notice"
            )

            notice_type = (
                notice.get(
                    "notice_type",
                    "General Notice"
                )
                or "General Notice"
            )

            course = (
                notice.get(
                    "course",
                    "General"
                )
                or "General"
            )

            expiry_date = (
                notice.get(
                    "expiry_date",
                    "Not specified"
                )
                or "Not specified"
            )


            # --------------------------------------------------
            # SINGLE LINE NOTICE
            # --------------------------------------------------

            with st.container(
                border=True
            ):

                col1, col2, col3, col4 = st.columns(
                    [3, 2, 2, 1.5]
                )


                with col1:

                    st.write(
                        f"**🔔 {title}**"
                    )


                with col2:

                    st.caption(
                        f"Type: {notice_type}"
                    )


                with col3:

                    st.caption(
                        f"Course: {course}"
                    )


                with col4:

                    st.caption(
                        f"Expiry: {expiry_date}"
                    )


    else:

        st.info(
            "No notices have been published for this student yet."
        )









def parent_dashboard(parent_id):

    # ==========================================================
    # GET PARENT + STUDENT DATA
    # ==========================================================

    dashboard = get_parent_dashboard(parent_id)

    if not dashboard:
        st.error("Parent record not found.")
        return


    # ==========================================================
    # UNPACK DATA
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

    st.title(
        f"Welcome, {father_name or 'Parent'}"
    )

    st.caption(
        "Parent Portal • Student Academic Dashboard"
    )

    st.divider()


    # ==========================================================
    # TODAY'S ATTENDANCE
    # ==========================================================

    try:

        today_attendance = get_today_attendance(
            student_id
        )

    except Exception:

        today_attendance = []


    if today_attendance:

        st.subheader(
            "Today's Attendance"
        )


        # Number of attendance entries/classes today
        attendance_count = len(
            today_attendance
        )


        # ------------------------------------------------------
        # ATTENDANCE SUMMARY
        # ------------------------------------------------------

        with st.container(border=True):

            col1, col2 = st.columns(2)


            with col1:

                st.metric(
                    "Classes Today",
                    attendance_count
                )


            with col2:

                st.caption(
                    "Attendance recorded today"
                )


        # ------------------------------------------------------
        # TODAY'S ATTENDANCE DETAILS
        # ------------------------------------------------------

        for attendance in today_attendance:

            with st.container(
                border=True
            ):

                col1, col2, col3 = st.columns(
                    [3, 2, 2]
                )


                with col1:

                    st.write(
                        f"**{attendance.get('course', 'Course')}**"
                    )


                with col2:

                    st.caption(
                        f"Status: {attendance.get('status', 'N/A')}"
                    )


                with col3:

                    st.caption(
                        f"Time: {attendance.get('time', 'N/A')}"
                    )


    # ==========================================================
    # RECENT ACADEMIC WORK
    # ==========================================================

    try:

        academic_work = parent_assignments(
            student_id
        )

    except Exception:

        academic_work = []


    if academic_work:

        st.subheader(
            "Recent Academic Work"
        )


        academic_work = academic_work[:5]


        for work in academic_work:

            title = (
                work.get(
                    "title",
                    "Untitled"
                )
                or "Untitled"
            )

            course = (
                work.get(
                    "course",
                    "N/A"
                )
                or "N/A"
            )

            work_type = (
                work.get(
                    "type",
                    "Assignment"
                )
                or "Assignment"
            )

            due_date = (
                work.get(
                    "due_date",
                    "Not specified"
                )
                or "Not specified"
            )


            # --------------------------------------------------
            # ONE LINE
            # --------------------------------------------------

            with st.container(
                border=True
            ):

                col1, col2, col3, col4 = st.columns(
                    [3, 2, 2, 1.5]
                )


                with col1:

                    st.write(
                        f"**{title}**"
                    )


                with col2:

                    st.caption(
                        f"Course: {course}"
                    )


                with col3:

                    st.caption(
                        f"Type: {work_type}"
                    )


                with col4:

                    st.caption(
                        f"Due: {due_date}"
                    )


    # ==========================================================
    # LATEST NOTICES
    # ==========================================================

    try:

        student_notices = get_student_notices(
            student_id
        )

    except Exception:

        student_notices = []


    if student_notices:

        st.subheader(
            "Latest Notices"
        )


        student_notices = student_notices[:5]


        for notice in student_notices:

            title = (
                notice.get(
                    "title",
                    "Notice"
                )
                or "Notice"
            )

            notice_type = (
                notice.get(
                    "notice_type",
                    "General Notice"
                )
                or "General Notice"
            )

            course = (
                notice.get(
                    "course",
                    "General"
                )
                or "General"
            )

            expiry_date = (
                notice.get(
                    "expiry_date",
                    "Not specified"
                )
                or "Not specified"
            )


            # --------------------------------------------------
            # ONE LINE NOTICE
            # --------------------------------------------------

            with st.container(
                border=True
            ):

                col1, col2, col3, col4 = st.columns(
                    [3, 2, 2, 1.5]
                )


                with col1:

                    st.write(
                        f"**🔔 {title}**"
                    )


                with col2:

                    st.caption(
                        f"Type: {notice_type}"
                    )


                with col3:

                    st.caption(
                        f"Course: {course}"
                    )


                with col4:

                    st.caption(
                        f"Expiry: {expiry_date}"
                    )













def parent_dashboard(parent_id):

    # ==========================================================
    # GET PARENT + STUDENT DATA
    # ==========================================================

    dashboard = get_parent_dashboard(parent_id)

    if not dashboard:
        st.error("Parent record not found.")
        return


    # ==========================================================
    # UNPACK DATA
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

    st.title(
        f"Welcome, {father_name or 'Parent'}"
    )

    st.caption(
        "Parent Portal • Student Academic Dashboard"
    )

    st.divider()


    # ==========================================================
    # TODAY'S ATTENDANCE
    # ==========================================================

    st.subheader("Today's Attendance")
    today_attendance =  get_child_today_attendance(student_id)
    if today_attendance:
        for attendance in today_attendance:
            course_name = attendance[0]
            status = attendance[1]
            if status.lower() == "present":
                st.success(f" **{course_name}**  —   Present")
            elif status.lower() == "absent":
                st.error(f" **{course_name}**  —   Absent")
            else:
                st.info(f" **{course_name}**  —  {status}")

    else:
        today_class =  get_child_today_attendance(student_id)
        if today_class:
            st.info("Today's class is scheduled, but attendance has not been taken yet.")
        else:
             st.info("There is no class scheduled for you today.")
    






    # Abhi function baad me banayenge
    # Isliye temporary message dikha rahe hain


    # ==========================================================
    # RECENT ACADEMIC WORK
    # ==========================================================

    st.subheader(
        "Recent Academic Work"
    )
    #
    academic_work = get_student_assignments(
        student_id
    )

    if academic_work:


        for work in academic_work[:5]:
            title = work.get("title", "Untitled") or "Untitled"
            course = work.get("course", "N/A") or "N/A"
            work_type = work.get("type", "Assignment") or "Assignment"
            due_date = work.get("due_date")
            if due_date:
                due_text = str(due_date)
            else:
                due_text = "No due date"
            with st.container(border=True):
                col1, col2, col3 = st.columns([4, 2, 1.5])
                with col1:
                    st.write(f"📝 **{title}**")
                with col2: 
                    st.caption(f"📚 {course}")
                with col3:
                    st.caption(f"⏰ Due: {due_text}")
    else:
            st.info("No academic work available.")


    # ==========================================================
    # LATEST NOTICES
    # ==========================================================

    student_notices = get_student_notices(
        student_id
    )

    if student_notices:

        st.subheader(
            "Latest Notices"
        )

        for notice in student_notices[:5]:

            title = notice.get("title", "Notice")or "Notice"
            

            notice_type = (
                notice.get(
                    "notice_type",
                    "General Notice"
                )
                or "General Notice"
            )

            course = (
                notice.get(
                    "course",
                    "General"
                )
                or "General"
            )

            expiry_date = notice.get("expiry_date")

            if expiry_date:
                expiry_text = str(expiry_date)
            else:
                expiry_text = "No expiry"

            with st.container(border=True):

                col1, col2, col3 = st.columns(
                    [4, 2, 1.5]
                )

                with col1:
                    st.write(
                        f"** {title}**"
                    )

                with col2:
                    st.caption(
                        st.caption(f" {course}")
                    )

                
                with col3:
                    st.caption(
                        f" {expiry_text}"
                    )











                    





def parent_profile():

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
    # PAGE HEADER
    # ==========================================================

    st.title("My Profile")

    st.caption(
        "Parent profile and linked student information"
    )

    st.divider()


    # ==========================================================
    # PARENT PROFILE HEADER
    # ==========================================================

    with st.container(border=True):

        header_col1, header_col2 = st.columns(
            [1, 4]
        )


        # ------------------------------------------------------
        # DEFAULT PARENT AVATAR
        # ------------------------------------------------------

        with header_col1:

            st.image(
                "https://avatar.iran.liara.run/public",
                width=120
            )


        # ------------------------------------------------------
        # PARENT BASIC INFORMATION
        # ------------------------------------------------------

        with header_col2:

            st.subheader(
                father_name
                or mother_name
                or "Parent"
            )

            st.caption(
                "Parent / Guardian"
            )


            # Parent contact information

            info_col1, info_col2 = st.columns(2)


            with info_col1:

                st.caption("Mobile Number")

                st.write(
                    parent_phone
                    or "Not Available"
                )


            with info_col2:

                st.caption("Email Address")

                st.write(
                    parent_email
                    or "Not Available"
                )


            st.success(
                f"● {account_status or 'Active'}"
            )


    # ==========================================================
    # PARENT INFORMATION
    # ==========================================================

    st.subheader("Parent Information")


    parent_col1, parent_col2 = st.columns(2)


    # ----------------------------------------------------------
    # FATHER INFORMATION
    # ----------------------------------------------------------

    with parent_col1:

        with st.container(border=True):

            st.markdown("### Father Information")


            st.caption("Father Name")

            st.write(
                father_name
                or "Not Available"
            )


            st.caption("Occupation")

            st.write(
                occupation
                or "Not Available"
            )


            st.caption("Mobile Number")

            st.write(
                parent_phone
                or "Not Available"
            )


    # ----------------------------------------------------------
    # MOTHER INFORMATION
    # ----------------------------------------------------------

    with parent_col2:

        with st.container(border=True):

            st.markdown("### Mother Information")


            st.caption("Mother Name")

            st.write(
                mother_name
                or "Not Available"
            )


            st.caption("Parent Email")

            st.write(
                parent_email
                or "Not Available"
            )


            st.caption("Account Status")

            st.write(
                account_status
                or "Not Available"
            )


    # ==========================================================
    # PARENT ADDRESS
    # ==========================================================

    st.subheader("Contact Address")


    with st.container(border=True):

        st.caption("Parent Address")

        st.write(
            parent_address
            or "Address not available"
        )


    # ==========================================================
    # LINKED STUDENT INFORMATION
    # ==========================================================

    st.divider()

    st.subheader("Student Information")

    st.caption(
        "Academic and personal information of your linked student"
    )


    # ==========================================================
    # STUDENT PROFILE CARD
    # ==========================================================

    with st.container(border=True):

        student_col1, student_col2 = st.columns(
            [1, 3]
        )


        # ------------------------------------------------------
        # STUDENT PHOTO
        # ------------------------------------------------------

        with student_col1:

            if photo:

                st.image(
                    photo,
                    width=150
                )

            else:

                # Default avatar based on gender

                if (
                    gender
                    and str(gender).lower() == "female"
                ):

                    st.image(
                        "https://avatar.iran.liara.run/public/girl?username=student",
                        width=150
                    )

                else:

                    st.image(
                        "https://avatar.iran.liara.run/public/boy?username=student",
                        width=150
                    )


        # ------------------------------------------------------
        # STUDENT BASIC INFORMATION
        # ------------------------------------------------------

        with student_col2:

            st.subheader(
                student_name
                or "Student"
            )


            st.caption(
                f"{department or 'Department'}"
                f" • Semester {semester or 'N/A'}"
            )


            student_basic_col1, student_basic_col2 = st.columns(2)


            # --------------------------------------------------
            # LEFT
            # --------------------------------------------------

            with student_basic_col1:

                st.caption("Roll Number")

                st.write(
                    roll_no
                    or "Not Available"
                )


                st.caption("Enrollment Number")

                st.write(
                    enrollment
                    or "Not Available"
                )


                st.caption("Department")

                st.write(
                    department
                    or "Not Available"
                )


            # --------------------------------------------------
            # RIGHT
            # --------------------------------------------------

            with student_basic_col2:

                st.caption("Semester")

                st.write(
                    semester
                    or "Not Available"
                )


                st.caption("Gender")

                st.write(
                    gender
                    or "Not Available"
                )


                st.caption("Student Status")

                st.write(
                    student_status
                    or "Not Available"
                )


    # ==========================================================
    # STUDENT PERSONAL INFORMATION
    # ==========================================================

    st.subheader("Student Personal Information")


    student_personal_col1, student_personal_col2 = st.columns(2)


    with student_personal_col1:

        with st.container(border=True):

            st.caption("Date of Birth")

            st.write(
                dob
                or "Not Available"
            )


            st.caption("Blood Group")

            st.write(
                blood_group
                or "Not Available"
            )


    with student_personal_col2:

        with st.container(border=True):

            st.caption("Student ID")

            st.write(
                student_id
                or "Not Available"
            )


            st.caption("Account Status")

            st.write(
                account_status
                or "Not Available"
            )


    # ==========================================================
    # STUDENT CONTACT INFORMATION
    # ==========================================================

    st.subheader("Student Contact Information")


    student_contact_col1, student_contact_col2 = st.columns(2)


    with student_contact_col1:

        with st.container(border=True):

            st.caption("Email Address")

            st.write(
                student_email
                or "Not Available"
            )


    with student_contact_col2:

        with st.container(border=True):

            st.caption("Phone Number")

            st.write(
                student_phone
                or "Not Available"
            )


    # ==========================================================
    # STUDENT ADDRESS
    # ==========================================================

    st.subheader("Student Address")


    with st.container(border=True):

        student_address_parts = []


        if student_address:
            student_address_parts.append(
                str(student_address)
            )


        if city:
            student_address_parts.append(
                str(city)
            )


        if state:
            student_address_parts.append(
                str(state)
            )


        student_full_address = ", ".join(
            student_address_parts
        )


        if pincode:

            if student_full_address:

                student_full_address += (
                    f" - {pincode}"
                )

            else:

                student_full_address = str(
                    pincode
                )


        st.write(
            student_full_address
            or "Address not available"
        )


    # ==========================================================
    # ACCOUNT
    # ==========================================================

    st.subheader("Account")


    if st.button(
        "🔒 Change Password",
        use_container_width=True
    ):

        st.info(
            "Password change feature will be available soon."
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

















