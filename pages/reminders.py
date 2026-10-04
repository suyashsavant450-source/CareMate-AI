import streamlit as st
from datetime import date

from utils.helpers import require_login

from database import (
    get_user_reminders,
    mark_reminder_read,
    delete_reminder,
    get_medicine_logs,
    mark_medicine_taken,
    add_reminder,
)


# =========================================================
# LOGIN
# =========================================================

user = require_login()

user_id = user["id"]


# =========================================================
# PAGE HEADER
# =========================================================

st.title("🔔 Reminders")

st.caption(
    "Medicine reminders, caregiver alerts and health notifications"
)


# =========================================================
# ADD NEW REMINDER
# =========================================================

with st.expander("➕ Add New Reminder", expanded=False):

    st.subheader("Create a New Reminder")

    with st.form("add_reminder_form"):

        reminder_title = st.text_input(
            "Reminder Title",
            placeholder="Example: Drink Water"
        )

        reminder_message = st.text_area(
            "Reminder Message",
            placeholder="Example: Remember to drink enough water."
        )

        col1, col2 = st.columns(2)

        with col1:

            reminder_type = st.selectbox(
                "Reminder Type",
                [
                    "health",
                    "medicine",
                    "report",
                    "general",
                ],
            )

        with col2:

            reminder_time = st.time_input(
                "Reminder Time"
            )

        repeat_type = st.selectbox(
            "Repeat",
            [
                "Once",
                "Daily",
                "Weekly",
            ],
        )

        submit_reminder = st.form_submit_button(
            "➕ Add Reminder",
            use_container_width=True,
        )

        if submit_reminder:

            if not reminder_title.strip():

                st.error(
                    "Please enter a reminder title."
                )

            else:

                try:

                    add_reminder(
                        user_id=user_id,
                        title=reminder_title.strip(),
                        message=reminder_message.strip(),
                        reminder_type=reminder_type,
                        reminder_time=reminder_time.strftime("%H:%M"),
                        repeat_type=repeat_type,
                    )

                    st.success(
                        "✅ Reminder added successfully!"
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"Could not add reminder: {error}"
                    )


# =========================================================
# GET REMINDERS
# =========================================================

reminders = get_user_reminders(
    user_id
)


# =========================================================
# CAREGIVER POPUP
# =========================================================

unread_caregiver_reminders = [
    reminder
    for reminder in reminders
    if reminder["reminder_type"] == "caregiver"
    and reminder["is_read"] == 0
]


if unread_caregiver_reminders:

    latest = unread_caregiver_reminders[0]

    sender_name = (
        latest.get("sender_name")
        or "Your caregiver"
    )

    relationship = (
        latest.get("sender_relationship")
        or "Caregiver"
    )

    popup_message = latest.get(
        "message",
        ""
    )

    if popup_message:

        st.toast(
            f"🔔 {popup_message}",
            icon="👨‍👩‍👧"
        )

    else:

        st.toast(
            f"🔔 {relationship} {sender_name} "
            f"sent you a reminder.",
            icon="👨‍👩‍👧"
        )


# =========================================================
# REFRESH
# =========================================================

if st.button(
    "🔄 Refresh",
    key="refresh_reminders"
):

    st.rerun()


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3 = st.tabs([
    "🔔 All Reminders",
    "💊 Medicines",
    "🚨 Alerts"
])


# =========================================================
# ALL REMINDERS
# =========================================================

