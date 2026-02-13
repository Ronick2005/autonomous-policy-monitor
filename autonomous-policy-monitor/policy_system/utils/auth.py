"""
Authentication utilities for Autonomous Policy Compliance Monitor
Role-based access control for research prototype
"""
import json
import os
from pathlib import Path
from typing import Optional, Dict
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User database file
USERS_FILE = Path(__file__).parent.parent / "users.json"

def load_users() -> Dict:
    """Load users from JSON file"""
    if USERS_FILE.exists():
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users: Dict):
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def hash_password(password: str) -> str:
    """Hash a password (bcrypt has 72 byte limit)"""
    # Truncate password to 72 bytes to avoid bcrypt error
    if len(password.encode('utf-8')) > 72:
        password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """Authenticate a user and return user data if successful"""
    users = load_users()
    
    if username not in users:
        return None
    
    user = users[username]
    if not verify_password(password, user.get("password_hash", "")):
        return None
    
    # Return user data without password hash
    return {
        "username": username,
        "full_name": user.get("full_name", username),
        "role": user.get("role", "researcher"),
        "organization": user.get("organization", "Research Lab")
    }

def create_user(username: str, password: str, role: str = "researcher", 
                full_name: str = "", organization: str = "Research Lab") -> bool:
    """Create a new user"""
    users = load_users()
    
    if username in users:
        return False
    
    users[username] = {
        "password_hash": hash_password(password),
        "full_name": full_name or username,
        "role": role,
        "organization": organization
    }
    
    save_users(users)
    return True

def has_agent_access(user: Dict, agent_name: str) -> bool:
    """Check if user has access to a specific agent"""
    # For research prototype, all users have access to all agents
    return True

# Initialize with default research user if no users exist
def init_default_users():
    """Initialize default users for research"""
    users = load_users()
    
    if not users:
        try:
            default_users = {
                "researcher": {
                    "password_hash": hash_password("research123"),
                    "full_name": "Dr. Policy Researcher",
                    "role": "researcher",
                    "organization": "AI Governance Lab"
                },
                "admin": {
                    "password_hash": hash_password("admin123"),
                    "full_name": "System Administrator",
                    "role": "admin",
                    "organization": "AI Governance Lab"
                },
                "auditor": {
                    "password_hash": hash_password("audit123"),
                    "full_name": "Compliance Auditor",
                    "role": "auditor",
                    "organization": "Regulatory Affairs"
                }
            }
            save_users(default_users)
            print("[OK] Default users created: researcher/research123, admin/admin123, auditor/audit123")
        except Exception as e:
            print(f"⚠ Warning: Could not initialize default users: {e}")

# Run initialization only if this module is imported directly
if __name__ != "__main__":
    init_default_users()

def get_all_users() -> Dict:
    """Get all users (for admin interface)"""
    users = load_users()
    # Return usernames and metadata, not password hashes
    return {
        username: {
            "full_name": data.get("full_name", username),
            "role": data.get("role", "researcher"),
            "organization": data.get("organization", "Research Lab")
        }
        for username, data in users.items()
    }
