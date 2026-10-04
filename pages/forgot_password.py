import streamlit as st

from database import reset_password


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CareMate AI | Forgot Password",
    page_icon="🔐",
    layout="centered",
)


# =========================================================
# HEADER
# =========================================================

st.title("🔐 Forgot Password")

st.caption(
    "Reset your CareMate AI account password securely."
)


# =========================================================
# RESET FORM
# =========================================================

with st.form("forgot_password_form"):

    st.subheader("Reset Your Password")

    email = st.text_input(
        "Registered Email",
        placeholder="Enter your registered email"
    )

    phone = st.text_input(
        "Registered Phone Number",
        placeholder="Enter your registered phone number"
    )

    new_password = st.text_input(
        "New Password",
        type="password",
        placeholder="Enter new password"
    )

    confirm_password = st.text_input(
        "Confirm New Password",
        type="password",
        placeholder="Re-enter new password"
    )

    reset_button = st.form_submit_button(
        "🔑 Reset Password",
        use_container_width=True
    )


# =========================================================
# PROCESS RESET
# =========================================================

if reset_button:

    if not email.strip():

        st.error(
            "Please enter your registered email."
        )

    elif not phone.strip():

        st.error(
            "Please enter your registered phone number."
        )

    elif not new_password:

        st.error(
            "Please enter a new password."
        )

    elif new_password != confirm_password:

        st.error(
            "Passwords do not match."
        )

    elif len(new_password) < 6:

        st.error(
            "Password must contain at least 6 characters."
        )

    else:

        success, message = reset_password(
            email=email,
            phone=phone,
            new_password=new_password
        )

        if success:

            st.success(
                "✅ Password reset successfully!"
            )

            st.info(
                "You can now return to the login page "
                "and sign in with your new password."
            )

        else:

            st.error(
                f"❌ {message}"
            )


# =========================================================
# BACK TO LOGIN
# =========================================================

st.write("")

if st.button(
    "← Back to Login",
    use_container_width=True
):
    st.switch_page("pages/login.py")