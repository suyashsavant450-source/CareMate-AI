import streamlit as st

from database import (
    get_user_by_id,
    update_user_profile,
    change_password,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CareMate AI | Profile",
    page_icon="👤",
    layout="wide",
)


# =========================================================
# LOGIN CHECK
# =========================================================

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login.py")

user = st.session_state.get("user")

if not user:
    st.switch_page("pages/login.py")


# =========================================================
# USER DATA
# =========================================================

user_id = user["id"]

current_user = get_user_by_id(user_id)

if current_user:
    user = current_user
    st.session_state.user = current_user


# =========================================================
# SINGLE PREMIUM USER PROFILE HEADER WITH AI AVATAR
# =========================================================

user_name = user.get("name", "CareMate User")
user_email = user.get("email", "")
user_photo_url = user.get("profile_pic_url", f"https://api.dicebear.com/7.x/bottts/svg?seed={user_name}")

profile_card_html = f"""
<style>
.user-profile-header {{
    display: flex;
    align-items: center;
    gap: 24px;
    padding: 24px 32px;
    margin-bottom: 24px;
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.8));
    border: 1px solid rgba(56, 189, 248, 0.25);
    box-shadow: 0 10px 30px -5px rgba(14, 165, 233, 0.2);
    backdrop-filter: blur(10px);
}}

.user-avatar-glow {{
    width: 95px;
    height: 95px;
    border-radius: 50%;
    background: linear-gradient(135deg, #0ea5e9, #6366f1, #a855f7);
    padding: 3px;
    box-shadow: 0 0 25px rgba(14, 165, 233, 0.4);
    flex-shrink: 0;
}}

.user-avatar-inner {{
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: #0f172a;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.user-avatar-inner img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
}}

.user-info-details {{
    display: flex;
    flex-direction: column;
    gap: 4px;
}}

.user-display-name {{
    font-size: 26px;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: -0.3px;
}}

.user-display-email {{
    font-size: 14px;
    color: #38bdf8;
    font-weight: 500;
}}

.user-display-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-top: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    background: rgba(14, 165, 233, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.3);
    color: #38bdf8;
    font-size: 12px;
    font-weight: 600;
    width: fit-content;
}}
</style>

<div class="user-profile-header">
    <div class="user-avatar-glow">
        <div class="user-avatar-inner">
            <img src="{user_photo_url}" alt="User AI Avatar" />
        </div>
    </div>
    <div class="user-info-details">
        <div class="user-display-name">{user_name}</div>
        <div class="user-display-email">{user_email}</div>
        <div class="user-display-badge">✦ CareMate AI Member</div>
    </div>
</div>
"""

try:
    st.html(profile_card_html)
except AttributeError:
    st.markdown(profile_card_html, unsafe_allow_html=True)

st.write("")


# =========================================================
# PERSONAL & HEALTH INFORMATION (DISPLAY ONLY)
# =========================================================

st.subheader("👤 Personal Information")

with st.container(border=True):

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Full Name**")
        st.write(user.get("name", "Not available"))

    with col2:
        st.markdown("**Email Address**")
        st.write(user.get("email", "Not available"))

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Phone Number**")
        st.write(user.get("phone", "Not added"))

    with col2:
        st.markdown("**Account ID**")
        st.write(f"CM-{user_id:04d}")

    st.divider()
    st.markdown("#### 🩺 Basic Health Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Date of Birth**")
        st.write(user.get("date_of_birth") or "Not added")

    with col2:
        st.markdown("**Gender**")
        st.write(user.get("gender") or "Not specified")

    with col3:
        st.markdown("**Blood Group**")
        st.write(user.get("blood_group") or "Not specified")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Height**")
        height_val = user.get("height")
        st.write(f"{height_val} cm" if height_val else "Not added")

    with col2:
        st.markdown("**Weight**")
        weight_val = user.get("weight")
        st.write(f"{weight_val} kg" if weight_val else "Not added")

    with col3:
        st.markdown("**Allergies**")
        st.write(user.get("allergies") or "None")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Existing Health Conditions**")
        st.write(user.get("health_conditions") or "None")

    with col2:
        st.markdown("**Emergency Contact**")
        em_name = user.get("emergency_contact_name") or ""
        em_phone = user.get("emergency_contact_phone") or ""
        if em_name or em_phone:
            st.write(f"{em_name} ({em_phone})".strip())
        else:
            st.write("Not added")


