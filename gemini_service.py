"""
Google Gemini API Service Module.
Handles prompt engineering, system career coach instructions,
and structured Pydantic output validation for both Student and HR personas.

CRITICAL INSTRUCTION:
Whenever a student is using the app, the next course of action and path forward
MUST be strictly suggested from the developer roadmap curriculum in the PDF (roadmap.sh guide).
"""

import json
import os
import re
from typing import Optional, List
from dotenv import load_dotenv
import google.generativeai as genai

from models import GapAnalysis, UserPersona, CheckpointMilestone
from roadmap_curriculum import ROADMAP_TRACKS, get_curriculum_track_for_role

# Load environment variables automatically from .env
load_dotenv()

CURRICULUM_SUMMARY = """
OFFICIAL DEVELOPER ROADMAP CURRICULUM (FROM ATTACHED PDF ROADMAP.SH GUIDE):
1. Frontend Developer Track: Internet fundamentals -> Semantic HTML5 & CSS3 -> JavaScript ES6+ -> Git & Package Managers -> React (Functional Components, Hooks, State) -> Testing (Jest, RTL) & Next.js SSR.
2. Backend Developer Track: Language Basics (Node/Python/Java/Go) -> OS & Linux/Terminal -> Relational Databases (PostgreSQL, SQL, Normalization, Indexes) -> RESTful APIs & JWT Auth -> Caching (Redis) & Queues -> CI/CD & Testing.
3. Full Stack Developer Track: Checkpoint 1 (Static Webpages & Interactivity) -> Checkpoint 2 (Git & React/Tailwind) -> Checkpoint 3 (Backend Node.js/Python & PostgreSQL CRUD) -> Checkpoint 4 (JWT Auth & REST Integration) -> Checkpoint 5 (Docker & Deployment).
4. Python Developer Track: Fundamentals & Data Structures -> OOP & Advanced (Decorators, Generators) -> Web Frameworks (FastAPI / Django) -> Testing (pytest) & Type Annotations.
5. React Developer Track: JSX & Components -> Hooks (useState, useEffect, custom hooks) -> State Management & Routing -> Testing & SSR.
6. SQL & Databases Track: DDL & DML -> Aggregations & Complex JOINs -> Subqueries, CTEs, Window Functions -> Indexes (B-Tree, Query Optimization) -> Transactions & ACID.
7. System Design Track: Scalability vs Performance, CAP Theorem -> Load Balancing, Caching (Redis) -> Database Sharding & Replication -> Asynchronous Message Queues (Kafka).
8. AI & Data Scientist Track: Mathematics & Statistics -> Python Data Engineering (Pandas, SQL, EDA) -> Classical Machine Learning -> Deep Learning (PyTorch, Transformers) -> MLOps.
9. DevOps Track: Linux & Networking -> Docker & Kubernetes -> CI/CD (GitHub Actions) -> Terraform & Cloud.
"""

SYSTEM_PROMPT = f"""You are an experienced technical career coach and talent assessment specialist for SkillGap.
You evaluate university student resumes against technical job descriptions.

CRITICAL REQUIREMENT:
Whenever a student is using the app, you MUST formulate the next course of action and path forward
STRICTLY from the official Developer Roadmaps curriculum provided below:
{CURRICULUM_SUMMARY}

KEY PRINCIPLES:
1. Tone: Encouraging, honest, direct, constructive mentor. Never harsh or dismissive.
2. Words to strictly AVOID: reject, fail, disqualified, unqualified, deficient.
3. Missing skills are a to-do list for growth, not a verdict of inadequacy.
4. Next Course of Action & Path Forward:
   - Identify the most relevant Roadmap Track from the curriculum (e.g., 'Full Stack Developer Roadmap', 'Frontend Developer Roadmap', 'Backend Developer Roadmap').
   - Provide sequential Checkpoint Milestones directly reflecting that roadmap track.
   - For every checkpoint, list concrete topics from the PDF and an action step starting with an action verb (e.g., 'Build...', 'Design...', 'Implement...', 'Master...').
5. Learning roadmap: Provide concise action-oriented steps for each missing skill starting with an action verb.
6. Hiring recommendation: Provide a constructive, professional hiring recommendation summarizing strengths.

Return a strictly valid JSON object matching the GapAnalysis schema:
- is_match: boolean
- match_status: "Strong Match", "Partial Match", or "Early-Stage Match"
- match_score_percentage: integer between 0 and 100
- summary: string (2-3 sentences of constructive evaluation)
- extracted_skills: list of strings (found in both resume and role)
- missing_skills: list of strings (in role but missing or unclear in resume)
- roadmap_track_name: string (e.g. "Full Stack Developer Roadmap (from PDF Guide)")
- roadmap_reference: string (e.g. "https://roadmap.sh/full-stack (Page 28 of Roadmap Guide)")
- path_forward: list of objects with fields:
    - checkpoint: string (e.g. "Checkpoint 1: Relational Schema & SQL CRUD")
    - topics: list of strings from the PDF
    - action: string starting with an action verb
- learning_roadmap: list of strings (action-oriented steps for student)
- hiring_recommendation: string (concise summary for HR)
"""


