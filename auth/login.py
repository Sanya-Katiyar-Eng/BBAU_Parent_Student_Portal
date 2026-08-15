from database.db import get_connection
from auth.auth_service import authenticate_user
import re
import base64
import streamlit as st
from database.auth_db import (
    verify_login,
    verify_student,
    create_password
)
from database.parent_db import save_parent_fcm_token
#=================================================================================================
#normlize
#===============================================================================================
def normalize_text(text):
    if text is None:
        return None
    return text.strip().lower()

















from database.auth_db import (
    verify_login,
    verify_student,
    create_password
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "role" not in st.session_state:
    st.session_state.role = None
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

    st.markdown("""
    <style>

    /* ===============================
       PAGE BACKGROUND
    =============================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 20%,
                rgba(33,150,243,0.13),
                transparent 25%
            ),
            radial-gradient(
                circle at 90% 80%,
                rgba(30,136,229,0.13),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                #eef6ff,
                #f8fbff,
                #edf6ff
            );

        overflow-x: hidden;
    }


    /* ===============================
       STREAMLIT MAIN AREA
    =============================== */

    .block-container {
        padding-top: 35px !important;
        padding-bottom: 30px !important;
    }


    /* ===============================
       ANIMATED GLOW
    =============================== */

    .login-glow {
        position: fixed;

        width: 460px;
        height: 460px;

        left: 50%;
        top: 50%;

        transform: translate(-50%, -50%);

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(33,150,243,0.22) 0%,
                rgba(33,150,243,0.12) 35%,
                rgba(33,150,243,0.05) 55%,
                transparent 72%
            );

        filter: blur(20px);

        animation: glowMove 4s ease-in-out infinite;

        pointer-events: none;

        z-index: 0;
    }


    @keyframes glowMove {

        0% {
            transform:
                translate(-50%, -50%)
                scale(.88);

            opacity: .55;
        }

        50% {
            transform:
                translate(-50%, -50%)
                scale(1.12);

            opacity: 1;
        }

        100% {
            transform:
                translate(-50%, -50%)
                scale(.88);

            opacity: .55;
        }
    }


    /* ===============================
       SMALL MOVING LIGHTS
    =============================== */

    .moving-light {
        position: fixed;

        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: #42a5f5;

        box-shadow:
            0 0 10px #42a5f5,
            0 0 25px rgba(33,150,243,.6);

        pointer-events: none;

        z-index: 0;

        animation: lightMove 6s ease-in-out infinite;
    }


    .light-a {
        left: 15%;
        top: 25%;
    }

    .light-b {
        right: 15%;
        top: 30%;
        animation-delay: 1.5s;
    }

    .light-c {
        left: 18%;
        bottom: 22%;
        animation-delay: 3s;
    }

    .light-d {
        right: 18%;
        bottom: 20%;
        animation-delay: 4.5s;
    }


    @keyframes lightMove {

        0%,100% {
            transform: translate(0,0);
            opacity: .25;
        }

        50% {
            transform: translate(20px,-30px);
            opacity: 1;
        }
    }


    /* ===============================
       CENTER LOGIN CARD
    =============================== */

    .login-card-bg {

        position: fixed;

        width: 430px;
        height: 590px;

        left: 50%;
        top: 50%;

        transform:
            translate(-50%, -50%);

        border-radius: 28px;

        background:
            rgba(255,255,255,.55);

        box-shadow:
            0 0 35px
            rgba(33,150,243,.15),

            0 0 80px
            rgba(33,150,243,.10);

        pointer-events: none;

        z-index: 0;
    }


    /* ===============================
       LOGO CENTER
    =============================== */

    div[data-testid="stImage"] {

        display: flex !important;

        justify-content: center !important;

        align-items: center !important;

        width: 100% !important;

        margin:
            0 auto 5px auto !important;

        text-align: center !important;
    }


    div[data-testid="stImage"] img {

        width: 82px !important;

        height: 82px !important;

        object-fit: contain !important;

        display: block !important;

        margin: 0 auto !important;

        filter:
            drop-shadow(
                0 6px 10px
                rgba(0,60,140,.22)
            )
            drop-shadow(
                0 0 12px
                rgba(33,150,243,.18)
            );
    }


    /* ===============================
       BBAU TITLE
    =============================== */

    .bbau-title {

        text-align: center;

        font-family: Arial, sans-serif;

        font-size: 23px;

        font-weight: 800;

        letter-spacing: 1.5px;

        color: #0d47a1;

        text-shadow:
            0 2px 3px rgba(0,0,0,.13),
            0 0 12px rgba(33,150,243,.25);

        margin-top: 3px;
    }


    .portal-title {

        text-align: center;

        font-size: 14px;

        font-weight: 600;

        color: #52677d;

        margin-top: 2px;
    }


    .title-line {

        width: 50px;

        height: 3px;

        margin:
            9px auto 8px auto;

        border-radius: 20px;

        background:
            linear-gradient(
                90deg,
                #0d47a1,
                #2196f3
            );

        box-shadow:
            0 0 10px
            rgba(33,150,243,.35);
    }


    .subtitle {

        text-align: center;

        font-size: 11px;

        color: #8292a5;

        margin-bottom: 20px;
    }


    /* ===============================
       INPUTS
    =============================== */

    .stTextInput label,
    .stSelectbox label {

        color: #34495e !important;

        font-size: 13px !important;

        font-weight: 600 !important;
    }


    .stTextInput input {

        height: 42px !important;

        border-radius: 11px !important;

        border:
            1px solid #d6e2ef !important;

        background:
            rgba(248,251,255,.95) !important;

        transition: .25s ease !important;
    }


    .stTextInput input:focus {

        border-color:
            #2196f3 !important;

        box-shadow:
            0 0 0 2px
            rgba(33,150,243,.08),

            0 0 15px
            rgba(33,150,243,.15) !important;
    }


    .stSelectbox > div > div {

        border-radius: 11px !important;

        border-color:
            #d6e2ef !important;

        background:
            rgba(248,251,255,.95) !important;
    }


    /* ===============================
       BUTTON
    =============================== */

    .stButton > button {

        height: 44px !important;

        border-radius: 11px !important;

        border: none !important;

        background:
            linear-gradient(
                135deg,
                #0d47a1,
                #1976d2,
                #42a5f5
            ) !important;

        color: white !important;

        font-size: 14px !important;

        font-weight: 700 !important;

        box-shadow:
            0 8px 22px
            rgba(25,118,210,.28);

        transition: .25s ease !important;
    }


    .stButton > button:hover {

        transform:
            translateY(-2px);

        box-shadow:
            0 12px 30px
            rgba(25,118,210,.40);
    }


    /* ===============================
       DIVIDER
    =============================== */

    hr {

        border-color:
            rgba(30,80,130,.10) !important;

        margin:
            17px 0 10px 0 !important;
    }


    /* ===============================
       MOBILE
    =============================== */

    @media(max-width:600px) {

        .login-card-bg {

            width: 90vw;
            height: 620px;
        }

        .login-glow {

            width: 95vw;
            height: 500px;
        }
    }

    </style>


    <!-- BACKGROUND ELEMENTS -->

    <div class="login-glow"></div>

    <div class="login-card-bg"></div>

    <div class="moving-light light-a"></div>
    <div class="moving-light light-b"></div>
    <div class="moving-light light-c"></div>
    <div class="moving-light light-d"></div>

    """,
    unsafe_allow_html=True
    )


    # =========================================================
    # CENTER EVERYTHING
    # =========================================================

    col1, col2, col3 = st.columns(
        [1, 1.05, 1]
    )

    with col2:

        # =====================================================
        # LOGO
        # =====================================================

        # =====================================================
# PERFECTLY CENTERED BBAU LOGO
# =====================================================

        logo_left, logo_center, logo_right = st.columns(
    [1, 1, 1],
    gap="small"
)

        with logo_center:
            st.image(
        "images/bbau logo.jpg",
        width=82)
    


        # =====================================================
        # TITLE
        # =====================================================

            st.markdown(
            """
            <div class="bbau-title">
                BBAU
            </div>

            <div class="portal-title">
                Student Parent Portal
            </div>

            <div class="title-line"></div>
            """,
            unsafe_allow_html=True
        )
            


        # =====================================================
        # LOGIN AS
        # =====================================================

        role = st.selectbox(
            "Login As",
            [
                "Admin",
                "Teacher",
                "Student",
                "Parent"
            ]
        )


        # =====================================================
        # USERNAME
        # =====================================================

        if role == "Admin":

            username = st.text_input(
                "Email",
                placeholder="Enter your email"
            )

        elif role == "Teacher":

            username = st.text_input(
                "Email",
                placeholder="Enter your email"
            )

        elif role == "Student":

            username = st.text_input(
                "Enrollment Number",
                placeholder="Enter enrollment number"
            )

        else:

            username = st.text_input(
                "Parent Mobile Number",
                placeholder="Enter mobile number"
            )


        # =====================================================
        # PASSWORD
        # =====================================================

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )


        # =====================================================
        # LOGIN
        # =====================================================

        if st.button(
            "Login",
            use_container_width=True
        ):

            user = verify_login(
                username,
                password,
                role
            )

            if user.get("first_login"):

                st.session_state.activate_user_id = (
                    user["user_id"]
                )

                st.session_state.auth_page = "password"

                st.rerun()

            elif user["success"]:

                st.session_state.logged_in = True

                st.session_state.user_id = (
                    user["user_id"]
                )

                st.session_state.role = (
                    user["role"]
                )

                st.session_state.email = (
                    user["email"]
                )

                if user["role"].lower() == "parent":

                    st.session_state.parent_id = (
                        user["parent_id"]
                    )

                    st.session_state.student_id = (
                        user["student_id"]
                    )

                    token = st.session_state.get(
                        "fcm_token"
                    )

                    if token:

                        save_parent_fcm_token(
                            user["parent_id"],
                            token
                        )

                st.rerun()

            else:

                st.error(
                    user["message"]
                )


        # =====================================================
        # ACTIVATE ACCOUNT
        # =====================================================

        st.divider()

        st.caption(
            "First time user? Activate your account."
        )

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
'''def show_create_password():

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
             st.error( "Password must be at least 8 characters.")
        elif not re.search(r"[A-Z]", password):
                st.error("One uppercase required")

        elif not re.search(r"[a-z]", password):
                st.error("One lowercase required")

        elif not re.search(r"\d", password):
                st.error("One digit required")

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
'''

