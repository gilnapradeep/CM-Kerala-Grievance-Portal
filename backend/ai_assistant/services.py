
import json
import os
import re
from difflib import SequenceMatcher

from google import genai
from google.genai import types

from departments.models import Department
from grievances.models import Grievance


VALID_CATEGORIES = {
    "INFRASTRUCTURE", "HEALTHCARE", "EDUCATION",
    "PUBLIC_SERVICES", "WATER", "ELECTRICITY",
    "TRANSPORT", "SANITATION", "OTHER",
}

VALID_PRIORITIES = {"LOW", "MEDIUM", "HIGH"}


def find_similar_grievances(grievance, limit=3):
    """Find possible duplicate grievances in the same district."""
    current_text = f"{grievance.subject} {grievance.description}".lower()

    candidates = Grievance.objects.filter(
        district=grievance.district
    ).exclude(id=grievance.id).order_by("-created_at")[:200]

    matches = []

    for item in candidates:
        other_text = f"{item.subject} {item.description}".lower()
        score = SequenceMatcher(
            None, current_text, other_text
        ).ratio()

        if score >= 0.35:
            matches.append({
                "reference_number": item.reference_number,
                "subject": item.subject,
                "similarity": round(score, 2),
                "status": item.status,
            })

    return sorted(
        matches,
        key=lambda item: item["similarity"],
        reverse=True
    )[:limit]


def local_analysis(grievance, error_message=None):
    """Fast local fallback when Gemini is unavailable."""
    text = (
        f"{grievance.subject} {grievance.description}"
    ).lower()

    rules = [
        (
            "WATER",
            ["water", "drinking water", "pipeline", "tap", "water supply"],
            ["water"],
        ),
        (
            "ELECTRICITY",
            ["electricity", "power cut", "electric", "transformer", "street light"],
            ["electricity", "power"],
        ),
        (
            "HEALTHCARE",
            ["hospital", "doctor", "health", "medicine", "clinic", "ambulance"],
            ["health"],
        ),
        (
            "EDUCATION",
            ["school", "college", "teacher", "student", "education"],
            ["education"],
        ),
        (
            "TRANSPORT",
            ["road", "bridge", "bus", "traffic", "transport", "pothole"],
            ["transport", "public works", "road"],
        ),
        (
            "SANITATION",
            ["garbage", "waste", "drainage", "sewage", "sanitation", "cleaning"],
            ["sanitation", "local self government"],
        ),
        (
            "INFRASTRUCTURE",
            ["building", "construction", "infrastructure", "dam"],
            ["public works", "infrastructure"],
        ),
    ]

    category = "PUBLIC_SERVICES"
    department_keywords = []

    for category_name, keywords, dept_keywords in rules:
        if any(keyword in text for keyword in keywords):
            category = category_name
            department_keywords = dept_keywords
            break

    # Identify a likely department from departments stored in the database.
    suggested_department = None
    departments = list(
        Department.objects.filter(is_active=True)
    )

    for department in departments:
        name = department.name.lower()
        if any(keyword in name for keyword in department_keywords):
            suggested_department = department.name
            break

    # Simple urgency estimation.
    urgent_words = [
        "emergency", "urgent", "danger", "life threatening",
        "accident", "severe", "critical", "immediately",
    ]
    medium_words = [
        "days", "week", "repeated", "not working",
        "damaged", "problem", "issue",
    ]

    if any(word in text for word in urgent_words):
        priority = "HIGH"
    elif any(word in text for word in medium_words):
        priority = "MEDIUM"
    else:
        priority = "LOW"

    summary = (
        f"A citizen from {grievance.district} has reported "
        f"{grievance.subject}. The complaint concerns "
        f"{category.replace('_', ' ').lower()}. "
        "The concerned department should review the issue "
        "and take appropriate action."
    )

    similar = find_similar_grievances(grievance)

    return {
        "suggested_department": suggested_department,
        "suggested_category": category,
        "suggested_priority": priority,
        "summary": summary,
        "reasoning": (
            "Generated using local keyword-based analysis because "
            "the external AI service was unavailable. "
            "This is a preliminary suggestion requiring human review."
        ),
        "similar_grievances": similar,
        "duplicate_candidates_found": bool(similar),
        "analysis_provider": "local_fallback",
        "ai_error": str(error_message)[:300] if error_message else None,
    }


def analyze_grievance(grievance):
    """Try Gemini first, then automatically use local analysis."""
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

    if not api_key:
        return local_analysis(grievance, "Gemini API key is not configured.")

    departments = list(
        Department.objects.filter(is_active=True).values_list(
            "name", flat=True
        )
    )

    prompt = f"""
You are an AI assistant for a public grievance portal.

Analyze the following citizen complaint and return ONLY valid JSON.

Available departments: {departments}
Valid categories: {sorted(VALID_CATEGORIES)}
Valid priorities: LOW, MEDIUM, HIGH

Complaint district: {grievance.district}
Subject: {grievance.subject}
Description: {grievance.description}

Return this JSON structure:
{{
  "suggested_department": "exact department name or null",
  "suggested_category": "one valid category",
  "suggested_priority": "LOW, MEDIUM, or HIGH",
  "summary": "short factual summary for CMO",
  "reasoning": "brief explanation"
}}

Do not invent facts. Do not make official decisions.
"""

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2,
            ),
        )

        raw_text = response.text or ""
        raw_text = re.sub(
            r"^```(?:json)?\s*|\s*```$",
            "",
            raw_text.strip(),
            flags=re.IGNORECASE,
        )

        result = json.loads(raw_text)

        category = str(
            result.get("suggested_category", "OTHER")
        ).upper()

        priority = str(
            result.get("suggested_priority", "MEDIUM")
        ).upper()

        if category not in VALID_CATEGORIES:
            category = "OTHER"

        if priority not in VALID_PRIORITIES:
            priority = "MEDIUM"

        department_name = result.get("suggested_department")
        valid_department = Department.objects.filter(
            name__iexact=department_name,
            is_active=True,
        ).first() if department_name else None

        similar = find_similar_grievances(grievance)

        return {
            "suggested_department": (
                valid_department.name if valid_department else None
            ),
            "suggested_category": category,
            "suggested_priority": priority,
            "summary": str(result.get("summary", "")),
            "reasoning": str(result.get("reasoning", "")),
            "similar_grievances": similar,
            "duplicate_candidates_found": bool(similar),
            "analysis_provider": "gemini",
            "ai_error": None,
        }

    except Exception as exc:
        # Do not let a Gemini outage break the grievance workflow.
        return local_analysis(grievance, str(exc))
