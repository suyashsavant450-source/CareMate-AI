import re
import streamlit as st
from database import create_user

if st.session_state.get("logged_in", False):
    st.stop()

st.set_page_config(
    page_title="Create Account | CareMate AI",
    page_icon="🏥",
    layout="wide"
)

# Premium Neon & Glassmorphism Styling
st.markdown(
    """<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes pulseGlow {
        0%, 100% { opacity: 0.4; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.05); }
    }

    .stApp {
        background: radial-gradient(circle at 15% 15%, rgba(14, 165, 233, 0.15) 0%, transparent 40%),
                    radial-gradient(circle at 85% 85%, rgba(139, 92, 246, 0.15) 0%, transparent 40%),
                    #030712 !important;
        color: #f8fafc;
    }

    .main .block-container {
        max-width: 1280px !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Animated Header */
    .project-header-container {
        text-align: center;
        margin-bottom: 35px;
    }

    .project-main-title {
        font-size: 34px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientBG 6s ease infinite;
        text-shadow: 0 0 30px rgba(56, 189, 248, 0.2);
    }

    /* Left Visual Panel */
    .brand-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 18px;
        border-radius: 9999px;
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.3);
        color: #38bdf8;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.15);
    }

    .brand-title {
        font-size: 40px;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.15;
        margin-bottom: 16px;
    }

    .brand-title span {
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .brand-description {
        font-size: 15px;
        line-height: 1.6;
        color: #94a3b8;
        margin-bottom: 30px;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
    }

    .feature-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 14px;
        display: flex;
        align-items: center;
        gap: 12px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .feature-card:hover {
        border-color: rgba(56, 189, 248, 0.4);
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
    }

    .feature-icon-box {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    .icon-blue { background: linear-gradient(135deg, #0284c7, #0369a1); }
    .icon-purple { background: linear-gradient(135deg, #7c3aed, #6d28d9); }
    .icon-indigo { background: linear-gradient(135deg, #4f46e5, #4338ca); }
    .icon-amber { background: linear-gradient(135deg, #d97706, #b45309); }
    .icon-emerald { background: linear-gradient(135deg, #059669, #047857); }
    .icon-teal { background: linear-gradient(135deg, #0d9488, #0f766e); }

    .feature-title {
        color: #f8fafc;
        font-size: 13px;
        font-weight: 700;
    }

    .feature-text {
        color: #64748b;
        font-size: 11px;
    }

    /* Premium Glass Form Card */
    div[data-testid="stForm"] {
        background: rgba(15, 23, 42, 0.75) !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        border-radius: 24px !important;
        padding: 32px !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 0 0 40px rgba(56, 189, 248, 0.08) !important;
        backdrop-filter: blur(16px);
    }

    .login-heading {
        font-size: 26px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 4px;
    }

    .login-caption {
        color: #94a3b8;
        font-size: 13px;
        margin-bottom: 20px;
    }

    div[data-testid="stForm"] label {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    div[data-testid="stForm"] input {
        background: rgba(2, 6, 23, 0.7) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        height: 42px !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="stForm"] input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.3) !important;
    }

    /* Submit Button Glow */
    div[data-testid="stFormSubmitButton"] button {
        height: 46px !important;
        border-radius: 12px !important;
        border: none !important;
        color: white !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #0284c7, #6366f1, #9333ea) !important;
        background-size: 200% auto !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4) !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="stFormSubmitButton"] button:hover {
        background-position: right center !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(147, 51, 234, 0.5) !important;
    }

    .back-btn .stButton > button {
        height: 42px !important;
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #94a3b8 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }

    .back-btn .stButton > button:hover {
        border-color: #38bdf8 !important;
        color: #38bdf8 !important;
        background: rgba(30, 41, 59, 0.8) !important;
    }

    .secure-footer {
        text-align: center;
        color: #475569;
        font-size: 11px;
        margin-top: 20px;
    }
    </style>""",
    unsafe_allow_html=True
)

st.markdown(
    """<div class="project-header-container">
        <div class="project-main-title">✨ AI Medical Report Simplifier & CareMate</div>
    </div>""",
    unsafe_allow_html=True
)

left, right = st.columns([1.1, 0.9], gap="large")

with left:
    st.markdown(
        """<div>
            <div class="brand-badge"><span>⚡ NEXT-GEN HEALTHCARE AI</span></div>
            <div class="brand-title">Simplify Health with <span>CareMate AI</span></div>
            <div class="brand-description">
                Experience intelligence in medical analysis. Transform complex medical jargon into clear, actionable, and personal health insights instantly.
            </div>
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-icon-box icon-blue">📄</div>
                    <div>
                        <div class="feature-title">Smart OCR Analysis</div>
                        <div class="feature-text">Instant report parsing</div>
                    </div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon-box icon-purple">💊</div>
                    <div>
                        <div class="feature-title">Meds Tracker</div>
                        <div class="feature-text">Smart daily reminders</div>
                    </div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon-box icon-indigo">🤖</div>
                    <div>
                        <div class="feature-title">Care Assistant</div>
                        <div class="feature-text">24/7 AI health guidance</div>
                    </div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon-box icon-amber">👨‍👩‍👧</div>
                    <div>
                        <div class="feature-title">Caregiver Hub</div>
                        <div class="feature-text">Family access & alerts</div>
                    </div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon-box icon-emerald">📊</div>
                    <div>
                        <div class="feature-title">Vitals Tracker</div>
                        <div class="feature-text">Real-time health trends</div>
                    </div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon-box icon-teal">🌐</div>
                    <div>
                        <div class="feature-title">Multilingual</div>
                        <div class="feature-text">Supports local languages</div>
                    </div>
                </div>
            </div>
        </div>""",
        unsafe_allow_html=True
    )

with right:
    with st.form("register_form"):
        st.markdown('<div class="login-heading">Create Account</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-caption">Join CareMate AI for personalized health tracking.</div>', unsafe_allow_html=True)

        name = st.text_input("Full Name", placeholder="e.g. John Doe")
        email = st.text_input("Email Address", placeholder="name@example.com")
        phone = st.text_input("Phone Number", placeholder="+91 9876543210")
        password = st.text_input("Password", type="password", placeholder="Min 6 characters")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")

        st.write("")
        submitted = st.form_submit_button("🚀 Get Started Free", use_container_width=True)

if submitted:
    name_clean = name.strip()
    email_clean = email.strip().lower()
    phone_clean = phone.strip()

    if not all([name_clean, email_clean, phone_clean, password, confirm_password]):
        st.error("Please fill in all fields.")
    elif len(name_clean) < 2:
        st.error("Please enter a valid full name.")
    elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email_clean):
        st.error("Please enter a valid email address.")
    elif not re.fullmatch(r"(?:\+91[\s-]?)?[6-9]\d{9}", phone_clean):
        st.error("Please enter a valid Indian mobile number.")
    elif len(password) < 6:
        st.error("Password must contain at least 6 characters.")
    elif password != confirm_password:
        st.error("Passwords do not match.")
    else:
        success, user_id, message = create_user(name_clean, email_clean, phone_clean, password)
        if success:
            st.success("🎉 Account created successfully!")
            if st.button("🔐 Go to Login", use_container_width=True):
                st.switch_page("pages/login.py")
        else:
            st.error(message)

st.write("")
st.markdown('<div class="back-btn">', unsafe_allow_html=True)
if st.button("← Already have an account? Sign In", use_container_width=True):
    st.switch_page("pages/login.py")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    """<div class="secure-footer">
        🛡️ End-to-End Encrypted • HIPAA Compliant Storage Standards
    </div>""",
    unsafe_allow_html=True
)