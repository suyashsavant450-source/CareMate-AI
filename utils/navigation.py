import streamlit as st


def go_dashboard():
    st.switch_page("pages/dashboard.py")


def go_back(page):
    st.switch_page(page)


def logout():

    st.session_state.logged_in = False
    st.session_state.user = None

    st.switch_page("pages/login.py")


def page_header(
    title,
    subtitle=None
):

    st.markdown(f"## {title}")

    if subtitle:
        st.caption(subtitle)