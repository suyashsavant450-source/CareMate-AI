import streamlit as st

from utils.helpers import require_login
from database import (
    find_user_by_email_or_phone,
    add_caregiver,
    get_monitored_patients,
    get_patient_medicines,
    get_patient_medicine_logs,
    get_patient_reports,
    get_patient_health_tracking,
    create_reminder
)


# =========================================================
# LOGIN
# =========================================================

current_user = require_login()

current_user_id = current_user["id"]
current_user_name = current_user["name"]


# =========================================================
# PAGE HEADER
# =========================================================

st.title("👨‍👩‍👧 Caregiver Mode")

st.caption(
    "Monitor authorized family members, medicines, reminders, "
    "medical reports and health progress."
)


# =========================================================
# ADD FAMILY MEMBER
# =========================================================

st.subheader("➕ Add Family Member")

with st.form("add_family_member"):

    identifier = st.text_input(
        "Family Member Email or Phone",
        placeholder="Enter registered email or phone"
    )

    relationship = st.selectbox(
        "Relationship",
        [
            "Mother",
            "Father",
            "Brother",
            "Sister",
            "Son",
            "Daughter",
            "Spouse",
            "Other"
        ]
    )

    add_button = st.form_submit_button(
        "➕ Add Family Member",
        use_container_width=True
    )


if add_button:

    if not identifier.strip():

        st.error(
            "Please enter the family member's "
            "registered email or phone."
        )

    else:

        patient = find_user_by_email_or_phone(
            identifier
        )

        if not patient:

            st.error(
                "No CareMate account found with "
                "this email or phone."
            )

        elif patient["id"] == current_user_id:

            st.error(
                "You cannot add your own account "
                "as a family member."
            )

        else:

            add_caregiver(
                patient_id=patient["id"],
                caregiver_name=current_user_name,
                caregiver_phone=current_user.get(
                    "phone",
                    ""
                ),
                caregiver_email=current_user.get(
                    "email",
                    ""
                ),
                relationship=relationship,
                caregiver_user_id=current_user_id,
                can_view_reports=True,
                can_view_medicines=True,
                can_view_progress=True,
                can_view_alerts=True,
                can_send_reminders=True
            )

            st.success(
                f"✅ {patient['name']} added successfully."
            )

            st.rerun()


# =========================================================
# GET MONITORED PATIENTS
# =========================================================

patients = get_monitored_patients(
    current_user_id
)


if not patients:

    st.info(
        "No family members added yet. "
        "Add a CareMate user above to monitor them."
    )

    st.stop()


# =========================================================
# SELECT FAMILY MEMBER
# =========================================================

st.divider()

st.subheader("👤 Select Family Member")

patient_names = [
    patient["patient_name"]
    for patient in patients
]

selected_name = st.selectbox(
    "Family Member",
    patient_names
)

selected_patient = next(
    patient
    for patient in patients
    if patient["patient_name"] == selected_name
)

patient_id = selected_patient["patient_user_id"]

patient_name = selected_patient["patient_name"]

relationship = selected_patient["relationship"]


st.success(
    f"Monitoring: **{patient_name}** "
    f"({relationship})"
)


# =========================================================
# PATIENT TABS
# =========================================================

tab_medicines, tab_reminders, tab_progress, tab_reports = st.tabs(
    [
        "💊 Medicines",
        "🔔 Reminders",
        "📊 Health Progress",
        "📄 Medical Reports"
    ]
)


# =========================================================
# MEDICINES
# =========================================================

with tab_medicines:

    st.subheader(
        f"💊 {patient_name}'s Medicines"
    )

    medicines = get_patient_medicines(
        patient_id
    )

    if not medicines:

        st.info(
            f"{patient_name} has no active medicines."
        )

    else:

        for medicine in medicines:

            with st.container(border=True):

                col1, col2 = st.columns(
                    [3, 1]
                )

                with col1:

                    st.markdown(
                        f"### 💊 {medicine['medicine_name']}"
                    )

                    st.write(
                        f"**Dosage:** "
                        f"{medicine.get('dosage') or 'Not specified'}"
                    )

                    st.write(
                        f"**Time:** "
                        f"{medicine.get('reminder_time') or 'Not set'}"
                    )

                    st.write(
                        f"**Frequency:** "
                        f"{medicine.get('frequency') or 'Not specified'}"
                    )

                    if medicine.get("notes"):

                        st.write(
                            f"**Notes:** "
                            f"{medicine['notes']}"
                        )

                with col2:

                    if st.button(
                        f"🔔 Remind {patient_name}",
                        key=f"remind_{medicine['id']}",
                        use_container_width=True
                    ):

                        st.session_state[
                            "selected_medicine_id"
                        ] = medicine["id"]

                        st.session_state[
                            "selected_medicine_name"
                        ] = medicine["medicine_name"]


    # =====================================================
    # IN-APP REMINDER FORM
    # =====================================================

    if "selected_medicine_id" in st.session_state:

        st.divider()

        medicine_id = st.session_state[
            "selected_medicine_id"
        ]

        medicine_name = st.session_state[
            "selected_medicine_name"
        ]

        st.subheader(
            f"🔔 Remind {patient_name}"
        )

        default_message = (
            f"{relationship} has reminded you to "
            f"take your {medicine_name}."
        )

        reminder_message = st.text_area(
            "Reminder Message",
            value=default_message,
            key="caregiver_reminder_message"
        )

        reminder_time = st.text_input(
            "Reminder Time (optional)",
            placeholder="Example: 8:00 PM",
            key="caregiver_reminder_time"
        )

        col1, col2 = st.columns(2)

        with col1:

            send_reminder = st.button(
                "🔔 Send Reminder",
                type="primary",
                use_container_width=True
            )

        with col2:

            cancel_reminder = st.button(
                "❌ Cancel",
                use_container_width=True
            )


        # =================================================
        # CANCEL REMINDER
        # =================================================

        if cancel_reminder:

            st.session_state.pop(
                "selected_medicine_id",
                None
            )

            st.session_state.pop(
                "selected_medicine_name",
                None
            )

            st.rerun()


        # =================================================
        # SAVE REMINDER
        # =================================================

        if send_reminder:

            if not reminder_message.strip():

                st.error(
                    "Please enter a reminder message."
                )

            else:

                try:

                    create_reminder(
                        user_id=patient_id,

                        reminder_type="caregiver",

                        title=(
                            f"🔔 Reminder from "
                            f"{relationship}"
                        ),

                        message=(
                            reminder_message.strip()
                        ),

                        reminder_time=(
                            reminder_time.strip()
                            if reminder_time.strip()
                            else None
                        ),

                        repeat_type=None,

                        related_medicine_id=medicine_id,

                        sender_id=current_user_id
                    )

                    st.success(
                        f"✅ Reminder sent to "
                        f"{patient_name}."
                    )

                    st.info(
                        f"🔔 {patient_name} can see "
                        "this reminder in their "
                        "CareMate Reminders page."
                    )

                    # Clear selected medicine
                    st.session_state.pop(
                        "selected_medicine_id",
                        None
                    )

                    st.session_state.pop(
                        "selected_medicine_name",
                        None
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        "Could not create reminder."
                    )

                    st.exception(error)


