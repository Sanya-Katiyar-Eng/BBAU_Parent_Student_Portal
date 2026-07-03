import streamlit as st
from database.student_db import add_student

def student_page():

    st.title("👨‍🎓 Student Management")

    if "show_add_form" not in st.session_state:
        st.session_state.show_add_form = False


    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("➕ Add Student", use_container_width=True):
            st.session_state.show_add_form = True

    with c2:
        st.button("📋 View Students", use_container_width=True)

    with c3:
        st.button("🗑 Delete Student", use_container_width=True)


    if st.session_state.show_add_form:

        with st.form("student_form"):

            name = st.text_input("Name")

            email = st.text_input("Email")

            password = st.text_input("Password", type="password")

            roll = st.text_input("Roll Number")

            enrollment = st.text_input("Enrollment Number")

            department = st.selectbox(
            "Department",
            [
                "Computer Science",
                "Management",
                "Commerce"
            ]
        )

            semester = st.selectbox(
            "Semester",
            [1,2,3,4,5,6,7,8]
        )

            gender = st.radio(
            "Gender",
            ["Male","Female","Other"]
        )

            dob = st.date_input("DOB")

            phone = st.text_input("Phone")

            parent = st.text_input("Parent Email")

            address = st.text_area("Address")

            photo = st.file_uploader(
            "Photo",
            type=["jpg","png","jpeg"]
        )

            submit = st.form_submit_button("Save Student")

            if submit:

                user_data = {
                "name": name,
                "email": email,
                "password": password
            }

                student_data = {
                "roll_no": roll,
                "enrollment_no": enrollment,
                "department": department,
                "semester": semester,
                "gender": gender,
                "dob": dob,
                "phone": phone,
                "parent_email": parent,
                "address": address,
                "photo": photo.name if photo else None
            }

                success = add_student(user_data, student_data)

                if success:
                    st.success("✅ Student Added Successfully")
                    st.session_state.show_add_form = False
                    st.rerun()

                else:
                    st.error("❌ Unable to Add Student")