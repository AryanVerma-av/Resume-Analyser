"""
SkillGap — AI-Powered Resume & Skill Gap Analyzer
Supports:
1. Student / Candidate: In-depth gap analysis & structured path forward from Developer Roadmaps (roadmap.sh)
2. HR / Recruiter: Candidate evaluation, targeted interview questions, and Batch Screening (100-200 Resumes) with CSV Export.
"""

import io
import os
import re
import textwrap
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from models import GapAnalysis, RoleCategory, ScreeningResult, UserPersona
from typesafe_service import TypeSafeService
from gemini_service import GeminiService
from parser import extract_text_from_pdf

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="SkillGap — Talent & Skill Gap Intelligence",
    page_icon="↗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Executive CSS System
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: #0F172A;
}

.stApp {
    background-color: #FAFAF9;
}

/* Executive Header */
.exec-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 0 20px 0;
    margin-bottom: 24px;
    border-bottom: 1px solid #E2E8F0;
}

.brand-wrapper {
    display: flex;
    align-items: center;
    gap: 14px;
}

.brand-badge {
    width: 44px;
    height: 44px;
    background: linear-gradient(135deg, #4F46E5 0%, #3730A3 100%);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 22px;
    font-weight: 800;
    box-shadow: 0 4px 10px rgba(79, 70, 229, 0.25);
}

.brand-name {
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #0F172A;
    margin: 0;
    line-height: 1.1;
}

.brand-sub {
    font-size: 13.5px;
    color: #64748B;
    margin: 3px 0 0 0;
    font-weight: 400;
}

/* Professional Surface Card */
.pro-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 22px 26px;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04), 0 1px 2px rgba(15, 23, 42, 0.02);
}

.pro-card-title {
    font-size: 17px;
    font-weight: 700;
    letter-spacing: -0.01em;
    color: #0F172A;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
}

.pro-card-sub {
    font-size: 13px;
    color: #64748B;
    margin-bottom: 16px;
}

/* Metric / KPI Tiles */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 12px;
    margin-bottom: 20px;
}

.kpi-tile {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 14px 16px;
    text-align: left;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}

.kpi-label {
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #64748B;
    margin-bottom: 4px;
}

.kpi-value {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #0F172A;
}

/* Status Badges */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 600;
}

.pill-strong {
    background: #ECFDF5;
    color: #065F46;
    border: 1px solid #A7F3D0;
}

.pill-partial {
    background: #FFFBEB;
    color: #92400E;
    border: 1px solid #FDE68A;
}

.pill-early {
    background: #EEF2FF;
    color: #3730A3;
    border: 1px solid #C7D2FE;
}

/* Track Badge */
.track-pill {
    background: #F1F5F9;
    color: #334155;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 12px;
    font-weight: 600;
    font-family: 'IBM Plex Mono', monospace;
}

/* Scope Guidance Banner */
.scope-alert {
    background: #FFFBEB;
    border: 1px solid #FCD34D;
    border-left: 4px solid #D97706;
    border-radius: 8px;
    padding: 16px 20px;
    margin: 16px 0;
}

.scope-alert-title {
    font-size: 15px;
    font-weight: 700;
    color: #92400E;
    margin: 0 0 4px 0;
}

.scope-alert-body {
    font-size: 13.5px;
    color: #78350F;
    margin: 0;
    line-height: 1.5;
}

/* Skill Tags with IBM Plex Mono */
.tag-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 8px;
}

.pro-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12.5px;
    font-weight: 500;
    padding: 5px 11px;
    border-radius: 6px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.tag-match {
    background: #F0FDF4;
    color: #15803D;
    border: 1px solid #BBF7D0;
}

.tag-gap {
    background: #FFFBEB;
    color: #B45309;
    border: 1px solid #FDE68A;
}

/* Sleek Timeline & Path Forward Cards */
.timeline-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 14px;
    position: relative;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.timeline-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}

.timeline-badge {
    background: #EEF2FF;
    color: #4F46E5;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11.5px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 4px;
    border: 1px solid #C7D2FE;
}

.timeline-title {
    font-size: 15px;
    font-weight: 700;
    color: #0F172A;
    margin-left: 10px;
}

.action-callout {
    background: #F8FAFC;
    border-left: 3px solid #4F46E5;
    padding: 10px 14px;
    border-radius: 0 6px 6px 0;
    margin-top: 10px;
    font-size: 13.5px;
    color: #1E293B;
    line-height: 1.5;
}

.action-callout strong {
    color: #4F46E5;
}

/* Interview Probe Card */
.probe-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #4F46E5;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 12px;
}

.probe-meta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    color: #4F46E5;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 4px;
}

.probe-text {
    font-size: 14px;
    color: #1E293B;
    line-height: 1.5;
    margin: 0;
}

/* Primary Button Styling */
div.stButton > button:first-child {
    background-color: #4F46E5;
    color: #FFFFFF;
    font-weight: 600;
    font-size: 14.5px;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    transition: background-color 0.15s ease, box-shadow 0.15s ease;
    width: 100%;
}

div.stButton > button:first-child:hover {
    background-color: #3730A3;
    color: #FFFFFF;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
}

/* Professional Streamlit Element Resets */
.stRadio > div {
    gap: 16px;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Sample Job Postings
SAMPLE_JDS = {
    "— Select a Preloaded Role —": "",
    "Frontend Software Engineer Intern (React, TypeScript)": """Frontend Software Engineer Intern
Responsibilities:
- Build responsive user interfaces using React, TypeScript, and modern CSS (Tailwind CSS).
- Collaborate with backend engineers to integrate RESTful APIs.
- Write unit tests using Jest and React Testing Library.
- Participate in code reviews and agile sprints.

Requirements:
- Strong knowledge of HTML, CSS, JavaScript, and TypeScript.
- Hands-on experience building projects with React.
- Familiarity with Git version control and GitHub workflows.
- Understanding of web performance, browser dev tools, and responsive design.
- Bonus: Experience with Next.js or GraphQL.""",

    "Junior Backend Engineer (Python, PostgreSQL, Docker)": """Junior Backend Software Engineer
Responsibilities:
- Design, build, and maintain robust REST APIs using Python (FastAPI / Django).
- Model relational databases using PostgreSQL and manage database migrations.
- Containerize backend services with Docker and setup CI/CD pipelines.
- Write comprehensive integration tests.

Requirements:
- Proficient in Python and object-oriented design.
- Experience with relational databases and SQL (PostgreSQL preferred).
- Understanding of HTTP protocols, RESTful principles, and authentication (JWT).
- Familiarity with Docker containerization and Git.
- Bonus: Experience with Redis or cloud platforms (AWS / GCP).""",

    "Data Science & Analytics Intern (Python, SQL)": """Data Science Intern
Responsibilities:
- Explore and clean large datasets using Python, Pandas, and NumPy.
- Train predictive machine learning models using Scikit-Learn and PyTorch.
- Create actionable data visualizations to communicate trends.

Requirements:
- Strong foundation in Python and statistical data analysis.
- Experience with Pandas, NumPy, and data visualization tools (Matplotlib/Seaborn).
- Knowledge of machine learning algorithms (regression, classification, clustering).
- Familiarity with SQL for data querying.""",

    "Non-Engineering Role (TypeSafe Gate Test: Corporate Event Lead)": """Senior Corporate Event Coordinator & Hospitality Lead
Responsibilities:
- Plan and coordinate large-scale corporate catering events and wedding banquets.
- Manage event budgets, vendor contracts, floral arrangements, and venue logistics.
- Oversee guest reception, banquet operations, and dining hospitality staff.

Requirements:
- 3+ years experience in hospitality management, banquet planning, or event design.
- Exceptional interpersonal communication and vendor negotiation skills.
- Knowledge of food safety regulations and catering logistics."""
}

SAMPLE_RESUME_TEXT = """ALEX CHEN
alex.chen@university.edu | github.com/alexchen | linkedin.com/in/alexchen
Computer Science B.S., Expected May 2025

TECHNICAL SKILLS:
- Languages: JavaScript, Python, HTML/CSS, SQL
- Frameworks & Libraries: React, Node.js, Express, Tailwind CSS
- Developer Tools: Git, GitHub, VS Code, Postman
- Concepts: Data Structures & Algorithms, RESTful APIs, Responsive Web Design

PROJECTS:
StudySync — Collaborative Student Task Tracker (React, Node.js, Express)
- Created a real-time Kanban board application supporting up to 10 concurrent team members.
- Implemented responsive UI components using React and Tailwind CSS.
- Developed backend REST endpoints in Node.js and Express to manage task states.
- Utilized Git for version control and deployed the frontend to Vercel.

CampusMarket — Student Marketplace Backend (Python, SQLite)
- Designed relational schemas in SQLite to handle student book and equipment listings.
- Built CRUD endpoints handling user authentication and listing queries.
"""


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
            <div style="background:#4F46E5; width:32px; height:32px; border-radius:8px; display:flex; align-items:center; justify-content:center; color:white; font-weight:700;">↗</div>
            <span style="font-size:19px; font-weight:800; color:#0F172A;">SkillGap</span>
        </div>
        """, unsafe_allow_html=True)

        st.caption("AI-Powered Talent & Skill Gap Intelligence")

        st.markdown("---")
        st.subheader("⚡ System Architecture")

        # TypeSafe status
        typesafe_ready = TypeSafeService.is_configured()
        st.markdown(f"""
        **1. TypeSafe Screening**
        - Primitives: `Noul` + `Choice`
        - Target Latency: `&lt;15ms`
        <span style="color:{'#16A34A' if typesafe_ready else '#4F46E5'}; font-size:12px; font-weight:600;">
            ● {'API Active' if typesafe_ready else 'Mock Primitive Active'}
        </span>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Gemini status
        if GeminiService.is_configured():
            st.markdown("""
            **2. Deep Assessment**
            - Engine: `Google Gemini 3.6 Flash`
            - Decoding: `Deterministic (T=0.0)`
            <span style="color:#16A34A; font-size:12px; font-weight:600;">● Live AI Active</span>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            **2. Deep Assessment**
            - Engine: `Deterministic Engine`
            <span style="color:#D97706; font-size:12px; font-weight:600;">● Offline Demo Mode</span>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        **3. Career Curriculum**
        - Grounded in official `roadmap.sh`
        - 31 Verified Developer Roadmaps
        """, unsafe_allow_html=True)


def render_student_path_forward(gap_analysis: GapAnalysis):
    """Renders the executive path forward with clean, unindented HTML."""
    st.markdown("""
    <div class="pro-card">
        <div class="pro-card-title">🗺️ Strategic Path Forward & Checkpoint Milestones</div>
        <div class="pro-card-sub">Sequenced curriculum roadmap derived directly from official engineering career standards.</div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="margin-bottom:16px;">
        <span class="track-pill">Curriculum Track: {gap_analysis.roadmap_track_name} ({gap_analysis.roadmap_reference})</span>
    </div>
    """, unsafe_allow_html=True)

    if gap_analysis.path_forward:
        for idx, milestone in enumerate(gap_analysis.path_forward, 1):
            topics_html = " ".join([f'<span class="pro-tag" style="background:#F1F5F9; color:#334155; border:1px solid #CBD5E1;">{t}</span>' for t in milestone.topics])
            card_html = f"""
<div class="timeline-card">
    <div class="timeline-header">
        <div style="display:flex; align-items:center;">
            <span class="timeline-badge">STAGE {idx:02d}</span>
            <span class="timeline-title">{milestone.checkpoint}</span>
        </div>
    </div>
    <div style="margin-bottom:10px;">{topics_html}</div>
    <div class="action-callout">
        <strong>Strategic Milestone:</strong> {milestone.action}
    </div>
</div>"""
            st.markdown(card_html, unsafe_allow_html=True)
    elif gap_analysis.learning_roadmap:
        for idx, item in enumerate(gap_analysis.learning_roadmap, 1):
            st.markdown(f"**{idx}.** {item}")

    st.markdown("</div>", unsafe_allow_html=True)





def handle_batch_screening(uploaded_files, jd_text: str):
    """Processes 100-200 resumes in high-speed batch mode."""
    st.markdown("""
    <div class="pro-card">
        <div class="pro-card-title">📊 Batch Resume Screening Dashboard</div>
        <div class="pro-card-sub">High-throughput processing pipeline for multiple candidate resumes.</div>
    </div>
    """, unsafe_allow_html=True)

    if not uploaded_files:
        st.info("Upload resumes using the batch uploader above to begin processing.")
        return

    total_files = len(uploaded_files)
    st.write(f"Initiating batch processing for **{total_files} resume{'s' if total_files != 1 else ''}**...")

    progress_bar = st.progress(0.0)
    status_text = st.empty()

    results = []

    for idx, pdf_file in enumerate(uploaded_files):
        status_text.text(f"Processing candidate {idx + 1} of {total_files}: {pdf_file.name}...")
        try:
            resume_text = extract_text_from_pdf(pdf_file)
            if not resume_text:
                results.append({
                    "Candidate File": pdf_file.name,
                    "Screening Result": "Unreadable PDF",
                    "Fit Score %": 0,
                    "Domain Track": "N/A",
                    "Matched Skills": "-",
                    "Gaps Count": 0,
                    "Hiring Recommendation": "Review file format (scanned/empty)"
                })
                progress_bar.progress((idx + 1) / total_files)
                continue

            # Stage 1: Fast TypeSafe Screen (<15ms)
            typesafe_res: ScreeningResult = TypeSafeService.screen(resume_text, jd_text)

            if not typesafe_res.is_engineering_role:
                results.append({
                    "Candidate File": pdf_file.name,
                    "Screening Result": "Out of Scope",
                    "Fit Score %": 10,
                    "Domain Track": typesafe_res.detected_category.value,
                    "Matched Skills": "-",
                    "Gaps Count": "-",
                    "Hiring Recommendation": "Filtered: Non-engineering profile"
                })
            else:
                # Stage 2: Deep Analysis (cached / deterministic)
                analysis: GapAnalysis = GeminiService.analyze(resume_text, jd_text)
                results.append({
                    "Candidate File": pdf_file.name,
                    "Screening Result": analysis.match_status,
                    "Fit Score %": analysis.match_score_percentage,
                    "Domain Track": typesafe_res.detected_category.value,
                    "Matched Skills": ", ".join(analysis.extracted_skills[:4]) if analysis.extracted_skills else "None",
                    "Gaps Count": len(analysis.missing_skills),
                    "Hiring Recommendation": analysis.hiring_recommendation
                })

        except Exception as e:
            results.append({
                "Candidate File": pdf_file.name,
                "Screening Result": "Error",
                "Fit Score %": 0,
                "Domain Track": "N/A",
                "Matched Skills": "-",
                "Gaps Count": 0,
                "Hiring Recommendation": f"Processing exception: {str(e)[:40]}"
            })

        progress_bar.progress((idx + 1) / total_files)

    status_text.text("✓ Batch processing completed successfully.")

    df = pd.DataFrame(results)
    # Sort by fit score descending
    if "Fit Score %" in df.columns:
        df = df.sort_values(by="Fit Score %", ascending=False).reset_index(drop=True)
        df.index = df.index + 1  # 1-based rank

    # Display KPI summary
    qualified_count = sum(1 for r in results if r["Fit Score %"] >= 65)
    gated_count = sum(1 for r in results if r["Screening Result"] == "Out of Scope")

    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    with col_kpi1:
        st.markdown(f'<div class="kpi-tile"><div class="kpi-label">Resumes Evaluated</div><div class="kpi-value">{total_files}</div></div>', unsafe_allow_html=True)
    with col_kpi2:
        st.markdown(f'<div class="kpi-tile"><div class="kpi-label">Qualified Candidates</div><div class="kpi-value" style="color:#16A34A;">{qualified_count}</div></div>', unsafe_allow_html=True)
    with col_kpi3:
        st.markdown(f'<div class="kpi-tile"><div class="kpi-label">TypeSafe Filtered</div><div class="kpi-value" style="color:#D97706;">{gated_count}</div></div>', unsafe_allow_html=True)
    with col_kpi4:
        avg_score = int(df["Fit Score %"].mean()) if not df.empty else 0
        st.markdown(f'<div class="kpi-tile"><div class="kpi-label">Average Fit Score</div><div class="kpi-value">{avg_score}%</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📋 Candidate Leaderboard")
    st.dataframe(df, use_container_width=True)

    # Download CSV
    csv_data = df.to_csv(index=True).encode("utf-8")
    st.download_button(
        label="📥 Download Batch Screening Report (CSV)",
        data=csv_data,
        file_name="skillgap_candidate_screening_report.csv",
        mime="text/csv"
    )


def main():
    render_sidebar()

    # Executive Header
    st.markdown("""
    <div class="exec-header">
        <div class="brand-wrapper">
            <div class="brand-badge">↗</div>
            <div>
                <h1 class="brand-name">SkillGap</h1>
                <p class="brand-sub">AI-Powered Talent & Skill Gap Intelligence Platform</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Persona Selector (Student vs HR)
    persona_col, info_col = st.columns([1, 2])

    with persona_col:
        selected_role = st.radio(
            "Select Operating Viewpoint:",
            options=["🎓 Student / Candidate", "💼 HR / Recruiter"],
            horizontal=True,
            help="Toggle between personalized career coaching and recruiter screening."
        )

    is_student = "Student" in selected_role

    with info_col:
        if is_student:
            st.markdown("""
            <div style="background:#EEF2FF; border:1px solid #C7D2FE; border-radius:8px; padding:10px 16px; font-size:13.5px; color:#3730A3;">
                <strong>Student Mode:</strong> Identifies matched qualifications, gaps to close, and an official step-by-step path forward grounded in developer career roadmaps.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:8px; padding:10px 16px; font-size:13.5px; color:#166534;">
                <strong>HR / Recruiter Mode:</strong> Evaluate candidate profiles, generate technical interview probes, or batch-screen 100+ resumes simultaneously.
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # In HR mode, allow toggling Batch Mode
    batch_mode = False
    if not is_student:
        hr_mode_tab = st.radio(
            "HR Screening Workflow:",
            options=["🔍 Single Candidate In-Depth Analysis", "⚡ Batch Screening (100–200 Resumes)"],
            horizontal=True
        )
        batch_mode = "Batch" in hr_mode_tab
        st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # BATCH WORKFLOW FOR HR (100-200 RESUMES)
    # -------------------------------------------------------------
    if not is_student and batch_mode:
        col_batch_upload, col_batch_jd = st.columns([1, 1], gap="large")

        with col_batch_upload:
            st.markdown('<div class="pro-card-title">📁 Upload Batch Resumes</div>', unsafe_allow_html=True)
            st.caption("Upload up to 200 PDF resumes simultaneously for automated evaluation.")
            uploaded_batch = st.file_uploader(
                "Upload Resume PDFs (Multiple)",
                type=["pdf"],
                accept_multiple_files=True,
                help="You can drag and drop 100-200 PDF files at once."
            )

        with col_batch_jd:
            st.markdown('<div class="pro-card-title">🎯 Benchmark Job Description</div>', unsafe_allow_html=True)
            batch_sample = st.selectbox(
                "Quick Select Target Role",
                options=list(SAMPLE_JDS.keys()),
                key="batch_jd_select"
            )
            default_batch_jd = SAMPLE_JDS[batch_sample] if batch_sample != "— Select a Preloaded Role —" else SAMPLE_JDS["Junior Backend Engineer (Python, PostgreSQL, Docker)"]
            batch_jd_text = st.text_area("Job Description Text", value=default_batch_jd, height=220, key="batch_jd_text")

        if st.button("🚀 Run Batch Screening Pipeline", type="primary"):
            if not uploaded_batch:
                st.warning("Please upload one or more PDF resumes to screen.", icon="ℹ️")
            elif not batch_jd_text.strip():
                st.warning("Please supply a benchmark job description.", icon="ℹ️")
            else:
                handle_batch_screening(uploaded_batch, batch_jd_text)

        return  # End batch workflow

    # -------------------------------------------------------------
    # INDIVIDUAL ANALYSIS WORKFLOW (STUDENT OR HR SINGLE CANDIDATE)
    # -------------------------------------------------------------
    col_resume, col_jd = st.columns(2, gap="large")

    with col_resume:
        resume_heading = "📄 Candidate Resume" if not is_student else "📄 Your Resume"
        st.markdown(f'<div class="pro-card-title">{resume_heading}</div>', unsafe_allow_html=True)
        st.caption("Upload a PDF resume or review extracted text below.")

        uploaded_pdf = st.file_uploader(
            "Upload Resume (PDF)",
            type=["pdf"],
            key="single_pdf_uploader",
            help="PDF text is extracted locally using pdfplumber."
        )

        extracted_text = ""
        if uploaded_pdf is not None:
            try:
                with st.spinner("Extracting text via pdfplumber..."):
                    extracted_text = extract_text_from_pdf(uploaded_pdf)
                if extracted_text:
                    st.success(f"Extracted {len(extracted_text.split())} words from PDF.", icon="✓")
                else:
                    st.error("No extractable text detected in this PDF (might be a scanned image).", icon="⚠️")
            except Exception as e:
                st.error(f"Error parsing PDF: {str(e)}", icon="⚠️")

        resume_input = st.text_area(
            "Resume Text Content",
            value=extracted_text if extracted_text else SAMPLE_RESUME_TEXT,
            height=260,
            help="Parsed text ready for gap analysis."
        )

    with col_jd:
        st.markdown('<div class="pro-card-title">🎯 Benchmark Job Description</div>', unsafe_allow_html=True)
        st.caption("Select a sample engineering posting or paste your target role.")

        selected_sample = st.selectbox(
            "Quick Load Preloaded Role",
            options=list(SAMPLE_JDS.keys()),
            help="Preloaded roles to quickly evaluate the application."
        )

        default_jd_value = SAMPLE_JDS[selected_sample] if selected_sample != "— Select a Preloaded Role —" else SAMPLE_JDS["Frontend Software Engineer Intern (React, TypeScript)"]

        jd_input = st.text_area(
            "Target Job Description Text",
            value=default_jd_value,
            height=260,
            placeholder="Paste role responsibilities, qualifications, and requirements..."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Action Button
    col_btn, _ = st.columns([1, 2])
    with col_btn:
        button_label = "🚀 Analyze Profile & Generate Path Forward" if is_student else "🔍 Screen Candidate & Generate Probes"
        analyze_clicked = st.button(button_label, type="primary")

    if analyze_clicked:
        if not resume_input.strip():
            st.warning("Please supply resume text or upload a PDF before proceeding.", icon="ℹ️")
            return

        if not jd_input.strip():
            st.warning("Please supply a benchmark job description.", icon="ℹ️")
            return

        # -------------------------------------------------------------
        # STEP 1: TypeSafe Fast Filtering (Noul Gatekeeper + Choice Categorizer)
        # -------------------------------------------------------------
        with st.status("Executing TypeSafe System One screening...", expanded=True) as status_box:
            st.write("Evaluating role scope via `TypeSafe Noul Gatekeeper`...")
            screening_result: ScreeningResult = TypeSafeService.screen(
                resume_text=resume_input,
                job_description=jd_input
            )

            if not screening_result.is_engineering_role:
                status_box.update(label="Initial screening: Role is outside engineering scope", state="complete")
                st.markdown(f"""
                <div class="scope-alert">
                    <p class="scope-alert-title">Domain Scope Notice</p>
                    <p class="scope-alert-body">{screening_result.scope_message}</p>
                </div>
                """, unsafe_allow_html=True)
                st.info("SkillGap is focused on engineering disciplines. Please test with an engineering role from the sample dropdown above!")
                return

            st.write(f"Domain Categorization confirmed: **{screening_result.detected_category.value}**")
            st.write("Synthesizing in-depth career evaluation...")

            # -------------------------------------------------------------
            # STEP 2: In-Depth Analysis via GeminiService
            # -------------------------------------------------------------
            gap_analysis: GapAnalysis = GeminiService.analyze(
                resume_text=resume_input,
                job_description=jd_input
            )
            status_box.update(label="Analysis complete!", state="complete")

        # -------------------------------------------------------------
        # STEP 3: Professional Executive Presentation
        # -------------------------------------------------------------
        st.markdown("<br>", unsafe_allow_html=True)

        badge_class = "pill-strong" if gap_analysis.match_status == "Strong Match" else (
            "pill-partial" if gap_analysis.match_status == "Partial Match" else "pill-early"
        )
        badge_symbol = "✓" if gap_analysis.is_match else "↗"

        # KPI Metrics Header
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.markdown(f"""
            <div class="kpi-tile">
                <div class="kpi-label">Match Assessment</div>
                <div class="kpi-value" style="font-size:18px; margin-top:2px;">
                    <span class="status-pill {badge_class}">{badge_symbol} {gap_analysis.match_status}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with kpi2:
            st.markdown(f"""
            <div class="kpi-tile">
                <div class="kpi-label">Fit Score</div>
                <div class="kpi-value" style="color:#4F46E5;">{gap_analysis.match_score_percentage}%</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi3:
            st.markdown(f"""
            <div class="kpi-tile">
                <div class="kpi-label">Skills Matched</div>
                <div class="kpi-value" style="color:#15803D;">{len(gap_analysis.extracted_skills)}</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi4:
            st.markdown(f"""
            <div class="kpi-tile">
                <div class="kpi-label">Identified Gaps</div>
                <div class="kpi-value" style="color:#B45309;">{len(gap_analysis.missing_skills)}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Overview Box
        overview_title = "Executive Career Coach Summary" if is_student else "Candidate Evaluation Summary"
        st.markdown(f"""
        <div class="pro-card" style="border-left: 4px solid #4F46E5;">
            <div style="font-size:14px; font-weight:700; color:#4F46E5; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:6px;">
                {overview_title}
            </div>
            <p style="font-size:15px; color:#1E293B; line-height:1.6; margin:0;">
                {gap_analysis.summary}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # HR-Specific Hiring Recommendation Box
        if not is_student:
            st.markdown(f"""
            <div class="pro-card" style="border-left: 4px solid #16A34A; background:#F0FDF4; padding:16px 20px;">
                <div style="font-size:13px; font-weight:700; color:#166534; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:4px;">
                    Hiring Recommendation
                </div>
                <p style="font-size:15px; color:#14532D; font-weight:600; margin:0;">
                    {gap_analysis.hiring_recommendation}
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Skills Comparison (Two Columns)
        col_matched, col_missing = st.columns(2, gap="medium")

        with col_matched:
            st.markdown("""
            <div class="pro-card">
                <div class="pro-card-title" style="color:#15803D;">✓ Verified Qualifications</div>
                <div class="pro-card-sub">Core competencies directly evidenced in the candidate profile.</div>
            """, unsafe_allow_html=True)

            if gap_analysis.extracted_skills:
                skill_tags = "".join([f'<span class="pro-tag tag-match">✓ {s}</span>' for s in gap_analysis.extracted_skills])
                st.markdown(f'<div class="tag-container">{skill_tags}</div>', unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#64748B; font-size:13.5px;'>No direct overlapping competencies detected.</p>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with col_missing:
            gaps_title = "○ Skills to Strengthen (To-Do List)" if is_student else "○ Unverified Competencies"
            gaps_sub = "Targeted areas to focus your next development milestones." if is_student else "Required skills not evidenced on the candidate resume."
            st.markdown(f"""
            <div class="pro-card">
                <div class="pro-card-title" style="color:#B45309;">{gaps_title}</div>
                <div class="pro-card-sub">{gaps_sub}</div>
            """, unsafe_allow_html=True)

            if gap_analysis.missing_skills:
                gap_tags = "".join([f'<span class="pro-tag tag-gap">○ {s}</span>' for s in gap_analysis.missing_skills])
                st.markdown(f'<div class="tag-container">{gap_tags}</div>', unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#15803D; font-size:13.5px;'>All benchmark technical requirements are satisfied!</p>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # Student Persona: Strategic Path Forward from Developer Roadmaps
        if is_student:
            render_student_path_forward(gap_analysis)


if __name__ == "__main__":
    main()
