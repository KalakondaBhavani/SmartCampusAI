import streamlit as st
from utils.json_db import log_activity

def init_session():
    """Initializes default session states if they don't already exist."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "email" not in st.session_state:
        st.session_state.email = None
    if "role" not in st.session_state:
        st.session_state.role = None
    if "user_details" not in st.session_state:
        st.session_state.user_details = {}

def login_user(user_data: dict) -> bool:
    """Sets session state variables on successful user login."""
    st.session_state.logged_in = True
    st.session_state.username = user_data.get("username")
    st.session_state.email = user_data.get("email")
    st.session_state.role = user_data.get("role", "Student")
    # Store full dict for convenience in updating
    st.session_state.user_details = user_data
    return True

def logout_user():
    """Logs activity and clears user session state variables, then reruns streamlit."""
    username = st.session_state.get("username", "unknown")
    log_activity(username, "Logout", "User logged out successfully")
    
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.email = None
    st.session_state.role = None
    st.session_state.user_details = {}
    
    st.toast("Logged out successfully!", icon="🔑")
    st.rerun()
