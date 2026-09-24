"""
FastAPI AI Backend for SkillGap Resume Analyzer.
Connects Next.js -> FastAPI -> Supabase -> Gemini AI.
Processes resume files stored in Supabase Storage, extracts text,
runs Gemini AI gap analysis, and records structured results in Supabase.
"""

import io
import os
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, BackgroundTasks, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pdfplumber

# Existing domain services
from gemini_service import GeminiService
from models import GapAnalysis

# Supabase Python client
try:
    from supabase import create_client, Client
except ImportError:
    create_client = None
    Client = None

load_dotenv()

app = FastAPI(
    title="SkillGap AI Resume Analyzer Engine",
    description="Processes resumes from Supabase Storage, performs Gemini-powered ATS & curriculum fit analysis.",
    version="1.0.0",
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = os.getenv("SUPABASE_URL") or os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase_client: Optional[Client] = None
if create_client and SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY:
    supabase_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


class AnalyzeResumeRequest(BaseModel):
    resume_id: str = Field(..., description="UUID of the resume record in Supabase")
    job_description: Optional[str] = Field(
        default="",
        description="Target job description. If empty, a general full-stack engineering rubric is used."
    )
    job_id: Optional[str] = Field(
        default=None,
        description="Optional job ID if analyzing against a saved job"
    )


def extract_text_from_bytes(file_bytes: bytes) -> str:
    """Extract plain text from PDF bytes using pdfplumber."""
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            pages_text = [page.extract_text() or "" for page in pdf.pages]
            return "\n".join(pages_text).strip()
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return ""


def run_ai_analysis_job(resume_id: str, job_description: str, job_id: Optional[str] = None):
    """
    Background worker task:
    1. Fetches resume metadata and file from Supabase Storage
    2. Extracts text
    3. Runs Gemini Career Coach analysis
    4. Persists the analysis to `resume_analyses`
    """
    if not supabase_client:
        print("Supabase client is not configured with service role key.")
        return

    try:
        # Mark analysis as 'processing'
        analysis_record = supabase_client.table("resume_analyses").insert({
            "resume_id": resume_id,
            "analysis_status": "processing",
            "strengths": [],
            "weaknesses": [],
            "missing_skills": [],
            "recommendations": {}
        }).execute()
        
        analysis_id = analysis_record.data[0]["id"] if analysis_record.data else None

        # Fetch resume record from Supabase
        res_response = supabase_client.table("resumes").select("*").eq("id", resume_id).single().execute()
        resume_data = res_response.data
        if not resume_data:
            raise ValueError(f"Resume {resume_id} not found in database.")

        file_path = resume_data.get("file_path")
        extracted_text = resume_data.get("extracted_text")

        # If text is not yet extracted, download PDF from Supabase Storage and extract
        if not extracted_text:
            file_bytes = supabase_client.storage.from_("resumes").download(file_path)
            extracted_text = extract_text_from_bytes(file_bytes)
            
            # Save extracted text to resumes table
            supabase_client.table("resumes").update({
                "extracted_text": extracted_text
            }).eq("id", resume_id).execute()

        # If target job was passed by job_id, retrieve description
        if job_id and not job_description:
            job_resp = supabase_client.table("jobs").select("description").eq("id", job_id).single().execute()
            if job_resp.data:
                job_description = job_resp.data.get("description", "")

        fallback_role = "Full Stack Software Engineer (React, Node.js, Python, PostgreSQL, REST APIs, Git)"
        jd = job_description if (job_description and job_description.strip()) else fallback_role

        # Run Gemini AI Career Coach Analysis
        analysis: GapAnalysis = GeminiService.analyze(extracted_text, jd)

        # Calculate balanced breakdown scores
        overall = analysis.match_score_percentage
        ats_score = min(100, max(10, overall + (5 if analysis.is_match else -5)))
        skills_score = min(100, max(10, len(analysis.extracted_skills) * 12))
        exp_score = min(100, max(20, overall - 5))
        edu_score = 85

        recommendations_payload = {
            "summary": analysis.summary,
            "match_status": analysis.match_status,
            "roadmap_track_name": analysis.roadmap_track_name,
            "roadmap_reference": analysis.roadmap_reference,
            "path_forward": [p.model_dump() for p in analysis.path_forward],
            "learning_roadmap": analysis.learning_roadmap,
            "interview_questions": analysis.interview_questions,
            "hiring_recommendation": analysis.hiring_recommendation,
        }

        # Update Supabase resume_analyses row to 'completed'
        update_payload = {
            "overall_score": overall,
            "ats_score": ats_score,
            "skills_score": skills_score,
            "experience_score": exp_score,
            "education_score": edu_score,
            "strengths": [analysis.summary] + [f"Matched skill: {s}" for s in analysis.extracted_skills[:4]],
            "weaknesses": [f"Missing skill: {s}" for s in analysis.missing_skills[:5]],
            "missing_skills": analysis.missing_skills,
            "recommendations": recommendations_payload,
            "analysis_status": "completed",
        }

        if analysis_id:
            supabase_client.table("resume_analyses").update(update_payload).eq("id", analysis_id).execute()
        else:
            supabase_client.table("resume_analyses").insert({
                "resume_id": resume_id,
                **update_payload
            }).execute()

        print(f"Successfully processed analysis for resume {resume_id}")

    except Exception as e:
        print(f"Failed processing resume {resume_id}: {e}")
        if supabase_client:
            supabase_client.table("resume_analyses").insert({
                "resume_id": resume_id,
                "analysis_status": "failed",
                "strengths": [],
                "weaknesses": [str(e)],
                "missing_skills": [],
                "recommendations": {"error": str(e)}
            }).execute()


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "supabase_configured": supabase_client is not None,
        "gemini_configured": GeminiService.is_configured(),
    }


@app.post("/api/analyze-resume", status_code=status.HTTP_202_ACCEPTED)
def trigger_resume_analysis(
    payload: AnalyzeResumeRequest,
    background_tasks: BackgroundTasks
):
    """
    Asynchronously queues a resume for AI analysis.
    The client receives 202 Accepted immediately and can poll Supabase
    or subscribe via Supabase Realtime for the 'completed' analysis.
    """
    if not supabase_client:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Supabase credentials (SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY) not configured on backend."
        )

    background_tasks.add_task(
        run_ai_analysis_job,
        payload.resume_id,
        payload.job_description or "",
        payload.job_id
    )

    return {
        "message": "Analysis started in background",
        "resume_id": payload.resume_id,
        "status": "processing"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi_server:app", host="0.0.0.0", port=8000, reload=True)
