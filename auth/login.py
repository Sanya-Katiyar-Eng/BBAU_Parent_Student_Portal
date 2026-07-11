from database.db import get_connection
from database.auth_db import (
    verify_login,
    verify_student,
    create_password
)
from auth.auth_service import authenticate_user

#===========================================
#use gif
#=============================================
import base64

def add_bg_gif():
    with open("images/bbau_watermark.gif", "rb") as f:
        data = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{
            background: url("data:image/gif;base64,{data}") center center;
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        .stApp::before {{
            content: "";
            position: fixed;
            inset: 0;
            background: rgba(255,255,255,0.55);   /* Opacity control */
            pointer-events: none;
            z-index: 0;
        }}

        .main, [data-testid="stAppViewContainer"] {{
            position: relative;
            z-index: 1;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )



 


import streamlit as st

from database.auth_db import (
    verify_login,
    verify_student,
    create_password
)


# ==========================================================
# Session State
# ==========================================================

if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"

if "activate_user_id" not in st.session_state:
    st.session_state.activate_user_id = None


# ==========================================================
# Login Screen
# ==========================================================

def show_login():

    st.image("images/bbau logo.jpg", width=170)

    st.markdown(
        """
        <h2 style='text-align:center;color:#0B5ED7'>
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

    # ------------------------------

    if role == "Admin":

        username = st.text_input("Email")

    elif role == "Student":

        username = st.text_input("Enrollment Number")

    else:

        username = st.text_input("Parent Mobile Number")

    password = st.text_input(
        "Password",
        type="password"
    )

    # ------------------------------

    if st.button(
        "Login",
        use_container_width=True
    ):

        user = verify_login(
            username,
            password,
            role
        )

        # --------------------------

        if user.get("first_login"):

            st.session_state.activate_user_id = user["user_id"]
            st.session_state.auth_page = "activate"

            st.rerun()
        elif user["success"]:

            st.session_state.logged_in = True
            st.session_state.user_id = user["user_id"]
            st.session_state.role = user["role"]

            st.rerun()

        # --------------------------


        else:

            st.error(user["message"])

    st.divider()

    st.caption("First time user? Activate your account.")

    if st.button(
        "Activate Account",
        use_container_width=True
    ):

        st.session_state.auth_page = "activate"

        st.rerun()


# ==========================================================
# Activate Account
# ==========================================================

def show_activate_account():

    st.title("Activate Account")

    enrollment = st.text_input(
        "Enrollment Number"
    )

    roll_no = st.text_input(
        "Roll Number"
    )

    if st.button(
        "Verify",
        use_container_width=True
    ):

        student = verify_student(
            enrollment,
            roll_no
        )

        if student:

            st.session_state.activate_user_id = student[0]
            st.session_state.auth_page = "password"

            st.rerun()

        else:

            st.error(
                "Enrollment Number or Roll Number is incorrect."
            )

    if st.button("Back"):

        st.session_state.auth_page = "login"

        st.rerun()


# ==========================================================
# Create Password
# ==========================================================

def show_create_password():

    st.title("Create Password")

    password = st.text_input(
        "New Password",
        type="password"
    )

    confirm = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button(
        "Save Password",
        use_container_width=True
    ):

        if password != confirm:

            st.error("Passwords do not match.")

            return

        if len(password) < 8:

            st.error(
                "Password must be at least 8 characters."
            )

            return

        success = create_password(
            st.session_state.activate_user_id,
            password
        )

        if success:

            st.success(
                "Password created successfully."
            )

            st.session_state.activate_user_id = None
            st.session_state.auth_page = "login"

            st.rerun()

        else:

            st.error(
                "Something went wrong."
            )


# ==========================================================
# Main Authentication Router
# ==========================================================

def authentication():

    if st.session_state.auth_page == "login":

        show_login()

    elif st.session_state.auth_page == "activate":

        show_activate_account()

    elif st.session_state.auth_page == "password":

        show_create_password()