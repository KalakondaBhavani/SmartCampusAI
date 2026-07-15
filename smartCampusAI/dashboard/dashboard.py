import streamlit as st
import pandas as pd
from datetime import datetime
from utils.json_db import load_json, ACTIVITY_FILE

def render_recent_activity():
    """Renders recent activities in a glassmorphic container."""
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Recent Activity Log")
    
    activities = load_json(ACTIVITY_FILE)
    if activities and isinstance(activities, list):
        formatted_list = []
        # Show top 7 actions
        for act in activities[:7]:
            ts = act.get("timestamp", "")
            time_display = ts
            if ts:
                try:
                    dt = datetime.fromisoformat(ts)
                    time_display = dt.strftime("%b %d, %I:%M %p")
                except ValueError:
                    pass
            
            formatted_list.append({
                "Timestamp": time_display,
                "Operator": act.get("username", "system"),
                "Action": act.get("action", "General"),
                "Details": act.get("details", "")
            })
            
        df = pd.DataFrame(formatted_list)
        # Display as styled dataframe
        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "Timestamp": st.column_config.TextColumn("Time"),
                "Operator": st.column_config.TextColumn("User"),
                "Action": st.column_config.TextColumn("Action"),
                "Details": st.column_config.TextColumn("Summary")
            },
            hide_index=True
        )
    else:
        st.info("No recent campus activities tracked.")
    st.markdown('</div>', unsafe_allow_html=True)

def render_notifications():
    """Renders real-time notifications or alerts for the dashboard."""
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Campus Alerts & Notifications")
    
    alerts = [
        {"type": "warning", "message": "Low attendance detected in class IT202 (74.2%)."},
        {"type": "info", "message": "Academic Year 2026-2027 configuration loaded successfully."},
        {"type": "success", "message": "Monthly campus report is ready for export in the Reports tab."},
        {"type": "error", "message": "Failed database backup sync check (scheduled next at 23:00)."},
    ]
    
    for alert in alerts:
        if alert["type"] == "warning":
            st.warning(alert["message"])
        elif alert["type"] == "info":
            st.info(alert["message"])
        elif alert["type"] == "success":
            st.success(alert["message"])
        elif alert["type"] == "error":
            st.error(alert["message"])
            
    st.markdown('</div>', unsafe_allow_html=True)
