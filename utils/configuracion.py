import streamlit as st

def initialize_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'rol' not in st.session_state:
        st.session_state.rol = ""

def hide_sidebar():
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
            [data-testid="collapsedControl"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def set_wide_layout_and_center_title():
    st.markdown(
        """
        <style>
            .main .block-container {
                max-width: 1200px;
                padding-left: 5%;
                padding-right: 5%;
            }
            h1 {
                text-align: center;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )