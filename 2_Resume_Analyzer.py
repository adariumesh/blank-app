import streamlit as st
import requests
import json
import time
import base64
import os
from datetime import datetime
import io

# Import custom modules
from auth import require_auth
from utils import call_n8n_webhook, poll_analysis_status, format_analysis_results

# Page configuration
st.set_page_config(
    page_title="Resume Analyzer - Resume Analyzer Pro",
    page_icon="⚡", # Changed icon
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- NEW MODERN SAAS CSS ---
st.markdown("""
<style>
    /* Import Google Font 'Inter' */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Animation: Fade In */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Base app styling */
    body {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #0d1117; /* Dark Slate Background */
        color: #c9d1d9;
    }

    /* Main container padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* Hide Streamlit Header/Footer */
    footer { visibility: hidden; }
    header[data-testid="stHeader"] { visibility: hidden; }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
        font-weight: 700;
    }
    
    /* Main Page Title */
    [data-testid="stAppViewContainer"] > .main h1:first-child {
        font-size: 2.75rem;
        color: #ffffff;
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Welcome markdown */
    [data-testid="stAppViewContainer"] > .main .stMarkdown:nth-of-type(1) {
        font-size: 1.1rem;
        color: #8b949e;
        margin-top: -1rem;
        margin-bottom: 1rem;
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Solid, Layered Containers */
    .analysis-container, .upload-section, .results-section {
        background: #161b22; /* Lighter dark color */
        border: 1px solid #30363d; /* Subtle border */
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        margin-bottom: 2rem;
        animation: fadeIn 0.7s ease-out;
    }
    
    .upload-section {
        border-style: dashed;
        border-width: 2px;
        border-color: #30363d;
        background-color: #0d1117; /* Darker bg for dropzone */
    }

    /* Input Controls */
    [data-testid="stFileUploader"] label,
    [data-testid="stTextArea"] label {
        color: #c9d1d9;
        font-weight: 600;
    }
    
    [data-testid="stFileUploader"] [data-testid="stFileDropzone"] {
        background: #0d1117;
        border-color: #30363d;
    }
    
    [data-testid="stTextArea"] textarea {
        background-color: #0d1117;
        border: 1px solid #30363d;
        color: #ffffff;
        border-radius: 8px;
    }
    [data-testid="stTextArea"] textarea:focus {
        border-color: #10b981;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
    }

    /* Button styling (Emerald Glow) */
    .stButton > button {
        background-color: #10b981;
        color: #ffffff;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.6);
        background-color: #34d399;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #161b22 !important; /* Lighter dark */
        border-right: 1px solid #30363d;
    }
    [data-testid="stSidebar"] [data-testid="stSelectbox"] label,
    [data-testid="stSidebar"] [data-testid="stCheckbox"] label,
    [data-testid="stSidebar"] h1, h2, h3, h4 {
        color: #c9d1d9;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdown"] p {
        color: #8b949e;
    }
    
    /* Logout Button (Sidebar) */
    [data-testid="stSidebar"] .stButton > button {
        background: transparent;
        border: 1px solid #30363d;
        color: #c9d1d9;
        box-shadow: none;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: #30363d;
        border-color: #8b949e;
        color: #ffffff;
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
    
    /* Expander (Recent Analysis) */
    [data-testid="stExpander"] {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 10px;
    }
    [data-testid="stExpander"] summary {
        color: #c9d1d9;
        font-weight: 600;
    }

    /* --- RESULTS STYLES --- */
    hr { border-top: 1px solid #30363d; }
    
    /* ATS Score */
    .ats-score {
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        margin: 1rem 0;
        line-height: 1;
    }
    .score-excellent { color: #10b981; } /* Emerald */
    .score-good { color: #34d399; } /* Light Emerald */
    .score-fair { color: #f59e0b; } /* Amber */
    .score-poor { color: #ef4444; } /* Red */

    /* Metric */
    [data-testid="stMetric"] {
        background: #0d1117;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #30363d;
    }
    [data-testid="stMetricLabel"] { color: #8b949e; }
    [data-testid="stMetricValue"] { color: #ffffff; font-size: 2rem; }
    
    /* Keyword Tags */
    .keyword-tag {
        display: inline-block;
        padding: 0.3rem 0.75rem;
        border-radius: 15px;
        margin: 0.25rem;
        font-size: 0.9rem;
        font-weight: 500;
    }
    .keyword-matched {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .keyword-missing {
        background: rgba(239, 68, 68, 0.1);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    /* Recommendation Card */
    .recommendation-card {
        background: #0d1117;
        border: 1px solid #30363d;
        border-left: 4px solid #10b981;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
        color: #8b949e;
    }
    .recommendation-card h4 {
        color: #34d399;
    }
    .recommendation-card p strong {
        color: #c9d1d9;
    }
    
    .impact-score {
        display: inline-block;
        background: #10b981;
        color: #0d1117;
        padding: 0.25rem 0.5rem;
        border-radius: 10px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    /* Download Buttons */
    [data-testid="stDownloadButton"] > button {
        background: transparent;
        border: 1px solid #30363d;
        color: #c9d1d9;
        box-shadow: none;
    }
    [data-testid="stDownloadButton"] > button:hover {
        background: #30363d;
        border-color: #8b949e;
        color: #ffffff;
    }

</style>
""", unsafe_allow_html=True)
# --- END OF CSS ---


# (UNCHANGED MAIN FUNCTION)
@require_auth
def main():
    # Header
    st.title("🎯 Resume Analyzer")
    st.markdown(f"Welcome, **{st.session_state.user_name}**! Let's optimize your resume for ATS success.")
    
    # Sidebar (UNCHANGED)
    with st.sidebar:
        st.header("📊 Analysis Options")
        
        analysis_type = st.selectbox(
            "Analysis Type",
            ["comprehensive", "ats_only", "keywords_only", "rewrite_suggestions"],
            format_func=lambda x: x.replace("_", " ").title(),
            help="Choose the depth of analysis"
        )
        
        include_markdown = st.checkbox(
            "Include Detailed Report",
            value=True,
            help="Generate a comprehensive markdown report"
        )
        
        st.divider()
        
        # User info
        st.header("👤 Account")
        st.write(f"**User:** {st.session_state.user_name}")
        st.write(f"**Role:** {st.session_state.user_role}")
        
        if st.button("🚪 Logout"):
            from auth import logout_user
            logout_user()
            st.rerun()
    
    # Main content area (UNCHANGED)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Upload section
        st.markdown("""
        <div class="upload-section">
            <h3>📄 Upload Your Resume</h3>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=["pdf"],
            label_visibility="collapsed",
            help="Upload your resume in PDF format (max 10MB)"
        )
        
        st.markdown("""
        <div class="upload-section">
            <h3>💼 Job Description</h3>
        </div>
        """, unsafe_allow_html=True)
        
        job_description = st.text_area(
            "Paste the complete job description",
            height=200,
            label_visibility="collapsed",
            placeholder="Paste the full job description here, including requirements, responsibilities, and qualifications...",
            help="Include as much detail as possible for better analysis"
        )
        
        # Analysis button
        analyze_button = st.button(
            "🚀 Analyze Resume",
            type="primary",
            use_container_width=True,
            disabled=not (uploaded_file and job_description)
        )
    
    with col2:
        # Quick tips
        st.markdown("""
        <div class="analysis-container">
            <h4>💡 Tips for Best Results</h4>
            <ul>
                <li>Use a clean, standard PDF format</li>
                <li>Include the complete job description</li>
                <li>Focus on relevant experience</li>
                <li>Use industry-standard section headers</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Recent analyses
        if st.session_state.analysis_history:
            st.markdown("""
            <div class="analysis-container">
                <h4>📈 Recent Analyses</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for analysis in st.session_state.analysis_history[-5:]:
                with st.expander(f"Analysis {analysis['id'][:8]}..."):
                    st.write(f"**Score:** {analysis['ats_score']}/100")
                    st.write(f"**Date:** {analysis['timestamp']}")
                    if st.button("Load Results", key=f"load_{analysis['id']}"):
                        st.session_state.current_analysis = analysis
                        st.rerun()
    
    # Analysis workflow (UNCHANGED)
    if analyze_button:
        if not uploaded_file:
            st.error("❌ Please upload a PDF resume")
        elif not job_description or len(job_description) < 50:
            st.error("❌ Please provide a complete job description (at least 50 characters)")
        else:
            # Process the analysis
            with st.spinner("🔄 Processing your resume... This may take a moment."):
                try:
                    # Read and encode PDF
                    pdf_bytes = uploaded_file.read()
                    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
                    
                    # Prepare request data
                    request_data = {
                        "resume_pdf": pdf_base64,
                        "job_description": job_description,
                        "analysis_type": analysis_type,
                        "include_markdown": include_markdown,
                        "user_id": st.session_state.user_id
                    }
                    
                    # Call n8n webhook
                    response = call_n8n_webhook(request_data)
                    
                    if response.get("status") == "success":
                        # Store analysis in history
                        analysis_record = {
                            "id": response.get("analysis_id"),
                            "ats_score": response.get("ats_score"),
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "job_title": job_description[:50] + "..."
                        }
                        
                        st.session_state.analysis_history.append(analysis_record)
                        st.session_state.current_analysis = response
                        
                        st.success("✅ Analysis completed successfully!")
                        st.rerun() # Rerun to show results immediately
                        
                    else:
                        st.error(f"❌ Analysis failed: {response.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")
    
    # Display results if available
    if hasattr(st.session_state, 'current_analysis') and st.session_state.current_analysis:
        display_analysis_results(st.session_state.current_analysis)

# (UNCHANGED DISPLAY FUNCTION)
def display_analysis_results(analysis_data):
    """Display analysis results in a formatted way"""
    
    st.markdown("---")
    st.header("📊 Analysis Results")
    
    # ATS Score
    ats_score = analysis_data.get("ats_score", 0)
    score_class = get_score_class(ats_score)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="results-section" style="text-align: center; padding: 1.5rem;">
            <h3>ATS Compatibility Score</h3>
            <div class="ats-score {score_class}">{ats_score}</div>
            <p style="color: #8b949e; margin-top: -1rem;">out of 100</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Keyword Analysis
    st.subheader("🔍 Keyword Analysis")
    keyword_data = analysis_data.get("keyword_analysis", {})
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Match Score", f"{keyword_data.get('match_score', 0)}%")
        st.metric("Total Keywords", keyword_data.get('total_keywords', 0))
    
    with col2:
        st.markdown("""
        <div class="analysis-container" style="padding: 1.5rem;">
            <strong>✅ Matched Keywords:</strong><br>
        """, unsafe_allow_html=True)
        matched_keywords = keyword_data.get('matched_keywords', [])
        if matched_keywords:
            for keyword in matched_keywords[:10]:  # Show first 10
                st.markdown(f'<span class="keyword-tag keyword-matched">{keyword}</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="keyword-tag">{keyword}</span>', unsafe_allow_html=True)
            
        st.markdown("""
            <br><br><strong>❌ Missing Keywords:</strong><br>
        """, unsafe_allow_html=True)
        missing_keywords = keyword_data.get('missing_keywords', [])
        if missing_keywords:
            for keyword in missing_keywords[:10]:  # Show first 10
                st.markdown(f'<span class="keyword-tag keyword-missing">{keyword}</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="keyword-tag">None missing!</span>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    
    # Experience Recommendations
    experience_recs = analysis_data.get("experience_recommendations", [])
    if experience_recs:
        st.subheader("✍️ Experience Recommendations")
        for rec in experience_recs[:5]:  # Show first 5 recommendations
            st.markdown(f"""
            <div class="recommendation-card">
                <h4>{rec.get('section', 'Experience Section')}</h4>
                <p><strong>Current:</strong> {rec.get('current_text', 'N/A')}</p>
                <p><strong>Suggested:</strong> {rec.get('suggested_text', 'N/A')}</p>
                <p><strong>Reasoning:</strong> {rec.get('reasoning', 'N/A')}</p>
                <span class="impact-score">Impact: {rec.get('impact_score', 0)}/10</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Skills Optimization
    skills_data = analysis_data.get("skills_optimization", {})
    if skills_data:
        st.subheader("🎯 Skills Optimization")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="analysis-container" style="padding: 1.5rem;">
                <strong>Add These Skills:</strong>
            """, unsafe_allow_html=True)
            missing_skills = skills_data.get('missing_skills', [])
            if missing_skills:
                for skill in missing_skills[:8]:
                    st.write(f"• {skill}")
            else:
                st.write("• None")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="analysis-container" style="padding: 1.5rem;">
                <strong>Consider Removing:</strong>
            """, unsafe_allow_html=True)
            redundant_skills = skills_data.get('redundant_skills', [])
            if redundant_skills:
                for skill in redundant_skills[:5]:
                    st.write(f"• {skill}")
            else:
                st.write("• None")
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Suggested Projects
    projects = analysis_data.get("suggested_projects", [])
    if projects:
        st.subheader("💡 Suggested Projects")
        for project in projects[:3]:
            with st.expander(f"**{project.get('title', 'Project')}"):
                st.write(f"**Description:** {project.get('description', 'N/A')}")
                st.write(f"**Technologies:** {', '.join(project.get('technologies', []))}")
                st.write("**Resume Bullets:**")
                for bullet in project.get('bullet_points', []):
                    st.write(f"• {bullet}")
    
    # Download options (UNCHANGED)
    st.subheader("📥 Download Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # JSON results
        json_str = json.dumps(analysis_data, indent=2)
        st.download_button(
            label="📄 Download JSON",
            data=json_str,
            file_name=f"resume_analysis_{analysis_data.get('analysis_id', 'unknown')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        # Markdown report
        markdown_content = analysis_data.get("markdown_recommendations", "")
        if markdown_content:
            st.download_button(
                label="📝 Download Report",
                data=markdown_content,
                file_name=f"resume_report_{analysis_data.get('analysis_id', 'unknown')}.md",
                mime="text/markdown",
                use_container_width=True
            )
    
    with col3:
        # Analysis summary
        summary_text = f"""
Resume Analysis Summary
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
Analysis ID: {analysis_data.get('analysis_id', 'N/A')}
ATS Score: {ats_score}/100
Keyword Match: {keyword_data.get('match_score', 0)}%
Recommendations: {len(experience_recs)} experience suggestions
"""
        st.download_button(
            label="📋 Download Summary",
            data=summary_text,
            file_name=f"analysis_summary_{analysis_data.get('analysis_id', 'unknown')}.txt",
            mime="text/plain",
            use_container_width=True
        )

# (UNCHANGED HELPER FUNCTION)
def get_score_class(score):
    """Get CSS class for ATS score"""
    if score >= 80:
        return "score-excellent"
    elif score >= 60:
        return "score-good"
    elif score >= 40:
        return "score-fair"
    else:
        return "score-poor"

if __name__ == "__main__":
    main()