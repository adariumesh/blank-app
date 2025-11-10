import streamlit as st
import hashlib
import time
import os
from datetime import datetime, timedelta

# Page configuration (Icon updated to match theme)
st.set_page_config(
    page_title="Login - Resume Analyzer Pro",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- MODERN CSS (DARK EMERALD THEME) ---
st.markdown("""
<style>
    /* Import Google Font 'Inter' */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Animation: Fade Up */
    @keyframes fadeUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Base app styling */
    body {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #0d1117; /* Dark Slate Background */
        color: #e0e0e0;
        
        /* Emerald "Thunder Web" Background */
        background-image: 
            linear-gradient(rgba(16, 185, 129, 0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(16, 185, 129, 0.08) 1px, transparent 1px),
            linear-gradient(45deg, rgba(16, 185, 129, 0.1) 1px, transparent 1px),
            linear-gradient(-45deg, rgba(16, 185, 129, 0.1) 1px, transparent 1px);
        background-size: 70px 70px, 70px 70px, 90px 90px, 90px 90px;
        background-position: center center;
    }

    /* Remove default Streamlit padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    /* Hide Streamlit Header/Footer */
    footer {
        visibility: hidden;
    }
    header[data-testid="stHeader"] {
        visibility: hidden;
    }

    /* --- LOGIN PAGE SPECIFIC STYLES --- */

    /* Login Card (Glassmorphic) */
    .login-container {
        background: rgba(13, 17, 23, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(16, 185, 129, 0.2);
        color: white;
        padding: 2.5rem;
        border-radius: 12px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        animation: fadeUp 0.6s ease-out forwards;
        margin: 0; /* Remove default margin */
        max-width: 450px;
    }
    
    .login-header h1 {
        color: #ffffff;
        font-weight: 700;
        font-size: 2.25rem;
    }
    .login-header p {
        color: #b0b0b0;
        font-size: 1.1rem;
    }

    /* Form Inputs */
    [data-testid="stTextInput"] label {
        color: #b0b0b0;
        font-weight: 600;
    }
    [data-testid="stTextInput"] input {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(16, 185, 129, 0.2);
        color: #ffffff;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: #10b981;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
    }

    /* Button styling (Emerald Glow) */
    .stButton > button {
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        color: #ffffff;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.3), 0 4px 10px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.03);
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.6), 0 6px 15px rgba(0, 0, 0, 0.3);
        background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }

    /* Form-specific button width */
    .stForm .stButton > button {
        width: 100%;
    }

    /* Expander for Demo Credentials */
    [data-testid="stExpander"] {
        background: rgba(13, 17, 23, 0.3);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 12px;
        margin-top: 1rem;
    }
    [data-testid="stExpander"] summary {
        color: #e0e0e0;
        font-weight: 600;
    }
    .demo-credentials {
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(16, 185, 129, 0.1);
        border-radius: 8px;
        padding: 1rem;
        color: #b0b0b0;
    }
    .demo-credentials strong {
        color: #e0e0e0;
    }

    /* Native Alerts */
    [data-testid="stError"] {
        background-color: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-left: 5px solid #ef4444;
        color: #f87171;
        border-radius: 8px;
    }
    [data-testid="stSuccess"] {
        background-color: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-left: 5px solid #10b981;
        color: #34d399;
        border-radius: 8px;
    }
    
    /* Footer override */
    div[style="text-align: center; color: #666;"] p {
        color: #888888 !important;
    }
    div[style="text-align: center; color: #666;"] p strong {
        color: #b0b0b0 !important;
    }
</style>
""", unsafe_allow_html=True)
# --- END OF CSS ---


# Demo credentials (UNCHANGED)
DEMO_USERS = {
    "demo@example.com": {
        "password": "demo123",
        "name": "Demo User",
        "role": "user"
    },
    "admin@example.com": {
        "password": "admin123",
        "name": "Admin User",
        "role": "admin"
    }
}

# (UNCHANGED HELPER FUNCTIONS)
def hash_password(password):
    """Simple password hashing for demo purposes"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(email, password):
    """Authenticate user against demo credentials"""
    if email in DEMO_USERS:
        stored_password = DEMO_USERS[email]["password"]
        if password == stored_password:
            return True, DEMO_USERS[email]
    return False, None

def create_session_token(user_data):
    """Create a simple session token"""
    timestamp = str(int(time.time()))
    user_string = f"{user_data['name']}{timestamp}"
    return hashlib.sha256(user_string.encode()).hexdigest()[:16]

# (UNCHANGED MAIN FUNCTION)
def main():
    # Center the login form
    st.markdown("""
    <div class="login-container">
        <div class="login-header">
            <h1>🔐 Login</h1>
            <p>Access Resume Analyzer Pro</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Login form
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="demo@example.com", key="email")
        password = st.text_input("Password", type="password", placeholder="demo123", key="password")
        
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if not email or not password:
                st.error("⚠️ Please enter both email and password")
            else:
                # Attempt authentication
                is_authenticated, user_data = authenticate_user(email, password)
                
                if is_authenticated:
                    # Create session
                    session_token = create_session_token(user_data)
                    
                    # Update session state
                    st.session_state.authenticated = True
                    st.session_state.user_id = email
                    st.session_state.user_name = user_data["name"]
                    st.session_state.user_role = user_data["role"]
                    st.session_state.session_token = session_token
                    st.session_state.login_time = datetime.now()
                    
                    # Show success message
                    st.success(f"✅ Welcome, {user_data['name']}!")
                    
                    # Redirect to main app
                    time.sleep(1)
                    st.switch_page("streamlit_app.py")
                else:
                    st.error("❌ Invalid email or password")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Demo credentials
    with st.expander("🎯 Demo Credentials"):
        st.markdown("""
        <div class="demo-credentials">
            <strong>User Account:</strong><br>
            Email: demo@example.com<br>
            Password: demo123<br><br>
            
            <strong>Admin Account:</strong><br>
            Email: admin@example.com<br>
            Password: admin123
        </div>
        """, unsafe_allow_html=True)
    
    # Features preview
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p><strong>✨ Features:</strong></p>
        <p>• ATS Score Analysis<br>
        • Keyword Optimization<br>
        • Resume Rewrites<br>
        • Skills Alignment</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    # Check if already authenticated
    if st.session_state.get("authenticated", False):
        st.switch_page("streamlit_app.py")
    else:
        main()