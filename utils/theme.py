import streamlit as st


def apply_caremate_theme():

    st.markdown(
        """
        <style>

        /* =====================================================
           GLOBAL
        ===================================================== */

        .stApp {
            background:
                radial-gradient(
                    circle at 80% 0%,
                    rgba(37, 99, 235, 0.16),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 10% 20%,
                    rgba(6, 182, 212, 0.08),
                    transparent 25%
                ),
                #07111F;

            color: #F8FAFC;
            font-family:
                Inter,
                "Segoe UI",
                Arial,
                sans-serif;
        }

        .main .block-container {
            max-width: 1500px;
            padding-top: 2rem;
            padding-bottom: 4rem;
            padding-left: 2.5rem;
            padding-right: 2.5rem;
        }


        /* =====================================================
           SIDEBAR
           ===================================================== */

        section[data-testid="stSidebar"] {
            background:
                linear-gradient(
                    180deg,
                    #081421 0%,
                    #0A1626 100%
                );

            border-right: 1px solid #1D3047;
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 1.4rem;
        }

        section[data-testid="stSidebar"] * {
            color: #CBD5E1 !important;
        }

        section[data-testid="stSidebar"] [data-testid="stNavLink"] {
            border-radius: 11px;
            margin: 4px 7px;
            transition: 0.2s ease;
        }

        section[data-testid="stSidebar"]
        [data-testid="stNavLink"]:hover {
            background: #10233B;
            color: #60A5FA !important;
        }

        section[data-testid="stSidebar"]
        [data-testid="stNavLink"][aria-current="page"] {
            background:
                linear-gradient(
                    90deg,
                    #12345A,
                    #10253E
                );

            color: #60A5FA !important;
            font-weight: 700;

            border-left: 3px solid #38BDF8;
        }


        /* =====================================================
           TEXT
           ===================================================== */

        h1,
        h2,
        h3,
        h4 {
            color: #F8FAFC !important;
        }

        p {
            color: #CBD5E1;
        }

        .stCaption {
            color: #94A3B8 !important;
        }


        /* =====================================================
           HERO
           ===================================================== */

        .cm-hero {
            position: relative;

            background:
                linear-gradient(
                    135deg,
                    #0D2036 0%,
                    #0B1728 50%,
                    #102C49 100%
                );

            border: 1px solid #244766;
            border-radius: 22px;

            padding: 30px 32px;
            margin-bottom: 24px;

            box-shadow:
                0 10px 40px rgba(0, 0, 0, 0.25),
                inset 0 1px 0 rgba(255,255,255,0.03);

            overflow: hidden;
        }

        .cm-hero:after {
            content: "";

            position: absolute;

            width: 240px;
            height: 240px;

            right: -70px;
            top: -100px;

            border-radius: 50%;

            background:
                radial-gradient(
                    circle,
                    rgba(56,189,248,0.22),
                    transparent 65%
                );
        }

        .cm-hero-title {
            color: #FFFFFF;

            font-size: 30px;
            font-weight: 800;

            position: relative;
            z-index: 2;
        }

        .cm-hero-subtitle {
            color: #AFC3D8;

            font-size: 14px;
            margin-top: 7px;

            position: relative;
            z-index: 2;
        }


        /* =====================================================
           AI STATUS
           ===================================================== */

        .cm-ai-status {
            display: inline-flex;

            align-items: center;

            gap: 7px;

            background: #0B2B27;

            border: 1px solid #17665A;

            color: #5EEAD4;

            padding: 6px 11px;

            border-radius: 20px;

            font-size: 12px;

            font-weight: 700;

            margin-bottom: 12px;
        }

        .cm-online-dot {
            width: 7px;
            height: 7px;

            background: #34D399;

            border-radius: 50%;

            box-shadow:
                0 0 10px #34D399;
        }


        /* =====================================================
           CARDS
           ===================================================== */

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background:
                linear-gradient(
                    145deg,
                    #0D1B2D,
                    #0A1726
                );

            border: 1px solid #1E344B;

            border-radius: 17px;

            box-shadow:
                0 8px 30px rgba(0,0,0,0.20);
        }


        /* =====================================================
           METRIC CARDS
           ===================================================== */

        [data-testid="stMetric"] {
            background:
                linear-gradient(
                    145deg,
                    #0E2034,
                    #0A1726
                );

            border: 1px solid #1F3A54;

            border-radius: 16px;

            padding: 18px 20px;

            min-height: 120px;

            box-shadow:
                0 7px 25px rgba(0,0,0,0.22);
        }

        [data-testid="stMetricLabel"] {
            color: #94A3B8 !important;

            font-size: 13px;

            font-weight: 600;
        }

        [data-testid="stMetricValue"] {
            color: #F8FAFC !important;

            font-size: 28px;

            font-weight: 800;
        }

        [data-testid="stMetricDelta"] {
            color: #5EEAD4 !important;
        }


        /* =====================================================
           AI CARD
           ===================================================== */

        .cm-ai-card {
            background:
                radial-gradient(
                    circle at 90% 10%,
                    rgba(59,130,246,0.25),
                    transparent 28%
                ),
                linear-gradient(
                    135deg,
                    #102A48,
                    #0A1728
                );

            border: 1px solid #28557C;

            border-radius: 20px;

            padding: 25px;

            box-shadow:
                0 12px 40px rgba(0,0,0,0.30),
                0 0 35px rgba(37,99,235,0.08);
        }

        .cm-ai-title {
            color: #FFFFFF;

            font-size: 23px;

            font-weight: 800;
        }

        .cm-ai-text {
            color: #AFC3D8;

            font-size: 14px;

            margin-top: 5px;
        }


        /* =====================================================
           AI INPUT
           ===================================================== */

        div[data-baseweb="input"] {
            background: #0A1726 !important;

            border: 1px solid #294762 !important;

            border-radius: 11px !important;
        }

        div[data-baseweb="input"] input {
            color: #F8FAFC !important;
        }

        textarea {
            background: #0A1726 !important;

            color: #F8FAFC !important;

            border: 1px solid #294762 !important;

            border-radius: 11px !important;
        }


        /* =====================================================
           SELECTBOX
           ===================================================== */

        div[data-baseweb="select"] {
            background: #0A1726 !important;

            border-radius: 10px;
        }


        /* =====================================================
           BUTTONS
           ===================================================== */

        .stButton > button {
            background: #0D1C2D;

            color: #E2E8F0;

            border: 1px solid #28445E;

            border-radius: 11px;

            min-height: 44px;

            font-weight: 650;

            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            background: #12304D;

            color: #FFFFFF;

            border-color: #38BDF8;

            box-shadow:
                0 0 18px rgba(56,189,248,0.12);
        }

        .stButton > button[kind="primary"] {
            background:
                linear-gradient(
                    135deg,
                    #2563EB,
                    #0891B2
                );

            color: #FFFFFF;

            border: none;

            box-shadow:
                0 6px 20px rgba(37,99,235,0.25);
        }

        .stButton > button[kind="primary"]:hover {
            background:
                linear-gradient(
                    135deg,
                    #3B82F6,
                    #06B6D4
                );

            color: #FFFFFF;
        }


        /* =====================================================
           INFO / SUCCESS
           ===================================================== */

        [data-testid="stAlert"] {
            background: #0D2034 !important;

            border: 1px solid #234968 !important;

            color: #CBD5E1 !important;

            border-radius: 12px;
        }


        /* =====================================================
           DIVIDER
           ===================================================== */

        hr {
            border-color: #1E344B !important;
        }


        /* =====================================================
           DATAFRAME
           ===================================================== */

        [data-testid="stDataFrame"] {
            border: 1px solid #1E344B;

            border-radius: 12px;

            overflow: hidden;
        }


        /* =====================================================
           CHAT WELCOME
           ===================================================== */

        .cm-chat-welcome {
            background:
                linear-gradient(
                    135deg,
                    #0E2944,
                    #0B192A
                );

            border: 1px solid #245278;

            border-radius: 18px;

            padding: 23px;

            margin-top: 18px;
        }


        /* =====================================================
           RESPONSIVE
           ===================================================== */

        @media (max-width: 900px) {

            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .cm-hero-title {
                font-size: 24px;
            }

        }

        </style>
        """,
        unsafe_allow_html=True
    )