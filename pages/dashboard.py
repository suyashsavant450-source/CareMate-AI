from datetime import date, datetime
import pandas as pd
import plotly.express as px
import streamlit as st

from database import get_connection
from utils.helpers import require_login

# =====================================================
# 1. USER AUTHENTICATION & LOGIN
# =====================================================
user = require_login()
user_id = user["id"]
user_name = user["name"]

# =====================================================
# 2. DYNAMIC GREETING
# =====================================================
hour = datetime.now().hour
if hour < 12:
    greeting = "Good Morning"
elif hour < 17:
    greeting = "Good Afternoon"
else:
    greeting = "Good Evening"

# =====================================================
# 3. DATABASE QUERIES (SAFE FETCHING)
# =====================================================
connection = get_connection()

try:
    report_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM medical_reports
        WHERE user_id = ?
        """,
        (user_id,),
    ).fetchone()[0]

    medicine_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM medicines
        WHERE user_id = ?
        AND active = 1
        """,
        (user_id,),
    ).fetchone()[0]

    caregiver_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM caregivers
        WHERE patient_id = ?
        """,
        (user_id,),
    ).fetchone()[0]

    tracking_records = connection.execute(
        """
        SELECT tracking_date,
               water_intake,
               sleep_hours,
               exercise_minutes
        FROM health_tracking
        WHERE user_id = ?
        ORDER BY tracking_date ASC
        LIMIT 30
        """,
        (user_id,),
    ).fetchall()

    medicines = connection.execute(
        """
        SELECT medicine_name,
               dosage,
               reminder_time,
               frequency
        FROM medicines
        WHERE user_id = ?
        AND active = 1
        ORDER BY reminder_time
        LIMIT 5
        """,
        (user_id,),
    ).fetchall()

    recent_reports = connection.execute(
        """
        SELECT file_name, uploaded_at
        FROM medical_reports
        WHERE user_id = ?
        ORDER BY uploaded_at DESC
        LIMIT 5
        """,
        (user_id,),
    ).fetchall()

finally:
    connection.close()

# =====================================================
# 4. TODAY'S METRIC COMPUTATION
# =====================================================
today = date.today().isoformat()
today_record = None

for row in tracking_records:
    if row["tracking_date"] == today:
        today_record = row
        break

water_today = float(today_record["water_intake"]) if today_record else 0.0
sleep_today = float(today_record["sleep_hours"]) if today_record else 0.0

# =====================================================
# 5. HERO SECTION
# =====================================================
st.markdown(
    f"""
    <div class="cm-hero">
        <div style="background: rgba(255,255,255,0.2); backdrop-filter: blur(8px); display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; color: #FFF; margin-bottom: 10px;">
            ✨ AI Health Guardian Active
        </div>
        <div class="cm-hero-title">
            {greeting}, {user_name} 👋
        </div>
        <div class="cm-hero-subtitle">
            Here is your health overview for today. Stay consistent, stay informed.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# 6. STATS METRICS ROW
# =====================================================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        label="📄 Medical Reports",
        value=report_count,
        delta="Analyzed Reports",
    )

with c2:
    st.metric(
        label="💊 Active Medicines",
        value=medicine_count,
        delta="Daily Routine",
    )

with c3:
    st.metric(
        label="💧 Water Intake",
        value=f"{water_today:.1f} L",
        delta="Target: 2.5 L",
    )

with c4:
    st.metric(
        label="😴 Sleep Recorded",
        value=f"{sleep_today:.1f} hrs",
        delta="Target: 8.0 hrs",
    )

st.write("")

# =====================================================
# 7. HEALTH TREND & ROUTINE
# =====================================================
left, right = st.columns([2, 1])

