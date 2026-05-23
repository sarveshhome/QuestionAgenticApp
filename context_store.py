"""
Predefined context store for subjects and exam types.
Loads sample questions, patterns, and difficulty metadata from JSON files
in the 'metadata/' folder. Each file is named {subject}_{exam}.json.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional

# Directory where all question metadata JSON files live
METADATA_DIR = Path(__file__).parent / "metadata"

# Subject name aliases for partial-match support
_SUBJECT_ALIASES: Dict[str, str] = {
    "maths": "mathematics",
    "math": "mathematics",
    "cs": "computer science",
    "comp sci": "computer science",
    "bio": "biology",
    "chem": "chemistry",
    "phy": "physics",
}


def _normalize(text: str) -> str:
    """Lowercase and strip a string."""
    return text.lower().strip()


def _file_key(subject: str, exam: str) -> str:
    """Build the filename stem: e.g. 'computer_science_gate'."""
    return f"{subject.replace(' ', '_')}_{exam}"


def _load_metadata(subject: str, exam: str) -> Optional[dict]:
    """
    Try to load metadata from metadata/{subject}_{exam}.json.
    Returns the parsed dict or None if the file doesn't exist.
    """
    filename = METADATA_DIR / f"{_file_key(subject, exam)}.json"
    if filename.exists():
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def _resolve_subject(raw_subject: str) -> str:
    """
    Map common aliases/abbreviations to the canonical subject name
    used in filenames (e.g. 'maths' → 'mathematics').
    """
    norm = _normalize(raw_subject)
    # Direct alias hit
    if norm in _SUBJECT_ALIASES:
        return _SUBJECT_ALIASES[norm]
    # Check if any canonical name is contained in / contains the input
    canonical_subjects = {
        p.stem.rsplit("_", 1)[0].replace("_", " ")
        for p in METADATA_DIR.glob("*.json")
    }
    for subj in canonical_subjects:
        if subj in norm or norm in subj:
            return subj
    return norm


def _fallback_exam(subject: str) -> Optional[dict]:
    """
    If the requested exam type has no file, fall back to the first
    available exam file for that subject.
    """
    prefix = subject.replace(" ", "_") + "_"
    matches = sorted(METADATA_DIR.glob(f"{prefix}*.json"))
    if matches:
        with open(matches[0], "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def get_context(subject: str, exam_type: str) -> dict:
    """
    Retrieve context for a given subject and exam type.

    Resolution order:
    1. Exact match  → metadata/{subject}_{exam}.json
    2. Alias match  → canonical subject name via _resolve_subject
    3. Exam fallback→ first available exam for that subject
    4. Default      → generic placeholder context
    """
    subj = _resolve_subject(subject)
    exam = _normalize(exam_type)

    # 1. Exact match
    data = _load_metadata(subj, exam)
    if data:
        return data

    # 2. Partial subject match already applied by _resolve_subject; try again
    #    with the resolved name (covers alias cases)
    data = _load_metadata(subj, exam)
    if data:
        return data

    # 3. Fallback to first available exam for this subject
    data = _fallback_exam(subj)
    if data:
        return data

    # 4. Generic default
    return _default_context(subject, exam_type)


def list_available_contexts() -> Dict[str, List[str]]:
    """
    Return a dict mapping each subject to its available exam types,
    derived from filenames in the metadata/ folder.

    Example: {'mathematics': ['gate', 'jee', 'sat'], ...}
    """
    result: Dict[str, List[str]] = {}
    for path in sorted(METADATA_DIR.glob("*.json")):
        stem = path.stem  # e.g. 'mathematics_jee'
        parts = stem.rsplit("_", 1)
        if len(parts) == 2:
            subj_raw, exam = parts
            subj = subj_raw.replace("_", " ")
            result.setdefault(subj, []).append(exam)
    return result


def _default_context(subject: str, exam_type: str) -> dict:
    return {
        "difficulty": "Medium",
        "pattern": "Mixed MCQ and descriptive questions",
        "sample_questions": [
            f"Explain a fundamental concept in {subject}.",
            f"What is the most important topic in {subject} for {exam_type}?",
            f"Solve a typical {exam_type} problem related to {subject}.",
            f"Describe the application of {subject} in real life.",
            f"Give an example of a difficult {exam_type} question on {subject}.",
        ],
    }
