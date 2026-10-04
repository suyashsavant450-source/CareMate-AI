import streamlit as st
import pandas as pd
from datetime import date

from database import get_connection
from utils.helpers import require_login


# =========================================================
# LOGIN
# =========================================================

user = require_login()
user_id = user["id"]


# =========================================================
# PAGE CONFIG
# =========================================================

st.title("📊 Health Progress")

st.caption(
    "Track your daily health habits, medicine adherence "
    "and health activity over time."
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .progress-card {
        background: linear-gradient(
            145deg,
            rgba(15, 23, 42, 0.95),
            rgba(30, 41, 59, 0.90)
        );
        border: 1px solid rgba(96,165,250,0.20);
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 10px;
    }

    .metric-label {
        color: #94a3b8;
        font-size: 13px;
        font-weight: 600;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 27px;
        font-weight: 800;
        margin-top: 4px;
    }

    .metric-sub {
        color: #64748b;
        font-size: 12px;
        margin-top: 3px;
    }

    .insight-card {
        background: rgba(15,23,42,0.70);
        border-left: 4px solid #60a5fa;
        border-radius: 10px;
        padding: 14px 16px;
        margin: 8px 0;
        color: #e2e8f0;
    }

    .section-title {
        font-size: 21px;
        font-weight: 750;
        margin-top: 25px;
        margin-bottom: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD HEALTH DATA
# =========================================================

connection = get_connection()

records = connection.execute(
    """
    SELECT
        tracking_date,
        water_intake,
        sleep_hours,
        exercise_minutes
    FROM health_tracking
    WHERE user_id = ?
    ORDER BY tracking_date ASC
    """,
    (user_id,)
).fetchall()

connection.close()


# =========================================================
# TODAY'S TRACKING
# =========================================================

st.markdown(
    '<div class="section-title">📝 Today\'s Tracking</div>',
    unsafe_allow_html=True
)

today = date.today().isoformat()


# Existing today's values
today_record = None

for row in records:
    if row["tracking_date"] == today:
        today_record = row
        break


default_water = (
    float(today_record["water_intake"])
    if today_record else 0.0
)

default_sleep = (
    float(today_record["sleep_hours"])
    if today_record else 0.0
)

default_exercise = (
    int(today_record["exercise_minutes"])
    if today_record else 0
)


col1, col2, col3 = st.columns(3)


with col1:

    water = st.number_input(
        "💧 Water (Litres)",
        min_value=0.0,
        max_value=20.0,
        value=default_water,
        step=0.25
    )


with col2:

    sleep = st.number_input(
        "😴 Sleep (Hours)",
        min_value=0.0,
        max_value=24.0,
        value=default_sleep,
        step=0.5
    )


with col3:

    exercise = st.number_input(
        "🚶 Exercise (Minutes)",
        min_value=0,
        max_value=600,
        value=default_exercise,
        step=5
    )


if st.button(
    "💾 Save Today's Progress",
    type="primary",
    use_container_width=True
):

    connection = get_connection()

    existing = connection.execute(
        """
        SELECT id
        FROM health_tracking
        WHERE user_id = ?
        AND tracking_date = ?
        """,
        (
            user_id,
            today
        )
    ).fetchone()

    if existing:

        connection.execute(
            """
            UPDATE health_tracking
            SET water_intake = ?,
                sleep_hours = ?,
                exercise_minutes = ?
            WHERE id = ?
            AND user_id = ?
            """,
            (
                water,
                sleep,
                exercise,
                existing["id"],
                user_id
            )
        )

    else:

        connection.execute(
            """
            INSERT INTO health_tracking
            (
                user_id,
                water_intake,
                sleep_hours,
                exercise_minutes,
                tracking_date
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                water,
                sleep,
                exercise,
                today
            )
        )

    connection.commit()
    connection.close()

    st.success(
        "✅ Today's progress saved successfully."
    )

    st.rerun()


# =========================================================
# RELOAD DATA AFTER SAVE
# =========================================================

connection = get_connection()

records = connection.execute(
    """
    SELECT
        tracking_date,
        water_intake,
        sleep_hours,
        exercise_minutes
    FROM health_tracking
    WHERE user_id = ?
    ORDER BY tracking_date ASC
    """,
    (user_id,)
).fetchall()

connection.close()


# =========================================================
# DATAFRAME
# =========================================================

if records:

    data = [
        {
            "Date": row["tracking_date"],
            "Water": float(row["water_intake"] or 0),
            "Sleep": float(row["sleep_hours"] or 0),
            "Exercise": int(row["exercise_minutes"] or 0)
        }
        for row in records
    ]

    df = pd.DataFrame(data)

    df["Date"] = pd.to_datetime(
        df["Date"]
    )

else:

    df = pd.DataFrame(
        columns=[
            "Date",
            "Water",
            "Sleep",
            "Exercise"
        ]
    )


# =========================================================
# OVERVIEW
# =========================================================

st.markdown(
    '<div class="section-title">📌 Health Overview</div>',
    unsafe_allow_html=True
)


if not df.empty:

    latest = df.iloc[-1]

    avg_water = df["Water"].mean()
    avg_sleep = df["Sleep"].mean()
    avg_exercise = df["Exercise"].mean()

    overview1, overview2, overview3, overview4 = st.columns(4)

    with overview1:

        st.markdown(
            f"""
            <div class="progress-card">
                <div class="metric-label">💧 Latest Water</div>
                <div class="metric-value">
                    {latest["Water"]:.2f} L
                </div>
                <div class="metric-sub">
                    Avg: {avg_water:.2f} L
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with overview2:

        st.markdown(
            f"""
            <div class="progress-card">
                <div class="metric-label">😴 Latest Sleep</div>
                <div class="metric-value">
                    {latest["Sleep"]:.1f} hrs
                </div>
                <div class="metric-sub">
                    Avg: {avg_sleep:.1f} hrs
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with overview3:

        st.markdown(
            f"""
            <div class="progress-card">
                <div class="metric-label">🚶 Latest Exercise</div>
                <div class="metric-value">
                    {latest["Exercise"]} min
                </div>
                <div class="metric-sub">
                    Avg: {avg_exercise:.0f} min
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with overview4:

        st.markdown(
            f"""
            <div class="progress-card">
                <div class="metric-label">📅 Tracking Days</div>
                <div class="metric-value">
                    {len(df)}
                </div>
                <div class="metric-sub">
                    Recorded days
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


else:

    st.info(
        "Start tracking your health to see your dashboard."
    )


# =========================================================
# PERIOD FILTER
# =========================================================

st.markdown(
    '<div class="section-title">📈 Health Trends</div>',
    unsafe_allow_html=True
)


period = st.radio(
    "Select period",
    [
        "7 Days",
        "30 Days",
        "All Time"
    ],
    horizontal=True
)


if not df.empty:

    if period == "7 Days":

        chart_df = df.tail(7)

    elif period == "30 Days":

        chart_df = df.tail(30)

    else:

        chart_df = df.copy()


# =========================================================
# WATER GRAPH
# =========================================================

if not df.empty:

    st.markdown("### 💧 Water Intake Trend")

    water_chart = chart_df[
        ["Date", "Water"]
    ].copy()

    water_chart = water_chart.set_index(
        "Date"
    )

    st.line_chart(
        water_chart,
        y="Water",
        height=280
    )


# =========================================================
# SLEEP GRAPH
# =========================================================

if not df.empty:

    st.markdown("### 😴 Sleep Trend")

    sleep_chart = chart_df[
        ["Date", "Sleep"]
    ].copy()

    sleep_chart = sleep_chart.set_index(
        "Date"
    )

    st.line_chart(
        sleep_chart,
        y="Sleep",
        height=280
    )


# =========================================================
# EXERCISE GRAPH
# =========================================================

if not df.empty:

    st.markdown("### 🚶 Exercise Activity")

    exercise_chart = chart_df[
        ["Date", "Exercise"]
    ].copy()

    exercise_chart = exercise_chart.set_index(
        "Date"
    )

    st.bar_chart(
        exercise_chart,
        y="Exercise",
        height=280
    )


# =========================================================
# DAILY GOALS
# =========================================================

st.markdown(
    '<div class="section-title">🎯 Daily Health Goals</div>',
    unsafe_allow_html=True
)


goal_col1, goal_col2, goal_col3 = st.columns(3)


WATER_GOAL = 2.5
SLEEP_GOAL = 8.0
EXERCISE_GOAL = 30


with goal_col1:

    water_percent = min(
        (water / WATER_GOAL) * 100,
        100
    )

    st.metric(
        "💧 Water Goal",
        f"{water:.2f} / {WATER_GOAL} L"
    )

    st.progress(
        int(water_percent)
    )

    st.caption(
        f"{water_percent:.0f}% of daily goal"
    )


with goal_col2:

    sleep_percent = min(
        (sleep / SLEEP_GOAL) * 100,
        100
    )

    st.metric(
        "😴 Sleep Goal",
        f"{sleep:.1f} / {SLEEP_GOAL} hrs"
    )

    st.progress(
        int(sleep_percent)
    )

    st.caption(
        f"{sleep_percent:.0f}% of daily goal"
    )


with goal_col3:

    exercise_percent = min(
        (exercise / EXERCISE_GOAL) * 100,
        100
    )

    st.metric(
        "🚶 Exercise Goal",
        f"{exercise} / {EXERCISE_GOAL} min"
    )

    st.progress(
        int(exercise_percent)
    )

    st.caption(
        f"{exercise_percent:.0f}% of daily goal"
    )


# =========================================================
# MEDICINE ADHERENCE
# =========================================================

st.markdown(
    '<div class="section-title">💊 Medicine Adherence</div>',
    unsafe_allow_html=True
)


connection = get_connection()

medicine_logs = connection.execute(
    """
    SELECT status
    FROM medicine_logs
    WHERE user_id = ?
    """,
    (user_id,)
).fetchall()

connection.close()


if medicine_logs:

    medicine_df = pd.DataFrame(
        [
            {
                "Status": row["status"]
            }
            for row in medicine_logs
        ]
    )

    total_medicines = len(medicine_df)

    taken_count = len(
        medicine_df[
            medicine_df["Status"] == "taken"
        ]
    )

    missed_count = len(
        medicine_df[
            medicine_df["Status"] == "missed"
        ]
    )

    pending_count = len(
        medicine_df[
            medicine_df["Status"] == "pending"
        ]
    )

    adherence = (
        taken_count / total_medicines * 100
        if total_medicines > 0
        else 0
    )

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "💊 Total",
            total_medicines
        )

    with m2:
        st.metric(
            "✅ Taken",
            taken_count
        )

    with m3:
        st.metric(
            "❌ Missed",
            missed_count
        )

    with m4:
        st.metric(
            "📊 Adherence",
            f"{adherence:.0f}%"
        )

    st.progress(
        int(min(adherence, 100))
    )

else:

    st.info(
        "No medicine tracking data available yet."
    )


# =========================================================
# HEALTH INSIGHTS
# =========================================================

st.markdown(
    '<div class="section-title">🧠 CareMate Health Insights</div>',
    unsafe_allow_html=True
)


if not df.empty:

    insights = []

    # Water insight
    if latest["Water"] > avg_water:

        insights.append(
            "💧 Your latest recorded water intake "
            "is above your recorded average."
        )

    elif latest["Water"] < avg_water:

        insights.append(
            "💧 Your latest recorded water intake "
            "is below your recorded average."
        )

    else:

        insights.append(
            "💧 Your latest water intake is close "
            "to your recorded average."
        )


    # Sleep insight
    if latest["Sleep"] > avg_sleep:

        insights.append(
            "😴 Your latest recorded sleep duration "
            "is above your recorded average."
        )

    elif latest["Sleep"] < avg_sleep:

        insights.append(
            "😴 Your latest recorded sleep duration "
            "is below your recorded average."
        )

    else:

        insights.append(
            "😴 Your latest sleep duration is close "
            "to your recorded average."
        )


    # Exercise insight
    if latest["Exercise"] > avg_exercise:

        insights.append(
            "🚶 Your latest recorded exercise time "
            "is above your recorded average."
        )

    elif latest["Exercise"] < avg_exercise:

        insights.append(
            "🚶 Your latest recorded exercise time "
            "is below your recorded average."
        )

    else:

        insights.append(
            "🚶 Your latest exercise time is close "
            "to your recorded average."
        )


    for insight in insights:

        st.markdown(
            f"""
            <div class="insight-card">
                {insight}
            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.info(
        "Add a few days of tracking to generate insights."
    )


# =========================================================
# BEST RECORDED DAY
# =========================================================

if not df.empty:

    st.markdown(
        '<div class="section-title">🏆 Personal Tracking Highlights</div>',
        unsafe_allow_html=True
    )

    best_exercise_index = df[
        "Exercise"
    ].idxmax()

    best_exercise_day = df.loc[
        best_exercise_index
    ]

    h1, h2, h3 = st.columns(3)

    with h1:

        st.metric(
            "🚶 Highest Exercise",
            f"{best_exercise_day['Exercise']:.0f} min"
        )

        st.caption(
            best_exercise_day["Date"].strftime(
                "%d %b %Y"
            )
        )

    with h2:

        best_water_index = df[
            "Water"
        ].idxmax()

        best_water_day = df.loc[
            best_water_index
        ]

        st.metric(
            "💧 Highest Water",
            f"{best_water_day['Water']:.2f} L"
        )

        st.caption(
            best_water_day["Date"].strftime(
                "%d %b %Y"
            )
        )

    with h3:

        best_sleep_index = df[
            "Sleep"
        ].idxmax()

        best_sleep_day = df.loc[
            best_sleep_index
        ]

        st.metric(
            "😴 Highest Sleep",
            f"{best_sleep_day['Sleep']:.1f} hrs"
        )

        st.caption(
            best_sleep_day["Date"].strftime(
                "%d %b %Y"
            )
        )


# =========================================================
# RECENT HISTORY
# =========================================================

st.markdown(
    '<div class="section-title">📅 Recent Progress</div>',
    unsafe_allow_html=True
)


if not df.empty:

    history_df = df.copy()

    history_df["Date"] = history_df[
        "Date"
    ].dt.strftime(
        "%d %b %Y"
    )

    history_df = history_df.rename(
        columns={
            "Date": "Date",
            "Water": "💧 Water (L)",
            "Sleep": "😴 Sleep (hrs)",
            "Exercise": "🚶 Exercise (min)"
        }
    )

    history_df = history_df.sort_values(
        "Date",
        ascending=False
    )

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No progress records yet."
    )


# =========================================================
# FOOTER
# =========================================================

st.caption(
    "CareMate AI tracks the information you record. "
    "These insights are informational and are not a medical diagnosis."
)