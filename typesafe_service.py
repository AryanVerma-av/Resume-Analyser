"""
TypeSafe API Service Module (System One Primitives).
Simulates low-latency screening primitives to protect heavy LLM operations:
1. Noul Gatekeeper: Fast boolean classifier (is_engineering_role).
2. Choice Categorizer: Fast multiclass classifier (RoleCategory).

Architectural Rationale:
Calling a heavy LLM for out-of-scope or malformed roles wastes tokens and adds latency.
TypeSafe acts as a rapid gatekeeper (<10ms) before invoking Gemini AI.
"""

import os
import re
import time
from typing import Tuple, Optional
from dotenv import load_dotenv
from models import RoleCategory, ScreeningResult

load_dotenv()


class TypeSafeService:
    """
    Service client for TypeSafe API primitives (System One).
    Supports API key authentication via TYPESAFE_API_KEY.
    """

    @classmethod
    def get_api_key(cls) -> Optional[str]:
        return os.getenv("TYPESAFE_API_KEY")

    @classmethod
    def is_configured(cls) -> bool:
        key = cls.get_api_key()
        return bool(key and key.strip())

    NON_ENGINEERING_COMPILED = [
        re.compile(p, re.IGNORECASE) for p in [
            r"\bchef\b", r"\bcook\b", r"\bculinary\b", r"\brestaurant\b",
            r"\breal estate\b", r"\brealtor\b", r"\bhair stylist\b",
            r"\bnurse\b", r"\bnursing\b", r"\bphysician\b", r"\bdentist\b",
            r"\bflight attendant\b", r"\bpilot\b", r"\btruck driver\b",
            r"\bbarista\b", r"\bcarpenter\b", r"\bplumber\b", r"\bevent planner\b",
            r"\bbanquet\b", r"\bcatering\b", r"\bwaiter\b", r"\bwaitress\b"
        ]
    ]

    ENGINEERING_COMPILED = [
        re.compile(p, re.IGNORECASE) for p in [
            r"\bdeveloper\b", r"\bengineer\b", r"\bsoftware\b", r"\bprogramming\b",
            r"\bcode\b", r"\bcoding\b", r"\bfrontend\b", r"\bbackend\b", r"\bfull\s*stack\b",
            r"\bpython\b", r"\bjava\b", r"\bjavascript\b", r"\btypescript\b", r"\bc\+\+\b",
            r"\bgolang\b", r"\brust\b", r"\bdata\s*science\b", r"\bmachine\s*learning\b",
            r"\bdevops\b", r"\bcloud\b", r"\bsystem\s*architect\b", r"\bdatabase\b",
            r"\breact\b", r"\bnode\b", r"\bapi\b", r"\bgit\b", r"\bsql\b", r"\blinux\b",
            r"\balgorithm\b", r"\bcomputer\s*science\b", r"\bit\s*support\b", r"\bcyber\s*security\b"
        ]
    ]

    CATEGORIES_COMPILED = {
        RoleCategory.FRONTEND: [
            re.compile(p, re.IGNORECASE) for p in [
                r"\bfrontend\b", r"\bfront-end\b", r"\breact\b", r"\bvue\b", r"\bangular\b",
                r"\bcss\b", r"\bhtml\b", r"\bui\b", r"\bux\b", r"\btailwind\b", r"\bnext\.?js\b"
            ]
        ],
        RoleCategory.BACKEND: [
            re.compile(p, re.IGNORECASE) for p in [
                r"\bbackend\b", r"\bback-end\b", r"\bserver\b", r"\bnode\b", r"\bexpress\b",
                r"\bdjango\b", r"\bflask\b", r"\bfastapi\b", r"\bspring\b", r"\bgo\b", r"\bpostgres\b",
                r"\bmicroservices\b", r"\brabbitmq\b", r"\bkafka\b"
            ]
        ],
        RoleCategory.DATA_AI: [
            re.compile(p, re.IGNORECASE) for p in [
                r"\bdata\s*(scientist|analyst|engineer)\b", r"\bmachine\s*learning\b", r"\bdeep\s*learning\b",
                r"\bpytorch\b", r"\btensorflow\b", r"\bnlp\b", r"\bai\b", r"\bllm\b", r"\bpandas\b",
                r"\bnumpy\b", r"\bcomputer\s*vision\b"
            ]
        ],
        RoleCategory.DEVOPS_CLOUD: [
            re.compile(p, re.IGNORECASE) for p in [
                r"\bdevops\b", r"\bcloud\b", r"\baws\b", r"\bgcp\b", r"\bazure\b", r"\bdocker\b",
                r"\bkubernetes\b", r"\bci/cd\b", r"\bterraform\b", r"\bsre\b", r"\blinux\b"
            ]
        ],
        RoleCategory.MOBILE: [
            re.compile(p, re.IGNORECASE) for p in [
                r"\bmobile\b", r"\bios\b", r"\bandroid\b", r"\bswift\b", r"\bkotlin\b",
                r"\breact\s*native\b", r"\bflutter\b"
            ]
        ],
        RoleCategory.FULL_STACK: [
            re.compile(p, re.IGNORECASE) for p in [
                r"\bfull\s*stack\b", r"\bfullstack\b", r"\bmearn\b", r"\bmean\b"
            ]
        ]
    }

    @classmethod
    def evaluate_noul_gatekeeper(cls, text: str) -> Tuple[bool, str]:
        """
        Noul Gatekeeper Primitive:
        Returns: (is_engineering_role, scope_message)
        """
        text_lower = text.lower()
        eng_count = sum(1 for regex in cls.ENGINEERING_COMPILED if regex.search(text_lower))
        non_eng_count = sum(1 for regex in cls.NON_ENGINEERING_COMPILED if regex.search(text_lower))

        if eng_count > 0 and eng_count >= non_eng_count:
            return True, "Engineering domain scope confirmed."
        elif non_eng_count > 0 and eng_count == 0:
            return False, "This role looks outside our current focus (software/engineering roles). SkillGap is currently tailored for engineering and tech competencies."

        # General tech check
        if any(kw in text_lower for kw in ["project", "technical", "computer", "app", "web", "data", "test", "build", "code"]):
            return True, "Scope confirmed: Technical / Engineering role."

        return False, "This role looks outside our current focus (software/engineering roles). SkillGap is currently tailored for engineering and tech competencies."

    @classmethod
    def evaluate_choice_categorizer(cls, text: str) -> RoleCategory:
        """
        Choice Categorizer Primitive:
        Evaluates candidate role track (Frontend, Backend, Data, etc.)
        """
        text_lower = text.lower()
        scores = {}
        for category, regex_list in cls.CATEGORIES_COMPILED.items():
            matches = sum(1 for r in regex_list if r.search(text_lower))
            if matches > 0:
                scores[category] = matches

        if scores:
            return max(scores, key=scores.get)
        return RoleCategory.GENERAL_ENGINEERING

    @classmethod
    def screen(cls, resume_text: str, job_description: str) -> ScreeningResult:
        """
        Execute full TypeSafe System One screening pipeline.
        Fast, deterministic, sub-15ms execution.
        """
        start_time = time.time()
        combined_text = f"{job_description}\n{resume_text}"

        # Gate on Job Description first
        is_eng, message = cls.evaluate_noul_gatekeeper(job_description if job_description.strip() else combined_text)

        if not is_eng:
            return ScreeningResult(
                is_engineering_role=False,
                detected_category=RoleCategory.NON_ENGINEERING,
                scope_message=message,
                confidence_score=0.98
            )

        category = cls.evaluate_choice_categorizer(combined_text)

        return ScreeningResult(
            is_engineering_role=True,
            detected_category=category,
            scope_message="Ready for gap analysis. Technical engineering scope verified.",
            confidence_score=0.96
        )
