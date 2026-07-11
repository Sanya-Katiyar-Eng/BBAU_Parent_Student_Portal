from database.auth_db import (
    get_user,
    verify_password
)


def authenticate_user(role, login_username, password):

    user = get_user(
        login_username,
        role
    )

    if user is None:

        return {
            "success": False,
            "message": "User not found."
        }

    user_id = user[0]
    db_username = user[1]
    db_password = user[2]
    db_role = user[3]
    first_login = user[4]
    account_status = user[5]

    # -------------------------------
    # Account Status
    # -------------------------------

    if account_status != "Active":

        return {

            "success": False,

            "message": "Account is inactive."

        }

    # -------------------------------
    # First Login
    # -------------------------------

    if first_login:

        return {

            "success": False,

            "message": "Please activate your account first."

        }

    # -------------------------------
    # Password Check
    # -------------------------------

    if not verify_password(
        password,
        db_password
    ):

        return {

            "success": False,

            "message": "Invalid Password."

        }

    # -------------------------------
    # Login Success
    # -------------------------------

    return {

        "success": True,

        "user_id": user_id,

        "role": db_role

    }