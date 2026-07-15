import streamlit as st

def action_button(label: str, key: str = None) -> bool:
    """
    Renders a premium styled button.
    In association with styles.css, this automatically gets styled as a gradient hover button.
    """
    return st.button(label, key=key)

def danger_button(label: str, key: str = None) -> bool:
    """
    Renders a styled red danger button by using key for custom styling.
    """
    # Adding inline style wrapper for danger buttons if they match key
    st.markdown("""
        <style>
            div.stButton > button[key*="danger"] {
                background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%) !important;
                box-shadow: 0 4px 14px rgba(239, 68, 68, 0.3) !important;
            }
            div.stButton > button[key*="danger"]:hover {
                background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%) !important;
                box-shadow: 0 6px 20px rgba(239, 68, 68, 0.5) !important;
            }
        </style>
    """, unsafe_allow_html=True)
    return st.button(label, key=key)