# ---------------- HEALTH TREND ----------------
with left:
    st.subheader("📈 Health & Vital Trends")

    with st.container(border=True):
        if tracking_records:
            chart_data = pd.DataFrame(
                [
                    {
                        "Date": row["tracking_date"],
                        "Water Intake (L)": float(row["water_intake"]),
                        "Sleep (Hours)": float(row["sleep_hours"]),
                        "Exercise (Mins)": int(row["exercise_minutes"]),
                    }
                    for row in tracking_records
                ]
            )

            metric = st.selectbox(
                "Select Health Metric",
                ["Water Intake (L)", "Sleep (Hours)", "Exercise (Mins)"],
            )

            # Interactive Plotly Chart
            fig = px.line(
                chart_data,
                x="Date",
                y=metric,
                markers=True,
                color_discrete_sequence=["#2563EB"],
            )

            fig.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis_title=None,
                yaxis_title=metric,
                height=290,
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(
                "📈 No health tracking data yet. "
                "Start tracking water, sleep, and exercise to see your personal trends."
            )

# ---------------- ROUTINE ----------------
with right:
    st.subheader("📅 Today's Routine")

    with st.container(border=True):
        if medicines:
            for medicine in medicines:
                dosage = medicine["dosage"] or "Not specified"
                reminder = medicine["reminder_time"] or "Not set"
                frequency = medicine["frequency"] or ""

                st.markdown(f"**💊 {medicine['medicine_name']}**")
                st.caption(f"🕐 {reminder}  •  {frequency}")
                st.write(f"Dosage: **{dosage}**")
                st.divider()
        else:
            st.info("🌿 No medicines scheduled for today.\n\nYour routine will appear here.")

# =====================================================
# 8. ACTIVITY & PROFILE
# =====================================================
left2, right2 = st.columns([1.4, 1])

# ---------------- ACTIVITY ----------------
with left2:
    st.subheader("🕘 Recent Health Activity")

    with st.container(border=True):
        if recent_reports:
            for report in recent_reports:
                file_name = report["file_name"] or "Medical report"
                st.markdown("📄 **Medical report uploaded**")
                st.caption(file_name)
                st.divider()

        if medicine_count > 0:
            st.markdown("💊 **Medicine routine active**")
            st.caption(f"{medicine_count} active medicine(s)")
            st.divider()

        if tracking_records:
            st.markdown("📊 **Health progress recorded**")
            st.caption(f"{len(tracking_records)} day(s) tracked")

        if not recent_reports and medicine_count == 0 and not tracking_records:
            st.info("No recent health activity recorded yet.")

# ---------------- PROFILE ----------------
with right2:
    st.subheader("👤 Patient Profile")

    with st.container(border=True):
        first_letter = user_name.strip()[0].upper() if user_name.strip() else "U"

        st.markdown(
            f"""
            <div style="
                width:56px;
                height:56px;
                border-radius:50%;
                background: linear-gradient(135deg, #2563EB, #1D4ED8);
                color:#FFFFFF;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:22px;
                font-weight:700;
                margin-bottom:12px;
                box-shadow: 0 4px 10px rgba(37,99,235,0.3);
            ">
                {first_letter}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(f"### {user_name}")
        st.caption("Active Health Account")
        st.divider()

        p1, p2 = st.columns(2)
        with p1:
            st.metric("Reports", report_count)
        with p2:
            st.metric("Medicines", medicine_count)

        st.metric("Assigned Caregivers", caregiver_count)

# =====================================================
# 9. QUICK ACTIONS
# =====================================================
st.write("")
st.subheader("⚡ Quick Actions")

q1, q2, q3, q4 = st.columns(4)

with q1:
    if st.button("📄 Upload Report", use_container_width=True):
        st.switch_page("pages/upload_report.py")

with q2:
    if st.button("💊 Add Medicine", use_container_width=True):
        st.switch_page("pages/medicines.py")

with q3:
    if st.button("🤖 Ask CareMate", use_container_width=True):
        st.switch_page("pages/caremate.py")

with q4:
    if st.button("📊 Track Health", use_container_width=True):
        st.switch_page("pages/progress.py")

# =====================================================
# 10. CAREMATE AI CARD
# =====================================================
st.write("")

st.markdown(
    f"""
    <div class="cm-chat-card">
        <div class="cm-chat-title">🤖 CareMate AI Assistant</div>
        <div class="cm-chat-text">
            Hi <b>{user_name}</b>, I am ready to analyze your medical reports, track symptoms, or answer your healthcare questions!
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
if st.button("Open CareMate AI Chatbot →", type="primary"):
    st.switch_page("pages/caremate.py")