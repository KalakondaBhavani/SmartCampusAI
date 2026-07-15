import streamlit as st
from auth.auth_utils import render_auth_header
from auth.session import login_user
from utils.json_db import authenticate_user, add_user, log_activity
from utils.validators import validate_email, validate_password_strength, validate_empty_fields
from utils.helpers import load_css, get_glass_card_html

def show_login_page():
    # Inject styling
    load_css()
    
    # Outer visual container
    render_auth_header("Secure Gateway")
    
    _, center_col, _ = st.columns([1, 2.5, 1])
    
    with center_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Sign In / Sign Up")
        
        # User Choice: Toggle fields depending on flow, but both forms are accessible
        flow = st.radio("Select Action", ["Login", "Register"], horizontal=True)
        
        # Username & Email
        username = st.text_input("Username", placeholder="e.g. admin")
        email = st.text_input("Email Address", placeholder="e.g. user@smartcampus.edu")
        
        # Show Password Toggle
        show_password = st.checkbox("Show Password")
        pwd_type = "default" if show_password else "password"
        
        password = st.text_input("Password", type=pwd_type, placeholder="••••••••")
        confirm_password = None
        
        if flow == "Register":
            confirm_password = st.text_input("Confirm Password", type=pwd_type, placeholder="••••••••")
            role = st.selectbox("Register As", ["Student", "Faculty"])
            
        remember_me = st.checkbox("Remember Me", value=True)
        
        # Form buttons layout
        st.write("")
        if flow == "Login":
            col_btn, col_link = st.columns([1, 1])
            with col_btn:
                login_clicked = st.button("Login")
            with col_link:
                # Forgot Password Simulation
                forgot_clicked = st.button("Forgot Password?")
                
            if forgot_clicked:
                if not username and not email:
                    st.warning("Please provide your Username or Email to request a reset.")
                else:
                    st.success(f"Password reset link sent to registered email for '{username or email}'!")
                    log_activity(username or "anonymous", "Forgot Password Request", f"Reset link simulated for input: {username or email}")
            
            if login_clicked:
                # Validation
                has_empty, empty_fields = validate_empty_fields(
                    username_or_email=username or email,
                    password=password
                )
                if has_empty:
                    st.error("Please fill in Username (or Email) and Password.")
                else:
                    success, user_data = authenticate_user(username or email, password)
                    if success and user_data:
                        login_user(user_data)
                        st.toast(f"Welcome back, {user_data['username']}!", icon="👋")
                        st.rerun()
                    else:
                        st.error("Invalid username/email or password.")
                        
        else: # Register flow
            col_reg, _ = st.columns([1, 1])
            with col_reg:
                register_clicked = st.button("Register")
                
            if register_clicked:
                # Validate inputs
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
                    is_strong, reason = validate_password_strength(password)
                    if not is_strong:
                        st.error(reason)
                    else:
                        success, message = add_user(username, email, password, role)
                        if success:
                            st.success(f"Registration successful! You can now log in.")
                            st.toast("Account created successfully!", icon="🎉")
                        else:
                            st.error(message)
                            
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_login_page()
