import re
from typing import List

from agents.base_agent import BaseAgent
from context_store import get_context

SYSTEM_PROMPT = (
    "You are an expert exam question generator. Based on the given subject, exam type, "
    "and existing context, generate high-quality, realistic, and practice-oriented questions. "
    "Maintain the difficulty level and pattern relevant to the exam. "
    "Ensure variety and clarity. Avoid repeating questions. "
    "Always return questions as a numbered list (1. 2. 3. ...). "
    "Each question should be clearly stated and self-contained."
)


class QuestionAgent(BaseAgent):
    """Reads context from metadata/ folder and generates exam questions."""

    def run(self, subject: str, exam_type: str, num_questions: int, chat_history: List[dict] = None) -> dict:
        # Read context from metadata folder via context_store
        context = get_context(subject, exam_type)
        user_prompt = self._build_prompt(subject, exam_type, num_questions, context)
        raw_text = self.call_llm(SYSTEM_PROMPT, user_prompt, chat_history or [])
        questions = self._parse(raw_text)
        return {
            "formatted_text": raw_text,
            "questions": questions,
            "subject": subject,
            "exam_type": exam_type,
            "num_questions": num_questions,
        }

    def _build_prompt(self, subject: str, exam_type: str, num_questions: int, context: dict) -> str:
        sample_qs = "\n".join(
            f"  {i+1}. {q}" for i, q in enumerate(context.get("sample_questions", []))
        )
        return (
            f"Generate practice questions for:\n"
            f"Subject: {subject}\nExam Type: {exam_type}\n\n"
            f"Context:\n"
            f"  Difficulty: {context.get('difficulty', 'Medium')}\n"
            f"  Pattern: {context.get('pattern', 'Mixed')}\n"
            f"  Sample Questions (do NOT repeat):\n{sample_qs}\n\n"
            f"Generate {num_questions} NEW questions matching the difficulty and pattern above."
        )

    def _parse(self, text: str) -> List[str]:
        lines = text.strip().split("\n")
        questions, current = [], []
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
