"""
Backward-compatibility adapter module for TypeSafe filter.
Delegates to typesafe_service.py.
"""

from typesafe_service import TypeSafeService
from models import RoleCategory, ScreeningResult


class NoulGatekeeper:
    @classmethod
    def evaluate(cls, text: str):
        return TypeSafeService.evaluate_noul_gatekeeper(text)


class ChoiceCategorizer:
    @classmethod
    def categorize(cls, text: str):
        return TypeSafeService.evaluate_choice_categorizer(text)


def run_screening(resume_text: str, job_description: str) -> ScreeningResult:
    return TypeSafeService.screen(resume_text, job_description)
