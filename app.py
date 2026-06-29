import streamlit as st
from auth.login import login_user

st.title("BBAU Parent Student Portal")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    role = login_user(email, password)

    if role:
        st.success(f"Welcome {role}")
    else:
        st.error("Invalid Email or Password")