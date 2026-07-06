import streamlit as st
from streamlit_option_menu import option_menu







from dashboard.student import student_page
from dashboard.teacher import teacher_page
from dashboard.parent import parent_page
from dashboard.reports import report_page
from dashboard.settings import settings_page
import pandas as pd

from database.dashboard_db import (
    get_dashboard_counts,
    get_recent_activity,
    get_students_by_department
)
def dashboard_home():
    counts = get_dashboard_counts()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("🎓 Students", counts["students"])

    with c2:
        st.metric("👨‍🏫 Teachers", counts["teachers"])

    with c3:
        st.metric("👨‍👩‍👧 Parents", counts["parents"])
    dept = get_students_by_department()
#department graph
#---------------
    df = pd.DataFrame(
    dept,
    columns=["Department", "Students"]
)

    st.bar_chart(df.set_index("Department"))
    #recent activity
    activity = get_recent_activity()

    df = pd.DataFrame(
    activity,
    columns=["Action", "Module", "Time"]
)

    st.dataframe(df, use_container_width=True)
    



# ===========================
# Admin Dashboard
# ===========================

def admin_dashboard():
     # ---------------- Header ----------------
    st.markdown("""
    <div style="
        background:linear-gradient(90deg,#2563EB,#1E40AF);
        padding:20px;
        border-radius:15px;
        color:white;
        margin-bottom:20px;
    ">

    <h2>🎓 BBAU Student Parent Portal</h2>

    <p>Administrator Dashboard</p>

    </div>
    """, unsafe_allow_html=True)

    # ---------------- Sidebar ----------------

    with st.sidebar:

        st.markdown("<br>", unsafe_allow_html=True)

        st.image(
            "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            width=90
        )

        st.markdown(
            """
            <h3 style='text-align:center;margin-bottom:0px;'>
            Sanya
            </h3>

            <p style='text-align:center;color:gray;'>
            Administrator
            </p>
            """,
            unsafe_allow_html=True
        )

        st.divider()
        st.markdown("""
<style>
[data-testid="stSidebar"] {
    overflow-y: auto;
}

[data-testid="stSidebarContent"] {
    overflow-y: auto;
    height: 100vh;
}
</style>
""", unsafe_allow_html=True)

        selected = option_menu(

            menu_title=None,

            options=[

                "Dashboard",

                "Students",

                "Teachers",

                "Parents",

                "Courses",

                "Attendance",

                "Results",

                "Reports",

                "Settings"

            ],

            default_index=0,

            styles={

                "container": {

                    "padding": "0px",

                    "background-color": "#D6DFF3",

                },


                "nav-link": {

                    "font-size": "16px",

                    "text-align": "left",

                    "margin": "6px",

                    "padding": "12px",

                    "border-radius": "10px",

                    "--hover-color": "#BFC7D4",

                },

                "nav-link-selected": {

                    "background-color": "#9AA3B6",

                    "color": "white",

                },

            }

        )

        st.divider()

        st.markdown("### 🟢 Database Status")

        st.success("Connected")

        st.markdown("### 🔔 Notifications")

        st.divider()

        if st.button("🚪 Logout", use_container_width=True):

            st.session_state.clear()

            st.rerun()

    # ---------------- Main Area ----------------

    if selected == "Dashboard":

        dashboard_home()

    elif selected == "Students":

        student_page()

    elif selected == "Teachers":

        teacher_page()

    elif selected == "Parents":

        parent_page()

    elif selected == "Reports":

        report_page()

    elif selected == "Settings":

        settings_page()

    else:

        st.title(selected)

        st.info(f"{selected} module is under development.")


