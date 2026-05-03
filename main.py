"""
FastAPI application entry point for the AI Question Generator Agent.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from models import GenerateRequest, GenerateResponse
from agent import generate_questions

app = FastAPI(
    title="AI Question Generator Agent",
    description="An intelligent exam question generator powered by Gemini AI",
    version="1.0.0",
)

# Mount static files (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", include_in_schema=False)
async def serve_frontend():
    """Serve the main frontend HTML."""
    return FileResponse("static/index.html")


@app.post("/api/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """
    Generate practice questions for a given subject and exam type.
    Uses Gemini LLM with predefined context and chat history support.
    """
    try:
        result = generate_questions(
            subject=request.subject,
            exam_type=request.exam_type,
            num_questions=request.num_questions,
            chat_history=request.chat_history,
        )
        return GenerateResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate questions: {str(e)}"
        )


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    api_key_set = bool(os.getenv("GEMINI_API_KEY", ""))
    return {
        "status": "ok",
        "gemini_api_key_configured": api_key_set,
    }


@app.get("/api/subjects")
async def list_subjects():
    """Return supported subjects and exam types."""
    return {
        "subjects": [
            "Mathematics",
            "Physics",
            "Chemistry",
            "Biology",
            "Computer Science",
        ],
        "exam_types": ["JEE", "NEET", "SAT", "GATE", "UPSC"],
    }
