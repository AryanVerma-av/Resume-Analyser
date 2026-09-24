# SkillGap — Student AI Resume & Gap Analyzer

> **"Turn 'am I qualified?' anxiety into a clear, actionable plan."**

SkillGap is a local Streamlit web application designed for university students and early-career job seekers. It compares student resumes against target job descriptions, highlights matched foundational skills, identifies skill gaps as constructive to-do lists, and delivers prioritized, verb-driven learning roadmaps to close those gaps.

Built in strict adherence to [`brandguideline.md`](./brandguideline.md).

---

## 🛠️ Tech Stack

- **Frontend UI:** [Streamlit](https://streamlit.io/) with customized Brand CSS (`Inter` typography, `IBM Plex Mono` skill tags, indigo primary accent, amber gap indicators).
- **Document Parsing:** [`pdfplumber`](https://github.com/jsvine/pdfplumber) for reliable local extraction of text from PDF resumes.
- **AI Career Coach:** [Google Gemini API](https://ai.google.dev/) (`google-generativeai`) configured with structured JSON schema output and mentor-oriented system instructions.
- **Data Validation:** [`pydantic`](https://docs.pydantic.dev/) v2 for strict type safety (`GapAnalysis`, `ScreeningResult`).
- **Career Curriculum Grounding:** When students use the app, all recommended next courses of action and paths forward are strictly derived from the official 31-page developer roadmap curriculum (`roadmap.sh` guides covering Frontend, Backend, Full Stack, React, Node.js, Python, TypeScript, Java, Spring Boot, SQL, PostgreSQL, System Design, DevOps, AI & Data Science, Mobile, etc.).
- **Fast Initial Screening:** Mock **TypeSafe API** System One primitives:
  - **`Noul` Gatekeeper:** Low-latency filter identifying engineering vs non-engineering roles, gating heavy LLM calls with friendly scope guidance.
  - **`Choice` Categorizer:** Fast multiclass categorization of technical tracks (Frontend, Backend, Data/AI, DevOps, Mobile, etc.).

---

## 🚀 Quickstart

### 1. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 2. Configure Environment (Optional)
If you want to use the live Gemini AI model, get an API key from [Google AI Studio](https://aistudio.google.com/) and copy `.env.example` to `.env`:
```bash
cp .env.example .env
# Edit .env and paste your GEMINI_API_KEY
```
*(Note: If no API key is provided, SkillGap automatically operates in interactive demo mode using realistic, brand-aligned mock analysis).*

### 3. Launch the Application
```bash
python -m streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🎨 Brand Guidelines Summary

- **Mentor, Not Harsh Recruiter:** Honest about gaps, but always concludes with "here's what to do next".
- **Amber, Never Red for Gaps:** Matched skills are shown in Green (`#16A34A`), missing skills in Amber (`#D97706`). Red (`#DC2626`) is strictly reserved for system errors.
- **Action-Oriented Roadmaps:** Every milestone item begins with an action verb (e.g. *Build*, *Complete*, *Implement*).
- **Scope-Based Screening:** Non-engineering roles are met with helpful scope clarity ("This role looks outside our current focus"), avoiding harsh rejection terminology.
