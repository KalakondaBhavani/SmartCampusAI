import streamlit as st
import pandas as pd
import json
from utils.helpers import load_css
from components.navbar import render_navbar
from components.footer import render_footer
from dashboard.sidebar import render_sidebar
from utils.json_db import get_all_students, get_all_faculty, get_all_attendance, log_activity

# Page settings
load_css()
render_sidebar()
render_navbar("Export Center & Reports")

students = get_all_students()
faculty = get_all_faculty()
attendance = get_all_attendance()

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("Data Export Hub")
st.write("Generate clean reports of your campus databases. Choose the category and format below.")

category = st.selectbox("Select Report Dataset", ["Student Roster", "Faculty Directory", "Attendance Registers"])
file_format = st.radio("Choose Output Format", ["CSV", "JSON"], horizontal=True)

st.write("")

# Process datasets
target_data = []
filename = ""

if category == "Student Roster":
    target_data = students
    filename = f"students_report_{pd.Timestamp.now().strftime('%Y%m%d')}"
elif category == "Faculty Directory":
    target_data = faculty
    filename = f"faculty_report_{pd.Timestamp.now().strftime('%Y%m%d')}"
elif category == "Attendance Registers":
    target_data = attendance
    filename = f"attendance_report_{pd.Timestamp.now().strftime('%Y%m%d')}"

if not target_data:
    st.warning(f"The selected dataset ({category}) is currently empty. No data to export.")
else:
    # Preview data
    st.write("**Dataset Preview:**")
    df_preview = pd.DataFrame(target_data)
    st.dataframe(df_preview.head(10), use_container_width=True, hide_index=True)
    if len(target_data) > 10:
        st.write(f"*Showing 10 of {len(target_data)} total records.*")
        
    # Generate download package
    if file_format == "CSV":
        export_bytes = df_preview.to_csv(index=False).encode("utf-8")
        mime_type = "text/csv"
        filename_full = f"{filename}.csv"
    else: # JSON
        export_bytes = json.dumps(target_data, indent=4, ensure_ascii=False).encode("utf-8")
        mime_type = "application/json"
        filename_full = f"{filename}.json"
        
    # Download Action
    st.write("")
    download_clicked = st.download_button(
        label=f"📥 Download {category} ({file_format})",
        data=export_bytes,
        file_name=filename_full,
        mime=mime_type,
        use_container_width=True
    )
    
    if download_clicked:
        st.toast("Report download initialized!", icon="📥")
        log_activity(
            st.session_state.get("username", "system"), 
            "Export Report", 
            f"Downloaded {category} as {file_format}"
        )
st.markdown('</div>', unsafe_allow_html=True)

render_footer()
