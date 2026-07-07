from database.db import get_connection
import streamlit as st
from database.db import get_connection


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



 


# =====================================================
# Login User
# =====================================================

def login_user(role, login_username, password):

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            SELECT
                id,
                role,
                first_login,
                account_status

            FROM users

            WHERE

                login_username=%s
                AND role=%s

        """,
        (
            login_username,
            role.lower()
        ))

        user = cur.fetchone()

        if user is None:
            return {
                "success": False,
                "message": "User Not Found"
            }

        user_id = user[0]
        db_role = user[1]
        first_login = user[2]
        account_status = user[3]

        if account_status.lower() != "active":

            return {
                "success": False,
                "message": "Account is Inactive"
            }

        # ------------------------------
        # First Login
        # ------------------------------

        if first_login:

            return {

                "success": True,
                "first_login": True,
                "user_id": user_id,
                "role": db_role

            }

        # ------------------------------
        # Normal Login
        # ------------------------------

        cur.execute("""

            SELECT id

            FROM users

            WHERE

            login_username=%s
            AND password=%s
            AND role=%s

        """,

        (
            login_username,
            password,
            role.lower()

        ))

        login = cur.fetchone()

        if login:

            return {

                "success": True,
                "first_login": False,
                "user_id": user_id,
                "role": db_role

            }

        return {

            "success": False,
            "message": "Invalid Password"

        }

    finally:

        cur.close()
        conn.close()









#first login
#=======================================
import streamlit as st
from database.db import get_connection


def set_new_password(user_id):

    st.title("🔐 First Time Login")

    st.info("Create your password to continue.")

    with st.form("first_login_form"):

        new_password = st.text_input(
            "New Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        submit = st.form_submit_button(
            "Create Password",
            use_container_width=True
        )

    if submit:

        if new_password == "" or confirm_password == "":
            st.error("All fields are required.")
            return False

        if len(new_password) < 8:
            st.error("Password must be at least 8 characters.")
            return False

        if new_password != confirm_password:
            st.error("Passwords do not match.")
            return False

        conn = get_connection()
        cur = conn.cursor()

        try:

            cur.execute("""
                UPDATE users

                SET

                password=%s,
                first_login=FALSE

                WHERE id=%s
            """,
            (
                new_password,
                user_id
            ))

            conn.commit()

            st.success("Password created successfully.")

            st.session_state.first_login = False

            st.rerun()

        except Exception as e:

            conn.rollback()

            st.error(e)

        finally:

            cur.close()
            conn.close()
