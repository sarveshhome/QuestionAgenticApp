"""
Agent orchestrator: delegates to agents in the agents/ folder.
"""

from typing import List
from models import ChatMessage
from agents import QuestionAgent, ReviewAgent


def generate_questions(
    subject: str,
    exam_type: str,
    num_questions: int,
    chat_history: List[ChatMessage] = None
) -> dict:
    history = [
        {"role": msg.role, "content": msg.content}
        for msg in (chat_history or [])[:-1]
    ]

    # Step 1: Generate questions
    result = QuestionAgent().run(
        subject=subject,
        exam_type=exam_type,
        num_questions=num_questions,
        chat_history=history,
    )

    # Step 2: Review generated questions
    review = ReviewAgent().run(
        subject=subject,
        exam_type=exam_type,
        questions=result["questions"],
    )

    result["review"] = review["review"]
    return result
