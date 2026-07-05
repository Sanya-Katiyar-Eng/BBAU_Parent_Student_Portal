import streamlit as st
from auth.login import login_user , add_bg_gif
from dashboard.admin import admin_dashboard



add_bg_gif()



if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None


if not st.session_state.logged_in:  
    st.set_page_config(layout="wide")

    left, center, right = st.columns([2, 1, 2])

    with center:
        st.image("images/bbau logo.jpg", width=180)
        st.markdown(
    """
    <p style="text-align:center; color:#0B5ED7;">
        BBAU Student Parent portal
    </p>
    """,
    unsafe_allow_html=True
)

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