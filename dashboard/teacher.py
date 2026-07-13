

import streamlit as st

from database.teacher_db import add_teacher,get_all_teachers,update_teacher
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

        st.subheader("✏️ Edit Teacher")

        teacher_name = st.text_input("Teacher Name")
        employee_id = st.text_input("Employee ID")
        department = st.text_input("Department")
        designation = st.text_input("Designation")
        email = st.text_input("Email")
        mobile = st.text_input("Mobile")
        qualification = st.text_input("Qualification")
        experience = st.number_input(
        "Experience (Years)",
        min_value=0,
        max_value=50,
        step=1
    )
        gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"]
    )
        address = st.text_area("Address")

        update_btn = st.form_submit_button("Update Teacher")

        if update_btn:
            edit_teacher = update_teacher(
        teacher_name=teacher_name,
        employee_id=employee_id,
        department=department,
        designation=designation,
        email=email,
        mobile=mobile,
        qualification=qualification,
        experience=experience,
        gender=gender,
        address=address,
    )

    if edit_teacher:
        st.success("Teacher updated successfully!")
    else:
        st.error("Failed to update teacher.")

    # =====================================================
    # DELETE
    # =====================================================

    with tab4:

        st.subheader("🗑 Delete Teacher")

        st.warning("Delete Teacher UI Coming Soon.")