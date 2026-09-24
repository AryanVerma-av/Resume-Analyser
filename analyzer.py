"""
Backward-compatibility adapter module.
Delegates to modular services:
- gemini_service.py (Gemini AI career coach)
- parser.py (pdfplumber text extraction)
"""

from parser import extract_text_from_pdf
from gemini_service import GeminiService
from models import GapAnalysis


def analyze_profile(resume_text: str, job_description: str, api_key: str = None) -> GapAnalysis:
    """Delegates to GeminiService.analyze."""
    return GeminiService.analyze(resume_text, job_description)
