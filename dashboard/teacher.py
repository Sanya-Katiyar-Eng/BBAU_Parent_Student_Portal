
import streamlit as st
from database.assignment import (
    add_assignment,
    get_teacher_assignments,
    update_assignment,
    delete_assignment,
    add_notice,
    get_teacher_notices,
    update_notice,
    delete_notice
)
from database.teacher_db import *
from database.dashboard_db import *
from database.timetable_db import *
from database.notification_db import *

# for assignment........................................................
import pandas as pd

from datetime import datetime
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if "user_id" not in st.session_state:
    st.session_state.user_id = None


if "role" not in st.session_state:
    st.session_state.role = None


if "teacher_name" not in st.session_state:
    st.session_state.teacher_name = None


def teacher_page():


    st.title("Teacher Management")
    st.markdown("---")

    # ================= Dashboard Cards ================= #
    total_teachers, active_teachers, inactive_teachers, total_departments = get_teacher_statistics()
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Teachers", total_teachers)

    with col2:
        st.metric("Active",active_teachers)

    with col3:
        st.metric("Inactive",inactive_teachers)

    with col4:
        st.metric("Departments",total_departments)

    st.markdown("---")

    # ================= Tabs ================= #

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            " Add Teacher",
            " View Teachers",
            " Edit Teacher",
            "Delete Teacher"
        ]
    )

    # =====================================================
    # ADD TEACHER
    # =====================================================

    with tab1:

        st.subheader(" Personal Information")

        col1, col2 = st.columns(2)

        with col1:
            teacher_name=st.text_input("Teacher Name")
            employee_id=st.text_input("Employee ID")
        
            dob = st.date_input("Date of Birth")
            gender=st.selectbox(
                "Gender",
                ["Male", "Female", "Other"]
            )
            mobile=st.text_input("Mobile Number")

        with col2:
            email=st.text_input("Email")
            aadhar=st.text_input("Aadhar Number")
            photo=st.file_uploader(
                "Upload Photo",
                type=["jpg", "jpeg", "png"]
            )

        st.markdown("---")

        st.subheader(" Address")

        address=st.text_area("Address")

        col1, col2, col3 = st.columns(3)

        with col1:
            city=st.text_input("City")

        with col2:
            state=st.text_input("State")

        with col3:
           pincode= st.text_input("Pincode")

        st.markdown("---")

        st.subheader(" Academic Information")

        col1, col2 = st.columns(2)

        with col1:
            qualification=st.text_input("Highest Qualification")
            specialization=st.text_input("Specialization")
            university=st.text_input("University")

        with col2:
            experience=st.number_input(
                "Experience (Years)",
                min_value=0
            )
            passing_year=st.number_input(
                "Passing Year",
                min_value=1990,
                max_value=2026
            )

        st.markdown("---")

        st.subheader(" Employment Details")

        col1, col2 = st.columns(2)

        with col1:
            department =st.text_input("Department")
            designation =st.text_input("Designation")

        with col2:
            joining_date = st.date_input("Joining Date")
            employment_type =st.selectbox(
                "Employment Type",
                [
                    "Full Time",
                    "Part Time",
                    "Guest Faculty"
                ]
            )

        st.markdown("---")

        st.markdown("---")

        st.subheader(" Login Details")

        col1, col2 = st.columns(2)

        with col1:
            username =st.text_input("Username")

        with col2:
            password =st.text_input(
                "Password",
                type="password"
            )

        st.markdown("###")

        c1, c2, c3 = st.columns(3)

        with c1:
            if st.button("Save"):
                try:

            # Save only filename (or None)
                    photo_path = photo.name if photo else None

                    success = add_teacher(
                teacher_name=teacher_name,
                employee_id=employee_id,
                department=department,
                designation=designation,
                qualification=qualification,
                phone=mobile,
                email=email,
                gender=gender,
                date_of_birth=dob,
                address=address,
                city=city,
                state=state,
                pincode=pincode,
                aadhar_number=aadhar,
                specialization=specialization,
                university=university,
                passing_year=passing_year,
                experience=experience,
                joining_date=joining_date,
                employment_type=employment_type,
                username=username,
                password=password,
                photo=photo_path
            )

                    if success:
                        st.success("Teacher added successfully!")
                    else:
                        st.error("Unable to add teacher.")

                except Exception as e:
                    st.exception(e)




    # =====================================================
    # VIEW
    # =====================================================

        with tab2:

            st.subheader("View Teachers")

            teachers = get_all_teachers()

            if not teachers:
                st.info("No teachers found.")
            else:

                data = []

            for teacher in teachers:
                data.append({
          "Teacher ID": teacher[0],
        "Teacher Name": teacher[1],
        "Employee ID": teacher[2],
        "Department": teacher[3],
        "Designation": teacher[4],
        "Phone": teacher[5],
        "Email": teacher[6],
        "Status": teacher[7]
})

                st.dataframe(
            data,
            use_container_width=True,
            hide_index=True
        )

    # =====================================================
    # EDIT
    # =====================================================

    with tab3:
        with st.form("edit_teacher_form"):

            teacher_name = st.text_input("Teacher Name", key="edit_teacher_name")
            employee_id = st.text_input("Employee ID", key="edit_employee_id")
            department = st.text_input("Department", key="edit_department")
            designation = st.text_input("Designation", key="edit_designation")
            email = st.text_input("Email", key="edit_email")
            mobile = st.text_input("Mobile", key="edit_mobile")
            qualification = st.text_input("Qualification", key="edit_qualification")
            experience = st.number_input("Experience", key="edit_experience")
            gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"],
        key="edit_gender"
    )
            address = st.text_area("Address", key="edit_address")

            update_btn = st.form_submit_button("Update Teacher")

            if update_btn:
                success=update_teacher(
        teacher_name,
        employee_id,
        department,
        designation,
        email,
        mobile,
        qualification,
        experience,
        gender,
        address,
    )
                if success:
                    st.success("Update Successfully !")
                else:
                    st.error("Update failed")


    # =====================================================
    # DELETE
    # =====================================================

    with tab4:

        st.subheader("🗑 Delete Teacher")

        name = st.text_input(
    "Search by Teacher Name",
    key="search_name"
)

        employee = st.text_input(
    "Search by Employee ID",
    key="search_employee"
)

        teachers = search_teachers(name, employee)

        if teachers:

            st.dataframe(
        teachers,
        use_container_width=True
    )

            selected = st.selectbox(
        "Select Teacher",
        [f"{t[0]} ({t[1]})" for t in teachers]
    )

            if st.button("Delete"):

                teacher_name = selected.split(" (")[0]
                employee_id = selected.split("(")[1].replace(")", "")

                if delete_teacher(
            teacher_name,
            employee_id
        ):
                    st.success("Teacher Deleted Successfully")
                    st.rerun()
                else:
                    st.error("Delete Failed")

            else:
                st.info("No Teacher Found")





# -----------------------------
# Session Initialization
# -----------------------------

















# =====================================
# Teacher Dashboard Controller
# =====================================

