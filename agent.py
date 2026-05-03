"""
Agent module: handles context retrieval, prompt construction, and Gemini API calls.
"""

import os
import re
from typing import List

from google import genai
from google.genai import types
from dotenv import load_dotenv

from context_store import get_context
from models import ChatMessage

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

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
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set. Please add it to your .env file.")

    # Step 1: Fetch context
    context = get_context(subject, exam_type)

    # Step 2: Build prompt
    user_prompt = build_user_prompt(subject, exam_type, num_questions, context)

    # Step 3: Build contents list (chat history + current prompt)
    contents = []
    if chat_history:
        for msg in chat_history[:-1]:  # exclude last user msg (we'll add it fresh)
            role = "user" if msg.role == "user" else "model"
            contents.append(types.Content(role=role, parts=[types.Part(text=msg.content)]))

    contents.append(types.Content(role="user", parts=[types.Part(text=user_prompt)]))

    # Step 4: Call Gemini via new google-genai SDK
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.8,
        ),
    )

    raw_text = response.text.strip()

    # Step 5: Parse questions
    questions = parse_questions(raw_text)

    return {
        "formatted_text": raw_text,
        "questions": questions,
        "subject": subject,
        "exam_type": exam_type,
        "num_questions": num_questions,
    }
