import streamlit as st
from utils.helpers import load_css
from components.navbar import render_navbar
from components.footer import render_footer
from dashboard.sidebar import render_sidebar
from utils.json_db import update_profile, get_all_users, log_activity
from utils.validators import validate_email, validate_empty_fields

# Page layout
load_css()
render_sidebar()
render_navbar("User Profile Page")

# Load session user
username = st.session_state.get("username")
email = st.session_state.get("email")
role = st.session_state.get("role")
user_details = st.session_state.get("user_details", {})

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("Edit Profile Card")

# Retrieve latest user details directly from DB to make sure we are in sync
users = get_all_users()
current_user = next((u for u in users if u["username"].lower() == username.lower()), user_details)

with st.form("profile_form"):
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.text_input("Username (Read Only)", value=username, disabled=True)
        role_input = st.text_input("Account Role (Read Only)", value=role, disabled=True)
        email_input = st.text_input("Registered Email Address", value=current_user.get("email", email))
        
    with col_r:
        phone_input = st.text_input("Contact Telephone", value=current_user.get("phone", ""))
        dept_input = st.selectbox(
            "Campus Department", 
            ["Not Assigned", "Computer Science", "Information Technology", "Electronics", "Mechanical", "Business Administration"],
            index=["Not Assigned", "Computer Science", "Information Technology", "Electronics", "Mechanical", "Business Administration"].index(current_user.get("department", "Not Assigned"))
        )
        
    bio_input = st.text_area("Personal Bio Description", value=current_user.get("bio", "Bio is empty."))
    
    st.write("")
    submit_profile = st.form_submit_button("Update Profile Details")
    
    if submit_profile:
        has_empty, _ = validate_empty_fields(email=email_input)
        if has_empty:
            st.error("Email address cannot be empty.")
        elif not validate_email(email_input):
            st.error("Invalid email address format.")
        else:
            # Build update package
            additional_info = {
                "phone": phone_input,
                "department": dept_input,
                "bio": bio_input
            }
            # Execute update
            success, message = update_profile(username, email_input, role, additional_info)
            if success:
                st.success("Profile details updated successfully!")
                st.toast("Profile updated!", icon="👤")
                
                # Sync session state
                st.session_state.email = email_input
                # Retrieve updated dict
                updated_users = get_all_users()
                st.session_state.user_details = next((u for u in updated_users if u["username"].lower() == username.lower()), current_user)
                
                st.rerun()
            else:
                st.error(message)

st.markdown('</div>', unsafe_allow_html=True)

render_footer()
