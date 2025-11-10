import streamlit as st
import os
from pathlib import Path

# Page configuration (Icon updated to match theme)
st.set_page_config(
    page_title="Resume Analyzer Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- MODERN CSS (DARK EMERALD THEME) ---
# This block injects all the custom styling.
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
            /* Subtle grid */
            linear-gradient(rgba(16, 185, 129, 0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(16, 185, 129, 0.08) 1px, transparent 1px),
            /* Fractal lines */
            linear-gradient(45deg, rgba(16, 185, 129, 0.1) 1px, transparent 1px),
            linear-gradient(-45deg, rgba(16, 185, 129, 0.1) 1px, transparent 1px);
        background-size: 70px 70px, 70px 70px, 90px 90px, 90px 90px;
        background-position: center center;
    }

    /* Remove default Streamlit padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* Hide Streamlit Header/Footer */
    footer {
        visibility: hidden;
    }
    header[data-testid="stHeader"] {
        visibility: hidden;
    }

    /* Main Header (Glassmorphic) */
    .main-header {
        background: rgba(13, 17, 23, 0.6); /* Glassmorphic background */
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(16, 185, 129, 0.2);
        color: white;
        padding: 2.5rem;
        margin-bottom: 2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        animation: fadeUp 0.6s ease-out forwards;
    }
    .main-header h1 {
        color: #ffffff;
        font-weight: 700;
        font-size: 2.75rem;
    }
    .main-header p {
        color: #b0b0b0; /* Lighter grey for subtext */
        font-size: 1.1rem;
    }

    /* Feature Cards (Glassmorphism) */
    .feature-card {
        background: rgba(13, 17, 23, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(16, 185, 129, 0.2);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
        height: 100%; /* Equal height columns */
        transition: all 0.3s ease;
        animation: fadeUp 0.8s ease-out forwards;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        border-color: rgba(16, 185, 129, 0.5);
        box-shadow: 0 10px 40px rgba(16, 185, 129, 0.1);
    }
    
    .feature-card h3, .feature-card h4 {
        color: #10b981; /* Emerald accent */
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .feature-card p {
        color: #b0b0b0;
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

    /* Native Streamlit components */
    [data-testid="stHeader"] {
        color: #ffffff;
        animation: fadeUp 0.7s ease-out forwards;
    }

    hr {
        border-top: 1px solid rgba(16, 185, 129, 0.2);
        margin: 2rem 0;
    }
    
    /* st.info override */
    [data-testid="stInfo"] {
        background-color: rgba(13, 17, 23, 0.6);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-left-width: 5px;
        border-left-color: #10b981;
        color: #b0b0b0;
        border-radius: 8px;
        padding: 1.25rem;
        animation: fadeUp 0.9s ease-out forwards;
    }
    
    [data-testid="stInfo"] strong {
        color: #10b981;
    }

    /* Footer override (targets the specific inline-styled div from your code) */
    div[style="text-align: center; color: #666;"] {
        padding-top: 1rem;
    }
    div[style="text-align: center; color: #666;"] p {
        color: #888888 !important; /* Brighter for dark mode */
    }
    div[style="text-align: center; color: #666;"] p strong {
        color: #b0b0b0 !important;
    }
</style>
""", unsafe_allow_html=True)
# --- END OF CSS ---


# Initialize session state (UNCHANGED)
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

def main():
    # Header (UNCHANGED)
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Resume Analyzer Pro</h1>
        <p>AI-powered resume optimization for job applications</p>
        <p><small>Upload your resume and target job description for instant ATS optimization recommendations</small></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation (UNCHANGED)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.authenticated:
            if st.button("🚀 Start Analysis", key="start_analysis", use_container_width=True):
                st.switch_page("pages/2_Resume_Analyzer.py")
        else:
            if st.button("🔐 Login to Continue", key="login", use_container_width=True):
                st.switch_page("pages/1_Login.py")
    
    # Feature showcase (UNCHANGED)
    st.markdown("---")
    st.header("✨ Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 ATS Optimization</h3>
            <p>Get detailed ATS compatibility scores and keyword matching analysis to pass automated screening systems.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>✍️ Smart Rewrites</h3>
            <p>AI-powered suggestions for bullet point improvements with specific action verbs and quantified results.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Skills Alignment</h3>
            <p>Optimize your skills section to match job requirements and identify missing technical competencies.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # How it works (UNCHANGED)
    st.markdown("---")
    st.header("🔄 How It Works")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>1. 📄 Upload</h4>
            <p>Upload your PDF resume and paste the target job description</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>2. 🤖 AI Analysis</h4>
            <p>Advanced AI analyzes your resume against the job requirements</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>3. 📊 Get Results</h4>
            <p>Receive detailed ATS score, keyword analysis, and improvement suggestions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <h4>4. ✅ Optimize</h4>
            <p>Apply recommendations and download your enhanced resume</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Security and privacy notice (UNCHANGED)
    st.markdown("---")
    st.info("""
    🔒 **Security & Privacy**
    - All file uploads are encrypted in transit and at rest
    - PDFs are automatically deleted after 30 days
    - No resume content is stored permanently
    - GDPR compliant data handling
    """)
    
    # Footer (UNCHANGED)
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p><strong>Resume Analyzer Pro</strong> - Powered by Advanced AI</p>
        <p>Built with Claude 3, Streamlit, and n8n for production-grade performance</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()