'''def teacher_dashboard():
    


    # Authentication Check

    if (
        "logged_in" not in st.session_state
        or not st.session_state.logged_in
        or st.session_state.role.lower() != "teacher"
    ):

        st.warning(
            "Please login as Teacher"
        )

        st.stop()



# ==========================
# Sidebar
# ==========================

    teacher = get_teacher_profile(st.session_state.user_id)

    teacher_name = teacher["teacher_name"] if teacher else "Faculty Member"
    designation = teacher["designation"] if teacher else ""
    department = teacher["department"] if teacher else ""

    with st.sidebar:

        st.markdown("""
    <div style="
        background:#1e3a8a;
        padding:20px;
        border-radius:10px;
        color:white;
        text-align:center;
    ">
        <h3 style="margin-bottom:5px;">BBAU Portal</h3>
        <hr style="border:1px solid rgba(255,255,255,0.3);">
        <h4 style="margin-bottom:0px;">{}</h4>
        <p style="margin:0;">{}</p>
        <p style="margin:0;">{}</p>
    </div>
    """.format(
        teacher_name,
        designation,
        department
    ), unsafe_allow_html=True)

        st.write("")

        menu = st.radio(
    "",
    [
        "Dashboard",
        "Students",
        "Attendance",
        "Courses",
        "Assignments",
        "Schedule Class",
        "Profile",
        "Logout"
    ]
)

    # ==========================
    # Routing
    # ==========================


    if menu == "Dashboard":

        teacher_home()



    elif menu == "Students":

        teacher_students()

    elif menu == "Schedule Class":

        teacher_class_schedule()

    elif menu == "Attendance":

        teacher_attendance()



    elif menu == "Courses":

        teacher_courses()



    elif menu == "Assignments":

        teacher_assignments()



    elif menu == "Profile":

        teacher_profile()



    elif menu == "Logout":

        st.session_state.logged_in = False

        st.session_state.user_id = None
        st.session_state.role = None
        st.session_state.teacher_name = None


        st.success(
        "Logout Successfully"
    )

        st.rerun()'''

import streamlit as st

