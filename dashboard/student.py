import streamlit as st

def student_page():

    st.title("👨‍🎓 Student Management")

    c1,c2,c3=st.columns(3)

    with c1:
        st.button("➕ Add Student",use_container_width=True)

    with c2:
        st.button("📋 View Students",use_container_width=True)

    with c3:
        st.button("🗑 Delete Student",use_container_width=True)

    st.divider()

    st.info("Student Table will appear here.")