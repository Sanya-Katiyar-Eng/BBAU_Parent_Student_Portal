import streamlit as st
from auth.login import login_user , add_bg_gif
from dashboard.admin import admin_dashboard
from dashboard.student import student_dashboard,student_profile_form
from database.student_db import get_registration_status,save_student_profile

add_bg_gif()




#from dashboard.parent import parent_dashboard


import streamlit as st

# =========================================
# Imports
# =========================================

from auth.login import login_user, add_bg_gif
from auth.login import set_new_password

from dashboard.admin import admin_dashboard
from dashboard.student import student_dashboard
from dashboard.parent import parent_dashboard

from dashboard.student import student_profile_form

from database.student_db import get_registration_status


# =========================================
# Page Config
# =========================================

st.set_page_config(
    page_title="BBAU Student Parent Portal",
    page_icon="🎓",
    layout="wide"
)

add_bg_gif()


# =========================================
# Session State Initialization
# =========================================

defaults = {
    "logged_in": False,
    "user_id": None,
    "role": None,
    "first_login": False
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# =========================================
# Login Screen
# =========================================

def show_login_page():

    left, center, right = st.columns([2,1,2])

    with center:

        st.image(
            "images/bbau logo.jpg",
            width=180
        )

        st.markdown(
        """
        <h2 style="text-align:center;color:#0B5ED7;">
        BBAU Student Parent Portal
        </h2>
        """,
        unsafe_allow_html=True
        )

        role = st.selectbox(
            "Login As",
            [
                "Admin",
                "Student",
                "Parent"
            ]
        )

        # -------------------------
        # Dynamic Username Field
        # -------------------------

        if role == "Admin":

            login_username = st.text_input(
                "Email"
            )

        elif role == "Student":

            login_username = st.text_input(
                "Enrollment Number"
            )

        else:

            login_username = st.text_input(
                "Parent Mobile Number"
            )

        password = st.text_input(
            "Password",
            type="password"
        )

        # -------------------------
        # Login Button
        # -------------------------

        if st.button(
            "Login",
            use_container_width=True
        ):

            user = login_user(
                role,
                login_username,
                password
            )

            if user["success"]:

                st.session_state.logged_in = True
                st.session_state.user_id = user["user_id"]
                st.session_state.role = user["role"]
                st.session_state.first_login = user["first_login"]

                st.rerun()

            else:

                st.error(
                    user["message"]
                )


# =========================================
# Dashboard Routing
# =========================================

def route_user():

    # -----------------------------------
    # First Login Password Setup
    # -----------------------------------

    if st.session_state.first_login:

        set_new_password(
            st.session_state.user_id
        )

        return

    # -----------------------------------
    # Admin
    # -----------------------------------

    if st.session_state.role == "admin":

        admin_dashboard()

        return

    # -----------------------------------
    # Student
    # -----------------------------------

    if st.session_state.role == "student":

        registration_status = (
            get_registration_status(
                st.session_state.user_id
            )
        )

        if registration_status == "Pending":

            student_profile_form()

        else:

            student_dashboard()

        return

    # -----------------------------------
    # Parent
    # -----------------------------------

    if st.session_state.role == "parent":

        parent_dashboard()

        return

    st.error("Invalid Role")


# =========================================
# Main App
# =========================================

if not st.session_state.logged_in:

    show_login_page()

else:

    route_user()