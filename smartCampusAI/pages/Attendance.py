import streamlit as st
import pandas as pd
from datetime import datetime
from utils.helpers import load_css
from components.navbar import render_navbar
from components.footer import render_footer
from dashboard.sidebar import render_sidebar
from utils.json_db import get_all_students, get_all_attendance, save_attendance, log_activity

# Setup visual elements
load_css()
render_sidebar()
render_navbar("Attendance Sheets")

# Permissions Check
role = st.session_state.get("role", "Student")
is_admin_or_faculty = role in ["Admin", "Faculty"]

attendance = get_all_attendance()
students = get_all_students()

tab1, tab2 = st.tabs(["Attendance Log", "Record Attendance"])

with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Attendance Records Search")
    
    # Filter tools
    col_d, col_c, col_s = st.columns([1, 1, 2])
    with col_d:
        dates = sorted(list(set(a["date"] for a in attendance if a.get("date"))), reverse=True)
        selected_date = st.selectbox("Date", ["All"] + dates)
    with col_c:
        classes = sorted(list(set(a["class_name"] for a in attendance if a.get("class_name"))))
        selected_class = st.selectbox("Class/Course", ["All"] + classes)
    with col_s:
        search_query = st.text_input("🔍 Search Student Name or ID", placeholder="Search...")
        
    filtered_att = attendance
    if selected_date != "All":
        filtered_att = [a for a in filtered_att if a.get("date") == selected_date]
    if selected_class != "All":
        filtered_att = [a for a in filtered_att if a.get("class_name") == selected_class]
    if search_query:
        q = search_query.lower()
        filtered_att = [
            a for a in filtered_att 
            if q in a.get("student_name", "").lower() or q in a.get("student_id", "").lower()
        ]
        
    if filtered_att:
        df = pd.DataFrame(filtered_att)
        df.columns = ["Date", "Student ID", "Student Name", "Class/Course", "Attendance Status"]
        # Sort by date descending
        df = df.sort_values("Date", ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No attendance logs found matching filters.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    if not is_admin_or_faculty:
        st.warning("⚠️ Access Denied. Only Admins and Faculty can record class attendance.")
    else:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Mark Class Attendance Sheet")
        
        # Setup form filters
        col_cname, col_cdate = st.columns(2)
        with col_cname:
            target_class = st.selectbox("Select Course/Class", ["CS101", "IT202", "ECE303", "ME404", "BA505"])
        with col_cdate:
            target_date = st.date_input("Select Date", max_value=datetime.today())
            
        date_str = target_date.strftime("%Y-%m-%d")
        
        if not students:
            st.warning("No students registered in the system. Go to the Students page to add records.")
        else:
            st.info("Mark the attendance status for each student below, then submit.")
            
            # Setup interactive container
            # We can use checkboxes or select boxes for each student
            attendance_map = {}
            
            # Load existing record if any to pre-populate statuses
            existing_records = {a["student_id"]: a["status"] for a in attendance if a["date"] == date_str and a["class_name"] == target_class}
            
            # Draw roster table
            st.write("---")
            for i, student in enumerate(students):
                col_name, col_dept, col_status = st.columns([2, 1, 1.5])
                with col_name:
                    st.write(f"**{student['name']}** ({student['id']})")
                with col_dept:
                    st.write(student["department"])
                with col_status:
                    # Pre-select status if exists, else Present
                    default_status = existing_records.get(student["id"], "Present")
                    status_idx = ["Present", "Absent", "Excused"].index(default_status)
                    
                    status_val = st.radio(
                        f"Status for {student['id']}",
                        ["Present", "Absent", "Excused"],
                        index=status_idx,
                        horizontal=True,
                        key=f"att_{student['id']}_{i}",
                        label_visibility="collapsed"
                    )
                    attendance_map[student["id"]] = {
                        "name": student["name"],
                        "status": status_val
                    }
                    
            st.write("---")
            submit_attendance = st.button("Save Roster Attendance")
            
            if submit_attendance:
                # Remove existing records for this class & date
                clean_attendance = [
                    a for a in attendance 
                    if not (a["date"] == date_str and a["class_name"] == target_class)
                ]
                
                # Append updated records
                for stu_id, data in attendance_map.items():
                    clean_attendance.append({
                        "date": date_str,
                        "student_id": stu_id,
                        "student_name": data["name"],
                        "class_name": target_class,
                        "status": data["status"]
                    })
                    
                if save_attendance(clean_attendance):
                    st.success(f"Attendance recorded successfully for class {target_class} on {date_str}!")
                    st.toast("Attendance sheet updated!", icon="📅")
                    log_activity(
                        st.session_state.get("username", "system"), 
                        "Mark Attendance", 
                        f"Logged attendance for {target_class} on {date_str}"
                    )
                    st.rerun()
                else:
                    st.error("Failed to write to attendance database.")
                    
        st.markdown('</div>', unsafe_allow_html=True)

render_footer()
