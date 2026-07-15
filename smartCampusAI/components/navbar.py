import streamlit as st

def render_navbar(title: str):
    """Renders the top application header with active session info."""
    username = st.session_state.get("username", "User")
    role = st.session_state.get("role", "Student")
    email = st.session_state.get("email", "")
    
    col_t, col_p = st.columns([3, 1])
    
    with col_t:
        st.markdown(f"""
            <div style='display: flex; align-items: center; gap: 15px; margin-bottom: 20px;'>
                <h1 style='margin: 0; font-size: 2.2rem; font-weight: 800;'>{title}</h1>
            </div>
        """, unsafe_allow_html=True)
        
    with col_p:
        # Glassmorphic user chip
        st.markdown(f"""
            <div style='text-align: right; background: rgba(30, 41, 59, 0.45); 
                        backdrop-filter: blur(12px); border-radius: 12px; 
                        border: 1px solid rgba(255, 255, 255, 0.08); 
                        padding: 10px 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
                <div style='font-weight: 700; color: #a78bfa; font-size: 0.95rem;'>{username}</div>
                <div style='font-size: 0.75rem; color: #94a3b8;'>{role} | {email}</div>
            </div>
        """, unsafe_allow_html=True)