# =========================================================
# EDIT PROFILE
# =========================================================

st.subheader("✏️ Edit Profile")

with st.expander("Edit your personal information"):

    with st.form("edit_profile_form"):

        new_name = st.text_input(
            "Full Name",
            value=user.get("name", ""),
        )

        new_email = st.text_input(
            "Email Address",
            value=user.get("email", ""),
        )

        new_phone = st.text_input(
            "Phone Number",
            value=user.get("phone", ""),
        )

        save_profile = st.form_submit_button(
            "💾 Save Changes",
            use_container_width=True,
        )

        if save_profile:

            if not new_name.strip():
                st.error("Please enter your name.")

            elif not new_email.strip():
                st.error("Please enter your email.")

            else:
                success, message = update_user_profile(
                    user_id=user_id,
                    name=new_name,
                    email=new_email,
                    phone=new_phone,
                    date_of_birth=user.get("date_of_birth", "") or "",
                    gender=user.get("gender", "") or "",
                    blood_group=user.get("blood_group", "") or "",
                    height=user.get("height"),
                    weight=user.get("weight"),
                    allergies=user.get("allergies", "") or "",
                    health_conditions=user.get("health_conditions", "") or "",
                    emergency_contact_name=user.get("emergency_contact_name", "") or "",
                    emergency_contact_phone=user.get("emergency_contact_phone", "") or "",
                )

                if success:
                    st.session_state.user = get_user_by_id(user_id)
                    st.success("✅ Profile updated successfully!")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")


# =========================================================
# BASIC HEALTH INFORMATION (EDIT EXPANDER)
# =========================================================

st.subheader("🩺 Edit Basic Health Information")

with st.expander("Edit your basic health information"):

    with st.form("health_profile_form"):

        col1, col2 = st.columns(2)

        with col1:
            date_of_birth = st.text_input(
                "1. Date of Birth",
                value=user.get("date_of_birth", "") or "",
                placeholder="YYYY-MM-DD"
            )

        with col2:
            gender_options = [
                "Not specified",
                "Male",
                "Female",
                "Other",
                "Prefer not to say"
            ]

            saved_gender = user.get("gender", "") or ""

            gender_index = (
                gender_options.index(saved_gender)
                if saved_gender in gender_options
                else 0
            )

            gender = st.selectbox(
                "2. Gender",
                gender_options,
                index=gender_index
            )

        col1, col2 = st.columns(2)

        with col1:
            blood_group_options = [
                "Not specified",
                "A+",
                "A-",
                "B+",
                "B-",
                "AB+",
                "AB-",
                "O+",
                "O-"
            ]

            saved_blood_group = user.get("blood_group", "") or ""

            blood_group_index = (
                blood_group_options.index(saved_blood_group)
                if saved_blood_group in blood_group_options
                else 0
            )

            blood_group = st.selectbox(
                "3. Blood Group",
                blood_group_options,
                index=blood_group_index
            )

        with col2:
            current_height = user.get("height")

            height = st.number_input(
                "4. Height (cm)",
                min_value=0.0,
                max_value=250.0,
                value=float(current_height if current_height is not None else 0.0),
                step=0.1
            )

        col1, col2 = st.columns(2)

        with col1:
            current_weight = user.get("weight")

            weight = st.number_input(
                "5. Weight (kg)",
                min_value=0.0,
                max_value=300.0,
                value=float(current_weight if current_weight is not None else 0.0),
                step=0.1
            )

        with col2:
            allergies = st.text_input(
                "6. Allergies",
                value=user.get("allergies", "") or "",
                placeholder="Example: Dust, peanuts"
            )

        health_conditions = st.text_area(
            "7. Existing Health Conditions",
            value=user.get("health_conditions", "") or "",
            placeholder="Example: Asthma, diabetes, hypertension or write None",
            height=100
        )

        col1, col2 = st.columns(2)

        with col1:
            emergency_contact_name = st.text_input(
                "8. Emergency Contact Name",
                value=user.get("emergency_contact_name", "") or "",
                placeholder="Example: Parent / Guardian"
            )

        with col2:
            emergency_contact_phone = st.text_input(
                "9. Emergency Contact Phone",
                value=user.get("emergency_contact_phone", "") or "",
                placeholder="Example: +91 9876543210"
            )

        st.write("")

        save_health = st.form_submit_button(
            "💾 Save Health Information",
            use_container_width=True
        )

        if save_health:

            gender_value = "" if gender == "Not specified" else gender
            blood_group_value = "" if blood_group == "Not specified" else blood_group
            height_value = None if height <= 0 else height
            weight_value = None if weight <= 0 else weight

            success, message = update_user_profile(
                user_id=user_id,
                name=user.get("name", ""),
                email=user.get("email", ""),
                phone=user.get("phone", ""),
                date_of_birth=date_of_birth,
                gender=gender_value,
                blood_group=blood_group_value,
                height=height_value,
                weight=weight_value,
                allergies=allergies,
                health_conditions=health_conditions,
                emergency_contact_name=emergency_contact_name,
                emergency_contact_phone=emergency_contact_phone
            )

            if success:
                st.session_state.user = get_user_by_id(user_id)
                st.success("✅ Health information saved successfully!")
                st.rerun()
            else:
                st.error(f"❌ {message}")