def show_activate_account():

    # =========================================================
    # ACTIVATION PAGE CSS
    # =========================================================

    st.markdown("""
    <style>

    /* ================= PAGE ================= */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 20%,
                rgba(33,150,243,.14),
                transparent 26%
            ),
            radial-gradient(
                circle at 90% 80%,
                rgba(21,101,192,.12),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                #edf6ff,
                #f9fcff,
                #edf6ff
            );

        min-height: 100vh;
    }


    .block-container {
        padding-top: 35px !important;
        padding-bottom: 30px !important;
    }


    /* ================= ANIMATED GLOW ================= */

    .activation-glow {
        position: fixed;

        width: 480px;
        height: 480px;

        left: 50%;
        top: 50%;

        transform: translate(-50%, -50%);

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(33,150,243,.22),
                rgba(33,150,243,.08) 45%,
                transparent 72%
            );

        filter: blur(25px);

        animation: pulseGlow 4s ease-in-out infinite;

        pointer-events: none;

        z-index: 0;
    }


    @keyframes pulseGlow {

        0%,100% {
            transform:
                translate(-50%,-50%)
                scale(.88);

            opacity: .55;
        }

        50% {
            transform:
                translate(-50%,-50%)
                scale(1.12);

            opacity: 1;
        }
    }


    /* ================= FLOATING LIGHTS ================= */

    .light1,
    .light2,
    .light3,
    .light4 {

        position: fixed;

        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: #42a5f5;

        box-shadow:
            0 0 12px rgba(33,150,243,.8),
            0 0 28px rgba(33,150,243,.5);

        pointer-events: none;

        z-index: 0;

        animation: floatLight 6s ease-in-out infinite;
    }


    .light1 {
        left: 12%;
        top: 22%;
    }

    .light2 {
        right: 13%;
        top: 28%;
        animation-delay: 1.5s;
    }

    .light3 {
        left: 16%;
        bottom: 20%;
        animation-delay: 3s;
    }

    .light4 {
        right: 17%;
        bottom: 18%;
        animation-delay: 4.5s;
    }


    @keyframes floatLight {

        0%,100% {
            transform: translate(0,0);
            opacity: .25;
        }

        50% {
            transform: translate(25px,-30px);
            opacity: 1;
        }
    }


    /* ================= CARD ================= */

    div[data-testid="stVerticalBlockBorderWrapper"] {

        background: rgba(255,255,255,.94) !important;

        border:
            1px solid
            rgba(255,255,255,.95) !important;

        border-radius: 26px !important;

        box-shadow:
            0 25px 65px rgba(15,70,130,.16),
            0 0 35px rgba(33,150,243,.12) !important;

        backdrop-filter: blur(15px);

        padding: 10px !important;
    }


    /* ================= INPUT ================= */

    .stTextInput label {

        font-size: 13px !important;

        font-weight: 600 !important;

        color: #34495e !important;
    }


    .stTextInput input {

        height: 43px !important;

        border-radius: 11px !important;

        border: 1px solid #d6e2ef !important;

        background: #f8fbff !important;

        transition: .25s ease !important;
    }


    .stTextInput input:focus {

        border-color: #2196f3 !important;

        box-shadow:
            0 0 0 2px rgba(33,150,243,.08),
            0 0 15px rgba(33,150,243,.15) !important;
    }


    /* ================= BUTTON ================= */

    .stButton > button {

        height: 44px !important;

        border-radius: 11px !important;

        border: none !important;

        background:
            linear-gradient(
                135deg,
                #0d47a1,
                #1976d2,
                #42a5f5
            ) !important;

        color: white !important;

        font-weight: 700 !important;

        box-shadow:
            0 8px 22px
            rgba(25,118,210,.28);

        transition: .25s ease !important;
    }


    .stButton > button:hover {

        transform: translateY(-2px);

        box-shadow:
            0 12px 30px
            rgba(25,118,210,.40);
    }

    </style>

    <div class="activation-glow"></div>

    <div class="light1"></div>
    <div class="light2"></div>
    <div class="light3"></div>
    <div class="light4"></div>
    """, unsafe_allow_html=True)


    # =========================================================
    # CENTER
    # =========================================================

    left, center, right = st.columns(
        [1, 1.05, 1]
    )

    with center:

        # =====================================================
        # REAL STREAMLIT CARD
        # =====================================================

        with st.container(border=True):

            # -------------------------------------------------
            # LOGO
            # -------------------------------------------------

            logo_left, logo_center, logo_right = st.columns(
                [1, 1, 1]
            )

            with logo_center:

                st.image(
                    "images/bbau logo.jpg",
                    width=78
                )


            # -------------------------------------------------
            # BBAU
            # -------------------------------------------------

            st.markdown(
                "<h2 style='"
                "text-align:center;"
                "color:#0d47a1;"
                "font-family:Arial;"
                "font-size:23px;"
                "letter-spacing:2px;"
                "margin:2px 0 0 0;"
                "text-shadow:0 2px 5px rgba(0,0,0,.15);"
                "'>BBAU</h2>",
                unsafe_allow_html=True
            )


            # -------------------------------------------------
            # TITLE
            # -------------------------------------------------

            st.markdown(
                "<p style='"
                "text-align:center;"
                "font-size:19px;"
                "font-weight:700;"
                "color:#263f59;"
                "margin:3px 0 4px 0;"
                "'>Activate Your Account</p>",
                unsafe_allow_html=True
            )


            st.markdown(
                "<p style='"
                "text-align:center;"
                "font-size:11px;"
                "color:#8292a5;"
                "margin:0 0 18px 0;"
                "'>Verify your student details to securely "
                "activate your portal account.</p>",
                unsafe_allow_html=True
            )


            # -------------------------------------------------
            # STEP INDICATOR
            # -------------------------------------------------

            step1, line, step2 = st.columns(
                [1, 1.4, 1]
            )

            with step1:
                st.markdown(
                    "<div style='"
                    "text-align:center;"
                    "color:white;"
                    "background:linear-gradient(135deg,#0d47a1,#42a5f5);"
                    "width:26px;"
                    "height:26px;"
                    "line-height:26px;"
                    "border-radius:50%;"
                    "margin:auto;"
                    "font-size:11px;"
                    "font-weight:700;"
                    "'>1</div>",
                    unsafe_allow_html=True
                )

            with line:
                st.markdown(
                    "<div style='"
                    "height:2px;"
                    "background:#dceaf8;"
                    "margin-top:12px;"
                    "'></div>",
                    unsafe_allow_html=True
                )

            with step2:
                st.markdown(
                    "<div style='"
                    "text-align:center;"
                    "color:#91a4b7;"
                    "background:#eef5fb;"
                    "width:26px;"
                    "height:26px;"
                    "line-height:26px;"
                    "border-radius:50%;"
                    "margin:auto;"
                    "font-size:11px;"
                    "font-weight:700;"
                    "'>2</div>",
                    unsafe_allow_html=True
                )


            st.write("")


            # =================================================
            # FORM
            # =================================================

            enrollment = st.text_input(
                "Enrollment Number",
                placeholder="Enter your enrollment number"
            )


            roll_no = st.text_input(
                "Roll Number",
                placeholder="Enter your roll number"
            )


            # =================================================
            # VERIFY
            # =================================================

            if st.button(
                "Verify & Continue",
                use_container_width=True
            ):

                student = verify_student(
                    enrollment,
                    roll_no
                )


                if student:

                    st.session_state.activate_user_id = (
                        student[0]
                    )

                    st.session_state.auth_page = (
                        "password"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Enrollment Number or Roll Number is incorrect."
                    )


            st.markdown(
                "<p style='"
                "text-align:center;"
                "font-size:11px;"
                "color:#8292a5;"
                "margin:12px 0 5px 0;"
                "'>Already have an account?</p>",
                unsafe_allow_html=True
            )


            # =================================================
            # BACK
            # =================================================

            if st.button(
                "← Back to Login",
                use_container_width=True
            ):

                st.session_state.auth_page = "login"

                st.rerun()





















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