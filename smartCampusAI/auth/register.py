import streamlit as st
from auth.auth_utils import render_auth_header
from utils.json_db import add_user, log_activity
from utils.validators import validate_email, validate_password_strength, validate_empty_fields
from utils.helpers import load_css

def show_register_page():
    # Load styling
    load_css()
    
    # Header branding
    render_auth_header("Create Account")
    
    _, center_col, _ = st.columns([1, 2.5, 1])
    
    with center_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Register New User")
        
        # Registration fields
        username = st.text_input("Username", placeholder="e.g. john_doe", key="reg_username")
        email = st.text_input("Email Address", placeholder="e.g. john@smartcampus.edu", key="reg_email")
        
        show_password = st.checkbox("Show Password", key="reg_show_pwd")
        pwd_type = "default" if show_password else "password"
        
        password = st.text_input("Password", type=pwd_type, placeholder="••••••••", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type=pwd_type, placeholder="••••••••", key="reg_confirm")
        
        role = st.selectbox("Register As", ["Student", "Faculty"], key="reg_role")
        
        st.write("")
        register_clicked = st.button("Register Now", key="reg_btn")
        
        if register_clicked:
            # Validate input fields
            has_empty, empty_fields = validate_empty_fields(
                username=username,
                email=email,
                password=password,
                confirm_password=confirm_password
            )
            
            if has_empty:
                st.error(f"Please fill in all fields: {', '.join(empty_fields)}")
            elif not validate_email(email):
                st.error("Please enter a valid email address.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                # Password strength check
                is_strong, reason = validate_password_strength(password)
                if not is_strong:
                    st.error(reason)
                else:
                    # Register user
                    success, message = add_user(username, email, password, role)
                    if success:
                        st.success("Account created successfully! Please navigate to Login.")
                        st.toast("Registration success!", icon="🎉")
                        log_activity(username, "Registration", f"New user registered as {role}")
                    else:
                        st.error(message)
                        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_register_page()
