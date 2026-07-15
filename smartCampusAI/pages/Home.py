import streamlit as st
from utils.helpers import load_css
from components.navbar import render_navbar
from components.footer import render_footer
from dashboard.sidebar import render_sidebar
from dashboard.cards import render_dashboard_cards
from dashboard.analytics import render_analytics
from dashboard.dashboard import render_recent_activity, render_notifications

# 1. Load CSS for styling
load_css()

# 2. Render Sidebar details
render_sidebar()

# 3. Render Navbar title
render_navbar("Campus Overview")

# 4. Render Metric Grid
render_dashboard_cards()

st.markdown("<br/>", unsafe_allow_html=True)

# 5. Render Plotly Charts
render_analytics()

st.markdown("<br/>", unsafe_allow_html=True)

# 6. Render Activity Log & Notifications
col_act, col_not = st.columns([1.6, 1.2])

with col_act:
    render_recent_activity()
    
with col_not:
    render_notifications()

# 7. Render Footer
render_footer()
