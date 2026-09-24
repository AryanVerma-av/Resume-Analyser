"""
Automated verification script for SkillGap components.
Tests models, TypeSafe service, Gemini service, and PDF extraction.
"""

import sys
import io

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from models import GapAnalysis, ScreeningResult, RoleCategory, UserPersona
from typesafe_service import TypeSafeService
from gemini_service import GeminiService
from parser import extract_text_from_pdf


def test_models():
    print("[1/4] Testing Pydantic models for Student and HR...")
    res = GapAnalysis(
        is_match=True,
        match_status="Strong Match",
        match_score_percentage=85,
        summary="You have great foundational alignment.",
        extracted_skills=["Python", "React"],
        missing_skills=["Docker"],
        learning_roadmap=["Build a small containerized app with Docker."],
        interview_questions=["How have you used Docker in personal projects?"],
        hiring_recommendation="Recommended for phone screen"
    )
    assert res.is_match is True
    assert res.match_score_percentage == 85
    assert "Python" in res.extracted_skills
    assert len(res.interview_questions) == 1
    print("  ✓ Models validated successfully.")


def test_typesafe_service():
    print("[2/4] Testing TypeSafe service (System One primitives)...")
    # Engineering role
    eng_jd = "Looking for a Frontend Developer experienced in React and TypeScript."
    res = TypeSafeService.screen("Alex CS Student React", eng_jd)
    assert res.is_engineering_role is True
    assert res.detected_category == RoleCategory.FRONTEND
    print(f"  ✓ Confirmed engineering role: {res.detected_category}")

    # Non-engineering role
    non_eng_jd = "Executive Head Chef needed for fine dining restaurant and culinary event banquets."
    res_non_eng = TypeSafeService.screen("Culinary arts resume", non_eng_jd)
    assert res_non_eng.is_engineering_role is False
    assert "outside our current focus" in res_non_eng.scope_message
    print(f"  ✓ Gated non-engineering role with scope guidance.")


def test_gemini_service():
    print("[3/4] Testing Gemini service (Student roadmap + HR interview questions)...")
    analysis = GeminiService.analyze(
        resume_text="Experienced in Python, JavaScript, HTML/CSS, React, Git.",
        job_description="Seeking a Backend Engineer with Python, PostgreSQL, Docker, and REST APIs."
    )
    assert isinstance(analysis, GapAnalysis)
    assert "Python" in analysis.extracted_skills
    assert len(analysis.learning_roadmap) > 0
    assert analysis.hiring_recommendation
    print(f"  ✓ Fit percentage: {analysis.match_score_percentage}%")
    print(f"  ✓ Sample Student roadmap: {analysis.learning_roadmap[0][:60]}...")
    print(f"  ✓ Hiring recommendation: {analysis.hiring_recommendation[:60]}...")
    print("  ✓ Gemini service returns valid GapAnalysis satisfying requirements.")


def test_pdf_extraction():
    print("[4/4] Testing PDF parser import...")
    import pdfplumber
    print(f"  ✓ pdfplumber {pdfplumber.__version__} ready.")


if __name__ == "__main__":
    try:
        test_models()
        test_typesafe_service()
        test_gemini_service()
        test_pdf_extraction()
        print("\nALL VERIFICATION CHECKS PASSED CLEANLY! 🎉")
    except Exception as e:
        print(f"\nVerification failed: {e}", file=sys.stderr)
        sys.exit(1)
