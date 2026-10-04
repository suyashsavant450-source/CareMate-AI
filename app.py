import streamlit as st

from database import init_database
from utils.theme import apply_caremate_theme


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CareMate AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# INITIALIZATION
# =========================================================

init_database()
apply_caremate_theme()


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# =========================================================
# LOGOUT FUNCTION
# =========================================================

def logout_user():

    st.session_state.logged_in = False
    st.session_state.user = None

    st.switch_page(login_page)


# =========================================================
# PAGE DEFINITIONS
# =========================================================

login_page = st.Page(
    "pages/login.py",
    title="Login",
    icon="🔐"
)

register_page = st.Page(
    "pages/register.py",
    title="Create Account",
    icon="📝"
)

forgot_password_page = st.Page(
    "pages/forgot_password.py",
    title="Forgot Password",
    icon="🔑",
    visibility="hidden"
)

dashboard_page = st.Page(
    "pages/dashboard.py",
    title="Dashboard",
    icon="🏠"
)

reports_page = st.Page(
    "pages/upload_report.py",
    title="Medical Reports",
    icon="📄"
)

caremate_page = st.Page(
    "pages/caremate.py",
    title="CareMate AI",
    icon="🤖"
)

medicines_page = st.Page(
    "pages/medicines.py",
    title="Medicines",
    icon="💊"
)

reminders_page = st.Page(
    "pages/reminders.py",
    title="Reminders",
    icon="🔔"
)

caregiver_page = st.Page(
    "pages/caregiver.py",
    title="Caregiver Mode",
    icon="👨‍👩‍👧"
)

progress_page = st.Page(
    "pages/progress.py",
    title="Health Progress",
    icon="📊"
)

profile_page = st.Page(
    "pages/profile.py",
    title="Profile",
    icon="👤",
    visibility="hidden"
)


# =========================================================
# LOGGED-IN USER
# =========================================================

if st.session_state.logged_in:

    # -----------------------------------------------------
    # SIDEBAR
    # -----------------------------------------------------

    with st.sidebar:

        st.markdown("## 🏥 CareMate AI")

        if st.session_state.user:

            st.caption(
                f"👤 {st.session_state.user['name']}"
            )

        st.divider()

        st.markdown("### Navigation")

    # -----------------------------------------------------
    # NAVIGATION
    # -----------------------------------------------------

    pg = st.navigation({
        "CareMate AI": [
            dashboard_page,
            reports_page,
            caremate_page,
            medicines_page,
            reminders_page,
            caregiver_page,
            progress_page,
            profile_page
        ]
    })

    pg.run()

    # -----------------------------------------------------
    # ACCOUNT
    # -----------------------------------------------------

    with st.sidebar:

        st.divider()

        st.caption("Account")

        # Profile
        if st.button(
            "👤  My Profile",
            use_container_width=True,
            type="secondary"
        ):
            st.switch_page(profile_page)

        st.write("")

        # Logout
        if st.button(
            "🚪  Logout",
            use_container_width=True,
            type="secondary"
        ):
            logout_user()


# =========================================================
# LOGGED-OUT USER
# =========================================================

else:

    pg = st.navigation(
        [
            login_page,
            register_page,
            forgot_password_page
        ]
    )

    pg.run()