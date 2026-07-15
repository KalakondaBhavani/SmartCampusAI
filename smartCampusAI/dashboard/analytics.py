import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.json_db import get_all_students, get_all_attendance

def render_analytics():
    """Generates and displays Plotly visual analytics matching the Antigravity Theme."""
    students = get_all_students()
    attendance = get_all_attendance()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Department Roster Distribution")
        if students:
            df_stu = pd.DataFrame(students)
            dept_counts = df_stu["department"].value_counts().reset_index()
            dept_counts.columns = ["Department", "Students Count"]
            
            # Premium color scale (indigo, blue, purple, magenta)
            fig = px.bar(
                dept_counts, 
                x="Department", 
                y="Students Count",
                color="Department",
                color_discrete_sequence=["#3b82f6", "#8b5cf6", "#a855f7", "#ec4899", "#6366f1"],
                text_auto=True
            )
            
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0",
                showlegend=False,
                xaxis=dict(showgrid=False, color="#94a3b8"),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)", color="#94a3b8"),
                margin=dict(l=20, r=20, t=20, b=20),
                height=320
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No student data available to chart.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Attendance Trends over Time")
        if attendance:
            df_att = pd.DataFrame(attendance)
            # Calculate daily attendance rate
            # (Present / Total) per day
            daily_rates = []
            for date, group in df_att.groupby("date"):
                total = len(group)
                present = sum(1 for _, r in group.iterrows() if r["status"] == "Present")
                rate = (present / total) * 100 if total > 0 else 0
                daily_rates.append({"Date": date, "Attendance Rate (%)": round(rate, 1)})
                
            df_trends = pd.DataFrame(daily_rates).sort_values("Date")
            
            fig = px.line(
                df_trends, 
                x="Date", 
                y="Attendance Rate (%)",
                markers=True,
                line_shape="spline"
            )
            
            # Stylize path
            fig.update_traces(
                line=dict(color="#d946ef", width=3),
                marker=dict(size=8, color="#8b5cf6", line=dict(width=2, color="#ffffff"))
            )
            
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0",
                xaxis=dict(showgrid=False, color="#94a3b8"),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)", color="#94a3b8", range=[0, 105]),
                margin=dict(l=20, r=20, t=20, b=20),
                height=320
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No attendance data available to chart.")
        st.markdown('</div>', unsafe_allow_html=True)
