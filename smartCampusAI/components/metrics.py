import streamlit as st

def render_custom_metric(label: str, value: str, icon: str = "📊", change: str = None, change_type: str = "up"):
    """Renders a glowing glassmorphic metric container with dynamic trend badges."""
    change_badge = ""
    if change:
        color = "#10b981" if change_type == "up" else "#ef4444"
        arrow = "▲" if change_type == "up" else "▼"
        change_badge = f"""
            <span style='background-color: {color}1A; color: {color}; 
                         font-size: 0.75rem; font-weight: 700; padding: 3px 8px; 
                         border-radius: 20px; margin-left: 8px; border: 1px solid {color}33;'>
                {arrow} {change}
            </span>
        """
        
    st.markdown(f"""
        <div class="glass-card" style="display: flex; align-items: center; justify-content: space-between; min-height: 120px;">
            <div class="metric-container">
                <div class="metric-label">{label}</div>
                <div style="display: flex; align-items: center; margin-top: 5px;">
                    <span class="metric-value" style="margin: 0;">{value}</span>
                    {change_badge}
                </div>
            </div>
            <div style="font-size: 2rem; background: rgba(255, 255, 255, 0.05); 
                        padding: 12px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05);
                        display: flex; align-items: center; justify-content: center; width: 56px; height: 56px;">
                {icon}
            </div>
        </div>
    """, unsafe_allow_html=True)
