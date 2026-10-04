import streamlit as st

from database import get_connection
from utils.helpers import require_login


user = require_login()
user_id = user["id"]


st.title("💊 Medicines")

st.caption(
    "Manage your medicines and reminder times."
)


with st.expander(
    "➕ Add Medicine",
    expanded=True
):

    name = st.text_input(
        "Medicine Name"
    )

    dosage = st.text_input(
        "Dosage",
        placeholder="Example: 500 mg"
    )

    time = st.time_input(
        "Reminder Time"
    )

    frequency = st.selectbox(
        "Frequency",
        [
            "Once Daily",
            "Twice Daily",
            "Three Times Daily",
            "As Required"
        ]
    )

    notes = st.text_area(
        "Notes"
    )

    if st.button(
        "Save Medicine",
        type="primary",
        use_container_width=True
    ):

        if not name.strip():

            st.error(
                "Please enter medicine name."
            )

        else:

            connection = get_connection()

            connection.execute(
                """
                INSERT INTO medicines
                (
                    user_id,
                    medicine_name,
                    dosage,
                    reminder_time,
                    frequency,
                    notes
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    name.strip(),
                    dosage.strip(),
                    time.strftime("%H:%M"),
                    frequency,
                    notes.strip()
                )
            )

            connection.commit()
            connection.close()

            st.success(
                "Medicine added successfully."
            )

            st.rerun()


st.subheader("Your Medicines")


connection = get_connection()

medicines = connection.execute(
    """
    SELECT *
    FROM medicines
    WHERE user_id = ?
    AND active = 1
    ORDER BY reminder_time
    """,
    (user_id,)
).fetchall()

connection.close()


if not medicines:

    st.info(
        "No medicines added yet."
    )

else:

    for medicine in medicines:

        with st.container(border=True):

            st.markdown(
                f"### 💊 {medicine['medicine_name']}"
            )

            st.write(
                f"**Dosage:** "
                f"{medicine['dosage'] or 'Not specified'}"
            )

            st.write(
                f"**Time:** "
                f"{medicine['reminder_time'] or 'Not set'}"
            )

            st.write(
                f"**Frequency:** "
                f"{medicine['frequency']}"
            )

            if medicine["notes"]:

                st.caption(
                    medicine["notes"]
                )

            if st.button(
                "Remove",
                key=f"remove_{medicine['id']}"
            ):

                connection = get_connection()

                connection.execute(
                    """
                    UPDATE medicines
                    SET active = 0
                    WHERE id = ?
                    AND user_id = ?
                    """,
                    (
                        medicine["id"],
                        user_id
                    )
                )

                connection.commit()
                connection.close()

                st.rerun()