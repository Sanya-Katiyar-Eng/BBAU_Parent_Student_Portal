import streamlit as st
from database.student_db import *
from database.student_db import (
    get_student_attendance_summary,
    get_today_attendance,
    get_student_attendance_history
)
from dashboard.parent_dash import parent_assignments
from database.assignment import get_student_assignments,get_student_notices
from dashboard.parent_dash import parent_attendance
from auth.login import normalize_text
import pandas as pd
from database.dashboard_db import (
    get_student_attendance,
    get_student_attendance_percentage
)
from database.student_db import save_student_profile
from database.student_db import (
    add_student,
    get_all_students,
    get_student_dashboard_counts,
    delete_student,
       get_student_by_enrollment,
)
from database.parent_db import create_parent_from_student
import pandas as pd





























def student_page():
    # =====================================================
    # PROFESSIONAL LIGHT BLUE CSS
    # =====================================================
    st.markdown("""
<style>
/* Smooth Entrance Animation */
.simple-container {
    animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Navigation Action Buttons */
div[data-testid="column"] div.stButton > button {
    border-radius: 10px !important;
    background-color: #f0f9ff !important;
    color: #0284c7 !important;
    border: 1px solid #bae6fd !important;
    font-weight: 600 !important;
    padding: 10px 16px !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 2px 4px rgba(2, 132, 199, 0.04) !important;
}

div[data-testid="column"] div.stButton > button:hover {
    background-color: #e0f2fe !important;
    border-color: #38bdf8 !important;
    color: #0369a1 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 10px rgba(2, 132, 199, 0.12) !important;
}

/* Metric Card Accent & Styling */
[data-testid="stMetric"] {
    background-color: #ffffff !important;
    border: 1px solid #e0f2fe !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(15, 23, 42, 0.06) !important;
}

[data-testid="stMetricValue"] {
    color: #0284c7 !important;
    font-weight: 700 !important;
    font-size: 26px !important;
}

[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}

/* Form Submit Button */
div.stForm button[type="submit"] {
    background-color: #0284c7 !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    transition: background-color 0.2s ease, transform 0.1s ease !important;
}

div.stForm button[type="submit"]:hover {
    background-color: #0369a1 !important;
    transform: translateY(-1px);
}

/* Clean Input Fields */
input[type="text"] {
    border-radius: 8px !important;
}

/* Table Card Styling */
div[data-testid="stDataFrame"] {
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
</style>
""", unsafe_allow_html=True)

    # =====================================================
    # SESSION STATES INITIALIZATION
    # =====================================================
    if "show_add_form" not in st.session_state:
        st.session_state.show_add_form = True
    if "show_view_students" not in st.session_state:
        st.session_state.show_view_students = False
    if "show_delete_student" not in st.session_state:
        st.session_state.show_delete_student = False
    if "delete_student_data" not in st.session_state:
        st.session_state.delete_student_data = None

    # Page Header
    st.title("Student Management")
    st.caption("Manage student records, directory, and profile setups")
    st.divider()

    # Navigation Buttons
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Add Student", use_container_width=True):
            st.session_state.show_add_form = True
            st.session_state.show_view_students = False
            st.session_state.show_delete_student = False

    with c2:
        if st.button("View Students", use_container_width=True):
            st.session_state.show_view_students = True
            st.session_state.show_add_form = False
            st.session_state.show_delete_student = False

    with c3:
        if st.button("Delete Student", use_container_width=True):
            st.session_state.show_delete_student = True
            st.session_state.show_add_form = False
            st.session_state.show_view_students = False

    st.markdown("<div class='simple-container'>", unsafe_allow_html=True)

    # =====================================================
    # SECTION 1: ADD NEW STUDENT
    # =====================================================
    if st.session_state.show_add_form:
        st.subheader("Add New Student Record")
        
        with st.form("add_student_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                enrollment_no = st.text_input("Enrollment Number", placeholder="e.g. BBAU/2026/1024")
            with col2:
                roll_no = st.text_input("Roll Number", placeholder="e.g. 2101052")

            col3, col4 = st.columns(2)
            with col3:
                department = st.selectbox(
                    "Department",
                    [
                        "Computer Science",
                        "Information Technology",
                        "Electronics",
                        "Mechanical",
                        "Civil",
                        "Electrical"
                    ]
                )
            with col4:
                semester = st.selectbox("Semester", [1, 2, 3, 4, 5, 6, 7, 8])

            submit = st.form_submit_button("Save Student Record", use_container_width=True)

        if submit:
            if not all([enrollment_no, roll_no]):
                st.error("Please fill all required fields before saving.")
            else:
                try:
                    success = add_student(
                        roll_no=roll_no,
                        enrollment_no=enrollment_no,
                        department=department,
                        semester=semester,
                    )
                    if success:
                        st.success("Student added successfully!")
                        st.info(f"**Enrollment No:** `{enrollment_no}`")
                    else:
                        st.error("Enrollment Number or Roll Number already exists.")
                except Exception as e:
                    st.error("An error occurred while saving.")
                    st.exception(e)

    # =====================================================
    # SECTION 2: VIEW & FILTER STUDENTS
    # =====================================================
    elif st.session_state.show_view_students:
        st.subheader("Registered Students Directory")

        try:
            total, completed, pending, active = get_student_dashboard_counts()
        except:
            total, completed, pending, active = 0, 0, 0, 0

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Students", total)
        m2.metric("Profile Completed", completed)
        m3.metric("Pending Profile", pending)
        m4.metric("Active Status", active)

        st.divider()

        search = st.text_input("Search Directory (Name, Enrollment, Roll No)")

        f1, f2, f3, f4 = st.columns(4)
        with f1:
            department = st.selectbox("Department", ["All", "Computer Science", "Information Technology", "Electronics", "Mechanical", "Civil", "Electrical"])
        with f2:
            semester = st.selectbox("Semester", ["All", 1, 2, 3, 4, 5, 6, 7, 8])
        with f3:
            registration = st.selectbox("Profile Status", ["All", "Pending", "Completed"])
        with f4:
            account = st.selectbox("Account Status", ["All", "Active", "Inactive", "Blocked"])

        students = get_all_students(search, department, semester, registration, account)

        if students:
            df = pd.DataFrame(
                students,
                columns=[
                    "ID",
                    "Enrollment No",
                    "Roll No",
                    "Student Name",
                    "Department",
                    "Semester",
                    "Profile Status",
                    "Account Status"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                height=380
            )
        else:
            st.info("No matching student records found.")

    # =====================================================
    # SECTION 3: DELETE STUDENT RECORD
    # =====================================================
    elif st.session_state.show_delete_student:
        st.subheader("Delete Student Record")

        col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
        with col1:
            enrollment = st.text_input("Enter Student Enrollment Number", placeholder="e.g. BBAU/2026/1024")
        with col2:
            if st.button("Search Record", use_container_width=True):
                if enrollment.strip():
                    st.session_state.delete_student_data = get_student_by_enrollment(enrollment.strip())
                else:
                    st.warning("Please enter an enrollment number.")

        student = st.session_state.delete_student_data

        if student:
            st.success("Student Record Found")
            
            st.write(f"**Enrollment No:** {student[1]}")
            st.write(f"**Roll Number:** {student[2]}")
            st.write(f"**Student Name:** {student[3] or 'N/A'}")
            st.write(f"**Department:** {student[4]}")
            st.write(f"**Semester:** {student[5]}")

            st.warning("Warning: Deleting this record is permanent.")
            confirm = st.checkbox("Confirm permanent deletion of this student record.")

            if confirm:
                if st.button("Permanently Delete", type="primary", use_container_width=True):
                    try:
                        if delete_student(student[1]):
                            st.success("Student deleted successfully!")
                            st.session_state.delete_student_data = None
                            st.rerun()
                        else:
                            st.error("Unable to delete record.")
                    except Exception as e:
                        st.error("Failed to delete record.")
                        st.exception(e)

        elif enrollment and not student:
            st.info("No active student record matches the entered enrollment number.")

    st.markdown("</div>", unsafe_allow_html=True)























from streamlit_option_menu import option_menu


def student_dashboard():
    # =====================================================
    # LIGHT THEME & SMOOTH ANIMATIONS
    # =====================================================
    st.markdown("""
        <style>
        /* Fade-in Animation for Page Content */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Subtle Floating Animation for Logo */
        @keyframes logoFloat {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-4px); }
            100% { transform: translateY(0px); }
        }

        /* Glowing Status Dot */
        @keyframes statusGlow {
            0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.4); }
            70% { box-shadow: 0 0 0 6px rgba(34, 197, 94, 0); }
            100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
        }

        /* Clean Light Sidebar Container */
        [data-testid="stSidebar"] {
            background-color: #f8fafc !important;
            border-right: 1px solid #e2e8f0 !important;
        }

        [data-testid="stSidebarContent"] {
            overflow-y: auto;
            height: 100vh;
            padding-top: 1rem;
        }

        /* Animated Logo Container */
        .sidebar-logo-container {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 8px;
            animation: logoFloat 3.5s ease-in-out infinite;
        }
        .sidebar-logo-container img {
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            border: 1px solid #e2e8f0;
        }

        /* Portal Title (Dark Text) */
        .portal-title {
            color: #0f172a;
            font-size: 1.25rem;
            font-weight: 700;
            text-align: center;
            margin-top: 8px;
            margin-bottom: 2px;
        }

        .portal-subtitle {
            color: #64748b;
            font-size: 0.82rem;
            text-align: center;
            margin-bottom: 12px;
        }

        /* Clean Divider */
        .custom-divider {
            height: 1px;
            background: #e2e8f0;
            margin: 14px 0;
            border: none;
        }

        /* Active Status Badge */
        .status-badge {
            background: #f0fdf4;
            border: 1px solid #bbf7d0;
            color: #16a34a;
            padding: 8px 12px;
            border-radius: 10px;
            font-size: 0.82rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
        }
        .status-dot {
            width: 8px;
            height: 8px;
            background-color: #22c55e;
            border-radius: 50%;
            animation: statusGlow 2s infinite;
        }

        /* Animated Hover Logout Button */
        div[data-testid="stSidebar"] div.stButton > button {
            border-radius: 10px !important;
            font-weight: 600 !important;
            transition: all 0.25s ease !important;
            background: #fef2f2 !important;
            color: #dc2626 !important;
            border: 1px solid #fecaca !important;
        }

        div[data-testid="stSidebar"] div.stButton > button:hover {
            background: #dc2626 !important;
            color: #ffffff !important;
            border-color: #dc2626 !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.25) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # =====================================================
    # SIDEBAR CONTENT
    # =====================================================
    with st.sidebar:

        # Header Logo
        st.markdown("""
            <div class='sidebar-logo-container'>
                <img src='images/bbau logo.jpg' width='90' alt='BBAU Logo'>
            </div>
            <div class='portal-title'>🎓 Student Portal</div>
            <div class='portal-subtitle'>Welcome back, Student</div>
            <div class='custom-divider'></div>
        """, unsafe_allow_html=True)

        # High-Contrast Light Option Menu
        selected = option_menu(
            menu_title=None,
            options=[
                "Dashboard",
                "My Profile",
                "My Courses",
                "Class Timetable",
                "Attendance",
                "Assignments",
            ],
            icons=[
                "grid-1x2",
                "person",
                "book",
                "calendar3",
                "check2-square",
                "bar-chart",
                "journal-text",
                "megaphone",
                "chat-dots",
                "folder2-open",
                "gear"
            ],
            default_index=0,
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "transparent",
                },
                "icon": {
                    "font-size": "15px",
                    "color": "#475569",
                },
                "nav-link": {
                    "font-size": "13.5px",
                    "font-weight": "500",
                    "text-align": "left",
                    "margin": "3px 0px",
                    "padding": "9px 12px",
                    "border-radius": "8px",
                    "color": "#1e293b",
                    "--hover-color": "#e2e8f0",
                    "transition": "all 0.25s ease",
                },
                "nav-link-selected": {
                    "background": "linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%)",
                    "color": "#ffffff",
                    "font-weight": "600",
                    "box-shadow": "0 4px 10px rgba(37, 99, 235, 0.25)",
                },
            },
        )

        st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

        # Active Status Indicator
        st.markdown("""
            <div class='status-badge'>
                <div class='status-dot'></div>
                <span>Account Active</span>
            </div>
        """, unsafe_allow_html=True)

        # Logout Button
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    # =====================================================
    # PAGE ROUTING CONTAINER
    # =====================================================
    st.markdown("<div style='animation: fadeIn 0.3s ease-out;'>", unsafe_allow_html=True)

    if selected == "Dashboard":
        dashboard_home()
    elif selected == "My Profile":
        student_profile(st.session_state.user_id)
    elif selected == "My Courses":
        student_courses(st.session_state.user_id)
    elif selected == "Class Timetable":
        student_timetable()
    elif selected == "Attendance":
        parent_attendance()
    elif selected == "Assignments":
        parent_assignments(st.session_state.user_id)


    st.markdown("</div>", unsafe_allow_html=True)













#================================================================
#student form
#=================================================================
def student_profile_form():

    st.title(" Complete Your Student Profile")
    st.info("Please complete your profile before accessing the dashboard.")

    with st.form("student_profile_form"):

        st.subheader("👤 Personal Information")

        student_name = st.text_input("Full Name")

        dob = st.date_input("Date of Birth")

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
        )

        blood_group = st.selectbox(
            "Blood Group",
            [
                "A+","A-","B+","B-",
                "AB+","AB-","O+","O-"
            ]
        )

        email = st.text_input("Email")

        phone = st.text_input("Mobile Number")

        st.subheader("📍 Address")

        address = st.text_area("Full Address")

        city = st.text_input("City")

        state = st.text_input("State")

        pincode = st.text_input("Pincode")

        st.subheader("Parent Information")

        father_name = st.text_input("Father Name")
        if not father_name:
            st.error("Father Name is required")
            return

        mother_name = st.text_input("Mother Name")
        if not mother_name:
            st.error("Mother Name is required")
            return

        parent_phone = st.text_input("Parent Mobile Number")
        if not parent_phone:
            st.error("parent phone num is required")
        if parent_phone == phone:
            st.error("Parent mobile number cannot be same as student's mobile number.")
            return

        parent_email = st.text_input("Parent Email")
        if not parent_email:
            st.error("parent email required")
        occupation = st.text_input("Parent Occupation")

        st.subheader(" Student Photo")

        photo = st.file_uploader(
            "Upload Passport Size Photo",
            type=["jpg", "jpeg", "png"]
        )

        submitted = st.form_submit_button(
            "Save Profile",
            use_container_width=True
        )

    if submitted:
        success = save_student_profile(

        st.session_state.user_id,

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

    )

        if success:
            create_parent_from_student(
        st.session_state.user_id
    )

            st.success("Profile Completed Successfully.")

            st.balloons()

            st.rerun()

    else:

        st.error("Unable to save profile.")




        









#==================================================================================================
#student dashboard home
#==========================================================================================================



import streamlit as st

def dashboard_home():

    student_id = st.session_state.get("user_id")

    # =====================================================
    # DATABASE DATA
    # =====================================================

    profile = get_student_profile(student_id) or {}
    summary = get_student_dashboard_summary(student_id) or {}
    today_classes = get_student_today_classes(student_id) or []
    notices = get_student_notices(student_id) or []

    student_name = profile.get("student_name", "Student")
    enrollment_no = profile.get("enrollment_no", "-")
    department = profile.get("department", "-")
    semester = profile.get("semester", "-")

    attendance = float(summary.get("attendance", 0) or 0)
    cgpa = float(summary.get("cgpa", 0) or 0)
    courses = int(summary.get("courses", 0) or 0)
    pending = int(summary.get("pending_assignments", 0) or 0)

    # =====================================================
    # LIGHT BLUE TITLE
    # =====================================================

    st.title("🎓 Student Dashboard")

    st.caption(
        f"Welcome back, {student_name}! "
        "Here's what's happening with your academic journey today."
    )

    # =====================================================
    # STUDENT INFORMATION
    # =====================================================

    with st.container(border=True):

        st.subheader(f"👋 Welcome, {student_name}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.info(
                f"🆔 Enrollment\n\n{enrollment_no}"
            )

        with col2:
            st.info(
                f"🏢 Department\n\n{department}"
            )

        with col3:
            st.info(
                f"📚 Semester\n\n{semester}"
            )

    st.write("")

    # =====================================================
    # NOTICES + TODAY CLASSES
    # =====================================================

    notice_col, class_col = st.columns(2)

    # -----------------------------------------------------
    # NOTICES
    # -----------------------------------------------------

    with notice_col:

        st.subheader("🔔 Notices")

        if notices:

            for notice in notices[:5]:

                title = notice.get(
                    "title",
                    "Notice"
                )

                description = notice.get(
                    "description",
                    ""
                )

                notice_date = notice.get(
                    "notice_date",
                    ""
                )

                with st.container(border=True):

                    st.write(f"**{title}**")

                    if notice_date:
                        st.caption(
                            f"📅 {notice_date}"
                        )

                    if description:
                        st.caption(
                            description
                        )

        else:

            st.info(
                "No new notices available."
            )

    # -----------------------------------------------------
    # TODAY'S CLASSES
    # -----------------------------------------------------

    with class_col:

        st.subheader("📅 Today's Classes")

        if today_classes:

            for cls in today_classes:

                course_name = cls.get(
                    "course_name",
                    "Course"
                )

                teacher_name = cls.get(
                    "teacher_name",
                    "Faculty"
                )

                start_time = cls.get(
                    "start_time",
                    ""
                )

                end_time = cls.get(
                    "end_time",
                    ""
                )

                with st.container(border=True):

                    st.write(
                        f"**{course_name}**"
                    )

                    if start_time:

                        if end_time:

                            st.caption(
                                f"🕐 {start_time} - {end_time}"
                            )

                        else:

                            st.caption(
                                f"🕐 {start_time}"
                            )

                    st.caption(
                        f"👨‍🏫 {teacher_name}"
                    )

        else:

            st.info(
                "No classes scheduled for today."
            )

    st.write("")

    # =====================================================
    # ACADEMIC OVERVIEW
    # =====================================================

    st.subheader("📊 Academic Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Attendance",
            f"{attendance:.0f}%"
        )

        st.progress(
            min(max(attendance / 100, 0), 1)
        )

    with c2:

        st.metric(
            "Current CGPA",
            f"{cgpa:.2f}"
        )

        st.progress(
            min(max(cgpa / 10, 0), 1)
        )

    with c3:

        st.metric(
            "Enrolled Courses",
            courses
        )

        st.progress(
            min(max(courses / 10, 0), 1)
        )

    with c4:

        st.metric(
            "Pending Assignments",
            pending
        )

        st.progress(
            min(max(pending / 5, 0), 1)
        )
















def student_timetable():

    student_id = st.session_state.get("user_id")

    st.title("📅 My Timetable")
    st.caption("Weekly lecture schedule and room assignments")

    # =====================================================
    # GET DATA
    # =====================================================

    try:
        timetable = get_student_timetable(student_id)
    except Exception as e:
        st.error(f"Unable to load timetable: {e}")
        return

    if not timetable:
        st.info("No timetable available.")
        return

    # =====================================================
    # DAY FILTER
    # =====================================================

    days = [
        "All",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday"
    ]

    selected_day = st.radio(
        "Select Day",
        days,
        horizontal=True
    )

    st.divider()

    # =====================================================
    # CONVERT TUPLES INTO DICTIONARIES
    # =====================================================

    timetable_data = []

    for row in timetable:

        # Expected:
        # day, start_time, end_time,
        # course_code, course_name,
        # teacher_name, room

        if len(row) >= 7:

            timetable_data.append({
                "day": row[0],
                "start_time": row[1],
                "end_time": row[2],
                "course_code": row[3],
                "course_name": row[4],
                "teacher_name": row[5],
                "room": row[6]
            })

    # =====================================================
    # FILTER
    # =====================================================

    if selected_day == "All":

        filtered_classes = timetable_data

    else:

        filtered_classes = [
            item
            for item in timetable_data
            if str(item["day"]).strip().lower()
            == selected_day.lower()
        ]

    # =====================================================
    # NO DATA
    # =====================================================

    if not filtered_classes:

        st.info(
            f"No classes scheduled for {selected_day}."
        )

        return

    # =====================================================
    # DISPLAY
    # =====================================================

    current_day = None

    for item in filtered_classes:

        day = item["day"]

        start_time = item["start_time"]
        end_time = item["end_time"]

        course_code = item["course_code"]
        course_name = item["course_name"]

        teacher_name = item["teacher_name"]
        room = item["room"]

        # -----------------------------------------------
        # DAY
        # -----------------------------------------------

        if day != current_day:

            st.subheader(
                f"🗓️ {day}"
            )

            current_day = day

        # -----------------------------------------------
        # CLASS
        # -----------------------------------------------

        with st.container(border=True):

            time_col, course_col, room_col = st.columns(
                [1.2, 2.8, 1.2]
            )

            # TIME
            with time_col:

                st.write(
                    f"🕐 **{start_time}**"
                )

                st.caption(
                    f"to {end_time}"
                )

            # COURSE
            with course_col:

                st.write(
                    f"**{course_name}**"
                )

                st.caption(
                    f"Course Code: {course_code}"
                )

                st.caption(
                    f"👨‍🏫 Teacher: {teacher_name}"
                )

            # ROOM
            with room_col:

                st.caption(
                    "🏫 Room"
                )

                st.write(
                    f"**{room or 'N/A'}**"
                )

        st.write("")

















from datetime import datetime, time



def student_timetable():
    # =====================================================
    # CUSTOM STYLING & ANIMATIONS (Matching Theme)
    # =====================================================
    st.markdown("""
        <style>
        /* Fade In Entry Animation */
        @keyframes cardFadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .timetable-container {
            animation: cardFadeIn 0.3s ease-out;
        }

        /* Glass Schedule Card */
        .schedule-card {
            background: #1e293b;
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-left: 4px solid #3b82f6;
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 14px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transition: all 0.25s ease;
        }

        .schedule-card:hover {
            border-color: rgba(59, 130, 246, 0.4);
            border-left-color: #60a5fa;
            transform: translateY(-2px);
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
        }

        /* Course Code Badge */
        .course-badge {
            background: rgba(59, 130, 246, 0.12);
            color: #60a5fa;
            border: 1px solid rgba(59, 130, 246, 0.25);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 700;
            display: inline-block;
            margin-bottom: 6px;
        }

        /* Time & Room Pill Badges */
        .time-pill {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 6px 12px;
            border-radius: 8px;
            color: #cbd5e1;
            font-size: 0.88rem;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .teacher-caption {
            color: #94a3b8;
            font-size: 0.82rem;
            margin-top: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Page Header
    st.title("📅 My Timetable")
    st.caption("Weekly class schedule and venue details")
    st.divider()

    # Session Verification (Exact Original Logic)
    student_id = st.session_state.get("student_id")
    if student_id is None:
        student_id = st.session_state.get("user_id")

    if student_id is None:
        st.error("Student session not found.")
        return

    # Database Retrieval (Exact Original Logic)
    schedules = get_student_timetable(student_id)

    if schedules:
        st.markdown("<div class='timetable-container'>", unsafe_allow_html=True)

        for row in schedules:
            (
                timetable_id,
                day_name,
                start_time,
                end_time,
                room_no,
                semester,
                course_code,
                course_name,
                department,
                teacher_name
            ) = row

            # Time Formatting
            formatted_start = start_time.strftime('%I:%M %p') if hasattr(start_time, 'strftime') else str(start_time)
            formatted_end = end_time.strftime('%I:%M %p') if hasattr(end_time, 'strftime') else str(end_time)

            # Animated Schedule Card Container
            with st.container():
                col1, col2, col3, col4 = st.columns([1.2, 3, 2.5, 2], vertical_alignment="center")

                with col1:
                    st.markdown(f"<h3 style='margin:0; color:#f8fafc;'>{day_name}</h3>", unsafe_allow_html=True)

                with col2:
                    st.markdown(f"<span class='course-badge'>{course_code}</span>", unsafe_allow_html=True)
                    st.markdown(f"<div style='font-weight: 600; color: #f1f5f9;'>{course_name}</div>", unsafe_allow_html=True)

                with col3:
                    st.markdown(
                        f"<div class='time-pill'>🕐 {formatted_start} &rarr; {formatted_end}</div>", 
                        unsafe_allow_html=True
                    )

                with col4:
                    st.markdown(f"🏫 **{room_no or 'Not Assigned'}**")
                    st.markdown(f"<div class='teacher-caption'>👤 {teacher_name or 'Not Assigned'}</div>", unsafe_allow_html=True)

                st.divider()

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.info("No classes scheduled.")


















def student_assignments(student_id):

    # =========================================================
    # CUSTOM CSS: TIMELINE LAYOUT & CARD ANIMATIONS (NO ICONS)
    # =========================================================
    st.markdown("""
        <style>
        /* Smooth Entrance Animation */
        @keyframes timelineSlideIn {
            from {
                opacity: 0;
                transform: translateY(12px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .assignment-wrapper {
            animation: timelineSlideIn 0.35s ease-out;
        }

        /* Overview Summary Bar */
        .summary-bar {
            background: #1e293b;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 8px;
            padding: 14px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }

        .summary-label {
            color: #94a3b8;
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .summary-value {
            color: #38bdf8;
            font-size: 1.4rem;
            font-weight: 700;
        }

        /* Timeline Card Item */
        .timeline-item {
            position: relative;
            background: #1e293b;
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-left: 3px solid #3b82f6;
            border-radius: 8px;
            padding: 16px 20px;
            margin-bottom: 16px;
            transition: all 0.25s ease-in-out;
        }

        .timeline-item:hover {
            transform: translateX(4px);
            border-left-color: #38bdf8;
            border-color: rgba(56, 189, 248, 0.3);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        }

        /* Type Badges */
        .badge-type {
            background: rgba(59, 130, 246, 0.15);
            color: #60a5fa;
            border: 1px solid rgba(59, 130, 246, 0.3);
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: inline-block;
        }

        /* Due Date Pill */
        .due-pill {
            background: rgba(245, 158, 11, 0.12);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.25);
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
        }

        /* Typography */
        .assignment-title {
            color: #f8fafc;
            font-size: 1.05rem;
            font-weight: 700;
            margin-top: 4px;
        }

        .assignment-course {
            color: #cbd5e1;
            font-size: 0.88rem;
            margin-top: 2px;
        }

        .meta-caption {
            color: #64748b;
            font-size: 0.8rem;
            margin-top: 6px;
        }
        </style>
    """, unsafe_allow_html=True)

    # =========================================================
    # LOAD ASSIGNMENTS
    # =========================================================

    with st.spinner("Loading academic work..."):
        time.sleep(0.1)
        try:
            assignments = get_assignments(student_id)
        except Exception as e:
            st.error("Unable to load assignments.")
            st.exception(e)
            return

    # Header
    st.title("Academic Work")
    st.caption("Assignments, homework, and projects assigned to you")
    st.divider()

    # Empty State
    if not assignments:
        st.info("No assignments, homework or projects have been assigned yet.")
        return

    # =========================================================
    # SUMMARY OVERVIEW
    # =========================================================

    total_assignments = len(assignments)

    summary_html = f"""<div class='summary-bar'>
<div>
<div class='summary-label'>Total Academic Work</div>
<div style='color: #64748b; font-size: 0.8rem;'>Assigned Tasks</div>
</div>
<div class='summary-value'>{total_assignments}</div>
</div>"""
    st.markdown(summary_html, unsafe_allow_html=True)

    # =========================================================
    # TIMELINE ASSIGNMENT LIST
    # =========================================================

    st.markdown("<div class='assignment-wrapper'>", unsafe_allow_html=True)

    for index, assignment in enumerate(assignments, start=1):

        assignment_id = assignment.get("Assignment ID", "N/A")
        title = assignment.get("Title", "Untitled Assignment")
        description = assignment.get("Description", "No instructions provided.")
        work_type = assignment.get("Type", "Assignment")
        course = assignment.get("Course", "Unknown Course")
        teacher = assignment.get("Teacher", "Teacher")
        due_date = assignment.get("Due Date")
        file_path = assignment.get("File")

        # Formatting Date
        if due_date:
            if isinstance(due_date, (datetime, date)):
                due_display = due_date.strftime("%d %b %Y")
            else:
                due_display = str(due_date)
        else:
            due_display = "No Deadline"

        # Timeline Card HTML (Indentation safe)
        card_html = f"""<div class='timeline-item'>
<div style='display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;'>
<div>
<span class='badge-type'>{work_type}</span>
<div class='assignment-title'>{title}</div>
<div class='assignment-course'>Course: <b>{course}</b></div>
</div>
<div style='text-align: right;'>
<div class='due-pill'>Due: {due_display}</div>
<div class='meta-caption'>Instructor: {teacher}</div>
</div>
</div>
</div>"""

        st.markdown(card_html, unsafe_allow_html=True)

        # Instructions & Attachment Drawer (Native Streamlit Expander)
        with st.expander(f"View Details ({title})", expanded=False):
            st.write("**Instructions:**")
            st.write(description if description else "No instructions provided.")

            if file_path:
                st.markdown("---")
                st.write(f"Attachment File: `{file_path}`")
                
                if str(file_path).startswith("http://") or str(file_path).startswith("https://"):
                    st.link_button(
                        "Open Attachment",
                        file_path,
                        use_container_width=True
                    )

            st.caption(f"Assignment ID: {assignment_id}")

        st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


















def student_courses(student_id):

    # =====================================================
    # CUSTOM STYLING & ANIMATIONS (NO EMOJIS / CLEAN DESIGN)
    # =====================================================
    st.markdown("""
        <style>
        /* Smooth Entry Animation */
        @keyframes courseFadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .courses-wrapper {
            animation: courseFadeIn 0.35s ease-out;
        }

        /* Metric Box Styling */
        .metric-card {
            background: #1e293b;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            padding: 16px 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            transition: all 0.25s ease-in-out;
        }

        .metric-card:hover {
            transform: translateY(-2px);
            border-color: rgba(56, 189, 248, 0.3);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
        }

        .metric-title {
            color: #94a3b8;
            font-size: 0.82rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .metric-value {
            color: #38bdf8;
            font-size: 1.8rem;
            font-weight: 700;
            margin-top: 4px;
        }

        /* Course Card Styling */
        .course-card {
            background: #1e293b;
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-left: 4px solid #3b82f6;
            border-radius: 10px;
            padding: 18px 22px;
            margin-bottom: 14px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            transition: all 0.25s ease-in-out;
        }

        .course-card:hover {
            transform: translateY(-2px);
            border-left-color: #38bdf8;
            border-color: rgba(56, 189, 248, 0.25);
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35);
        }

        .code-pill {
            background: rgba(59, 130, 246, 0.15);
            color: #60a5fa;
            border: 1px solid rgba(59, 130, 246, 0.3);
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 700;
            display: inline-block;
        }

        .credit-pill {
            background: rgba(255, 255, 255, 0.05);
            color: #f8fafc;
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
        }

        .course-title {
            color: #f8fafc;
            font-size: 1.1rem;
            font-weight: 700;
            margin-top: 6px;
        }

        .info-label {
            color: #64748b;
            font-size: 0.78rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.4px;
        }

        .info-value {
            color: #cbd5e1;
            font-size: 0.9rem;
            font-weight: 600;
            margin-top: 1px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Fetch Data
    courses = get_student_courses(student_id)

    # Title Section (No Emojis)
    st.title("My Courses")
    st.caption("Courses assigned to you")
    st.divider()

    if not courses:
        st.info("No courses have been assigned to you yet.")
        return

    # =====================================================
    # SUMMARY METRICS
    # =====================================================
    total_courses = len(courses)
    total_credits = sum(course.get("Credits") or 0 for course in courses)

    col1, col2 = st.columns(2)

    with col1:
        metric_html = f"""<div class='metric-card'>
<div class='metric-title'>Total Courses</div>
<div class='metric-value'>{total_courses}</div>
</div>"""
        st.markdown(metric_html, unsafe_allow_html=True)

    with col2:
        metric_html = f"""<div class='metric-card'>
<div class='metric-title'>Total Credits</div>
<div class='metric-value'>{total_credits}</div>
</div>"""
        st.markdown(metric_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # COURSE LIST (ANIMATED CARDS)
    # =====================================================
    st.markdown("<div class='courses-wrapper'>", unsafe_allow_html=True)

    for course in courses:
        c_code = course.get("Course Code", "N/A")
        c_name = course.get("Course Name", "N/A")
        c_dept = course.get("Department", "N/A")
        c_sem = course.get("Semester", "N/A")
        c_credits = course.get("Credits", "N/A")
        c_teacher = course.get("Teacher", "Not Assigned")
        c_id = course.get("Course ID", "N/A")

        card_html = f"""<div class='course-card'>
<div style='display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px; margin-bottom: 12px;'>
<div>
<span class='code-pill'>{c_code}</span>
<div class='course-title'>{c_name}</div>
</div>
<div>
<span class='credit-pill'>Credits: {c_credits}</span>
</div>
</div>
<div style='display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px; border-top: 1px solid rgba(255, 255, 255, 0.05); padding-top: 12px;'>
<div style='flex: 1; min-width: 120px;'>
<div class='info-label'>Department</div>
<div class='info-value'>{c_dept}</div>
</div>
<div style='flex: 1; min-width: 100px;'>
<div class='info-label'>Semester</div>
<div class='info-value'>{c_sem}</div>
</div>
<div style='flex: 1.2; min-width: 130px;'>
<div class='info-label'>Teacher</div>
<div class='info-value'>{c_teacher}</div>
</div>
</div>
<div style='color: #475569; font-size: 0.75rem; margin-top: 10px; text-align: right;'>Course ID: {c_id}</div>
</div>"""

        st.markdown(card_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)











def student_profile(student_id):

    # =====================================================
    # FETCH EXISTING PROFILE
    # =====================================================

    profile = get_student_profile(student_id)

    if not profile:
        st.error("Student profile not found.")
        return

    # =====================================================
    # CUSTOM CSS & ANIMATIONS INJECTION
    # =====================================================
    st.markdown("""
        <style>
        /* Smooth Entrance Keyframe */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Rotating Gradient Ring for Profile Avatar */
        @keyframes spinGradient {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Avatar Breathing Float Animation */
        @keyframes avatarFloat {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-6px); }
            100% { transform: translateY(0px); }
        }

        /* Modern Animated Avatar Frame */
        .avatar-container {
            position: relative;
            width: 140px;
            height: 140px;
            margin: auto;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: avatarFloat 4s ease-in-out infinite;
        }

        .avatar-container::before {
            content: '';
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: linear-gradient(45deg, #6366f1, #a855f7, #ec4899, #6366f1);
            animation: spinGradient 4s linear infinite;
            filter: blur(4px);
        }

        .avatar-container img {
            position: relative;
            width: 130px !important;
            height: 130px !important;
            border-radius: 50% !important;
            border: 3px solid #0f172a;
            object-fit: cover;
            z-index: 1;
        }

        /* Animated Section Cards */
        .profile-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
            animation: fadeInUp 0.6s ease-out forwards;
            transition: all 0.3s ease;
        }

        .profile-card:hover {
            transform: translateY(-4px);
            border-color: rgba(99, 102, 241, 0.4);
            box-shadow: 0 12px 40px 0 rgba(99, 102, 241, 0.15);
        }

        /* Section Header with Stylish Icon Box */
        .section-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 18px;
        }

        .icon-badge {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white;
            padding: 8px;
            border-radius: 10px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }

        .section-title {
            font-size: 1.25rem;
            font-weight: 700;
            margin: 0;
            color: #f8fafc;
        }

        /* Title Gradient */
        .gradient-header {
            background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }

        /* Input Styling */
        .stTextInput input, .stSelectbox select, .stTextArea textarea {
            border-radius: 10px !important;
            transition: all 0.3s ease-in-out !important;
        }
        .stTextInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {
            box-shadow: 0 0 12px rgba(99, 102, 241, 0.3) !important;
        }

        /* Animated Submit Button */
        div.stButton > button {
            border-radius: 12px !important;
            font-weight: 600 !important;
            letter-spacing: 0.5px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            background: linear-gradient(90deg, #4f46e5, #7c3aed) !important;
            border: none !important;
        }

        div.stButton > button:hover {
            transform: scale(1.02) !important;
            box-shadow: 0 10px 25px -5px rgba(124, 58, 237, 0.5) !important;
        }
        </style>

        <!-- Material Icons CDN -->
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">
    """, unsafe_allow_html=True)

    # =====================================================
    # PAGE HEADER
    # =====================================================

    
    st.divider()

    # =====================================================
    # STUDENT NAME & HEADER
    # =====================================================

    student_display_name = profile.get("student_name") or "Student"

    col1, col2 = st.columns([1, 4], vertical_alignment="center")

    with col1:
        avatar_url = (
            "https://ui-avatars.com/api/"
            "?name=" + student_display_name.replace(" ", "+") +
            "&size=180" +
            "&background=6366f1" +
            "&color=ffffff" +
            "&bold=true"
        )
        # Glowing & Rotating Avatar Frame
        st.markdown(f"""
            <div class='avatar-container'>
                <img src='{avatar_url}' alt='Avatar' />
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader(student_display_name)
        st.caption("Student Profile")
        st.caption("Personal and academic information overview")

    st.divider()

    # =====================================================
    # PERSONAL INFORMATION
    # =====================================================

    st.markdown("""
        <div class='profile-card'>
            <div class='section-header'>
                <div class='icon-badge'><span class='material-icons-round'>person</span></div>
                <h3 class='section-title'>Personal Information</h3>
            </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        student_name = st.text_input(
            "Full Name",
            value=profile.get("student_name") or ""
        )

    with col2:
        gender_options = ["Male", "Female", "Other"]
        current_gender = profile.get("gender")

        if current_gender in gender_options:
            gender_index = gender_options.index(current_gender)
        else:
            gender_index = 0

        gender = st.selectbox(
            "Gender",
            gender_options,
            index=gender_index
        )

    col1, col2 = st.columns(2)

    with col1:
        dob = profile.get("dob")
        if isinstance(dob, datetime):
            dob = dob.date()
        if not isinstance(dob, date):
            dob = date.today()

        dob = st.date_input(
            "Date of Birth",
            value=dob
        )

    with col2:
        blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        current_blood = profile.get("blood_group")

        if current_blood in blood_groups:
            blood_index = blood_groups.index(current_blood)
        else:
            blood_index = 0

        blood_group = st.selectbox(
            "Blood Group",
            blood_groups,
            index=blood_index
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # ACADEMIC INFORMATION
    # =====================================================

    st.markdown("""
        <div class='profile-card'>
            <div class='section-header'>
                <div class='icon-badge'><span class='material-icons-round'>school</span></div>
                <h3 class='section-title'>Academic Information</h3>
            </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.text_input(
            "Enrollment Number",
            value=profile.get("enrollment_no") or "",
            disabled=True
        )

    with col2:
        st.text_input(
            "Roll Number",
            value=str(profile.get("roll_no") or ""),
            disabled=True
        )

    col1, col2 = st.columns(2)

    with col1:
        st.text_input(
            "Department",
            value=profile.get("department") or "",
            disabled=True
        )

    with col2:
        st.text_input(
            "Semester",
            value=str(profile.get("semester") or ""),
            disabled=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # CONTACT INFORMATION
    # =====================================================

    st.markdown("""
        <div class='profile-card'>
            <div class='section-header'>
                <div class='icon-badge'><span class='material-icons-round'>alternate_email</span></div>
                <h3 class='section-title'>Contact Information</h3>
            </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        email = st.text_input(
            "Email Address",
            value=profile.get("email") or ""
        )

    with col2:
        phone = st.text_input(
            "Phone Number",
            value=str(profile.get("phone") or "")
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # ADDRESS
    # =====================================================

    st.markdown("""
        <div class='profile-card'>
            <div class='section-header'>
                <div class='icon-badge'><span class='material-icons-round'>home</span></div>
                <h3 class='section-title'>Address Details</h3>
            </div>
    """, unsafe_allow_html=True)

    address = st.text_area(
        "Address",
        value=profile.get("address") or "",
        height=90
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        city = st.text_input(
            "City",
            value=profile.get("city") or ""
        )

    with col2:
        state = st.text_input(
            "State",
            value=profile.get("state") or ""
        )

    with col3:
        pincode = st.text_input(
            "Pincode",
            value=str(profile.get("pincode") or "")
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # PARENT / GUARDIAN INFORMATION
    # =====================================================

    st.markdown("""
        <div class='profile-card'>
            <div class='section-header'>
                <div class='icon-badge'><span class='material-icons-round'>family_restroom</span></div>
                <h3 class='section-title'>Parent / Guardian Information</h3>
            </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        father_name = st.text_input(
            "Father's Name",
            value=profile.get("father_name") or ""
        )

    with col2:
        mother_name = st.text_input(
            "Mother's Name",
            value=profile.get("mother_name") or ""
        )

    col1, col2 = st.columns(2)

    with col1:
        parent_phone = st.text_input(
            "Parent Mobile Number",
            value=profile.get("parent_phone") or ""
        )

    with col2:
        parent_email = st.text_input(
            "Parent Email",
            value=profile.get("parent_email") or ""
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # =====================================================
    # UPDATE PROFILE
    # =====================================================

    st.divider()

    if st.button(
        "Update Profile",
        use_container_width=True,
        type="primary"
    ):

        try:

            success = save_student_profile(
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
                profile.get("occupation") or ""
            )

            if success:
                st.success("Profile updated successfully.")
                st.balloons()
                st.rerun()
            else:
                st.error("Unable to update profile.")

        except Exception as e:
            st.error("Something went wrong while updating profile.")
            st.exception(e)