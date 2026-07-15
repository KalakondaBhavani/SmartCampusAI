import os
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from utils.security import hash_password, verify_password

# Constants
DB_DIR = os.getenv("DB_DIR", "database")
USERS_FILE = os.path.join(DB_DIR, "users.json")
ACTIVITY_FILE = os.path.join(DB_DIR, "activity.json")
SETTINGS_FILE = os.path.join(DB_DIR, "settings.json")
STUDENTS_FILE = os.path.join(DB_DIR, "students.json")
FACULTY_FILE = os.path.join(DB_DIR, "faculty.json")
ATTENDANCE_FILE = os.path.join(DB_DIR, "attendance.json")

def ensure_db_dir():
    """Ensure the database directory exists."""
    os.makedirs(DB_DIR, exist_ok=True)

def load_json(file_path: str) -> Any:
    """Loads a JSON file from disk. Returns empty dict or list if file not found."""
    ensure_db_dir()
    if not os.path.exists(file_path):
        return [] if "settings.json" not in file_path else {}
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return [] if "settings.json" not in file_path else {}
            return json.loads(content)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return [] if "settings.json" not in file_path else {}

def save_json(file_path: str, data: Any) -> bool:
    """Saves data to a JSON file on disk."""
    ensure_db_dir()
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        return False

# Activity Logging
def log_activity(username: str, action: str, details: str = ""):
    """Logs system and user actions to activity.json."""
    activities = load_json(ACTIVITY_FILE)
    if not isinstance(activities, list):
        activities = []
    
    activities.insert(0, {
        "timestamp": datetime.now().isoformat(),
        "username": username,
        "action": action,
        "details": details
    })
    
    # Cap at 500 records
    save_json(ACTIVITY_FILE, activities[:500])

# Settings management
def load_settings() -> Dict[str, Any]:
    """Loads system settings or returns default settings if none exist."""
    settings = load_json(SETTINGS_FILE)
    if not settings:
        settings = {
            "app_name": "SmartCampusAI",
            "academic_year": "2026-2027",
            "allow_registration": True,
            "theme": "Antigravity Theme",
            "ai_model": "Gemini 1.5 Flash"
        }
        save_json(SETTINGS_FILE, settings)
    return settings

def save_settings(new_settings: Dict[str, Any]) -> bool:
    """Saves updated system settings."""
    return save_json(SETTINGS_FILE, new_settings)

# User Database Functions
def get_all_users() -> List[Dict[str, Any]]:
    """Retrieves all registered users."""
    users = load_json(USERS_FILE)
    return users if isinstance(users, list) else []

def add_user(username: str, email: str, password_raw: str, role: str = "Student") -> Tuple[bool, str]:
    """Registers a new user, hashes password, and stores in JSON database."""
    users = get_all_users()
    
    # Check if duplicate email or username
    for u in users:
        if u["username"].lower() == username.lower():
            return False, "Username is already registered."
        if u["email"].lower() == email.lower():
            return False, "Email address is already registered."
            
    hashed_pwd = hash_password(password_raw)
    new_user = {
        "username": username,
        "email": email,
        "password": hashed_pwd,
        "role": role,
        "created_at": datetime.now().isoformat(),
        "bio": "Bio is empty.",
        "department": "Not Assigned",
        "phone": ""
    }
    
    users.append(new_user)
    if save_json(USERS_FILE, users):
        log_activity(username, "Registration", f"User registered successfully as role: {role}")
        return True, "User registered successfully."
    return False, "Error writing to database."

def authenticate_user(username_or_email: str, password_raw: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """Authenticates user with username or email, and plaintext password."""
    users = get_all_users()
    for u in users:
        if u["username"].lower() == username_or_email.lower() or u["email"].lower() == username_or_email.lower():
            if verify_password(password_raw, u["password"]):
                log_activity(u["username"], "Login", "User logged in successfully")
                return True, u
    return False, None

def update_profile(username: str, email: str, role: str, additional_info: Dict[str, Any]) -> Tuple[bool, str]:
    """Updates user details in the JSON database."""
    users = get_all_users()
    found = False
    for i, u in enumerate(users):
        if u["username"].lower() == username.lower():
            # Check if email is updated and unique
            if u["email"].lower() != email.lower():
                for other in users:
                    if other["username"].lower() != username.lower() and other["email"].lower() == email.lower():
                        return False, "Email is already in use by another account."
            
            # Apply updates
            users[i]["email"] = email
            users[i]["role"] = role
            # Apply all additional info keys (bio, department, phone, etc.)
            for k, v in additional_info.items():
                users[i][k] = v
            found = True
            break
            
    if found:
        if save_json(USERS_FILE, users):
            log_activity(username, "Update Profile", "Profile details updated")
            return True, "Profile updated successfully."
        return False, "Failed to write database file."
    return False, "User not found."

def delete_user(username: str) -> bool:
    """Removes a user from the database."""
    users = get_all_users()
    initial_count = len(users)
    users = [u for u in users if u["username"].lower() != username.lower()]
    if len(users) < initial_count:
        save_json(USERS_FILE, users)
        log_activity("system", "Delete User", f"User account deleted: {username}")
        return True
    return False

# Student Records CRUD
def get_all_students() -> List[Dict[str, Any]]:
    """Loads all student records."""
    students = load_json(STUDENTS_FILE)
    return students if isinstance(students, list) else []

def save_students(students_list: List[Dict[str, Any]]) -> bool:
    """Saves students list."""
    return save_json(STUDENTS_FILE, students_list)

# Faculty Records CRUD
def get_all_faculty() -> List[Dict[str, Any]]:
    """Loads all faculty records."""
    faculty = load_json(FACULTY_FILE)
    return faculty if isinstance(faculty, list) else []

def save_faculty(faculty_list: List[Dict[str, Any]]) -> bool:
    """Saves faculty list."""
    return save_json(FACULTY_FILE, faculty_list)

# Attendance CRUD
def get_all_attendance() -> List[Dict[str, Any]]:
    """Loads attendance data."""
    attendance = load_json(ATTENDANCE_FILE)
    return attendance if isinstance(attendance, list) else []

def save_attendance(attendance_list: List[Dict[str, Any]]) -> bool:
    """Saves attendance list."""
    return save_json(ATTENDANCE_FILE, attendance_list)
