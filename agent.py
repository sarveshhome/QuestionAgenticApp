"""
Agent module: handles context retrieval, prompt construction, and LLM calls via adapter.
"""

import re
from typing import List

from context_store import get_context
from models import ChatMessage
from llm_adapter import get_adapter

SYSTEM_PROMPT = (
    "You are an expert exam question generator. Based on the given subject, exam type, "
    "and existing context, generate high-quality, realistic, and practice-oriented questions. "
    "Maintain the difficulty level and pattern relevant to the exam. "
    "Ensure variety and clarity. Avoid repeating questions. "
    "Always return questions as a numbered list (1. 2. 3. ...). "
    "Each question should be clearly stated and self-contained."
)


def build_user_prompt(
    subject: str,
    exam_type: str,
    num_questions: int,
    context: dict
) -> str:
    sample_qs = "\n".join(
        f"  {i+1}. {q}" for i, q in enumerate(context.get("sample_questions", []))
    )
    return (
        f"Generate practice questions for:\n"
        f"Subject: {subject}\n"
        f"Exam Type: {exam_type}\n\n"
        f"Use this context:\n"
        f"  Difficulty Level: {context.get('difficulty', 'Medium')}\n"
        f"  Question Pattern: {context.get('pattern', 'Mixed')}\n"
        f"  Sample Questions (for reference style only, do NOT repeat these):\n"
        f"{sample_qs}\n\n"
        f"Generate {num_questions} NEW similar questions that match the difficulty and pattern above."
    )


def parse_questions(text: str) -> List[str]:
    """Extract individual questions from the LLM numbered-list response."""
    lines = text.strip().split("\n")
    questions = []
    current = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if re.match(r"^\d+\.", stripped):
            if current:
                questions.append(" ".join(current).strip())
            current = [stripped]
        else:
            current.append(stripped)
    if current:
        questions.append(" ".join(current).strip())
    return questions


def generate_questions(
    subject: str,
    exam_type: str,
    num_questions: int,
    chat_history: List[ChatMessage] = None
) -> dict:
    """
    Main agent function:
    1. Retrieve context
    2. Build prompt
    3. Call Gemini
    4. Parse & return results
    """
    # Step 1: Fetch context
    context = get_context(subject, exam_type)

    # Step 2: Build prompt
    user_prompt = build_user_prompt(subject, exam_type, num_questions, context)

    # Step 3: Build chat history for adapter
    history = [
        {"role": msg.role, "content": msg.content}
        for msg in (chat_history or [])[:-1]
    ]

    # Step 4: Call LLM via adapter
    adapter = get_adapter()
    raw_text = adapter.generate(SYSTEM_PROMPT, user_prompt, history)

    # Step 5: Parse questions
    questions = parse_questions(raw_text)

    return {
        "formatted_text": raw_text,
        "questions": questions,
        "subject": subject,
        "exam_type": exam_type,
        "num_questions": num_questions,
    }
