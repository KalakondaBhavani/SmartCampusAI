import streamlit as st
from components.metrics import render_custom_metric
from utils.json_db import get_all_students, get_all_faculty, get_all_attendance, load_json, ACTIVITY_FILE

def render_dashboard_cards():
    """Aggregates campus metrics from JSON databases and renders a 4-column metric grid."""
    # 1. Fetch Students
    students = get_all_students()
    total_students = len(students)
    
    # 2. Fetch Faculty
    faculty = get_all_faculty()
    total_faculty = len(faculty)
    
    # 3. Calculate Attendance %
    attendance = get_all_attendance()
    attendance_pct = "0%"
    if attendance:
        present_count = sum(1 for a in attendance if a.get("status") == "Present")
        pct = (present_count / len(attendance)) * 100
        attendance_pct = f"{pct:.1f}%"
        
    # 4. Count Departments
    depts = set()
    for s in students:
        if s.get("department"):
            depts.add(s["department"])
    for f in faculty:
        if f.get("department"):
            depts.add(f["department"])
    total_depts = len(depts) if depts else 0
    
    # 5. Count AI requests from activity log
    activities = load_json(ACTIVITY_FILE)
    ai_requests = 0
    if isinstance(activities, list):
        ai_requests = sum(1 for a in activities if "AI" in a.get("action", "") or "ai" in a.get("action", "").lower())
        
    # Render columns
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        render_custom_metric("Total Students", str(total_students), "🎓", change="+12%", change_type="up")
    with col2:
        render_custom_metric("Total Faculty", str(total_faculty), "🧑‍🏫", change="+2", change_type="up")
    with col3:
        render_custom_metric("Attendance Rate", attendance_pct, "📅", change="-0.8%", change_type="down")
    with col4:
        render_custom_metric("Departments", str(total_depts), "🏛️", change="Stable", change_type="up")
    with col5:
        render_custom_metric("AI API Requests", str(ai_requests), "⚡", change="+24%", change_type="up")
