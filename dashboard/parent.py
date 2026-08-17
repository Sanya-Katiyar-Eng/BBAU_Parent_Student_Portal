import streamlit as st
import pandas as pd
import re

from database.parent_db import (

    get_students_for_dropdown,
    get_student_by_id,

    add_parent,
    get_all_parents,
    get_parent_by_id,
    update_parent,
    delete_parent,

    search_parent,
    filter_parents,

    check_parent_phone,
    check_parent_email,
    check_student_parent_exists,

    count_total_parents,
    count_active_parents,
    count_inactive_parents
)


#===========================================================================================
from database.db import get_connection



'''def parent_login(phone,password):


    conn=get_connection()

    cur=conn.cursor()


    cur.execute(
    """
    SELECT 
    parent_id,
    student_id

    FROM parents

    WHERE phone=%s
    AND status='Active'
    """,

    (phone,)

    )


    parent=cur.fetchone()


    cur.close()

    conn.close()



    if parent:

        return parent


    return None'''

from database.db import get_connection
from werkzeug.security import check_password_hash


from database.db import get_connection
from werkzeug.security import check_password_hash

#parent login
def parent_login(roll_no, password):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            u.id AS user_id,
            p.student_id,
            u.password,
            u.first_login
        FROM users u
        JOIN parents p
            ON p.user_id = u.id
        JOIN students s
            ON s.student_id = p.student_id
        WHERE u.login_username = %s
          AND u.role = 'parent'
          AND LOWER(u.account_status) = 'active'
          AND s.roll_number = %s
        """,
        (
            str(roll_no).strip(),
            str(roll_no).strip()
        )
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        return None

    user_id, student_id, stored_password, first_login = user

    if not check_password_hash(stored_password, password):
        return None

    return {
        "user_id": user_id,
        "student_id": student_id,
        "first_login": first_login
    }
















#===========================================================================
# ==========================================================
# MAIN PARENT MANAGEMENT PAGE
# ==========================================================

def parent_page():

    st.title("Parent Management")


    parent_dashboard_cards()


    st.divider()


    tab1, tab2, tab3= st.tabs(
        [
            " View Parents",
            " Update Parent",
            " Delete Parent"
        ]
    )


   

    with tab1:
        view_parent_tab()


    with tab2:
        update_parent_tab()


    with tab3:
        delete_parent_tab()











# ==========================================================
# DASHBOARD CARDS
# ==========================================================

def parent_dashboard_cards():


    total = count_total_parents()

    active = count_active_parents()

    inactive = count_inactive_parents()



    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Total Parents",
            total
        )


    with col2:

        st.metric(
            "Active Parents",
            active
        )


    with col3:

        st.metric(
            "Inactive Parents",
            inactive
        )



# ==========================================================
# ADD PARENT FORM
# ==========================================================


def parent_registration_form():


    st.subheader(" Register Parent")


    students = get_students_for_dropdown()


    if not students:

        st.warning(
            "No students available"
        )

        return



    student_options = {

        label:student_id

        for student_id,label in students

    }



    selected_student = st.selectbox(

        "Select Student",

        list(student_options.keys())

    )



    student_id = student_options[selected_student]



    student = get_student_by_id(student_id)



    if student:


        st.info(
f"""
Student Name : {student[2]}

Enrollment No : {student[1]}

Department : {student[3]}