class GeminiService:
    """
    Service client for Google Gemini AI Engine.
    Reads API key securely from environment (GEMINI_API_KEY).
    """

    @classmethod
    def get_api_key(cls) -> Optional[str]:
        # 1. Check environment variable / .env file
        key = os.getenv("GEMINI_API_KEY")
        if key and key.strip() and not key.startswith("your_gemini_api_key"):
            return key.strip()

        # 2. Check Streamlit secrets (.streamlit/secrets.toml)
        try:
            import streamlit as st
            if "GEMINI_API_KEY" in st.secrets:
                secret_key = st.secrets["GEMINI_API_KEY"]
                if secret_key and secret_key.strip():
                    return secret_key.strip()
        except Exception:
            pass

        return None

    @classmethod
    def is_configured(cls) -> bool:
        return cls.get_api_key() is not None

    @classmethod
    def _generate_mock_analysis(cls, resume_text: str, job_description: str) -> GapAnalysis:
        """
        Deterministic, high-quality analysis fallback grounded strictly in the PDF curriculum.
        """
        jd_lower = job_description.lower()
        resume_lower = resume_text.lower()

        tech_keywords = [
            "python", "javascript", "typescript", "react", "node.js", "next.js",
            "sql", "postgresql", "mongodb", "docker", "kubernetes", "aws", "git",
            "rest apis", "graphql", "tailwind css", "html/css", "ci/cd", "linux",
            "jest", "unit testing", "fastapi", "django", "machine learning", "pandas"
        ]

        matched = []
        missing = []

        for kw in tech_keywords:
            in_jd = kw in jd_lower
            in_res = kw in resume_lower
            if in_jd and in_res:
                matched.append(kw.title())
            elif in_jd and not in_res:
                missing.append(kw.title())

        if not matched and not missing:
            matched = ["Git Version Control", "Core Programming Fundamentals", "Problem Solving"]
            missing = ["Docker Containerization", "PostgreSQL Database Design", "Automated Testing"]

        total = len(matched) + len(missing)
        ratio = len(matched) / max(total, 1)
        score = int(min(max(ratio * 100, 35), 95))

        if ratio >= 0.65:
            is_match = True
            status = "Strong Match"
            summary = "Strong alignment — your resume already demonstrates the primary foundational competencies required for this role. Following the roadmap below will close the remaining gaps quickly."
            hiring_rec = "Strong candidate to advance directly to technical phone interview."
        elif ratio >= 0.4:
            is_match = True
            status = "Partial Match"
            summary = "Promising foundational alignment. You have valuable core building blocks; targeting the specific checkpoints below will bridge your profile to full readiness."
            hiring_rec = "Good potential for an internship or junior track. Recommend probing practical project depth."
        else:
            is_match = False
            status = "Early-Stage Match"
            summary = "Good baseline skills with significant growth opportunity. The role requires key specialized technologies outlined in the structured path forward."
            hiring_rec = "Candidate has solid fundamentals; best suited for an apprentice track or with dedicated onboarding mentorship."

        # Select exact curriculum track from the PDF
        curriculum_track = get_curriculum_track_for_role(job_description, resume_text)
        track_name = curriculum_track["title"]
        track_ref = curriculum_track["reference"]

        path_milestones: List[CheckpointMilestone] = []
        for cp in curriculum_track["checkpoints"]:
            path_milestones.append(
                CheckpointMilestone(
                    checkpoint=cp["checkpoint"],
                    topics=cp["topics"],
                    action=cp["action"]
                )
            )

        # Concise actionable steps
        roadmap = []
        for milestone in path_milestones[:3]:
            roadmap.append(milestone.action)
        for skill in missing[:2]:
            roadmap.append(f"Build a small, focused project applying {skill} to highlight practical experience on GitHub.")

        return GapAnalysis(
            is_match=is_match,
            match_status=status,
            match_score_percentage=score,
            summary=summary,
            extracted_skills=matched,
            missing_skills=missing,
            roadmap_track_name=track_name,
            roadmap_reference=track_ref,
            path_forward=path_milestones,
            learning_roadmap=roadmap,
            interview_questions=[],
            hiring_recommendation=hiring_rec
        )

    _CACHE = {}

    @classmethod
    def analyze(cls, resume_text: str, job_description: str) -> GapAnalysis:
        """
        Analyze resume against job description using Gemini AI.
        Uses SHA-256 caching and temperature=0.0 to ensure deterministic, consistent results.
        """
        import hashlib
        cache_key = hashlib.sha256(f"{resume_text.strip()}|||{job_description.strip()}".encode("utf-8")).hexdigest()
        if cache_key in cls._CACHE:
            return cls._CACHE[cache_key]

        api_key = cls.get_api_key()

        if not api_key:
            result = cls._generate_mock_analysis(resume_text, job_description)
            cls._CACHE[cache_key] = result
            return result

        try:
            genai.configure(api_key=api_key)

            prompt = f"""
TARGET JOB DESCRIPTION:
\"\"\"{job_description}\"\"\"

CANDIDATE RESUME:
\"\"\"{resume_text}\"\"\"

Provide your structured technical gap analysis in the specified JSON format.
Ensure the roadmap_track_name, roadmap_reference, and path_forward are strictly selected
from the official Roadmap.sh curriculum provided in your system instructions.
"""
            model = genai.GenerativeModel(
                model_name="gemini-3.6-flash",
                system_instruction=SYSTEM_PROMPT,
                generation_config={
                    "response_mime_type": "application/json",
                    "temperature": 0.0
                }
            )

            response = model.generate_content(prompt)
            data = json.loads(response.text.strip())
            result = GapAnalysis.model_validate(data)
            cls._CACHE[cache_key] = result
            return result

        except Exception as e:
            print(f"Gemini API call returned: {e}. Using deterministic curriculum engine.")
            return cls._generate_mock_analysis(resume_text, job_description)
