from typing import List

from agents.base_agent import BaseAgent
from context_store import get_context

SYSTEM_PROMPT = (
    "You are an expert exam question reviewer. "
    "Given a list of questions, review them for clarity, difficulty, and relevance to the exam. "
    "Return a brief review for each question and an overall quality score out of 10."
)


class ReviewAgent(BaseAgent):
    """Reads context from metadata/ folder and reviews generated questions."""

    def run(self, subject: str, exam_type: str, questions: List[str]) -> dict:
        # Read context from metadata folder to validate against difficulty/pattern
        context = get_context(subject, exam_type)
        user_prompt = self._build_prompt(subject, exam_type, questions, context)
        review_text = self.call_llm(SYSTEM_PROMPT, user_prompt)
        return {
            "review": review_text,
            "subject": subject,
            "exam_type": exam_type,
            "questions_reviewed": len(questions),
        }

    def _build_prompt(self, subject: str, exam_type: str, questions: List[str], context: dict) -> str:
        qs = "\n".join(f"  {i+1}. {q}" for i, q in enumerate(questions))
        return (
            f"Review these {subject} ({exam_type}) questions:\n{qs}\n\n"
            f"Expected difficulty: {context.get('difficulty', 'Medium')}\n"
            f"Expected pattern: {context.get('pattern', 'Mixed')}\n\n"
            f"For each question, comment on clarity and relevance. Give an overall score out of 10."
        )
