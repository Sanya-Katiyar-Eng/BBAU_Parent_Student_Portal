

import streamlit as st
from auth.login import normalize_text
from database.teacher_db import add_teacher,get_all_teachers,update_teacher,search_teachers,delete_teacher
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
            dob=st.date_input("Date of Birth")
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
    photo=photo)
                if success:
                    st.success("Teacher add Successfully")
                else:
                    st.error("Unable to add teacher")




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