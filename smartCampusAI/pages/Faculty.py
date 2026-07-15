import streamlit as st
import pandas as pd
from utils.helpers import load_css
from components.navbar import render_navbar
from components.footer import render_footer
from dashboard.sidebar import render_sidebar
from utils.json_db import get_all_faculty, save_faculty, log_activity
from utils.validators import validate_email, validate_empty_fields

# Setup UI layout
load_css()
render_sidebar()
render_navbar("Faculty Management")

# Role checking - Faculty & Admin can browse, only Admin can write
role = st.session_state.get("role", "Student")
is_admin = role == "Admin"

faculty = get_all_faculty()

tab1, tab2 = st.tabs(["Faculty Directory", "Manage Faculty"])

with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Roster Directory")
    
    # Filter controllers
    col_s, col_d = st.columns([2, 1])
    with col_s:
        search_query = st.text_input("🔍 Search by Name or ID", placeholder="Search...", key="fac_search")
    with col_d:
        depts = sorted(list(set(f["department"] for f in faculty if f.get("department"))))
        selected_dept = st.selectbox("Filter by Department", ["All"] + depts, key="fac_dept_filter")
        
    filtered_faculty = faculty
    if search_query:
        q = search_query.lower()
        filtered_faculty = [
            f for f in filtered_faculty 
            if q in f.get("name", "").lower() or q in f.get("id", "").lower() or q in f.get("email", "").lower()
        ]
    if selected_dept != "All":
        filtered_faculty = [f for f in filtered_faculty if f.get("department") == selected_dept]
        
    if filtered_faculty:
        df = pd.DataFrame(filtered_faculty)
        df.columns = ["Faculty ID", "Full Name", "Email", "Department", "Designation", "Status"]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No faculty profiles matched current criteria.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    if not is_admin:
        st.warning("⚠️ Access Denied. Only Admins can modify faculty profiles.")
    else:
        col_add, col_edit = st.columns(2)
        
        with col_add:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Add Faculty Member")
            
            with st.form("add_faculty_form", clear_on_submit=True):
                fac_id = st.text_input("Faculty ID (e.g. FAC206)")
                name = st.text_input("Full Name")
                email = st.text_input("Email Address")
                dept = st.selectbox("Department", ["Computer Science", "Information Technology", "Electronics", "Mechanical", "Business Administration"], key="add_fac_dept")
                designation = st.selectbox("Designation", ["Professor & Head", "Professor", "Associate Professor", "Assistant Professor", "Lecturer"])
                status = st.selectbox("Status", ["Active", "On Leave", "Retired"])
                
                submit_add = st.form_submit_button("Add Member")
                
                if submit_add:
                    has_empty, _ = validate_empty_fields(id=fac_id, name=name, email=email)
                    if has_empty:
                        st.error("Please fill in Faculty ID, Name, and Email.")
                    elif not validate_email(email):
                        st.error("Invalid email address format.")
                    elif any(f["id"].lower() == fac_id.lower() for f in faculty):
                        st.error(f"Faculty ID '{fac_id}' already exists.")
                    elif any(f["email"].lower() == email.lower() for f in faculty):
                        st.error(f"Email '{email}' is already in use.")
                    else:
                        new_fac = {
                            "id": fac_id,
                            "name": name,
                            "email": email,
                            "department": dept,
                            "designation": designation,
                            "status": status
                        }
                        faculty.append(new_fac)
                        if save_faculty(faculty):
                            st.success(f"Successfully added faculty: {name}")
                            st.toast("Faculty record added!", icon="🧑‍🏫")
                            log_activity(st.session_state.get("username", "system"), "Add Faculty", f"Added faculty member: {name} (ID: {fac_id})")
                            st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_edit:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Modify / Delete Faculty")
            
            if not faculty:
                st.info("No faculty profiles available to edit.")
            else:
                fac_options = {f"{f['name']} ({f['id']})": f for f in faculty}
                selected_opt = st.selectbox("Select Faculty Profile", list(fac_options.keys()))
                
                if selected_opt:
                    target_fac = fac_options[selected_opt]
                    
                    with st.form("edit_faculty_form"):
                        edit_name = st.text_input("Full Name", value=target_fac["name"])
                        edit_email = st.text_input("Email Address", value=target_fac["email"])
                        edit_dept = st.selectbox(
                            "Department", 
                            ["Computer Science", "Information Technology", "Electronics", "Mechanical", "Business Administration"],
                            index=["Computer Science", "Information Technology", "Electronics", "Mechanical", "Business Administration"].index(target_fac["department"])
                        )
                        edit_designation = st.selectbox(
                            "Designation",
                            ["Professor & Head", "Professor", "Associate Professor", "Assistant Professor", "Lecturer"],
                            index=["Professor & Head", "Professor", "Associate Professor", "Assistant Professor", "Lecturer"].index(target_fac["designation"])
                        )
                        edit_status = st.selectbox(
                            "Status", 
                            ["Active", "On Leave", "Retired"],
                            index=["Active", "On Leave", "Retired"].index(target_fac["status"])
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
                                for i, f in enumerate(faculty):
                                    if f["id"] == target_fac["id"]:
                                        faculty[i]["name"] = edit_name
                                        faculty[i]["email"] = edit_email
                                        faculty[i]["department"] = edit_dept
                                        faculty[i]["designation"] = edit_designation
                                        faculty[i]["status"] = edit_status
                                        break
                                if save_faculty(faculty):
                                    st.success(f"Updated profile: {edit_name}")
                                    st.toast("Profile updated!", icon="✏️")
                                    log_activity(st.session_state.get("username", "system"), "Edit Faculty", f"Updated faculty ID: {target_fac['id']}")
                                    st.rerun()
                                    
                        if delete_clicked:
                            updated_fac = [f for f in faculty if f["id"] != target_fac["id"]]
                            if save_faculty(updated_fac):
                                st.success(f"Deleted profile: {target_fac['name']}")
                                st.toast("Profile deleted!", icon="🗑️")
                                log_activity(st.session_state.get("username", "system"), "Delete Faculty", f"Deleted faculty member: {target_fac['name']} (ID: {target_fac['id']})")
                                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

render_footer()