# =========================================================
# MEDICINE DETAILS
# =========================================================

st.subheader("💊 Medicine-Related Details")

with st.container(border=True):

    st.write(
        "Your medicine information is managed through "
        "the Medicines section."
    )

    if st.button(
        "💊 Open Medicines",
        use_container_width=True,
    ):
        st.switch_page("pages/medicines.py")


# =========================================================
# CAREGIVER INFORMATION
# =========================================================

st.subheader("👨‍👩‍👧 Caregiver Information")

with st.container(border=True):

    st.write(
        "Manage caregiver access and permissions from "
        "Caregiver Mode."
    )

    if st.button(
        "👨‍👩‍👧 Open Caregiver Mode",
        use_container_width=True,
    ):
        st.switch_page("pages/caregiver.py")


# =========================================================
# REMINDER PREFERENCES
# =========================================================

st.subheader("🔔 Reminder Preferences")

with st.container(border=True):

    st.write(
        "Medicine, appointment and health routine reminders "
        "can be managed from the Reminders section."
    )

    if st.button(
        "🔔 Open Reminders",
        use_container_width=True,
    ):
        st.switch_page("pages/reminders.py")


# =========================================================
# PRIVACY & ACCOUNT SETTINGS
# =========================================================

st.subheader("🔐 Privacy & Account Settings")

with st.container(border=True):

    st.success(
        "Your CareMate AI health data is linked to "
        "your individual account."
    )

    st.write(
        "Your medical reports, medicines, reminders and "
        "health tracking data are accessed using your "
        "user account."
    )


# =========================================================
# CHANGE PASSWORD
# =========================================================

st.subheader("🔑 Change Password")

with st.expander("Update your password"):

    with st.form("change_password_form"):

        current_password = st.text_input(
            "Current Password",
            type="password",
        )

        new_password = st.text_input(
            "New Password",
            type="password",
        )

        confirm_password = st.text_input(
            "Confirm New Password",
            type="password",
        )

        change_button = st.form_submit_button(
            "🔑 Change Password",
            use_container_width=True,
        )

        if change_button:

            if not current_password:
                st.error("Please enter your current password.")

            elif not new_password:
                st.error("Please enter a new password.")

            elif len(new_password) < 6:
                st.error(
                    "New password must contain at least "
                    "6 characters."
                )

            elif new_password != confirm_password:
                st.error("New passwords do not match.")

            else:
                success, message = change_password(
                    user_id,
                    current_password,
                    new_password,
                )

                if success:
                    st.success("✅ Password changed successfully!")
                else:
                    st.error(f"❌ {message}")


# =========================================================
# LOGOUT
# =========================================================

st.divider()

st.subheader("🚪 Account")

if st.button(
    "🚪 Logout from CareMate AI",
    use_container_width=True,
    type="secondary",
):
    st.session_state.logged_in = False
    st.session_state.user = None

    st.switch_page("pages/login.py")