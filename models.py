from pydantic import BaseModel, Field
from typing import List, Optional


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class GenerateRequest(BaseModel):
    subject: str = Field(..., description="Subject (e.g. Mathematics, Physics)")
    exam_type: str = Field(..., description="Exam type (e.g. JEE, NEET, SAT)")
    num_questions: int = Field(default=2, ge=1, le=15, description="Number of questions to generate")
    chat_history: Optional[List[ChatMessage]] = Field(default=[], description="Previous chat turns")


class GenerateResponse(BaseModel):
    formatted_text: str
    questions: List[str]
    subject: str
    exam_type: str
    num_questions: int
