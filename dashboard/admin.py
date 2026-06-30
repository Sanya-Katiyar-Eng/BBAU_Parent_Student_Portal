import streamlit as st


from dashboard.student import student_page
from dashboard.teacher import teacher_page
from dashboard.parent import parent_page
from dashboard.reports import report_page
from dashboard.settings import settings_page












def admin_dashboard():
    st.markdown("""
<div style="background:#0F172A;
padding:20px;
border-radius:12px;
color:white">

<h2>BBAU Student Parent Portal</h2>

<p>Administrator Dashboard</p>

</div>
""",
unsafe_allow_html=True)
    left,right=st.columns([1,4])
    with left:

        st.markdown("## 👤 Admin")

        menu = [
        "Dashboard",
        "Students",
        "Teachers",
        "Parents",
        "Courses",
        "Attendance",
        "Results",
        " Events",
        "Jobs",
        "Reports",
        "Settings",
    ]

        selected = st.radio(
        "",
        menu,
        label_visibility="collapsed"
    )

    st.session_state.page = selected
#---------------------
# right
#==================
   
    with right:

        page = st.session_state.page

        if page == "Dashboard":
            dashboard_home()

        elif page == "Students":
            student_page()

        elif page == "Teachers":
            teacher_page()

        elif page == "Parents":
            parent_page()

        elif page == "Courses":
            course_page()

        elif page == "Results":
            result_page()

        elif page == "Reports":
            report_page()

        elif page == "Settings":
            settings_page()
