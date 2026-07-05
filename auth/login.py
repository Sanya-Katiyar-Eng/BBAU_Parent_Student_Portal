from database.db import get_connection
import streamlit as st



#===========================================
#use gif
#=============================================
import base64

def add_bg_gif():
    with open("images/bbau_watermark.gif", "rb") as f:
        data = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{
            background: url("data:image/gif;base64,{data}") center center;
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        .stApp::before {{
            content: "";
            position: fixed;
            inset: 0;
            background: rgba(255,255,255,0.55);   /* Opacity control */
            pointer-events: none;
            z-index: 0;
        }}

        .main, [data-testid="stAppViewContainer"] {{
            position: relative;
            z-index: 1;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )


#=====================================================================================
#login user
#========================================================================================
def login_user(email, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT role FROM users WHERE email=%s AND password=%s",
        (email, password)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        return user[0]   # role
    return None


