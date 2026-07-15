import os
import streamlit as st
from typing import Dict, Any, List
from datetime import datetime, timedelta
import random
from utils.json_db import (
    get_all_users, add_user, get_all_students, save_students,
    get_all_faculty, save_faculty, get_all_attendance, save_attendance,
    log_activity, load_settings, save_json, USERS_FILE, SETTINGS_FILE
)

def load_css(file_path: str = "assets/styles.css"):
    """Loads a CSS file and injects it into the Streamlit app layout."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    else:
        # Fallback inline CSS if stylesheet is missing
        st.markdown("""
            <style>
                .stApp { background-color: #0b0c10; color: #c5c6c7; }
                .glass-card { background: rgba(31, 38, 135, 0.07); border-radius: 10px; border: 1px solid rgba(255,255,255,0.08); padding: 20px; }
            </style>
        """, unsafe_allow_html=True)

def bootstrap_database():
    """Bootstraps default users, settings, and mock campus data if databases are empty."""
    # 1. Initialize settings if empty
    load_settings()
    
    # 2. Check and generate users
    users = get_all_users()
    if not users:
        # Default Admin Account
        add_user("admin", "admin@smartcampus.edu", "AdminPassword123!", "Admin")
        # Default Faculty Account
        add_user("faculty", "faculty@smartcampus.edu", "FacultyPassword123!", "Faculty")
        # Default Student Account
        add_user("student", "student@smartcampus.edu", "StudentPassword123!", "Student")
        log_activity("system", "Bootstrap Users", "Default admin, faculty, and student user accounts created")

    # 3. Check and generate students
    students = get_all_students()
    if not students:
        departments = ["Computer Science", "Information Technology", "Electronics", "Mechanical", "Business Administration"]
        mock_students = [
            {"id": "STU101", "name": "Alice Johnson", "email": "alice.j@smartcampus.edu", "department": "Computer Science", "enrollment_year": 2023, "status": "Active"},
            {"id": "STU102", "name": "Bob Smith", "email": "bob.s@smartcampus.edu", "department": "Information Technology", "enrollment_year": 2023, "status": "Active"},
            {"id": "STU103", "name": "Charlie Brown", "email": "charlie.b@smartcampus.edu", "department": "Electronics", "enrollment_year": 2024, "status": "Active"},
            {"id": "STU104", "name": "Diana Prince", "email": "diana.p@smartcampus.edu", "department": "Computer Science", "enrollment_year": 2022, "status": "Active"},
            {"id": "STU105", "name": "Ethan Hunt", "email": "ethan.h@smartcampus.edu", "department": "Mechanical", "enrollment_year": 2024, "status": "Active"},
            {"id": "STU106", "name": "Fiona Gallagher", "email": "fiona.g@smartcampus.edu", "department": "Business Administration", "enrollment_year": 2023, "status": "Suspended"},
            {"id": "STU107", "name": "George Cooper", "email": "george.c@smartcampus.edu", "department": "Electronics", "enrollment_year": 2024, "status": "Active"},
            {"id": "STU108", "name": "Hannah Abbott", "email": "hannah.a@smartcampus.edu", "department": "Computer Science", "enrollment_year": 2025, "status": "Active"},
        ]
        save_students(mock_students)
        log_activity("system", "Bootstrap Students", f"Created {len(mock_students)} mock student profiles")
        students = mock_students

    # 4. Check and generate faculty
    faculty = get_all_faculty()
    if not faculty:
        mock_faculty = [
            {"id": "FAC201", "name": "Dr. Robert Chen", "email": "r.chen@smartcampus.edu", "department": "Computer Science", "designation": "Professor & Head", "status": "Active"},
            {"id": "FAC202", "name": "Dr. Sarah Jenkins", "email": "s.jenkins@smartcampus.edu", "department": "Information Technology", "designation": "Associate Professor", "status": "Active"},
            {"id": "FAC203", "name": "Prof. Alan Turing", "email": "a.turing@smartcampus.edu", "department": "Computer Science", "designation": "Professor Emeritus", "status": "Active"},
            {"id": "FAC204", "name": "Dr. Grace Hopper", "email": "g.hopper@smartcampus.edu", "department": "Information Technology", "designation": "Professor", "status": "Active"},
            {"id": "FAC205", "name": "Dr. Richard Feynman", "email": "r.feynman@smartcampus.edu", "department": "Mechanical", "designation": "Associate Professor", "status": "Active"},
        ]
        save_faculty(mock_faculty)
        log_activity("system", "Bootstrap Faculty", f"Created {len(mock_faculty)} mock faculty profiles")

    # 5. Check and generate attendance history
    attendance = get_all_attendance()
    if not attendance:
        mock_attendance = []
        classes = ["CS101", "IT202", "ECE303", "ME404", "BA505"]
        statuses = ["Present", "Present", "Present", "Absent", "Excused"] # weight present higher
        
        # Populate attendance for the last 5 days
        today = datetime.now()
        for d in range(5, 0, -1):
            date_str = (today - timedelta(days=d)).strftime("%Y-%m-%d")
            for student in students:
                # determine class based on department
                if student["department"] == "Computer Science":
                    c_name = "CS101"
                elif student["department"] == "Information Technology":
                    c_name = "IT202"
                elif student["department"] == "Electronics":
                    c_name = "ECE303"
                elif student["department"] == "Mechanical":
                    c_name = "ME404"
                else:
                    c_name = "BA505"
                    
                mock_attendance.append({
                    "date": date_str,
                    "student_id": student["id"],
                    "student_name": student["name"],
                    "class_name": c_name,
                    "status": random.choice(statuses)
                })
        save_attendance(mock_attendance)
        log_activity("system", "Bootstrap Attendance", "Created mock attendance logs for past 5 days")

def get_gradient_text_html(text: str, font_size: str = "24px", align: str = "left") -> str:
    """Helper to get glowing gradient text markup."""
    return f"""
    <div style='text-align: {align}; font-size: {font_size}; font-weight: 800;
                background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
        {text}
    </div>
    """

def get_glass_card_html(content_html: str) -> str:
    """Helper to wrap HTML content in a styled glassmorphic container."""
    return f"""
    <div class="glass-card">
        {content_html}
    </div>
    """