Semester : {student[4]}
"""
        )



    st.divider()



    father_name = st.text_input(
        "Father Name"
    )


    mother_name = st.text_input(
        "Mother Name"
    )


    occupation = st.text_input(
        "Occupation"
    )


    phone = st.text_input(
        "Phone Number"
    )


    email = st.text_input(
        "Email"
    )


    address = st.text_area(
        "Address"
    )


    password = st.text_input(

        "Temporary Password",

        value="Parent@123",

        type="password"

    )



    if st.button("Save Parent"):



        if check_student_parent_exists(student_id):

            st.error(
                "Parent already exists for this student"
            )

            return



        if check_parent_phone(phone):

            st.error(
                "Phone number already exists"
            )

            return



        if check_parent_email(email):

            st.error(
                "Email already exists"
            )

            return




        parent_data = {


            "student_id":student_id,

            "father_name":father_name,

            "mother_name":mother_name,

            "occupation":occupation,

            "phone":phone,

            "email":email,

            "address":address,

            "password":password


        }




        success,message = add_parent(
            parent_data
        )



        if success:

            st.success(message)

            st.rerun()


        else:

            st.error(message)





# ==========================================================
# VIEW PARENT TAB
# ==========================================================


def view_parent_tab():


    st.subheader(
        "👀 View Parents"
    )


    keyword = parent_search_bar()



    col1,col2,col3 = st.columns(3)



    with col1:

        department = st.selectbox(

            "Department",

            [
                "",
                "BCA",
                "B.Tech",
                "MBA",
                "MCA"
            ]

        )



    with col2:

        semester = st.selectbox(

            "Semester",

            [
                "",
                1,2,3,4,5,6,7,8
            ]

        )



    with col3:

        relation = st.selectbox(

            "Relation",

            [
                "",
                "Father",
                "Mother"
            ]

        )




    if keyword:


        parents = search_parent(
            keyword
        )



    elif department or semester or relation:


        parents = filter_parents(

            department,

            semester,

            relation

        )



    else:


        parents = get_all_parents()



    show_parent_table(
        parents
    )





# ==========================================================
# SEARCH BAR
# ==========================================================


def parent_search_bar():


    keyword = st.text_input(

        "🔍 Search Parent",

        placeholder=
        "Father Name, Mother Name, Student Name, Phone"

    )


    return keyword.strip()





# ==========================================================
# SHOW PARENT TABLE
# ==========================================================


def show_parent_table(parents):


    if not parents:


        st.warning(
            "No parent records found"
        )

        return




    columns=[


        "Parent ID",

        "Father Name",

        "Mother Name",

        "Phone",

        "Email",

        "Occupation",

        "Status",

        "Student ID",

        "Enrollment No",

        "Student Name",

        "Department",

        "Semester"

    ]




    df = pd.DataFrame(

        parents,

        columns=columns

    )



    st.dataframe(

        df,

        use_container_width=True,

        hide_index=True

    )


    st.success(

        f"Total Records : {len(df)}"

    )


# ==========================================================
# UPDATE PARENT TAB
# ==========================================================


def update_parent_tab():


    st.subheader(
        "✏ Update Parent"
    )


    parents = get_all_parents()



    if not parents:

        st.warning(
            "No parent records found"
        )

        return



    parent_options = {


        f"{p[0]} - {p[1]} ({p[9]})":p[0]


        for p in parents

    }



    selected_parent = st.selectbox(

        "Select Parent",

        list(parent_options.keys())

    )



    parent_id = parent_options[selected_parent]



    parent_edit_form(
        parent_id
    )





# ==========================================================
# EDIT PARENT FORM
# ==========================================================


def parent_edit_form(parent_id):


    parent = get_parent_by_id(parent_id)



    if not parent:


        st.error(
            "Parent record not found"
        )

        return




    st.subheader(
        "✏ Edit Parent Details"
    )



    father_name = st.text_input(

        "Father Name",

        value=parent[2]

    )


    mother_name = st.text_input(

        "Mother Name",

        value=parent[3]

    )


    occupation = st.text_input(

        "Occupation",

        value=parent[4]

    )


    phone = st.text_input(

        "Phone",

        value=parent[5]

    )


    email = st.text_input(

        "Email",

        value=parent[6]

    )


    address = st.text_area(

        "Address",

        value=parent[7]

    )


    status = st.selectbox(

        "Status",

        [
            "Active",
            "Inactive"
        ],

        index=0 if parent[8]=="Active" else 1

    )




    if st.button(
        "Update Parent"
    ):



        if check_parent_phone(phone) and phone != parent[5]:


            st.error(
                "Phone already exists"
            )

            return




        if check_parent_email(email) and email != parent[6]:


            st.error(
                "Email already exists"
            )

            return




        parent_data = {


            "father_name":father_name,

            "mother_name":mother_name,

            "occupation":occupation,

            "phone":phone,

            "email":email,

            "address":address,

            "status":status,

            "old_phone":parent[5]


        }



        success,message = update_parent(

            parent_id,

            parent_data

        )



        if success:

            st.success(message)

            st.rerun()



        else:

            st.error(message)






# ==========================================================
# DELETE PARENT TAB
# ==========================================================


def delete_parent_tab():


    st.subheader(
        "🗑 Delete Parent"
    )



    parents = get_all_parents()



    if not parents:


        st.warning(
            "No parent records found"
        )

        return




    parent_options = {


        f"{p[0]} - {p[1]} ({p[9]})":p[0]


        for p in parents

    }




    selected_parent = st.selectbox(
    "Select Parent",
    options=list(parent_options.keys()),
    key="delete_parent_selectbox"
)


    parent_id = parent_options[selected_parent]



    confirm_delete_parent(
        parent_id
    )






# ==========================================================
# CONFIRM DELETE
# ==========================================================


def confirm_delete_parent(parent_id):


    parent = get_parent_by_id(parent_id)



    if not parent:


        st.error(
            "Parent not found"
        )

        return




    st.warning(
        "⚠ This action cannot be undone"
    )



    st.write(
f"""
Father Name : {parent[2]}

