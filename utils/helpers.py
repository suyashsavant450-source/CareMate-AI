import streamlit as st


def require_login():

    if not st.session_state.get(
        "logged_in",
        False
    ):
        st.stop()

    return st.session_state.user


def get_user_id():

    user = require_login()

    return user["id"]