# =========================================================
# REMINDERS
# =========================================================

with tab_reminders:

    st.subheader(
        f"🔔 {patient_name}'s Reminders"
    )

    medicines = get_patient_medicines(
        patient_id
    )

    medicine_logs = get_patient_medicine_logs(
        patient_id
    )


    # -----------------------------------------------------
    # MEDICINE REMINDERS
    # -----------------------------------------------------

    if medicines:

        st.markdown(
            "### 💊 Medicine Reminders"
        )

        for medicine in medicines:

            with st.container(border=True):

                st.write(
                    f"💊 **{medicine['medicine_name']}**"
                )

                st.caption(
                    f"⏰ Time: "
                    f"{medicine.get('reminder_time') or 'Not set'}"
                )

                st.caption(
                    f"🔄 Frequency: "
                    f"{medicine.get('frequency') or 'Not specified'}"
                )

    else:

        st.info(
            "No medicine reminders available."
        )


    # -----------------------------------------------------
    # MEDICINE ACTIVITY
    # -----------------------------------------------------

    if medicine_logs:

        st.divider()

        st.markdown(
            "### 📋 Medicine Activity"
        )

        for log in medicine_logs[:10]:

            status = (
                log.get("status")
                or "pending"
            )

            if status == "taken":

                status_icon = "🟢"

            elif status == "missed":

                status_icon = "🔴"

            else:

                status_icon = "🟡"

            with st.container(border=True):

                st.write(
                    f"{status_icon} "
                    f"**{log.get('medicine_name', 'Medicine')}**"
                )

                st.caption(
                    f"Scheduled: "
                    f"{log.get('scheduled_time', 'N/A')}"
                )

                st.caption(
                    f"Status: {status.title()}"
                )

    else:

        st.caption(
            "No medicine activity recorded yet."
        )


# =========================================================
# HEALTH PROGRESS
# =========================================================

with tab_progress:

    st.subheader(
        f"📊 {patient_name}'s Health Progress"
    )

    records = get_patient_health_tracking(
        patient_id
    )

    if not records:

        st.info(
            "No health tracking data available."
        )

    else:

        latest = records[0]

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "💧 Water",
                f"{latest.get('water_intake', 0)} L"
            )

        with col2:

            st.metric(
                "😴 Sleep",
                f"{latest.get('sleep_hours', 0)} hrs"
            )

        with col3:

            st.metric(
                "🚶 Exercise",
                f"{latest.get('exercise_minutes', 0)} min"
            )


        st.divider()

        st.markdown(
            "### 📅 Tracking History"
        )

        for record in records:

            with st.container(border=True):

                st.write(
                    f"**📅 "
                    f"{record.get('tracking_date', 'N/A')}**"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.write(
                        f"💧 "
                        f"{record.get('water_intake', 0)} L"
                    )

                with col2:

                    st.write(
                        f"😴 "
                        f"{record.get('sleep_hours', 0)} hrs"
                    )

                with col3:

                    st.write(
                        f"🚶 "
                        f"{record.get('exercise_minutes', 0)} min"
                    )


# =========================================================
# MEDICAL REPORTS
# =========================================================

with tab_reports:

    st.subheader(
        f"📄 {patient_name}'s Medical Reports"
    )

    reports = get_patient_reports(
        patient_id
    )

    if not reports:

        st.info(
            "No medical reports available."
        )

    else:

        for report in reports:

            file_name = (
                report.get("file_name")
                or "Medical Report"
            )

            with st.expander(
                f"📄 {file_name}"
            ):

                st.caption(
                    f"Uploaded: "
                    f"{report.get('uploaded_at', 'N/A')}"
                )

                st.markdown(
                    "### 🤖 Simplified Report"
                )

                st.write(
                    report.get(
                        "simplified_report",
                        "No simplified report available."
                    )
                )


# =========================================================
# SECURITY INFORMATION
# =========================================================

st.divider()

st.caption(
    "🔐 CareMate AI only displays data belonging "
    "to authorized family members."
)