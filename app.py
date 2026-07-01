import streamlit as st
from auth.login import login_user
from dashboard.admin import admin_dashboard
from utils.load_css import load_css

load_css()
st.set_page_config(
    page_title="BBAU Student Parent Portal",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None


if not st.session_state.logged_in:  
    st.title("BBAU Parent Student Portal")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login",use_container_width=True):
        role = login_user(email, password)

        if role:
           st.session_state["logged_in"] = True
           st.session_state["role"] = role
           st.rerun()
        else:
            st.error("Invalid Email or Password")

#-------------------------
## Dashboard Routing
#--------------------------
else:
    if st.session_state['role'].lower()=="admin":
        admin_dashboard()
    elif st.session_state["role"].lower() == "student":
        #student_dashboard()
        pass

    elif st.session_state["role"].lower() == "teacher":
        #teacher_dashboard()
        pass

    elif st.session_state["role"].lower() == "parent":
        #parent_dashboard()
        pass
    else:
        st.error("invalid Role")