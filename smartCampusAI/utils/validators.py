import re
from typing import Tuple

def validate_email(email: str) -> bool:
    """Validates email format using regular expressions."""
    if not email:
        return False
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(email_regex, email))

def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Checks the password strength and returns a tuple (is_strong, reason_message).
    Password rules:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one number
    - Contains at least one special character (e.g. !@#$%^&*(),.?":{}|<>)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character (!@#$%^&* etc.)."
    return True, "Strong password."

def validate_empty_fields(**kwargs) -> Tuple[bool, list[str]]:
    """
    Checks if any of the passed keyword arguments are empty.
    Returns (has_empty, list_of_empty_field_names).
    """
    empty_fields = []
    for field_name, value in kwargs.items():
        if value is None or (isinstance(value, str) and not value.strip()):
            empty_fields.append(field_name)
    return len(empty_fields) > 0, empty_fields
