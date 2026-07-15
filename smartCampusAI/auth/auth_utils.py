import streamlit as st
import os

def render_auth_header(subtitle: str = "Modern Smart Campus Hub"):
    """Renders a visually striking brand header with application logo."""
    logo_path = "assets/logo.png"
    
    # Visual grid centering
    _, col2, _ = st.columns([1, 1.5, 1])
    with col2:
        if os.path.exists(logo_path):
            st.image(logo_path, width=160)
        st.markdown(f"""
            <div class="auth-header">
                <div class="auth-logo-text">SmartCampusAI</div>
                <p class="auth-subtitle">{subtitle}</p>
            </div>
        """, unsafe_allow_html=True)
