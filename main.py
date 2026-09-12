from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from qa_engine import answer_question


app = FastAPI(
    title="StudyVault AI",
    description="Course Material Study Assistant",
    version="1.0"
)


class QuestionRequest(BaseModel):
    question: str


# Serve frontend files
app.mount("/app", StaticFiles(directory="frontend", html=True), name="frontend")


@app.get("/")
def home():
    return {
        "message": "StudyVault AI is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    result = answer_question(request.question)

    return {
        "question": request.question,
        "status": result["status"],
        "answer": result["answer"],
        "sources": result["sources"]
    }