import streamlit as st
from auth.login import login_user , add_bg_gif
from dashboard.admin import admin_dashboard



add_bg_gif()



#from dashboard.student import student_dashboard
#from dashboard.parent import parent_dashboard


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None


if not st.session_state.logged_in:

    st.set_page_config(layout="wide")

    left, center, right = st.columns([2,1,2])

    with center:

        st.image("images/bbau logo.jpg", width=180)

        st.markdown(
        """
        <h3 style="text-align:center;color:#0B5ED7;">
        BBAU Student Parent Portal
        </h3>
        """,
        unsafe_allow_html=True
        )

        role = st.selectbox(
            "Login As",
            ["Admin","Student","Parent"]
        )

        # Dynamic Username Field
        if role == "Admin":
            login_username = st.text_input("Email")

        elif role == "Student":
            login_username = st.text_input("Enrollment Number")

        elif role == "Parent":
            login_username = st.text_input("Parent Mobile Number")

        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):

            user_role = login_user(role, login_username, password)

            if user_role:

                st.session_state.logged_in = True
                st.session_state.user_id=user_role[0]
                st.session_state.role = user_role[1]
                st.rerun()
            else:
                st.error("Invalid Credentials")


else:

    if st.session_state.role.lower() == "admin":

        admin_dashboard()

    elif st.session_state.role.lower() == "student":

        # student_dashboard()
        st.write("Student Dashboard")

    elif st.session_state.role.lower() == "parent":

        # parent_dashboard()
        st.write("Parent Dashboard")

    else:

        st.error("Invalid Role")