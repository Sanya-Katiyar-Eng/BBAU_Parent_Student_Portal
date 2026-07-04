import streamlit as st
import pandas as pd
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

            password = st.text_input(
        "Temporary Password",
        type="password",
        help="Student will change this after first login."
    )

            submit = st.form_submit_button("Add Student")

        if submit:

            if not all([enrollment_no, roll_no, password]):
                st.error("Please fill all required fields.")

            else:

                success = add_student(
                roll_no=roll_no,
                enrollment_no=enrollment_no,
                department=department,
                semester=semester,
                password=password
            )

                if success:
                    st.success("Student added successfully.")
                else:
                    st.error("Enrollment Number already exists.")


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