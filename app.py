import streamlit as st
from auth.login import add_bg_gif
st.markdown("""
<style>

/* Main page text */
html, body, [class*="css"] {
    color: black !important;
}

/* Labels */
label, .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6 {
    color: black !important;
    font-weight: 600;
}

/* Text Input */
.stTextInput label {
    color: black !important;
}

/* Selectbox */
.stSelectbox label {
    color: black !important;
}

/* Checkbox */
.stCheckbox label {
    color: black !important;
}

/* Radio */
.stRadio label {
    color: black !important;
}

/* Form labels */
[data-testid="stWidgetLabel"] {
    color: black !important;
    font-weight: bold;
}

/* Sidebar (optional) */
section[data-testid="stSidebar"] * {
    color: black !important;
}

</style>
""", unsafe_allow_html=True)



#from dashboard.parent import parent_dashboard


from auth.login import authentication
from dashboard.admin import admin_dashboard
from dashboard.student import student_dashboard,dashboard_home
# from dashboard.parent import parent_dashboard

from dashboard.student import student_profile_form,dashboard_home
from database.student_db import get_registration_status

if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"

if "activate_user_id" not in st.session_state:
    st.session_state.activate_user_id = None
# ==========================================================
# Page Config
# ==========================================================

st.set_page_config(
    
    page_title="BBAU Student Parent Portal",
    page_icon="🎓",
    layout="wide"
)
# ==========================================================
# Session State Initialization
# ==========================================================

defaults = {
    "logged_in": False,
    "user_id": None,
    "role": None,
    "auth_page": "login",
    "activate_user_id": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value



# ==========================================================
# Logout
# ==========================================================

def logout():

    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.role = None

    st.rerun()


# ==========================================================
# Student Router
# ==========================================================

def student_route():

    registration_status = get_registration_status(
        st.session_state.user_id
    )

    if registration_status == "Pending":

        student_profile_form()

    else:

        student_dashboard()


# ==========================================================
# Dashboard Router
# ==========================================================

def dashboard_router():

    role = st.session_state.role.lower()

    if role == "admin":

        admin_dashboard()

    elif role == "student":

        student_dashboard()

    elif role == "parent":

        st.write("Parent Dashboard")

        # parent_dashboard()

    else:

        st.error("Invalid Role")

    st.sidebar.divider()

    if st.sidebar.button(
        "Logout",
        use_container_width=True
    ):

        logout()
# ==========================================================
# Main Application
# ==========================================================

def main():

    # -------------------------------
    # User Not Logged In
    # -------------------------------

    if not st.session_state.logged_in:

        authentication()

        return

    # -------------------------------
    # User Logged In
    # -------------------------------

    dashboard_router()


# ==========================================================
# Run Application
# ==========================================================

if __name__ == "__main__":

    main()
    