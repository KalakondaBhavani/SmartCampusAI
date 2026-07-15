import streamlit as st
import pandas as pd
from utils.helpers import load_css
from components.navbar import render_navbar
from components.footer import render_footer
from dashboard.sidebar import render_sidebar
from utils.json_db import get_all_students, save_students, log_activity
from utils.validators import validate_email, validate_empty_fields

# Load styling
load_css()
render_sidebar()
render_navbar("Students Management")

# Check permissions
role = st.session_state.get("role", "Student")
is_admin_or_faculty = role in ["Admin", "Faculty"]

students = get_all_students()

# Tabs
tab1, tab2 = st.tabs(["Student Roster", "Manage Records"])

with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Roster Directory")
    
    # Filter controls
    col_s, col_d = st.columns([2, 1])
    with col_s:
        search_query = st.text_input("🔍 Search by Name or ID", placeholder="Search...")
    with col_d:
        depts = sorted(list(set(s["department"] for s in students if s.get("department"))))
        selected_dept = st.selectbox("Filter by Department", ["All"] + depts)
        
    # Apply filters
    filtered_students = students
    if search_query:
        q = search_query.lower()
        filtered_students = [
            s for s in filtered_students 
            if q in s.get("name", "").lower() or q in s.get("id", "").lower() or q in s.get("email", "").lower()
        ]
    if selected_dept != "All":
        filtered_students = [s for s in filtered_students if s.get("department") == selected_dept]
        
    if filtered_students:
        df = pd.DataFrame(filtered_students)
        df.columns = ["Student ID", "Full Name", "Email", "Department", "Enrollment Year", "Status"]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No students found matching current search parameters.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    if not is_admin_or_faculty:
        st.warning("⚠️ Access Denied. Only Admins and Faculty can edit student records.")
    else:
        col_add, col_edit = st.columns(2)
        
        with col_add:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Add Student Record")
            
            with st.form("add_student_form", clear_on_submit=True):
                stu_id = st.text_input("Student ID (e.g. STU109)")
                name = st.text_input("Full Name")
                email = st.text_input("Email Address")
                dept = st.selectbox("Department", ["Computer Science", "Information Technology", "Electronics", "Mechanical", "Business Administration"])
                year = st.number_input("Enrollment Year", min_value=2020, max_value=2030, value=2026)
                status = st.selectbox("Status", ["Active", "Suspended", "Graduated"])
                
                submit_add = st.form_submit_button("Add Record")
                
                if submit_add:
                    has_empty, _ = validate_empty_fields(id=stu_id, name=name, email=email)
                    if has_empty:
                        st.error("Please fill in ID, Name, and Email.")
                    elif not validate_email(email):
                        st.error("Invalid email address format.")
                    elif any(s["id"].lower() == stu_id.lower() for s in students):
                        st.error(f"Student ID '{stu_id}' already exists.")
                    elif any(s["email"].lower() == email.lower() for s in students):
                        st.error(f"Student Email '{email}' already registered.")
                    else:
                        new_student = {
                            "id": stu_id,
                            "name": name,
                            "email": email,
                            "department": dept,
                            "enrollment_year": int(year),
                            "status": status
                        }
                        students.append(new_student)
                        if save_students(students):
                            st.success(f"Added student: {name}")
                            st.toast("Student record added!", icon="🎓")
                            log_activity(st.session_state.get("username", "system"), "Add Student", f"Added student: {name} (ID: {stu_id})")
                            st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_edit:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Modify / Delete Student")
            
            if not students:
                st.info("No student records available to edit.")
            else:
                student_options = {f"{s['name']} ({s['id']})": s for s in students}
                selected_opt = st.selectbox("Select Student Profile", list(student_options.keys()))
                
                if selected_opt:
                    target_student = student_options[selected_opt]
                    
                    with st.form("edit_student_form"):
                        edit_name = st.text_input("Full Name", value=target_student["name"])
                        edit_email = st.text_input("Email Address", value=target_student["email"])
                        edit_dept = st.selectbox(
                            "Department", 
                            ["Computer Science", "Information Technology", "Electronics", "Mechanical", "Business Administration"],
                            index=["Computer Science", "Information Technology", "Electronics", "Mechanical", "Business Administration"].index(target_student["department"])
                        )
                        edit_year = st.number_input("Enrollment Year", min_value=2020, max_value=2030, value=target_student["enrollment_year"])
                        edit_status = st.selectbox(
                            "Status", 
                            ["Active", "Suspended", "Graduated"],
                            index=["Active", "Suspended", "Graduated"].index(target_student["status"])
                        )
                        
                        col_save, col_del = st.columns([1, 1])
                        with col_save:
                            save_clicked = st.form_submit_button("Save Updates")
                        with col_del:
                            delete_clicked = st.form_submit_button("Delete Profile")
                            
                        if save_clicked:
                            if not edit_name or not edit_email:
                                st.error("Name and Email are required.")
                            elif not validate_email(edit_email):
                                st.error("Invalid email address format.")
                            else:
                                # Apply changes
                                for i, s in enumerate(students):
                                    if s["id"] == target_student["id"]:
                                        students[i]["name"] = edit_name
                                        students[i]["email"] = edit_email
                                        students[i]["department"] = edit_dept
                                        students[i]["enrollment_year"] = int(edit_year)
                                        students[i]["status"] = edit_status
                                        break
                                if save_students(students):
                                    st.success(f"Updated profile: {edit_name}")
                                    st.toast("Profile updated!", icon="✏️")
                                    log_activity(st.session_state.get("username", "system"), "Edit Student", f"Updated student ID: {target_student['id']}")
                                    st.rerun()
                                    
                        if delete_clicked:
                            updated_students = [s for s in students if s["id"] != target_student["id"]]
                            if save_students(updated_students):
                                st.success(f"Deleted profile: {target_student['name']}")
                                st.toast("Profile deleted!", icon="🗑️")
                                log_activity(st.session_state.get("username", "system"), "Delete Student", f"Deleted student: {target_student['name']} (ID: {target_student['id']})")
                                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

render_footer()