def teacher_dashboard():
    # Authentication Check
    if (
        "logged_in" not in st.session_state
        or not st.session_state.logged_in
        or st.session_state.role.lower() != "teacher"
    ):
        st.warning("Please login as Teacher")
        st.stop()

    # =====================================================
    # HIGH CONTRAST & CLEAR VISIBILITY THEME (LIGHT & BLUE)
    # =====================================================
    st.markdown("""
<style>
/* Main Background */
.stApp {
    background-color: #f1f5f9;
}

/* Sidebar Clean Background */
section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 2px solid #e2e8f0;
}

/* Profile Card Styling */
.teacher-profile-card {
    background: #0f172a;
    padding: 18px 14px;
    border-radius: 10px;
    color: #ffffff;
    text-align: center;
    border: 1px solid #1e293b;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    margin-bottom: 20px;
}

.teacher-profile-card h3 {
    margin: 0 0 6px 0 !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    color: #ffffff !important;
}

.teacher-profile-card hr {
    border: 0;
    height: 1px;
    background: #334155;
    margin: 8px 0;
}

.teacher-profile-card h4 {
    margin: 4px 0 2px 0 !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    color: #38bdf8 !important;
}

.teacher-profile-card p {
    margin: 2px 0 !important;
    font-size: 12px !important;
    color: #cbd5e1 !important;
}

/* Radio Button Container Styling (Make Buttons Clearly Visible) */
section[data-testid="stSidebar"] div[role="radiogroup"] > label {
    background-color: #f8fafc !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
    padding: 10px 14px !important;
    margin-bottom: 8px !important;
    transition: all 0.2s ease-in-out !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
}

/* Text inside radio options */
section[data-testid="stSidebar"] div[role="radiogroup"] > label div[data-testid="stMarkdownContainer"] p {
    color: #1e293b !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}

/* Hover State */
section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
    background-color: #e0f2fe !important;
    border-color: #0284c7 !important;
    transform: translateX(2px);
}

/* Active / Selected Radio Button State */
section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"] {
    background-color: #1e3a8a !important;
    border-color: #1e3a8a !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"] div[data-testid="stMarkdownContainer"] p {
    color: #ffffff !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

    # =====================================================
    # SIDEBAR PROFILE & NAVIGATION
    # =====================================================
    teacher = get_teacher_profile(st.session_state.user_id)

    teacher_name = teacher["teacher_name"] if teacher else "Faculty Member"
    designation = teacher["designation"] if teacher else "Professor"
    department = teacher["department"] if teacher else "Academic Dept."

    with st.sidebar:
        # Profile Header Card
        st.markdown("""
<div class="teacher-profile-card">
    <h3>BBAU Portal</h3>
    <hr>
    <h4>{}</h4>
    <p>{}</p>
    <p>{}</p>
</div>
""".format(
            teacher_name,
            designation,
            department
        ), unsafe_allow_html=True)

        # Main Navigation Menu
        menu = st.radio(
            "",
            [
                "Dashboard",
                "Students",
                "Attendance",
                "Courses",
                "Assignments",
                "Schedule Class",
                "Profile",
                "Logout"
            ],
            label_visibility="collapsed"
        )

    # =====================================================
    # ROUTING LOGIC
    # =====================================================
    if menu == "Dashboard":
        teacher_home()

    elif menu == "Students":
        teacher_students()

    elif menu == "Schedule Class":
        teacher_class_schedule()

    elif menu == "Attendance":
        teacher_attendance()

    elif menu == "Courses":
        teacher_courses()

    elif menu == "Assignments":
        teacher_assignments()

    elif menu == "Profile":
        teacher_profile()

    elif menu == "Logout":
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.role = None
        st.session_state.teacher_name = None

        st.success("Logout Successfully")
        st.rerun()

























def get_student_today_classes(semester):

    conn=get_connection()
    cur=conn.cursor()

    cur.execute("""

    SELECT
    c.course_name,
    t.day_name,
    t.start_time,
    t.end_time,
    t.room_no

    FROM timetable t

    JOIN courses c
    ON t.course_id=c.course_id

    WHERE t.semester=%s

    ORDER BY start_time

    """,(semester,))

    data=cur.fetchall()

    conn.close()

    return data

# =====================================
# Teacher Home Dashboard
# =====================================
def teacher_class_schedule():

    from datetime import date, datetime
    import streamlit as st

    st.title("Class Schedule")

    teacher_id = st.session_state.user_id

    st.write("**DEBUG TEACHER ID:**", teacher_id)

    st.divider()

    # =====================================================
    # SCHEDULE NEW CLASS
    # =====================================================

    st.subheader("Schedule New Class")

    col1, col2 = st.columns(2)

    # =====================================================
    # SEMESTER
    # =====================================================

    with col1:

        semester = st.selectbox(
            "Semester",
            [
                "Semester 1",
                "Semester 2",
                "Semester 3",
                "Semester 4",
                "Semester 5",
                "Semester 6",
                "Semester 7",
                "Semester 8"
            ],
            key="schedule_semester"
        )

    # =====================================================
    # COURSES
    # =====================================================

    courses = get_teacher_courses(teacher_id)

    semester_number = int(
        semester.replace("Semester ", "").strip()
    )

    semester_courses = []

    for course in courses:

        try:
            course_semester = int(
                str(course["Semester"])
                .replace("Semester", "")
                .strip()
            )

            if course_semester == semester_number:
                semester_courses.append(course)

        except:
            continue

    if not semester_courses:

        st.warning(
            "Is semester ke liye koi course assigned nahi hai."
        )

        return

    with col2:

        selected_course = st.selectbox(
            "Course",
            semester_courses,
            format_func=lambda x:
                f'{x["Course Name"]} ({x["Department"]})',
            key="schedule_course"
        )

    # =====================================================
    # CLASS DATE + DAY
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        class_date = st.date_input(
            "Class Date",
            value=date.today(),
            min_value=date.today(),
            key="class_date"
        )

    with col2:

        day_name = class_date.strftime("%A")

        st.text_input(
            "Day",
            value=day_name,
            disabled=True,
            key="class_day"
        )

    # =====================================================
    # TIME
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        start_time = st.time_input(
            "Start Time (IST)",
            value=datetime.strptime(
                "10:00",
                "%H:%M"
            ).time(),
            key="class_start"
        )

    with col2:

        end_time = st.time_input(
            "End Time (IST)",
            value=datetime.strptime(
                "11:00",
                "%H:%M"
            ).time(),
            key="class_end"
        )

    # =====================================================
    # ROOM
    # =====================================================

    room_no = st.text_input(
        "Room Number",
        placeholder="Example: BCA Lab / Room 204",
        key="class_room"
    )

    st.divider()

    # =====================================================
    # SCHEDULE CLASS
    # =====================================================

    if st.button(
        "Schedule Class",
        type="primary",
        use_container_width=True
    ):

        # -----------------------------------------------
        # Date validation
        # -----------------------------------------------

        if class_date < date.today():

            st.error(
                "Past date par class schedule nahi kar sakte."
            )

        # -----------------------------------------------
        # Time validation
        # -----------------------------------------------

        elif start_time >= end_time:

            st.error(
                "End time, start time ke baad hona chahiye."
            )

        else:

            success, message = add_class_schedule(

                teacher_id=teacher_id,

                course_id=selected_course["Course ID"],

                class_date=class_date,

                day_name=day_name,

                start_time=start_time,

                end_time=end_time,

                room_no=room_no,

                semester=semester_number
            )

            if success:

                st.success(
                    "Class scheduled successfully."
                )

                st.rerun()

            else:

                st.error(message)

    # =====================================================
    # MY CLASS SCHEDULE
    # =====================================================

    st.divider()

    st.subheader("My Class Schedule")

    schedules = get_teacher_timetable(
        teacher_id
    )

    if not schedules:
        st.warning("No classes scheduled yet.")

        st.write("DEBUG: Teacher ID =", teacher_id)
        st.write("DEBUG: Timetable Data =", schedules)

        return
    today = date.today()

    today_classes = []
    upcoming_classes = []

    # =====================================================
    # SEPARATE TODAY / UPCOMING
    # =====================================================

    for row in schedules:

        class_date = row[1]

        if class_date == today:

            today_classes.append(row)

        elif class_date > today:

            upcoming_classes.append(row)

    # =====================================================
    # TODAY
    # =====================================================

    if today_classes:

        for row in today_classes:

            (
                timetable_id,
                class_date,
                day_name,
                start_time,
                end_time,
                room_no,
                semester_no,
                course_id,
                course_name,
                course_code
            ) = row

            st.markdown(
                f"### 📘 {course_name}"
            )

            st.write(
                f"**Course Code:** {course_code}"
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.write(
                    f" {class_date.strftime('%d-%m-%Y')}"
                )

            with col2:

                st.write(
                    f" {start_time.strftime('%I:%M %p')} - "
                    f"{end_time.strftime('%I:%M %p')}"
                )

            with col3:

                st.write(
                    f" {room_no if room_no else 'Room not assigned'}"
                )

                st.write(
                    f" Semester {semester_no}"
                )

            with col4:

                if st.button(
                    " Delete",
                    key=f"delete_today_{timetable_id}",
                    use_container_width=True
                ):

                    success, message = delete_class_schedule(
                        timetable_id,
                        teacher_id
                    )

                    if success:

                        st.success(message)

                        st.rerun()

                    else:

                        st.error(message)

            st.divider()

    else:

        st.info(
            "Aaj koi class scheduled nahi hai."
        )

    # =====================================================
    # UPCOMING
    # =====================================================

    st.subheader(" Upcoming Classes")

    if upcoming_classes:

        for row in upcoming_classes:

            (
                timetable_id,
                class_date,
                day_name,
                start_time,
                end_time,
                room_no,
                semester_no,
                course_id,
                course_name,
                course_code
            ) = row

            st.markdown(
                f"###  {course_name}"
            )

            st.write(
                f"**Course Code:** {course_code}"
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.write(
                    f" {class_date.strftime('%d-%m-%Y')}"
                )

                st.write(
                    f" {day_name}"
                )

            with col2:

                st.write(
                    f" {start_time.strftime('%I:%M %p')} - "
                    f"{end_time.strftime('%I:%M %p')}"
                )

            with col3:

                st.write(
                    f" {room_no if room_no else 'Room not assigned'}"
                )

                st.write(
                    f" Semester {semester_no}"
                )

            with col4:

                if st.button(
                    " Delete",
                    key=f"delete_upcoming_{timetable_id}",
                    use_container_width=True
                ):

                    success, message = delete_class_schedule(
                        timetable_id,
                        teacher_id
                    )

                    if success:

                        st.success(message)

                        st.rerun()

                    else:

                        st.error(message)

            st.divider()

    else:

        st.info(
            "Koi upcoming class scheduled nahi hai."
        )


























'''def teacher_home():

    teacher = get_teacher_profile(st.session_state.user_id)

    if teacher is None:
        st.error("Teacher profile not found.")
        return

    teacher_id = teacher["teacher_id"]
    department = teacher["department"]
    designation = teacher["designation"]
    teacher_name = teacher["teacher_name"]

    st.markdown(f"""
    <div style="
        background:#1e3a8a;
        padding:25px;
        border-radius:12px;
        color:white;
    ">
        <h2 style="margin-bottom:5px;">{teacher_name}</h2>
        <p style="margin:0;font-size:17px;">
            {designation} | {department}
        </p>
        <p style="margin-top:8px;">
            Babasaheb Bhimrao Ambedkar University
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Students", 1)

    with col2:
        st.metric("Courses", 0)

    with col3:
        st.metric("Assignments", 0)

    with col4:
        st.metric("Results", 0)

    st.divider()

    show_teacher_activity()'''


import streamlit as st

def teacher_home():
    teacher = get_teacher_profile(st.session_state.user_id)

    if teacher is None:
        st.error("Teacher profile not found.")
        return

    teacher_id = teacher["teacher_id"]
    department = teacher["department"]
    designation = teacher.get("designation", "")
    teacher_name = teacher["teacher_name"]

    # =====================================================
    # PREMIUM SOFT LIGHT THEME (SKY BLUE & WHITE)
    # =====================================================
    st.markdown("""
<style>
/* Welcome Banner Styling */
.teacher-welcome-banner {
    background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 100%);
    padding: 24px 28px;
    border-radius: 16px;
    border: 1px solid #bae6fd;
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.05);
    margin-bottom: 24px;
}

.teacher-welcome-banner h2 {
    margin: 0 0 4px 0 !important;
    font-size: 26px !important;
    font-weight: 700 !important;
    color: #0369a1 !important;
}

.teacher-welcome-banner .sub-info {
    margin: 0;
    font-size: 15px;
    color: #0284c7;
    font-weight: 600;
}

.teacher-welcome-banner .univ-info {
    margin-top: 6px;
    font-size: 13px;
    color: #64748b;
    font-weight: 500;
}

/* Dynamic Metric Cards Styling */
[data-testid="stMetric"] {
    background-color: #ffffff !important;
    border: 1px solid #e0f2fe !important;
    border-radius: 14px !important;
    padding: 18px 20px !important;
    box-shadow: 0 4px 10px rgba(15, 23, 42, 0.03) !important;
    transition: all 0.25s ease !important;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 18px rgba(2, 132, 199, 0.1) !important;
    border-color: #38bdf8 !important;
}

[data-testid="stMetricValue"] {
    color: #0284c7 !important;
    font-weight: 800 !important;
    font-size: 28px !important;
}

[data-testid="stMetricLabel"] {
    color: #475569 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}
</style>
""", unsafe_allow_html=True)

    # =====================================================
    # WELCOME HEADER BANNER (FETCHED DATA)
    # =====================================================
    sub_text = f"{designation} | Department of {department}" if designation else f"Department of {department}"
    
    st.markdown("""
<div class="teacher-welcome-banner">
    <h2>Welcome back, {}</h2>
    <p class="sub-info">{}</p>
    <p class="univ-info">Babasaheb Bhimrao Ambedkar University</p>
</div>
""".format(
        teacher_name,
        sub_text
    ), unsafe_allow_html=True)

    # =====================================================
    # METRICS SECTION (ORIGINAL FETCHED VALUES)
    # =====================================================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Students", 1)

    with col2:
        st.metric("Courses", 0)

    with col3:
        st.metric("Assignments", 0)

    with col4:
        st.metric("Results", 0)

    st.divider()

    # Dynamic backend data & activity loader
    show_teacher_activity()












from database.teacher_db import *

def show_teacher_activity():

    teacher = get_teacher_profile(st.session_state.user_id)

    teacher_id = teacher["teacher_id"]

    left, right = st.columns([2,1])

    with left:

        st.subheader("Today's Timetable")

        classes = get_today_classes(teacher_id)

        if classes:

            for cls in classes:

                 st.info(
            f"""
Course : {cls[0]}

Semester : {cls[1]}

Day : {cls[2]}

Time : {cls[3]} - {cls[4]}

Room : {cls[5]}
"""
        )
        else:
            st.info("No classes scheduled for today.")

    with right:

        st.subheader("Notice Board")

        st.info("No notices.")

    st.divider()

    st.subheader("Recent Academic Activity")

    st.success("Dashboard loaded successfully.")



















    #teacher-student
    #========================

def teacher_students():

    st.title("My Students")
    st.divider()


    teacher_id = st.session_state.get("user_id")


    students = get_teacher_students(
        teacher_id
    )


    if not students:
        st.info("No students assigned yet.")
        return



    # Top Count

    col1,col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Students",
            len(students)
        )


    with col2:
        st.metric(
            "Active Students",
            len(
                [
                    s for s in students
                    if s[7]=="Active"
                ]
            )
        )


    st.divider()



    # Search

    search = st.text_input(
        "Search Student",
        placeholder="Enter Name, Enrollment Number or Roll Number"
    )


    # Semester Filter

    semesters = [
        "All"
    ] + sorted(
        list(
            set(
                [
                    s[4]
                    for s in students
                ]
            )
        )
    )


    semester = st.selectbox(
        "Semester",
        semesters
    )



    filtered_students = students



    if search:

        filtered_students = [
            s for s in filtered_students
            if search.lower() in str(s[2]).lower()
            or search.lower() in str(s[1]).lower()
            or search.lower() in str(s[5]).lower()
        ]



    if semester != "All":

        filtered_students = [
            s for s in filtered_students
            if s[4] == semester
        ]



    st.divider()



    if not filtered_students:

        st.warning(
            "No students found."
        )

        return



    # Student Display


    for student in filtered_students:


        with st.container():

            c1,c2,c3 = st.columns(
                [2,2,1]
            )


            with c1:

                st.markdown(
                    f"""
                    **{student[2]}**

                    Roll No: {student[1]}

                    Enrollment:
                    {student[5]}
                    """
                )


            with c2:

                st.markdown(
                    f"""
                    Department:
                    {student[3]}

                    Semester:
                    {student[4]}

                    Gender:
                    {student[6]}
                    """
                )


            with c3:

                if st.button(
                    "View",
                    key=f"student_{student[0]}"
                ):

                    show_selected_student(
                        student[0]
                    )


            st.divider()












#================================================================================
# attendence
# =========================================================================================
def teacher_attendance():

    st.title("Attendance ")
    st.divider()
    teacher_id = st.session_state.user_id

    # ==========================
    # Filters
    # ==========================

    col1, col2, col3 = st.columns(3)

    with col1:

        semester = st.selectbox(
            "Semester",
            [
                "Semester 1",
                "Semester 2",
                "Semester 3",
                "Semester 4",
                "Semester 5",
                "Semester 6",
                "Semester 7",
                "Semester 8"
            ]
        )

    with col2:

        courses = get_teacher_courses(teacher_id)

        if not courses:
            st.warning("No course assigned.")
            return
        
        selected_course = st.selectbox(
            "Course",
            courses,
            format_func=lambda x: f"{x['Course Name']} ({x['Department']})"   # Course Name
        )

    with col3:

        attendance_date = st.date_input(
            "Attendance Date"
        )

        st.divider()

    # ==========================
    # Students
    # ==========================

        students = get_students_by_course(
        course_id=selected_course["Course ID"]  
           # course_id
    )

        if not students:
            st.info("No students found.")
            return

    attendance_data = []

    for student in students:

        col1, col2, col3 = st.columns([2,4,2])

        with col1:
            st.write(student[2])      # Enrollment

        with col2:
            st.write(student[1])      # Student Name

        with col3:

            status = st.radio(
            "",
            ["Present", "Absent"],
            horizontal=True,
            key=f"attendance_{student[0]}"
)

        attendance_data.append({
    "student_id": student[0],
    "status": status
})


    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Save Attendance",
            use_container_width=True
        ):

            success = save_attendance(

                course_id=selected_course["Course ID"],
                attendance_date=attendance_date,
                teacher_id=teacher_id,
                attendance_data=attendance_data

                )

            if success:

                st.success("Attendance saved successfully.")
                for row in attendance_data:
                    parent=get_parent_details(
                        row["student_id"]
                        )
                    st.write("Parent Data:", parent)

                    if parent:
                        phone = parent[0]
                        parent_name = parent[2]


                        sms_result=send_attendance_sms(
                                phone,
                                parent_name,
                                selected_course["Course Name"],
                                row["status"]
                            )
                            
                        st.write("SMS Status:", sms_result)
            

                history = get_attendance_by_date(
        selected_course["Course ID"],
        attendance_date
    )

                st.divider()
                st.subheader("Today's Attendance")

                st.dataframe(
        history,
        use_container_width=True
    )

            else:

                st.error("Failed to save attendance.")

    with col2:

        if st.button(
            "Reset",
            use_container_width=True
        ):
            st.rerun()

    st.divider()
    st.subheader("Attendence History")
    history = get_attendance_by_date(
    selected_course["Course ID"],
    attendance_date
)
    if history:
        st.dataframe(
        history,
        use_container_width=True
    )

    else:
         st.info("No attendance found for this date.")

    st.divider()

    analytics = get_attendance_analytics(
    selected_course["Course ID"],
    attendance_date
)

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.metric(
        "Total Students",
        analytics["total"]
    )

    with c2:
        st.metric(
        "Present",
        analytics["present"]
    )

    with c3:
        st.metric(
        "Absent",
        analytics["absent"]
    )

    with c4:
        st.metric(
        "Attendance %",
        f"{analytics['percentage']}%"
    )
    st.divider()

    if st.button("Export Attendance to Excel"):

        data,columns=export_attendance(

        selected_course["Course ID"],
        attendance_date

    )

        df=pd.DataFrame(data,columns=columns)

        output=BytesIO()

        with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

            df.to_excel(
            writer,
            index=False
        )

        st.download_button(

        "Download Excel",

            data=output.getvalue(),

            file_name=f"Attendance_{attendance_date}.xlsx",

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )
    




















#================================================================================
# result
# =========================================================================================
def teacher_results():

    st.title("Results")
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        semester = st.selectbox(
            "Semester",
            [
                "Semester 1",
                "Semester 2",
                "Semester 3",
                "Semester 4",
                "Semester 5",
                "Semester 6",
                "Semester 7",
                "Semester 8"
            ]
        )

    with col2:
        courses = get_teacher_courses(
        st.session_state.user_id
)
    course = st.selectbox(
    "Course",
    courses,
    format_func=lambda x:x["Course Name"]
)
    with col3:
        exam_type = st.selectbox(
            "Exam Type",
            [
                "Internal",
                "Mid Semester",
                "Practical",
                "End Semester"
            ]
        )

    st.divider()

    # Replace with database data
    students = get_students_by_course(
        course_id=course["Course ID"]
)

    result_data = {}

    st.subheader("Enter Marks")

    for student in students:

        col1, col2, col3 = st.columns([2, 4, 2])

        with col1:
            st.write(student[3])

        with col2:
            st.write(student[1])

        with col3:
            marks = st.number_input(
                "Marks",
                min_value=0,
                max_value=100,
                step=1,
                key=f"marks_{student[3]}"
            )

        result_data[student[3]] = marks

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Save Results", use_container_width=True):
            save_result(
            course["Course ID"],
            exam_type,
            result_data,
            st.session_state.user_id
)

        st.success("Results saved successfully.")

    with col2:
        if st.button("Clear", use_container_width=True):
            st.rerun()


#================================================================================
# courses
# =========================================================================================
def teacher_courses():

    st.title("My Courses")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        semester = st.selectbox(
            "Semester",
            [
                "All",
                "Semester 1",
                "Semester 2",
                "Semester 3",
                "Semester 4",
                "Semester 5",
                "Semester 6",
                "Semester 7",
                "Semester 8"
            ]
        )

    with col2:
        search = st.text_input(
            "Search Course",
            placeholder="Enter Course Name"
        )


    teacher_id = st.session_state.user_id

    courses = get_teacher_courses(teacher_id)


    if semester != "All":
        courses = [
            course for course in courses
            if course["Semester"] == semester
        ]


    if search:
        courses = [
            course for course in courses
            if search.lower() in course["Course Name"].lower()
        ]


    if courses:

        st.dataframe(
            courses,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No courses available.")





























def teacher_assignments():

    # ==========================================================
    # PAGE STYLE
    # ==========================================================

    st.markdown("""
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .stButton > button {
        border-radius: 10px;
        transition: all 0.25s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 18px rgba(0,0,0,0.12);
    }

    button[data-baseweb="tab"] {
        transition: all 0.25s ease;
    }

    button[data-baseweb="tab"]:hover {
        transform: translateY(-2px);
    }

    </style>
    """, unsafe_allow_html=True)


    # ==========================================================
    # PAGE HEADER
    # ==========================================================

    st.title("Academic Work")

    st.caption(
        "Create, publish and manage assignments, homework, projects and notices."
    )

    st.divider()


    # ==========================================================
    # OVERVIEW CARDS
    # ==========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        with st.container(border=True):

            st.subheader("Assignments")

            st.caption(
                "Academic tasks"
            )

            st.button(
                "Create",
                key="assignment_create_btn",
                use_container_width=True
            )


    with col2:

        with st.container(border=True):

            st.subheader("Homework")

            st.caption(
                "Practice work"
            )

            st.button(
                "Create",
                key="homework_create_btn",
                use_container_width=True
            )


    with col3:

        with st.container(border=True):

            st.subheader("Projects")

            st.caption(
                "Long-term work"
            )

            st.button(
                "Create",
                key="project_create_btn",
                use_container_width=True
            )


    with col4:

        with st.container(border=True):

            st.subheader("Notices")

            st.caption(
                "Important updates"
            )

            st.button(
                "Create",
                key="notice_create_btn",
                use_container_width=True
            )


    st.write("")


    # ==========================================================
    # TABS
    # ==========================================================

    create_tab, notice_tab, published_tab = st.tabs(
        [
            "Create Academic Work",
            "Create Notice",
            "Published Work"
        ]
    )


    # ==========================================================
    # CREATE ACADEMIC WORK
    # ==========================================================

    with create_tab:

        st.subheader(
            "Create Academic Work"
        )

        st.caption(
            "Assign work to a course and define its submission deadline."
        )


        with st.container(border=True):

            # --------------------------------------------------
            # WORK TYPE
            # --------------------------------------------------

            work_type = st.selectbox(
                "Work Type",
                [
                    "Assignment",
                    "Homework",
                    "Project"
                ],
                key="work_type"
            )


            # --------------------------------------------------
            # SEMESTER + COURSE
            # --------------------------------------------------

            col1, col2 = st.columns(2)


            with col1:

                semester = st.selectbox(
                    "Semester",
                    [
                        "Semester 1",
                        "Semester 2",
                        "Semester 3",
                        "Semester 4",
                        "Semester 5",
                        "Semester 6",
                        "Semester 7",
                        "Semester 8"
                    ],
                    key="academic_semester"
                )


            with col2:

                courses = get_teacher_courses(
                    st.session_state.user_id
                )


                if courses:

                    course = st.selectbox(
                        "Course",
                        courses,
                        format_func=lambda x: x["Course Name"],
                        key="academic_course"
                    )

                else:

                    course = None

                    st.warning(
                        "No courses are currently assigned to you."
                    )


            # --------------------------------------------------
            # TITLE
            # --------------------------------------------------

            title = st.text_input(
                "Title",
                placeholder="Enter a clear title"
            )


            # --------------------------------------------------
            # DESCRIPTION
            # --------------------------------------------------

            description = st.text_area(
                "Instructions",
                placeholder="Write instructions for students...",
                height=160
            )


            # --------------------------------------------------
            # DATES
            # --------------------------------------------------

            col1, col2 = st.columns(2)


            with col1:

                assigned_date = st.date_input(
                    "Assigned Date"
                )


            with col2:

                due_date = st.date_input(
                    "Submission Deadline"
                )


            # --------------------------------------------------
            # FILE
            # --------------------------------------------------

            uploaded_file = st.file_uploader(
                "Reference File",
                type=[
                    "pdf",
                    "doc",
                    "docx",
                    "ppt",
                    "pptx",
                    "xls",
                    "xlsx",
                    "zip"
                ]
            )


            if uploaded_file:

                st.success(
                    f"File attached: {uploaded_file.name}"
                )


            st.divider()


            # --------------------------------------------------
            # PUBLISH
            # --------------------------------------------------

            if st.button(
                f"Publish {work_type}",
                use_container_width=True,
                type="primary"
            ):

                if not title.strip():

                    st.warning(
                        "Please enter a title."
                    )

                elif course is None:

                    st.warning(
                        "Please select a course."
                    )

                elif due_date < assigned_date:

                    st.error(
                        "Submission deadline cannot be before assigned date."
                    )

                else:

                    result = add_assignment(
                        course["Course ID"],
                        title,
                        description,
                        due_date,
                        uploaded_file,
                        st.session_state.user_id,
                        work_type
                    )


                    if result:

                        st.success(
                            f"{work_type} published successfully."
                        )

                    else:

                        st.error(
                            "Unable to publish academic work."
                        )


    # ==========================================================
    # CREATE NOTICE
    # ==========================================================

    with notice_tab:

        st.subheader(
            "Create Notice"
        )

        st.caption(
            "Share important information and announcements with students."
        )


        with st.container(border=True):

            # --------------------------------------------------
            # COURSE
            # --------------------------------------------------

            notice_courses = get_teacher_courses(
                st.session_state.user_id
            )


            if notice_courses:

                notice_course = st.selectbox(
                    "Course",
                    notice_courses,
                    format_func=lambda x: x["Course Name"],
                    key="notice_course"
                )

            else:

                notice_course = None

                st.warning(
                    "No courses are currently assigned to you."
                )


            # --------------------------------------------------
            # NOTICE TYPE
            # --------------------------------------------------

            notice_type = st.selectbox(
                "Notice Type",
                [
                    "General Notice",
                    "Vacation Notice",
                    "Holiday Notice",
                    "Exam Notice",
                    "Deadline Reminder",
                    "Class Announcement",
                    "Important Information"
                ],
                key="notice_type"
            )


            # --------------------------------------------------
            # NOTICE TITLE
            # --------------------------------------------------

            notice_title = st.text_input(
                "Notice Title",
                placeholder="Example: Vacation Ending Soon",
                key="notice_title"
            )


            # --------------------------------------------------
            # MESSAGE
            # --------------------------------------------------

            notice_message = st.text_area(
                "Message",
                placeholder="Write the announcement...",
                height=180,
                key="notice_message"
            )


            # --------------------------------------------------
            # DATES
            # --------------------------------------------------

            col1, col2 = st.columns(2)


            with col1:

                notice_date = st.date_input(
                    "Published Date",
                    key="notice_date"
                )


            with col2:

                notice_expiry = st.date_input(
                    "Expiry Date",
                    key="notice_expiry"
                )


            # --------------------------------------------------
            # FILE
            # --------------------------------------------------

            notice_file = st.file_uploader(
                "Attachment",
                type=[
                    "pdf",
                    "doc",
                    "docx",
                    "jpg",
                    "jpeg",
                    "png"
                ],
                key="teacher_notice_file"
            )


            if notice_file:

                st.success(
                    f"File attached: {notice_file.name}"
                )


            st.divider()


            # --------------------------------------------------
            # PUBLISH NOTICE
            # --------------------------------------------------

            if st.button(
                "Publish Notice",
                use_container_width=True,
                type="primary",
                key="publish_notice_btn"
            ):

                if notice_course is None:

                    st.warning(
                        "Please select a course."
                    )

                elif not notice_title.strip():

                    st.warning(
                        "Please enter a notice title."
                    )

                elif not notice_message.strip():

                    st.warning(
                        "Please enter the notice message."
                    )

                elif notice_expiry < notice_date:

                    st.error(
                        "Expiry date cannot be before published date."
                    )

                else:

                    result = add_notice(
                        notice_course["Course ID"],
                        notice_title,
                        notice_message,
                        notice_type,
                        notice_expiry,
                        notice_file.name
                        if notice_file
                        else None,
                        st.session_state.user_id
                    )


                    if result:

                        st.success(
                            "Notice published successfully."
                        )

                    else:

                        st.error(
                            "Unable to publish notice."
                        )


    # ==========================================================
    # PUBLISHED WORK
    # ==========================================================

    with published_tab:

        st.subheader(
            "Published Work"
        )

        st.caption(
            "Manage assignments, homework and projects created by you."
        )


        # ======================================================
        # GET ASSIGNMENTS
        # ======================================================

        assignments = get_teacher_assignments(
            st.session_state.user_id
        )


        if assignments:

            for assignment in assignments:

                assignment_id = assignment["Assignment ID"]


                # ==================================================
                # ASSIGNMENT CARD
                # ==================================================

                with st.container(border=True):

                    col1, col2, col3 = st.columns(
                        [5, 1, 1]
                    )


                    # --------------------------------------------------
                    # DETAILS
                    # --------------------------------------------------

                    with col1:

                        st.subheader(
                            assignment["Title"]
                        )

                        st.caption(
                            f"Course: {assignment['Course']}"
                        )

                        st.write(
                            assignment["Description"]
                            if assignment["Description"]
                            else "No description provided."
                        )

                        st.write(
                            f"Type: {assignment['Type']}"
                        )

                        st.write(
                            f"Due Date: {assignment['Due Date']}"
                        )


                        if assignment["File"]:

                            st.caption(
                                f"Attached file: {assignment['File']}"
                            )


                    # --------------------------------------------------
                    # EDIT BUTTON
                    # --------------------------------------------------

                    with col2:

                        edit_clicked = st.button(
                            "Edit",
                            key=f"edit_{assignment_id}",
                            use_container_width=True
                        )


                    # --------------------------------------------------
                    # DELETE BUTTON
                    # --------------------------------------------------

                    with col3:

                        delete_clicked = st.button(
                            "Delete",
                            key=f"delete_{assignment_id}",
                            use_container_width=True
                        )


                    # ==================================================
                    # OPEN EDIT MODE
                    # ==================================================

                    if edit_clicked:

                        st.session_state[
                            f"editing_{assignment_id}"
                        ] = True


                    # ==================================================
                    # EDIT FORM
                    # ==================================================

                    if st.session_state.get(
                        f"editing_{assignment_id}",
                        False
                    ):

                        st.divider()

                        st.subheader(
                            "Edit Academic Work"
                        )


                        edit_title = st.text_input(
                            "Title",
                            value=assignment["Title"],
                            key=f"title_{assignment_id}"
                        )


                        edit_description = st.text_area(
                            "Description",
                            value=assignment["Description"] or "",
                            height=150,
                            key=f"description_{assignment_id}"
                        )


                        work_types = [
                            "Assignment",
                            "Homework",
                            "Project"
                        ]


                        current_type = assignment["Type"]


                        if current_type not in work_types:

                            current_type = "Assignment"


                        edit_type = st.selectbox(
                            "Work Type",
                            work_types,
                            index=work_types.index(
                                current_type
                            ),
                            key=f"type_{assignment_id}"
                        )


                        edit_due_date = st.date_input(
                            "Due Date",
                            value=assignment["Due Date"],
                            key=f"due_{assignment_id}"
                        )


                        edit_file = st.file_uploader(
                            "Replace File (Optional)",
                            type=[
                                "pdf",
                                "doc",
                                "docx",
                                "ppt",
                                "pptx",
                                "xls",
                                "xlsx",
                                "zip"
                            ],
                            key=f"file_{assignment_id}"
                        )


                        save_col, cancel_col = st.columns(2)


                        # --------------------------------------------------
                        # SAVE
                        # --------------------------------------------------

                        with save_col:

                            if st.button(
                                "Save Changes",
                                type="primary",
                                use_container_width=True,
                                key=f"save_{assignment_id}"
                            ):

                                if not edit_title.strip():

                                    st.warning(
                                        "Title cannot be empty."
                                    )

                                else:

                                    result = update_assignment(
                                        assignment_id,
                                        edit_title,
                                        edit_description,
                                        edit_due_date,
                                        edit_file,
                                        edit_type
                                    )


                                    if result:

                                        st.success(
                                            "Academic work updated successfully."
                                        )

                                        st.session_state[
                                            f"editing_{assignment_id}"
                                        ] = False

                                        st.rerun()

                                    else:

                                        st.error(
                                            "Unable to update academic work."
                                        )


                        # --------------------------------------------------
                        # CANCEL
                        # --------------------------------------------------

                        with cancel_col:

                            if st.button(
                                "Cancel",
                                use_container_width=True,
                                key=f"cancel_{assignment_id}"
                            ):

                                st.session_state[
                                    f"editing_{assignment_id}"
                                ] = False

                                st.rerun()


                    # ==================================================
                    # DELETE BUTTON LOGIC
                    # ==================================================

                    if delete_clicked:

                        st.session_state[
                            f"confirm_delete_{assignment_id}"
                        ] = True


                    # ==================================================
                    # DELETE CONFIRMATION
                    # ==================================================

                    if st.session_state.get(
                        f"confirm_delete_{assignment_id}",
                        False
                    ):

                        st.warning(
                            "Are you sure you want to delete this academic work?"
                        )


                        confirm_col, cancel_col = st.columns(2)


                        # --------------------------------------------------
                        # CONFIRM DELETE
                        # --------------------------------------------------

                        with confirm_col:

                            if st.button(
                                "Yes, Delete",
                                type="primary",
                                use_container_width=True,
                                key=f"confirm_{assignment_id}"
                            ):

                                result = delete_assignment(
                                    assignment_id
                                )


                                if result:

                                    st.success(
                                        "Academic work deleted successfully."
                                    )

                                    st.session_state[
                                        f"confirm_delete_{assignment_id}"
                                    ] = False

                                    st.rerun()

                                else:

                                    st.error(
                                        "Unable to delete academic work."
                                    )


                        # --------------------------------------------------
                        # CANCEL DELETE
                        # --------------------------------------------------

                        with cancel_col:

                            if st.button(
                                "Cancel",
                                use_container_width=True,
                                key=f"cancel_delete_{assignment_id}"
                            ):

                                st.session_state[
                                    f"confirm_delete_{assignment_id}"
                                ] = False

                                st.rerun()


        else:

            st.info(
                "No academic work has been published yet."
            )


        # ==========================================================
        # PUBLISHED NOTICES
        # ==========================================================

        st.divider()

        st.subheader(
            "Published Notices"
        )

        st.caption(
            "Manage notices and announcements published for students."
        )


        notices = get_teacher_notices(
            st.session_state.user_id
        )


        if notices:

            for notice in notices:

                notice_id = notice["notice_id"]


                # ==================================================
                # NOTICE CARD
                # ==================================================

                with st.container(border=True):

                    col1, col2, col3 = st.columns(
                        [5, 1, 1]
                    )


                    # --------------------------------------------------
                    # DETAILS
                    # --------------------------------------------------

                    with col1:

                        st.subheader(
                            notice["title"]
                        )

                        st.caption(
                            f"{notice['notice_type']} • "
                            f"{notice['course']}"
                        )

                        st.write(
                            notice["message"]
                            if notice["message"]
                            else "No description provided."
                        )

                        st.caption(
                            f"Expiry: {notice['expiry_date']}"
                        )


                    # --------------------------------------------------
                    # EDIT BUTTON
                    # --------------------------------------------------

                    with col2:

                        edit_notice_clicked = st.button(
                            "Edit",
                            key=f"edit_notice_{notice_id}",
                            use_container_width=True
                        )


                    # --------------------------------------------------
                    # DELETE BUTTON
                    # --------------------------------------------------

                    with col3:

                        delete_notice_clicked = st.button(
                            "Delete",
                            key=f"delete_notice_{notice_id}",
                            use_container_width=True
                        )


                    # ==================================================
                    # OPEN NOTICE EDIT MODE
                    # ==================================================

                    if edit_notice_clicked:

                        st.session_state[
                            f"editing_notice_{notice_id}"
                        ] = True


                    # ==================================================
                    # NOTICE EDIT FORM
                    # ==================================================

                    if st.session_state.get(
                        f"editing_notice_{notice_id}",
                        False
                    ):

                        st.divider()

                        st.subheader(
                            "Edit Notice"
                        )


                        # --------------------------------------------------
                        # COURSE
                        # --------------------------------------------------

                        teacher_courses = get_teacher_courses(
                            st.session_state.user_id
                        )


                        if teacher_courses:

                            course_names = [
                                c["Course Name"]
                                for c in teacher_courses
                            ]


                            current_course = notice["course"]


                            if current_course in course_names:

                                course_index = course_names.index(
                                    current_course
                                )

                            else:

                                course_index = 0


                            edit_course = st.selectbox(
                                "Course",
                                teacher_courses,
                                index=course_index,
                                format_func=lambda x: x["Course Name"],
                                key=f"notice_course_{notice_id}"
                            )

                        else:

                            edit_course = None

                            st.warning(
                                "No courses are assigned to you."
                            )


                        # --------------------------------------------------
                        # NOTICE TYPE
                        # --------------------------------------------------

                        notice_types = [
                            "General Notice",
                            "Vacation Notice",
                            "Holiday Notice",
                            "Exam Notice",
                            "Deadline Reminder",
                            "Class Announcement",
                            "Important Information"
                        ]


                        current_type = notice["notice_type"]


                        if current_type in notice_types:

                            type_index = notice_types.index(
                                current_type
                            )

                        else:

                            type_index = 0


                        edit_notice_type = st.selectbox(
                            "Notice Type",
                            notice_types,
                            index=type_index,
                            key=f"notice_type_{notice_id}"
                        )


                        # --------------------------------------------------
                        # TITLE
                        # --------------------------------------------------

                        edit_notice_title = st.text_input(
                            "Notice Title",
                            value=notice["title"],
                            key=f"notice_title_{notice_id}"
                        )


                        # --------------------------------------------------
                        # MESSAGE
                        # --------------------------------------------------

                        edit_notice_description = st.text_area(
                            "Message",
                            value=notice["message"] or "",
                            height=150,
                            key=f"notice_description_{notice_id}"
                        )


                        # --------------------------------------------------
                        # EXPIRY DATE
                        # --------------------------------------------------

                        edit_notice_expiry = st.date_input(
                            "Expiry Date",
                            value=notice["expiry_date"],
                            key=f"notice_expiry_{notice_id}"
                        )


                        # --------------------------------------------------
                        # FILE
                        # --------------------------------------------------

                        edit_notice_file = st.file_uploader(
                            "Replace Attachment (Optional)",
                            type=[
                                "pdf",
                                "doc",
                                "docx",
                                "jpg",
                                "jpeg",
                                "png"
                            ],
                            key=f"notice_file_{notice_id}"
                        )


                        save_col, cancel_col = st.columns(2)


                        # ==================================================
                        # SAVE NOTICE
                        # ==================================================

                        with save_col:

                            if st.button(
                                "Save Changes",
                                type="primary",
                                use_container_width=True,
                                key=f"save_notice_{notice_id}"
                            ):

                                if edit_course is None:

                                    st.warning(
                                        "Please select a course."
                                    )

                                elif not edit_notice_title.strip():

                                    st.warning(
                                        "Please enter a notice title."
                                    )

                                elif not edit_notice_description.strip():

                                    st.warning(
                                        "Please enter a notice message."
                                    )

                                elif (
                                    edit_notice_expiry
                                    < notice["created_at"].date()
                                    if hasattr(
                                        notice["created_at"],
                                        "date"
                                    )
                                    else False
                                ):

                                    st.error(
                                        "Expiry date cannot be before the published date."
                                    )

                                else:

                                    result = update_notice(
                                        notice_id,
                                        edit_course["Course ID"],
                                        edit_notice_title,
                                        edit_notice_description,
                                        edit_notice_type,
                                        edit_notice_expiry,
                                        (
                                            edit_notice_file.name
                                            if edit_notice_file
                                            else None
                                        )
                                    )


                                    if result:

                                        st.success(
                                            "Notice updated successfully."
                                        )

                                        st.session_state[
                                            f"editing_notice_{notice_id}"
                                        ] = False

                                        st.rerun()

                                    else:

                                        st.error(
                                            "Unable to update notice."
                                        )


                        # ==================================================
                        # CANCEL NOTICE EDIT
                        # ==================================================

                        with cancel_col:

                            if st.button(
                                "Cancel",
                                use_container_width=True,
                                key=f"cancel_notice_{notice_id}"
                            ):

                                st.session_state[
                                    f"editing_notice_{notice_id}"
                                ] = False

                                st.rerun()


                    # ==================================================
                    # DELETE NOTICE
                    # ==================================================

                    if delete_notice_clicked:

                        st.session_state[
                            f"confirm_delete_notice_{notice_id}"
                        ] = True


                    # ==================================================
                    # DELETE NOTICE CONFIRMATION
                    # ==================================================

                    if st.session_state.get(
                        f"confirm_delete_notice_{notice_id}",
                        False
                    ):

                        st.warning(
                            "Are you sure you want to delete this notice?"
                        )


                        confirm_col, cancel_col = st.columns(2)


                        # --------------------------------------------------
                        # CONFIRM
                        # --------------------------------------------------

                        with confirm_col:

                            if st.button(
                                "Yes, Delete",
                                type="primary",
                                use_container_width=True,
                                key=f"confirm_delete_notice_{notice_id}"
                            ):

                                result = delete_notice(
                                    notice_id
                                )


                                if result:

                                    st.success(
                                        "Notice deleted successfully."
                                    )

                                    st.session_state[
                                        f"confirm_delete_notice_{notice_id}"
                                    ] = False

                                    st.rerun()

                                else:

                                    st.error(
                                        "Unable to delete notice."
                                    )


                        # --------------------------------------------------
                        # CANCEL
                        # --------------------------------------------------

                        with cancel_col:

                            if st.button(
                                "Cancel",
                                use_container_width=True,
                                key=f"cancel_delete_notice_{notice_id}"
                            ):

                                st.session_state[
                                    f"confirm_delete_notice_{notice_id}"
                                ] = False

                                st.rerun()


        else:

            st.info(
                "No notices have been published yet."
            )






























        # profile
# =========================================================================================

def teacher_profile():

    st.title("My Profile")
    st.divider()

    # Replace these values with database data
    teacher = get_teacher_profile(
        st.session_state.user_id
)
    col1, col2 = st.columns(2)

    with col1:
        st.text_input("Teacher Name", teacher["teacher_name"], disabled=True)
        st.text_input("Employee ID", teacher["employee_id"], disabled=True)
        st.text_input("Department", teacher["department"], disabled=True)
        st.text_input("Designation", teacher["designation"], disabled=True)
        st.text_input("Qualification", teacher["qualification"], disabled=True)
        st.text_input("Experience", teacher["experience"], disabled=True)

    with col2:
        st.text_input("Email", teacher["email"], disabled=True)
        st.text_input("Phone", teacher["phone"], disabled=True)
        st.text_input("Gender", teacher["gender"], disabled=True)
        st.text_input("Date of Birth", teacher["date_of_birth"], disabled=True)
        st.text_input("Joining Date", teacher["joining_date"], disabled=True)
        st.text_input("Employment Type", teacher["employment_type"], disabled=True)
        st.text_input("University", teacher["university"], disabled=True)

    st.text_area(
        "Address",
        teacher["address"],
        disabled=True,
        height=80
    )

    st.divider()

    if st.button("Change Password", use_container_width=True):
        st.info("Password change feature will be available soon.")















def show_selected_student(student_id):

    st.subheader("Student Profile")

    student = get_student_by_id(student_id)


    if not student:

        st.warning("Student details not found.")

        return



    # Profile Layout

    col1, col2 = st.columns([1,3])


    with col1:

        if student.get("photo"):

            st.image(
                student["photo"],
                width=120
            )

        else:

            st.info("No Photo")



    with col2:

        st.markdown(
            f"""
            ## {student.get('name','N/A')}

            **Roll Number:** {student.get('roll_no','N/A')}

            **Enrollment Number:** {student.get('enrollment_no','N/A')}

            **Department:** {student.get('department','N/A')}

            **Semester:** {student.get('semester','N/A')}
            """
        )


    st.divider()



    # More Details

    c1,c2,c3 = st.columns(3)


    with c1:

        st.metric(
            "Gender",
            student.get(
                "gender",
                "-"
            )
        )


    with c2:

        st.metric(
            "Status",
            student.get(
                "status",
                "-"
            )
        )


    with c3:

        st.metric(
            "Account",
            student.get(
                "account_status",
                "-"
            )
        )



    st.divider()



    st.subheader("Academic Information")


    st.write(
        {
            "Course":
            student.get("course_name","-"),

            "Semester":
            student.get("semester","-"),

            "Enrollment":
            student.get("enrollment_no","-")
        }
    )


















def assign_course_page():

    st.subheader("Assign Course to Teacher")

    teachers = get_all_teachers()
    courses = get_all_courses()

    if not teachers:
        st.error("No Teacher Found")
        return

    if not courses:
        st.error("No Course Found")
        return

    teacher = st.selectbox(
        "Teacher",
        teachers,
        format_func=lambda x: x[1]
    )

    course = st.selectbox(
        "Course",
        courses,
        format_func=lambda x: x[1]
    )

    semester = st.selectbox(
        "Semester",
        [1, 2, 3, 4, 5, 6, 7, 8]
    )

    session = st.text_input(
        "Session",
        "2026-27"
    )

    if st.button("Assign Course"):

        teacher_id = teacher[0]
        course_id = course[0]

        try:

            # =====================================
            # 1. Update course teacher
            # =====================================

            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                UPDATE courses
                SET teacher_id = %s
                WHERE course_id = %s
            """, (
                teacher_id,
                course_id
            ))

            conn.commit()

            cur.close()
            conn.close()

            # =====================================
            # 2. Save teacher-course assignment
            # =====================================

            assign_course(
                teacher_id,
                course_id,
                semester,
                session
            )

            st.success(
                f"Course assigned successfully to Semester {semester}"
            )

        except Exception as e:

            st.error(
                f"Error while assigning course: {e}"
            )