import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
from database.dashboard_db import (
    get_all_students,
    get_all_courses,
    assign_student_to_course
)
from dashboard.student import student_page
from dashboard.teacher import teacher_page,assign_course_page
from dashboard.reports import report_page
from dashboard.settings import settings_page
from dashboard.parent import parent_page
import pandas as pd

from database.dashboard_db import (
    get_dashboard_counts,
    get_recent_activity,
    get_students_by_department,
    get_monthly_registration,
    get_students_by_gender,
    get_all_courses


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

    # ======================================================
    # ADMIN UI STYLE
    # ======================================================

    st.markdown("""
<style>
/* ---------- MAIN BACKGROUND ---------- */
.stApp {
    background: radial-gradient(circle at 0% 0%, rgba(33,150,243,.08), transparent 30%), #f5f8fc;
}

.block-container {
    padding-top: 28px !important;
}

/* ---------- SIDEBAR ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f9fcff 0%, #edf5fd 100%);
    border-right: 1px solid #dce8f5;
}

[data-testid="stSidebarContent"] {
    padding-top: 15px;
}

/* ---------- BBAU BRAND & ANIMATIONS ---------- */
.bbau-brand {
    text-align: center;
    color: #0d47a1;
    font-size: 25px;
    font-weight: 800;
    letter-spacing: 2px;
    animation: fadeInDown 0.8s ease-out;
}

.portal-brand {
    text-align: center;
    color: #8192a5;
    font-size: 11px;
    margin-top: 2px;
    animation: fadeIn 1s ease-out;
}

/* ---------- PROFILE BOX ---------- */
.profile-box {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    margin: 8px 0 10px 0;
    animation: fadeIn 1s ease-out;
}

.profile-icon {
    width: 58px;
    height: 58px;
    min-width: 58px;
    border-radius: 50%;
    background: #e7f1fb;
    border: 3px solid white;
    box-shadow: 0 7px 18px rgba(25,118,210,.18);
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.profile-icon:hover {
    transform: scale(1.06);
    box-shadow: 0 10px 22px rgba(25,118,210,.28);
}

.profile-icon .head {
    position: absolute;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #71869a;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
}

.profile-icon .body {
    position: absolute;
    width: 36px;
    height: 25px;
    border-radius: 20px 20px 7px 7px;
    background: #71869a;
    bottom: 6px;
    left: 50%;
    transform: translateX(-50%);
}

.profile-name {
    color: #263f59;
    font-size: 16px;
    font-weight: 700;
}

/* ---------- MENU HOVER & ANIMATIONS ---------- */
[data-testid="stSidebar"] .nav-link {
    color: #40566f !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    margin: 4px 6px !important;
    padding: 11px 13px !important;
    border-radius: 11px !important;
    transition: all 0.3s ease !important;
}

[data-testid="stSidebar"] .nav-link:hover {
    background: #e3f1ff !important;
    color: #1565c0 !important;
    transform: translateX(5px) !important;
}

[data-testid="stSidebar"] .nav-link-selected {
    background: linear-gradient(135deg, #0d47a1, #1976d2) !important;
    color: white !important;
    box-shadow: 0 6px 18px rgba(25,118,210,.20) !important;
    transform: scale(1.02) !important;
}

/* ---------- SIDEBAR BUTTON ---------- */
[data-testid="stSidebar"] .stButton > button {
    border-radius: 10px !important;
    background: white !important;
    color: #40566f !important;
    border: 1px solid #d7e5f3 !important;
    font-weight: 650 !important;
    transition: all 0.25s ease !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #eaf4ff !important;
    color: #1565c0 !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(25,118,210,.12);
}

/* ---------- WELCOME CARD & KEYFRAMES ---------- */
.welcome-card {
    background: linear-gradient(135deg, #0d47a1, #1976d2, #42a5f5);
    border-radius: 22px;
    padding: 30px;
    margin-bottom: 25px;
    box-shadow: 0 12px 30px rgba(25,118,210,.20);
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.6s ease-out;
}

.welcome-card:after {
    content: "";
    position: absolute;
    width: 180px;
    height: 180px;
    right: -60px;
    top: -80px;
    border-radius: 50%;
    background: rgba(255,255,255,.10);
    animation: glow 4s ease-in-out infinite;
}

@keyframes glow {
    0%, 100% { transform: scale(.85); }
    50% { transform: scale(1.15); }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-15px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.welcome-title {
    color: white;
    font-size: 30px;
    font-weight: 800;
    position: relative;
    z-index: 2;
}

.welcome-subtitle {
    color: rgba(255,255,255,.88);
    font-size: 14px;
    margin-top: 7px;
    position: relative;
    z-index: 2;
}

[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e1eaf3;
    border-radius: 16px;
    padding: 15px;
    box-shadow: 0 5px 20px rgba(40,80,120,.06);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(40,80,120,.12);
}
</style>
""", unsafe_allow_html=True)

    # ======================================================
    # SIDEBAR
    # ======================================================

    with st.sidebar:
        st.markdown('<div class="bbau-brand">BBAU</div>', unsafe_allow_html=True)
        st.markdown('<div class="portal-brand">Student Parent Portal</div>', unsafe_allow_html=True)
        st.divider()

        # ==================================================
        # PROFILE
        # ==================================================
        st.markdown("""
<div class="profile-box">
    <div class="profile-icon">
        <div class="head"></div>
        <div class="body"></div>
    </div>
    <div class="profile-name">Sanya</div>
</div>
""", unsafe_allow_html=True)

        st.divider()

        # ==================================================
        # MENU
        # ==================================================
        selected = option_menu(
            menu_title=None,
            options=[
                "Dashboard",
                "Students",
                "Teachers",
                "Parents",
                "Courses",
                "Assign Student Course",
                "Reports",
                "Settings"
            ],
            icons=[
                "grid-fill",
                "people-fill",
                "person-badge-fill",
                "house-door-fill",
                "journal-bookmark-fill",
                "pencil-square",
                "calendar-check-fill",
                "trophy-fill",
                "file-bar-graph-fill",
                "gear-fill"
            ],
            default_index=0,
            styles={
                "container": {
                    "padding": "0px",
                    "background-color": "transparent"
                },
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "4px 6px",
                    "padding": "11px 13px",
                    "border-radius": "11px",
                    "color": "#40566f",
                    "--hover-color": "#e3f1ff"
                },
                "nav-link-selected": {
                    "background-color": "#1976D2",
                    "color": "white"
                }
            }
        )

        st.divider()

        # ==================================================
        # STATUS & NOTIFICATIONS
        # ==================================================
        st.markdown("### DATABASE STATUS")
        st.success("Connected")

        st.markdown("### NOTIFICATIONS")
        st.info("You're all caught up")

        st.divider()

        # ==================================================
        # LOGOUT
        # ==================================================
        if st.button("Logout", use_container_width=True, key="admin_logout_button"):
            st.session_state.clear()
            st.rerun()

    # ======================================================
    # MAIN PAGE CONTENT
    # ======================================================
    st.markdown("""
<div class="welcome-card">
    <div class="welcome-title">Welcome Admin</div>
    <div class="welcome-subtitle">Manage your university portal from one place</div>
</div>
""", unsafe_allow_html=True)

    # ======================================================
    # ROUTING LOGIC
    # ======================================================
    if selected == "Dashboard":
        dashboard_home()
    elif selected == "Students":
        student_page()
    elif selected == "Teachers":
        teacher_page()
    elif selected == "Parents":
        parent_page()
    elif selected == "Courses":
        assign_course_page()
    elif selected == "Assign Student Course":
        assign_student_course_page()
    elif selected == "Reports":
        report_page()
    elif selected == "Settings":
        settings_page()
    else:
        st.title(selected)
        st.info(f"{selected} module is under development.")

















def assign_student_course_page():

    st.subheader("Assign Student To Course")


    students = get_all_students()
    courses = get_all_courses()


    if not students:
        st.warning("No Students Found")
        return


    if not courses:
        st.warning("No Courses Found")
        return


    student = st.selectbox(
        "Student",
        students,
        format_func=lambda x:f"{x[1]} ({x[2]})"
    )


    course = st.selectbox(
        "Course",
        courses,
        format_func=lambda x: x[1]
    )


    if st.button("Assign Course"):


        success = assign_student_to_course(

            student_id=student[0],
            course_id=course[0]

        )


        if success:
            st.success(
                "Student Assigned Successfully"
            )

        else:
            st.error(
                "Already Assigned / Failed"
            )



