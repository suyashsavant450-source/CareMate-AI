import streamlit as st
from database import authenticate_user


# ---------------------------------------------------------
# AUTH CHECK
# ---------------------------------------------------------
if st.session_state.get("logged_in", False):
    st.stop()


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Login | AI-Medical Report Simplifier",
    page_icon="🤖",
    layout="wide"
)


# ---------------------------------------------------------
# DARK THEME MATCHING CSS
# ---------------------------------------------------------
st.markdown(
    """<style>
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .stApp {
        background: #020617 !important;
        color: #f8fafc;
    }

    .main .block-container {
        max-width: 1350px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    .project-header-container {
        text-align: center;
        margin-bottom: 25px;
        animation: fadeUp 0.6s ease forwards;
    }

    .project-main-title {
        font-size: 32px;
        font-weight: 900;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc, #38bdf8);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    .ai-panel {
        padding: 10px;
        animation: fadeUp 0.8s ease forwards;
    }

    .brand-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        background: rgba(14, 165, 233, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.3);
        color: #38bdf8;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 20px;
    }

    .brand-title {
        font-size: 36px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.5px;
        line-height: 1.2;
        margin-bottom: 14px;
    }

    .brand-title span {
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .brand-description {
        font-size: 14px;
        line-height: 1.6;
        color: #94a3b8;
        max-width: 480px;
        margin-bottom: 25px;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px 16px;
        margin-top: 15px;
    }

    .feature-item {
        display: flex;
        align-items: flex-start;
        gap: 14px;
        background: transparent;
        padding: 6px;
    }

    .feature-icon-box {
        min-width: 46px;
        height: 46px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
    }

    .icon-blue { background: linear-gradient(135deg, #0284c7, #0369a1); }
    .icon-purple { background: linear-gradient(135deg, #7c3aed, #6d28d9); }
    .icon-indigo { background: linear-gradient(135deg, #4f46e5, #4338ca); }
    .icon-amber { background: linear-gradient(135deg, #d97706, #b45309); }
    .icon-emerald { background: linear-gradient(135deg, #059669, #047857); }
    .icon-teal { background: linear-gradient(135deg, #0d9488, #0f766e); }

    .feature-info {
        display: flex;
        flex-direction: column;
    }

    .feature-title {
        color: #ffffff !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        margin-bottom: 2px !important;
    }

    .feature-text {
        color: #94a3b8 !important;
        font-size: 12px !important;
        font-weight: 400 !important;
        line-height: 1.4 !important;
    }

    div[data-testid="stForm"] {
        background: rgba(15, 23, 42, 0.75) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 24px !important;
        padding: 35px !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(12px);
        animation: fadeUp 0.9s ease forwards;
    }

    .login-heading {
        font-size: 28px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 4px;
        letter-spacing: -0.5px;
    }

    .login-caption {
        color: #94a3b8;
        font-size: 13px;
        margin-bottom: 22px;
    }

    div[data-testid="stForm"] label {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }

    div[data-testid="stForm"] input {
        background: rgba(2, 6, 23, 0.8) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        border-radius: 12px !important;
        min-height: 46px !important;
    }

    div[data-testid="stForm"] input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 14px rgba(56, 189, 248, 0.3) !important;
    }

    div[data-testid="stFormSubmitButton"] button {
        min-height: 48px !important;
        border-radius: 12px !important;
        border: none !important;
        color: white !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #2563eb, #4f46e5, #7c3aed) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.35) !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 28px rgba(99, 102, 241, 0.5) !important;
    }

    .create-account .stButton > button {
        min-height: 42px !important;
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        color: #38bdf8 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    .create-account .stButton > button:hover {
        border-color: rgba(56, 189, 248, 0.5) !important;
        background: rgba(30, 41, 59, 0.9) !important;
        color: #ffffff !important;
    }

    .secure-note {
        text-align: center;
        color: #64748b;
        font-size: 11px;
        margin-top: 14px;
    }
    </style>""",
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# TOP MAIN HEADER
# ---------------------------------------------------------
st.markdown(
    """<div class="project-header-container">
        <div class="project-main-title">
            AI-MEDICAL REPORT SIMPLIFIER AND CAREMATE
        </div>
    </div>""",
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# MAIN LAYOUT
# ---------------------------------------------------------
left, right = st.columns([1.1, 0.9], gap="large")


# ---------------------------------------------------------
# LEFT — BRAND & FEATURES
# ---------------------------------------------------------
with left:
    left_side_html = """<div class="ai-panel">
<div class="brand-badge">✦ AI-POWERED HEALTHCARE PLATFORM</div>
<div class="brand-title">Smarter Health<br>with <span>CareMate AI</span></div>
<div class="brand-description">Get simple explanations for your medical reports, manage medicines, track your health, and get AI assistance — all in one place.</div>
<div class="feature-grid">
<div class="feature-item">
<div class="feature-icon-box icon-blue">📄</div>
<div class="feature-info">
<div class="feature-title">Medical Reports</div>
<div class="feature-text">OCR + AI powered report simplification</div>
</div>
</div>
<div class="feature-item">
<div class="feature-icon-box icon-purple">💊</div>
<div class="feature-info">
<div class="feature-title">Medicine Management</div>
<div class="feature-text">Track medicines and daily reminders</div>
</div>
</div>
<div class="feature-item">
<div class="feature-icon-box icon-indigo">🤖</div>
<div class="feature-info">
<div class="feature-title">AI Health Assistant</div>
<div class="feature-text">Patient-friendly health conversations</div>
</div>
</div>
<div class="feature-item">
<div class="feature-icon-box icon-amber">👨‍👩‍👧</div>
<div class="feature-info">
<div class="feature-title">Caregiver Mode</div>
<div class="feature-text">Monitor authorized family members</div>
</div>
</div>
<div class="feature-item">
<div class="feature-icon-box icon-emerald">📊</div>
<div class="feature-info">
<div class="feature-title">Health Progress</div>
<div class="feature-text">Track water, sleep and exercise</div>
</div>
</div>
<div class="feature-item">
<div class="feature-icon-box icon-teal">🌐</div>
<div class="feature-info">
<div class="feature-title">Multilingual Support</div>
<div class="feature-text">English, Marathi, Hindi and Kannada</div>
</div>
</div>
</div>
</div>"""

    st.markdown(left_side_html, unsafe_allow_html=True)


# ---------------------------------------------------------
# RIGHT — LOGIN FORM
# ---------------------------------------------------------
with right:

    if "login_failed" not in st.session_state:
        st.session_state.login_failed = False

    with st.form("login_form"):

        st.markdown(
            '<div class="login-heading">Welcome Back!</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="login-caption">Sign in to access your health information, medicines and AI assistant.</div>',
            unsafe_allow_html=True
        )

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email address"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        st.write("")

        submitted = st.form_submit_button(
            "➔ Sign In",
            use_container_width=True
        )

    # ---------------------------------------------------------
    # LOGIN CHECK
    # ---------------------------------------------------------
    if submitted:
        if not email.strip() or not password:
            st.session_state.login_failed = False
            st.error("Please enter your email and password.")
        else:
            user = authenticate_user(
                email.strip(),
                password
            )

            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.session_state.login_failed = False
                st.rerun()
            else:
                st.session_state.login_failed = True

    # ---------------------------------------------------------
    # WRONG LOGIN MESSAGE
    # ---------------------------------------------------------
    if st.session_state.get("login_failed", False):
        st.error("Invalid email or password.")

        if st.button("🔐 Forgot Password?", use_container_width=True, key="forgot_pass_btn"):
            st.switch_page("pages/forgot_password.py")

    # ---------------------------------------------------------
    # CREATE ACCOUNT
    # ---------------------------------------------------------
    st.write("")
    st.caption("Don't have an account?")

    st.markdown('<div class="create-account">', unsafe_allow_html=True)

    if st.button("Create Account", use_container_width=True, key="create_acc_btn"):
        st.switch_page("pages/register.py")

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # SECURITY NOTE
    # ---------------------------------------------------------
    st.markdown(
        """<div class="secure-note">
            🔒 CareMate AI system ready • Secure personal health workspace
        </div>""",
        unsafe_allow_html=True
    )