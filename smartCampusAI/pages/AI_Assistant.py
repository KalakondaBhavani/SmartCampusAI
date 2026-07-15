import streamlit as st
import os
import requests
from dotenv import load_dotenv
from utils.helpers import load_css
from components.navbar import render_navbar
from components.footer import render_footer
from dashboard.sidebar import render_sidebar
from utils.json_db import get_all_students, get_all_faculty, get_all_attendance, log_activity, load_json, ACTIVITY_FILE

# Load environment variables
load_dotenv()

# Setup UI
load_css()
render_sidebar()
render_navbar("AI Smart Campus Assistant")

# Check API Keys
env_openai_key = os.getenv("OPENAI_API_KEY", "").strip()
env_gemini_key = os.getenv("GEMINI_API_KEY", "").strip()

# Let user override or input key in the sidebar if not set in environment
with st.sidebar:
    st.markdown("### 🤖 AI Service Config")
    user_api_provider = st.selectbox("API Provider", ["Gemini (Recommended)", "OpenAI", "Local Campus Solver"])
    
    custom_key = st.text_input("Enter API Key (Optional Override)", type="password", help="If empty, looks in .env")
    
    active_key = custom_key if custom_key else (env_gemini_key if "Gemini" in user_api_provider else env_openai_key)
    
    if active_key:
        st.success("API Key Status: Configured ✓")
    else:
        st.warning("Running in Local Offline mode. Fill .env or input key to enable LLM.")

# Fetch system data context to feed into prompt or fallback solver
students = get_all_students()
faculty = get_all_faculty()
attendance = get_all_attendance()
activities = load_json(ACTIVITY_FILE)

# Local query handler (off-line intelligence)
def local_campus_solver(query: str) -> str:
    query_lower = query.lower()
    
    # 1. Students count
    if "student" in query_lower and ("count" in query_lower or "how many" in query_lower or "total" in query_lower):
        active_count = sum(1 for s in students if s.get("status") == "Active")
        suspended_count = sum(1 for s in students if s.get("status") == "Suspended")
        return f"Currently, there are **{len(students)}** registered students in the database. Out of these, **{active_count}** are Active and **{suspended_count}** are Suspended."
    
    # 2. Faculty count
    if "faculty" in query_lower or "professor" in query_lower or "teacher" in query_lower:
        if "how many" in query_lower or "count" in query_lower or "total" in query_lower:
            return f"There are **{len(faculty)}** faculty members across all campus departments."
        # search specific professor
        for fac in faculty:
            if fac["name"].lower().split()[-1] in query_lower or fac["name"].lower() in query_lower:
                return f"**Faculty Match Found:**\n- **Name:** {fac['name']}\n- **Designation:** {fac['designation']}\n- **Department:** {fac['department']}\n- **Status:** {fac['status']}\n- **Email:** {fac['email']}"
        depts = set(f["department"] for f in faculty)
        dept_str = ", ".join(depts)
        return f"Campus Faculty comprises {len(faculty)} professors across departments: {dept_str}. Ask me about a specific professor!"

    # 3. Attendance rates
    if "attendance" in query_lower:
        if attendance:
            present = sum(1 for a in attendance if a["status"] == "Present")
            rate = (present / len(attendance)) * 100
            
            # check specific student attendance
            for s in students:
                name_words = s["name"].lower().split()
                if any(w in query_lower for w in name_words if len(w) > 2):
                    stu_att = [a for a in attendance if a["student_id"] == s["id"]]
                    if stu_att:
                        stu_pres = sum(1 for a in stu_att if a["status"] == "Present")
                        stu_rate = (stu_pres / len(stu_att)) * 100
                        return f"**Attendance Profile for {s['name']} ({s['id']}):**\n- Recorded days: {len(stu_att)}\n- Present: {stu_pres}\n- Attendance rate: **{stu_rate:.1f}%**"
                    return f"No attendance history recorded yet for student {s['name']} ({s['id']})."
                    
            return f"The general campus attendance rate across all recorded courses is **{rate:.1f}%** (Total: {len(attendance)} logs)."
        return "No class attendance logs have been recorded in the JSON database yet."
        
    # 4. Recent activities
    if "activity" in query_lower or "recent" in query_lower or "log" in query_lower:
        if activities:
            latest = activities[0]
            return f"The latest system action was performed by **{latest.get('username')}** at {latest.get('timestamp')[:16].replace('T', ' ')}:\n- **Action:** {latest.get('action')}\n- **Details:** {latest.get('details')}"
        return "System activity log is currently empty."
        
    # Default message
    return """
    **Hello! I am your SmartCampusAI Offline Assistant.** 
    Since no LLM API key is actively configured, I am resolving queries locally based on the database. Try asking:
    1. *'How many students are enrolled?'*
    2. *'Who is on the faculty list?'*
    3. *'What is the overall attendance rate?'*
    4. *'Show attendance details for Alice Johnson.'*
    """

# LLM remote caller
def query_llm(provider: str, key: str, prompt: str) -> str:
    # Build database context summaries to inject
    context = f"""
    You are an AI Campus Assistant for SmartCampusAI.
    Here is the current live campus database context to help you answer user queries accurately.
    
    1. Students list: {students}
    2. Faculty list: {faculty}
    3. Attendance summary: {attendance[:30]} (showing up to 30 logs)
    4. Recent activity logged: {activities[:5]}
    
    Query: {prompt}
    
    Answer concisely based on the data provided above.
    """
    
    try:
        if "Gemini" in provider:
            # REST endpoint for Gemini
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": context}]}]
            }
            res = requests.post(url, json=payload, headers=headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return f"Gemini API Error (Status {res.status_code}): {res.text}"
                
        elif "OpenAI" in provider:
            # REST endpoint for OpenAI
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}"
            }
            payload = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": context}],
                "temperature": 0.5
            }
            res = requests.post(url, json=payload, headers=headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                return data["choices"][0]["message"]["content"]
            else:
                return f"OpenAI API Error (Status {res.status_code}): {res.text}"
    except Exception as e:
        return f"Connection Failed: {e}. Falling back to offline solver..."
        
    return local_campus_solver(prompt)

# Chat engine state management
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Welcome! I can assist you with student directory details, faculty allocations, attendance stats, and recent campus activities. What would you like to know?"}
    ]

# Render conversational interface
st.markdown('<div class="glass-card" style="margin-bottom: 20px;">', unsafe_allow_html=True)
st.subheader("Conversational Campus Assistant")

# Display chats
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
st.markdown('</div>', unsafe_allow_html=True)

# Process User Prompt
user_input = st.chat_input("Ask a question about the campus...")

if user_input:
    # Append user question
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Render immediately
    with st.chat_message("user"):
        st.write(user_input)
        
    with st.spinner("Processing campus intelligence..."):
        if not active_key or "Local" in user_api_provider:
            response_text = local_campus_solver(user_input)
        else:
            response_text = query_llm(user_api_provider, active_key, user_input)
            
        # Log AI action in database
        log_activity(st.session_state.get("username", "system"), "AI Query", f"Question: {user_input[:40]}...")
        
    # Append and render assistant answer
    st.session_state.chat_history.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.write(response_text)
    
    st.rerun()

render_footer()
