import streamlit as st
from auth.session import init_session
from utils.helpers import bootstrap_database, load_css

# 1. Page Configuration (MUST be called first in app.py entrypoint)
st.set_page_config(
    page_title="SmartCampusAI Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Load Global Visual Accent Stylesheet
load_css("assets/styles.css")

# 3. Bootstrap JSON Database and Setup Session
bootstrap_database()
init_session()

# 4. Declare Page Routers dynamically based on Session Authenticated state
if not st.session_state.get("logged_in", False):
    # Public Gateway routes
    login_page = st.Page("auth/login.py", title="Login Gateway", icon=":material/login:", default=True)
    register_page = st.Page("auth/register.py", title="Register Account", icon=":material/person_add:")
    
    pg = st.navigation([login_page, register_page])
else:
    # Private Authorized Campus Hub routes
    home_page = st.Page("pages/Home.py", title="Dashboard Overview", icon=":material/dashboard:", default=True)
    students_page = st.Page("pages/Students.py", title="Students Directory", icon=":material/school:")
    faculty_page = st.Page("pages/Faculty.py", title="Faculty Directory", icon=":material/badge:")
    attendance_page = st.Page("pages/Attendance.py", title="Attendance Sheets", icon=":material/how_to_reg:")
    ai_page = st.Page("pages/AI_Assistant.py", title="AI Assistant", icon=":material/smart_toy:")
    reports_page = st.Page("pages/Reports.py", title="Export Reports", icon=":material/analytics:")
    settings_page = st.Page("pages/Settings.py", title="System Settings", icon=":material/settings:")
    profile_page = st.Page("pages/Profile.py", title="User Profile", icon=":material/account_circle:")
    
    pg = st.navigation({
        "Campus Hub": [home_page, students_page, faculty_page, attendance_page],
        "AI Agent": [ai_page],
        "System Management": [reports_page, settings_page, profile_page]
    })

# 5. Run the routing engine
try:
    pg.run()
except Exception as e:
    st.error(f"Navigation routing encountered an issue: {e}")
