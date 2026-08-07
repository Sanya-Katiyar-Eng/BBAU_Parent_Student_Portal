
import streamlit as st
from database.dashboard_db import get_parent_details

from database.notification_db import (
    send_parent_email,
    send_parent_sms
)
import pandas as pd
from io import BytesIO

from database.teacher_db import export_attendance
from database.teacher_db import get_attendance_analytics
from database.teacher_db import (
    get_attendance_for_edit,
    update_attendance
)
from database.teacher_db import get_attendance_by_date
from database.dashboard_db import get_students_by_course
from datetime import datetime
from database.teacher_db import add_teacher
# Teacher Database Functions
from database.teacher_db import (
    get_teacher_courses,
    update_teacher,
    search_teachers,
    delete_teacher
)
#from database.student_db import get_students_by_course

# Dashboard Database Functions
from database.dashboard_db import (
    get_all_courses,
    get_all_teachers
)
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

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Teachers", "0")

    with col2:
        st.metric("Active", "0")

    with col3:
        st.metric("Inactive", "0")

    with col4:
        st.metric("Departments", "0")

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
    "Teacher ID": teacher["teacher_id"],
    "Teacher Name": teacher["teacher_name"],
    "Employee ID": teacher["employee_id"],
    "Department": teacher["department"],
    "Designation": teacher["designation"],
    "Phone": teacher["phone"],
    "Email": teacher["email"],
    "Status": teacher["status"]
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

def teacher_dashboard():
    


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
        "Results",
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

        teacher_schedule()

    elif menu == "Attendance":

        teacher_attendance()



    elif menu == "Results":

        teacher_results()



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























def teacher_schedule():

    st.title("Schedule Class")

    teacher = get_teacher_profile(st.session_state.user_id)

    if teacher is None:
        st.error("Teacher profile not found")
        return


    teacher_id = teacher["teacher_id"]


    st.subheader("Create New Class")


    courses = get_teacher_courses(teacher_id)


    if not courses:
        st.warning("No courses assigned.")
        return


    course = st.selectbox(
        "Select Course",
        courses,
        format_func=lambda x: x["Course Name"]
    )


    day = st.selectbox(
        "Select Day",
        [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday"
        ]
    )


    start = st.time_input(
        "Start Time"
    )


    end = st.time_input(
        "End Time"
    )


    room = st.text_input(
        "Room Number"
    )


    if st.button("Schedule Class"):

        result = add_class_schedule(
            teacher_id,
            course["Course ID"],     # course_id
            day,
            start,
            end,
            room
        )


        if result:
            st.success("Class Scheduled Successfully")
        else:
            st.error("Failed")
























def teacher_home():

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
                    if row["status"]=="Absent":
                        parent=get_parent_details(
                            row["student_id"]
                        )
                        st.write("Parent Data:", parent)

                        if parent:
                            sms_result=send_parent_sms(
                                parent[0],
                                parent[2],
                                selected_course["Course Name"],
                                attendance_data
                            )
                            
                            st.write("SMS Status:", sms_result)
                            send_parent_email(
                                parent[1],
                                parent[2],
                                selected_course["Course Name"],
                                attendance_data
                            )

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
# ================================================================================
# assignments
# ========================================================================================= 
def teacher_assignments():

    st.title("Assignments")
    st.divider()

    tab1, tab2 = st.tabs(["Add Assignment", "View Assignments"])

    # ==========================
    # Add Assignment
    # ==========================
    with tab1:

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
                key="assignment_semester"
            )

        with col2:
            courses = get_teacher_courses(
                st.session_state.user_id
)

            course = st.selectbox(
    "Course",
    courses,
    format_func=lambda x: x["Course Name"]
)
        title = st.text_input("Assignment Title")

        description = st.text_area("Description")

        due_date = st.date_input("Due Date")

        uploaded_file = st.file_uploader(
            "Upload Assignment",
            type=["pdf", "doc", "docx"]
        )

        if st.button("Save Assignment", use_container_width=True):
            add_assignment(
                course["Course ID"],
                title,
                description,
                due_date,
                uploaded_file,
                st.session_state.user_id
            )

        st.success("Assignment saved successfully.")

    # ==========================
    # View Assignments
    # ==========================
    with tab2:

        assignments = get_assignments(
            st.session_state.user_id
)

        if assignments:

            st.dataframe(
                assignments,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("No assignments available.")


#================================================================================
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

    if teachers:
        teacher = st.selectbox(
        "Teacher",
        teachers,
        format_func=lambda x: x[1]
    )
    else:
        st.error("No Teacher Found")    
        
    course = st.selectbox(
        "Course",
        courses,
        format_func=lambda x: x[1]
    )

    semester = st.selectbox(
        "Semester",
        [1,2,3,4,5,6,7,8]
    )

    session = st.text_input(
        "Session",
        "2026-27"
    )

    if st.button("Assign Course"):

        teacher_id = teacher[0]
        course_id = course[0]

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        UPDATE courses
        SET teacher_id = %s
        WHERE course_id = %s
    """,(teacher_id,course_id))

        conn.commit()

        cur.close()
        conn.close()

        st.success("Course Assigned Successfully")