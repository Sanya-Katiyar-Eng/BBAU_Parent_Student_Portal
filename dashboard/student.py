import streamlit as st
import pandas as pd
from database.student_db import save_student_profile
from database.student_db import (
    add_student,
    get_all_students,
    get_student_dashboard_counts,
    delete_student,
       get_student_by_enrollment,
)
def student_page():

    st.title(" Student Management")

    if "show_add_form" not in st.session_state:
        st.session_state.show_add_form = False
    if "show_view_students" not in st.session_state:
        st.session_state.show_view_students = False
    if "show_delete_student" not in st.session_state:
        st.session_state.show_delete_student = False
    if "delete_student_data" not in st.session_state:
        st.session_state.delete_student_data = None
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button(" Add Student", use_container_width=True):
            st.session_state.show_add_form = True
            st.session_state.show_view_students = False

    with c2:
        if st.button(" View Students", use_container_width=True):
            st.session_state.show_view_students = True
            st.session_state.show_add_form = False

    with c3:
        if st.button("Delete Student", use_container_width=True):
            st.session_state.show_add_form = False
            st.session_state.show_view_students = False
            st.session_state.show_delete_student = True

    if st.session_state.show_add_form:

        st.subheader(" Add New Student")

        with st.form("add_student_form"):

            enrollment_no = st.text_input("Enrollment Number")
            roll_no = st.text_input("Roll Number")

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

            semester = st.selectbox(
        "Semester",
        [1,2,3,4,5,6,7,8]
    )

            submit = st.form_submit_button("Add Student")

        if submit:

            if not all([enrollment_no, roll_no]):
                st.error("Please fill all required fields.")

            else:

                success = add_student(
                roll_no=roll_no,
                enrollment_no=enrollment_no,
                department=department,
                semester=semester,
            )

                if success:
                    st.success("Student added successfully.")

                    #st.info(f"""
#Temporary Login

#Enrollment Number : {enrollmen
               # else:
                 #   st.error("Enrollment Number already exists.")


#======================================================================================
#view student
#===============================================================
    if st.session_state.show_view_students:

        st.subheader("View Students")
        total, completed, pending, active = get_student_dashboard_counts()

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(" Total Students", total)

        with c2:
            st.metric("✅ Completed", completed)

        with c3:
            st.metric("🟡 Pending", pending)

        with c4:
            st.metric("🟢 Active", active)
        search = st.text_input(" Search Student")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            department = st.selectbox(
        "Department",
        [
            "All",
            "Computer Science",
            "Information Technology",
            "Electronics",
            "Mechanical",
            "Civil",
            "Electrical"
        ]
    )
        with c2:
            semester = st.selectbox(
        "Semester",
        ["All",1,2,3,4,5,6,7,8]
    )
            
        with c3:
            registration = st.selectbox(
        "Registration",
        ["All","Pending","Completed"]
    )

        with c4:
            account = st.selectbox(
        "Account",
        ["All","Active","Inactive","Blocked"]
    )
        students = get_all_students(
    search,
    department,
    semester,
    registration,
    account
)

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
                "Registration",
                "Account Status"
            ]
        )

            st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No Students Found.")



#------------------------------------------
#delete student
#----------------------------------------------------
    if st.session_state.show_delete_student:

        st.subheader(" Delete Student")

        enrollment = st.text_input("Enrollment Number")

        c1,c2 = st.columns(2)

        with c1:

            if st.button("Search Student"):

                st.session_state.delete_student_data = \
                    get_student_by_enrollment(enrollment)

        student = st.session_state.delete_student_data

        if student:

            st.success("Student Found")

            st.write("### Student Details")

            st.write(f"**Enrollment :** {student[1]}")
            st.write(f"**Roll No :** {student[2]}")
            st.write(f"**Name :** {student[3]}")
            st.write(f"**Department :** {student[4]}")
            st.write(f"**Semester :** {student[5]}")
            st.write(f"**Registration :** {student[6]}")
            st.write(f"**Account :** {student[7]}")

            st.warning("This action cannot be undone.")

            confirm = st.checkbox(
            "I understand that this student will be permanently deleted."
        )

            if confirm:

                if st.button("Delete Student", type="primary"):

                    if delete_student(student[1]):

                        st.success("Student deleted successfully.")

                        st.session_state.delete_student_data = None

                        st.rerun()

                    else:

                        st.error("Unable to delete student.")

        elif enrollment:
            st.info("Search for a student to view details before deletion.")


#===========================================================================
#student dashboard
#===========================================================================
from streamlit_option_menu import option_menu
def student_dashboard():
    st.markdown("""
<style>
[data-testid="stSidebar"] {
    overflow-y: auto;
}

[data-testid="stSidebarContent"] {
    overflow-y: auto;
    height: 100vh;
}
</style>
""", unsafe_allow_html=True)
    with st.sidebar:

        st.image("images/bbau logo.jpg", width=120)

        st.markdown("## 🎓 Student Portal")
        st.caption("Welcome, Student")

        st.divider()

        selected = option_menu(
            menu_title=None,
            options=[
            "Dashboard",
            "My Profile",
            "My Courses",
            "Class Timetable",
            "Attendance",
            "Results",
            "Assignments",
            "Notices",
            "Messages",
            "Documents",
            "Settings"
        ],
            icons=[
            "house",
            "person-circle",
            "book",
            "calendar3",
            "clipboard-check",
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
                "background-color": "#D6DFF3",
            },
            "icon": {
                "font-size": "18px",
                "color": "#1F3A93",
            },
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "6px",
                "padding": "12px",
                "border-radius": "10px",
                "--hover-color": "#BFC7D4",
            },
            "nav-link-selected": {
                "background-color": "#0B5ED7",
                "color": "white",
            },
        },
    )

        st.divider()

        st.success("🟢 Account Active")

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()


#================================================================
#student form
#=================================================================
def student_profile_form():

    st.title("🎓 Complete Your Student Profile")
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

        st.subheader("👨 Parent Information")

        father_name = st.text_input("Father Name")

        mother_name = st.text_input("Mother Name")

        parent_phone = st.text_input("Parent Mobile Number")

        parent_email = st.text_input("Parent Email")

        occupation = st.text_input("Parent Occupation")

        st.subheader("📷 Student Photo")

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

            st.success("Profile Completed Successfully.")

            st.balloons()

            st.rerun()

    else:

        st.error("Unable to save profile.")

        