Mother Name : {parent[3]}

Phone : {parent[5]}

Email : {parent[6]}
"""
    )



    confirm = st.checkbox(

        "I confirm delete"

    )



    if st.button(
        "Delete Parent",
        type="primary"
    ):



        if not confirm:


            st.warning(
                "Please confirm deletion"
            )

            return




        success,message = delete_parent(

            parent_id

        )



        if success:


            st.success(message)

            st.rerun()



        else:


            st.error(message)






# ==========================================================
# PARENT PROFILE
# ==========================================================


def show_parent_profile(parent_id):


    parent = get_parent_by_id(parent_id)



    if not parent:


        st.error(
            "Parent not found"
        )

        return



    st.subheader(
        " Parent Profile"
    )



    col1,col2 = st.columns(2)



    with col1:


        st.write(
            "### Parent Information"
        )


        st.write(
            f"Father Name : {parent[2]}"
        )


        st.write(
            f"Mother Name : {parent[3]}"
        )


        st.write(
            f"Occupation : {parent[4]}"
        )


        st.write(
            f"Phone : {parent[5]}"
        )


        st.write(
            f"Email : {parent[6]}"
        )


        st.write(
            f"Address : {parent[7]}"
        )




    with col2:


        st.write(
            "### Student Information"
        )


        st.write(
            f"Student Name : {parent[10]}"
        )


        st.write(
            f"Enrollment : {parent[9]}"
        )


        st.write(
            f"Department : {parent[11]}"
        )


        st.write(
            f"Semester : {parent[12]}"
        )






# ==========================================================
# EXPORT CSV
# ==========================================================


def export_parent_data():


    parents = get_all_parents()



    if not parents:


        st.warning(
            "No data available"
        )

        return




    columns=[


        "Parent ID",

        "Father Name",

        "Mother Name",

        "Phone",

        "Email",

        "Occupation",

        "Status",

        "Student ID",

        "Enrollment No",

        "Student Name",

        "Department",

        "Semester"

    ]




    df=pd.DataFrame(

        parents,

        columns=columns

    )




    csv=df.to_csv(

        index=False

    ).encode("utf-8")




    st.download_button(

        "📥 Export Parent Data",

        csv,

        "parent_data.csv",

        "text/csv"

    )







# ==========================================================
# VALIDATION
# ==========================================================


def validate_parent_form(data):


    if not data["father_name"].strip():

        return False,"Father name required"



    if not data["mother_name"].strip():

        return False,"Mother name required"



    phone=data["phone"]



    if not phone.isdigit():

        return False,"Invalid phone"



    if len(phone)!=10:

        return False,"Phone must be 10 digits"




    email=data["email"]


    pattern=r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'



    if not re.match(pattern,email):


        return False,"Invalid email"




    return True,"Valid"






# ==========================================================
# RESET FILTERS
# ==========================================================


def reset_parent_filters():


    keys=[

        "parent_search",

        "parent_department",

        "parent_semester"

    ]



    for key in keys:


        if key in st.session_state:


            st.session_state[key]=""






# ==========================================================
# CLEAR FORM
# ==========================================================


def clear_parent_form():


    fields=[

        "father_name",

        "mother_name",

        "occupation",

        "parent_phone",

        "parent_email",

        "parent_address"

    ]



    for field in fields:


        if field in st.session_state:


            st.session_state[field]=""






# ==========================================================
# REFRESH TABLE
# ==========================================================


def refresh_parent_table():
    pass