with tab1:

    reminders = get_user_reminders(
        user_id
    )

    if not reminders:

        st.info(
            "🎉 No reminders available."
        )

    else:

        unread_count = sum(
            1
            for reminder in reminders
            if reminder["is_read"] == 0
        )

        if unread_count:

            st.info(
                f"🔔 {unread_count} unread reminder(s)"
            )

        for reminder in reminders:

            reminder_type = reminder[
                "reminder_type"
            ]

            # ---------------------------------------------
            # ICON
            # ---------------------------------------------

            if reminder_type == "medicine":
                icon = "💊"

            elif reminder_type == "caregiver":
                icon = "👨‍👩‍👧"

            elif reminder_type == "health":
                icon = "❤️"

            elif reminder_type == "report":
                icon = "📄"

            elif reminder_type == "medicine_alert":
                icon = "🚨"

            else:
                icon = "🔔"


            # ---------------------------------------------
            # CAREGIVER REMINDER
            # ---------------------------------------------

            if reminder_type == "caregiver":

                sender_name = (
                    reminder.get("sender_name")
                    or "Your caregiver"
                )

                relationship = (
                    reminder.get("sender_relationship")
                    or "Caregiver"
                )

                with st.container(
                    border=True
                ):

                    st.markdown(
                        "### 👨‍👩‍👧 Caregiver Reminder"
                    )

                    if reminder["is_read"] == 0:

                        st.caption(
                            "🔵 NEW"
                        )

                    else:

                        st.caption(
                            "⚪ Read"
                        )

                    st.markdown(
                        f"**{relationship} "
                        f"{sender_name}**"
                    )

                    st.write(
                        reminder["message"]
                    )

                    if reminder["reminder_time"]:

                        st.caption(
                            f"⏰ Reminder time: "
                            f"{reminder['reminder_time']}"
                        )

                    col1, col2 = st.columns(2)

                    with col1:

                        if reminder["is_read"] == 0:

                            if st.button(
                                "✓ Mark as Read",
                                key=f"caregiver_read_{reminder['id']}",
                                use_container_width=True
                            ):

                                mark_reminder_read(
                                    reminder["id"],
                                    user_id
                                )

                                st.rerun()

                    with col2:

                        if st.button(
                            "🗑️ Delete",
                            key=f"caregiver_delete_{reminder['id']}",
                            use_container_width=True
                        ):

                            delete_reminder(
                                reminder["id"],
                                user_id
                            )

                            st.rerun()

                continue


            # ---------------------------------------------
            # NORMAL REMINDER
            # ---------------------------------------------

            with st.container(
                border=True
            ):

                col1, col2 = st.columns(
                    [5, 1.5]
                )

                with col1:

                    status = (
                        "🔵 New"
                        if reminder["is_read"] == 0
                        else "⚪ Read"
                    )

                    st.markdown(
                        f"### {icon} {reminder['title']}"
                    )

                    st.caption(
                        status
                    )

                    if reminder["message"]:

                        st.write(
                            reminder["message"]
                        )

                    if reminder["reminder_time"]:

                        st.caption(
                            f"⏰ {reminder['reminder_time']}"
                        )

                    if reminder["repeat_type"]:

                        st.caption(
                            f"🔁 {reminder['repeat_type']}"
                        )

                with col2:

                    if reminder["is_read"] == 0:

                        if st.button(
                            "✓ Read",
                            key=f"read_{reminder['id']}"
                        ):

                            mark_reminder_read(
                                reminder["id"],
                                user_id
                            )

                            st.rerun()

                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_{reminder['id']}"
                    ):

                        delete_reminder(
                            reminder["id"],
                            user_id
                        )

                        st.rerun()


# =========================================================
# MEDICINES
# =========================================================

with tab2:

    st.subheader(
        "💊 Medicine Status"
    )

    logs = get_medicine_logs(
        user_id
    )

    if not logs:

        st.info(
            "No medicine tracking records available."
        )

    else:

        today = date.today().isoformat()

        today_logs = [
            log
            for log in logs
            if str(
                log["scheduled_time"]
            ).startswith(today)
        ]

        if not today_logs:

            today_logs = logs[:10]

        for log in today_logs:

            status = log["status"]

            if status == "taken":

                status_icon = "✅"
                status_text = "Taken"

            elif status == "missed":

                status_icon = "🔴"
                status_text = "Missed"

            else:

                status_icon = "⏳"
                status_text = "Pending"

            with st.container(
                border=True
            ):

                col1, col2, col3 = st.columns(
                    [3, 2, 2]
                )

                with col1:

                    st.markdown(
                        f"### 💊 {log['medicine_name']}"
                    )

                    if log["dosage"]:

                        st.caption(
                            f"Dosage: {log['dosage']}"
                        )

                with col2:

                    st.write(
                        f"⏰ {log['scheduled_time']}"
                    )

                with col3:

                    st.write(
                        f"{status_icon} {status_text}"
                    )

                if status == "pending":

                    if st.button(
                        "✅ Mark as Taken",
                        key=f"taken_{log['id']}"
                    ):

                        mark_medicine_taken(
                            log["id"],
                            user_id
                        )

                        st.success(
                            "Medicine marked as taken."
                        )

                        st.rerun()


# =========================================================
# ALERTS
# =========================================================

with tab3:

    st.subheader(
        "🚨 Important Alerts"
    )

    reminders = get_user_reminders(
        user_id
    )

    alerts = [
        reminder
        for reminder in reminders
        if reminder["reminder_type"]
        in [
            "caregiver",
            "health",
            "report",
            "medicine_alert"
        ]
    ]

    if not alerts:

        st.success(
            "🎉 No important alerts right now."
        )

    else:

        for alert in alerts:

            with st.container(
                border=True
            ):

                if alert["reminder_type"] == "caregiver":

                    sender_name = (
                        alert.get("sender_name")
                        or "Your caregiver"
                    )

                    relationship = (
                        alert.get("sender_relationship")
                        or "Caregiver"
                    )

                    st.markdown(
                        "### 👨‍👩‍👧 Caregiver Reminder"
                    )

                    st.markdown(
                        f"**{relationship} "
                        f"{sender_name}**"
                    )

                    st.write(
                        alert["message"]
                    )

                else:

                    st.markdown(
                        f"### 🚨 {alert['title']}"
                    )

                    if alert["message"]:

                        st.write(
                            alert["message"]
                        )

                col1, col2 = st.columns(2)

                with col1:

                    if alert["is_read"] == 0:

                        if st.button(
                            "✓ Mark as Read",
                            key=f"alert_read_{alert['id']}"
                        ):

                            mark_reminder_read(
                                alert["id"],
                                user_id
                            )

                            st.rerun()

                with col2:

                    if st.button(
                        "🗑️ Delete",
                        key=f"alert_delete_{alert['id']}"
                    ):

                        delete_reminder(
                            alert["id"],
                            user_id
                        )

                        st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "CareMate AI • Your health reminders in one place"
)