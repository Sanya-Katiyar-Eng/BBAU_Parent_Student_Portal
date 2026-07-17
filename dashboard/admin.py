import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px






from dashboard.student import student_page
from dashboard.teacher import teacher_page
from dashboard.parent import parent_page
from dashboard.reports import report_page
from dashboard.settings import settings_page
import pandas as pd

from database.dashboard_db import (
    get_dashboard_counts,
    get_recent_activity,
    get_students_by_department,
    get_monthly_registration,
    get_students_by_gender


)
def dashboard_home():
    counts = get_dashboard_counts()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Students", counts["students"])

    with c2:
        st.metric("Teachers", counts["teachers"])

    with c3:
        st.metric("Parents", counts["parents"])
    dept = get_students_by_department()
    if dept:
        df = pd.DataFrame(
        dept,
        columns=["Department", "Students"]
        )
    else:
          st.info("No department data available.")


    fig1 = px.bar(
    df,
    x="Department",
    y="Students",
    color="Students",
    text="Students",
    title=" Department Wise Students",
    template="plotly_white"
)

    fig1.update_traces(textposition="outside")
    fig1.update_layout(height=400)


    gender = get_students_by_gender()
    if gender:
        gender_df = pd.DataFrame(
        gender,
        columns=["Gender", "Students"])

        fig2 = px.pie(
    gender_df,
    values="Students",
    names="Gender",
    hole=0.5,
    title="Gender Distribution"
)
        fig2.update_traces(textinfo="percent+label")
        fig2.update_layout(height=400)

    else:
        st.info("No gender data available.")
    fig1.update_layout(
    height=400,
    xaxis_title="Department",
    yaxis_title="Students",
    showlegend=False
)
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader(" Recent Activity")

    activity = get_recent_activity()

    df = pd.DataFrame(
    activity,
    columns=["Action","Module","Time"]
)

    st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)
    registration = get_monthly_registration()
    if registration:
        reg_df = pd.DataFrame(
        registration,
        columns=["Month","Students"]
)
        fig3 = px.line(
    reg_df,
    x="Month",
    y="Students",
    markers=True,
    title=" Monthly Registrations"
)
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No registration data available.")
    st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    height=250
)
    

    























# ===========================
# Admin Dashboard

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







