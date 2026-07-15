import streamlit as st
from utils.helpers import load_css
from components.navbar import render_navbar
from components.footer import render_footer
from dashboard.sidebar import render_sidebar
from utils.json_db import load_settings, save_settings, log_activity

# Page components
load_css()
render_sidebar()
render_navbar("System Settings")

# Permissions Guard
role = st.session_state.get("role", "Student")
is_admin = role == "Admin"

current_settings = load_settings()

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("Global Configuration Settings")

if not is_admin:
    st.warning("⚠️ Access Denied. Only Admins can modify global campus configurations.")
    # Show read-only details
    st.write("**Current System Details:**")
    st.write(f"- **Application Name:** {current_settings.get('app_name')}")
    st.write(f"- **Academic Year:** {current_settings.get('academic_year')}")
    st.write(f"- **Public Registrations:** {'Enabled' if current_settings.get('allow_registration') else 'Disabled'}")
    st.write(f"- **System Theme:** {current_settings.get('theme')}")
    st.write(f"- **Default AI Engine:** {current_settings.get('ai_model')}")
else:
    with st.form("settings_form"):
        app_name = st.text_input("Application Name", value=current_settings.get("app_name", "SmartCampusAI"))
        academic_year = st.selectbox("Academic Calendar Year", ["2025-2026", "2026-2027", "2027-2028"], index=["2025-2026", "2026-2027", "2027-2028"].index(current_settings.get("academic_year", "2026-2027")))
        allow_reg = st.toggle("Allow New Registrations", value=current_settings.get("allow_registration", True))
        app_theme = st.selectbox("App Theme Style", ["Antigravity Theme", "Cyberpunk Violet", "Emerald Forest", "Standard Slate"], index=["Antigravity Theme", "Cyberpunk Violet", "Emerald Forest", "Standard Slate"].index(current_settings.get("theme", "Antigravity Theme")))
        ai_engine = st.selectbox("Default LLM Provider Model", ["Gemini 1.5 Flash", "Gemini 1.5 Pro", "OpenAI GPT-4o-mini", "OpenAI GPT-4o"], index=["Gemini 1.5 Flash", "Gemini 1.5 Pro", "OpenAI GPT-4o-mini", "OpenAI GPT-4o"].index(current_settings.get("ai_model", "Gemini 1.5 Flash")))
        
        submit_settings = st.form_submit_button("Save System Settings")
        
        if submit_settings:
            updated = {
                "app_name": app_name,
                "academic_year": academic_year,
                "allow_registration": allow_reg,
                "theme": app_theme,
                "ai_model": ai_engine
            }
            if save_settings(updated):
                st.success("Global configurations saved successfully!")
                st.toast("System settings updated!", icon="⚙️")
                log_activity(st.session_state.get("username", "admin"), "Edit Settings", "Updated global system configurations")
                st.rerun()
            else:
                st.error("Failed to save settings to disk.")
                
st.markdown('</div>', unsafe_allow_html=True)

render_footer()
