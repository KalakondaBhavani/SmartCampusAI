import streamlit as st
import os
from auth.session import logout_user

def render_sidebar():
    """Adds branding, user profile preview, and logout functions to the sidebar area."""
    with st.sidebar:
        st.markdown("<br/>", unsafe_allow_html=True)
        logo_path = "assets/logo.png"
        if os.path.exists(logo_path):
            st.image(logo_path, width=80)
            
        st.markdown("""
            <div style='margin-bottom: 20px;'>
                <span style='font-size: 1.2rem; font-weight: 800; 
                             background: linear-gradient(135deg, #60a5fa 0%, #c084fc 100%);
                             -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                    SmartCampusAI
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        # User details preview card
        username = st.session_state.get("username", "Guest")
        role = st.session_state.get("role", "Student")
        email = st.session_state.get("email", "N/A")
        
        st.markdown(f"""
            <div style='background: rgba(255, 255, 255, 0.03); 
                        border: 1px solid rgba(255, 255, 255, 0.08); 
                        border-radius: 12px; padding: 15px; margin-bottom: 25px;'>
                <div style='font-size: 0.75rem; color: #64748b; text-transform: uppercase; font-weight: 700;'>Logged In As</div>
                <div style='font-size: 1rem; font-weight: 600; color: #f8fafc; margin: 3px 0;'>{username}</div>
                <div style='font-size: 0.8rem; color: #94a3b8;'>Role: <span style='color: #8b5cf6;'>{role}</span></div>
                <div style='font-size: 0.75rem; color: #64748b; overflow: hidden; text-overflow: ellipsis;'>{email}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Divider line
        st.markdown("<hr style='border: none; border-top: 1px solid rgba(255, 255, 255, 0.08); margin: 15px 0;'/>", unsafe_allow_html=True)
        
        # Logout button
        logout_clicked = st.button("Log Out", key="sidebar_logout_btn")
        if logout_clicked:
            logout_user()
