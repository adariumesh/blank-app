import streamlit as st
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Resume Analyzer Pro",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        color: white;
        padding: 2rem 0;
        margin-bottom: 2rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Card styling */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #4a5568;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 5px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Success message styling */
    .success-message {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Info message styling */
    .info-message {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Resume Analyzer Pro</h1>
        <p>AI-powered resume optimization for job applications</p>
        <p><small>Upload your resume and target job description for instant ATS optimization recommendations</small></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.authenticated:
            if st.button("🚀 Start Analysis", key="start_analysis", use_container_width=True):
                st.switch_page("pages/2_Resume_Analyzer.py")
        else:
            if st.button("🔐 Login to Continue", key="login", use_container_width=True):
                st.switch_page("pages/1_Login.py")
    
    # Feature showcase
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
    
    # How it works
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
    
    # Security and privacy notice
    st.markdown("---")
    st.info("""
    🔒 **Security & Privacy**
    - All file uploads are encrypted in transit and at rest
    - PDFs are automatically deleted after 30 days
    - No resume content is stored permanently
    - GDPR compliant data handling
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p><strong>Resume Analyzer Pro</strong> - Powered by Advanced AI</p>
        <p>Built with Claude 3, Streamlit, and n8n for production-grade performance</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()