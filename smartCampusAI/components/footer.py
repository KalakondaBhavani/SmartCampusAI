import streamlit as st

def render_footer():
    """Renders a beautiful footer with modern dark styling."""
    st.markdown("""
        <div class="footer-text">
            © 2026 SmartCampusAI. Powered by Antigravity AI Engine. All rights reserved.<br/>
            <span style="font-size: 0.75rem; color: #475569;">System Status: Operational | Database: JSON Local Cache</span>
        </div>
    """, unsafe_allow_html=True)
