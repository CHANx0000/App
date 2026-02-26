from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.llm import chat_completion

router = APIRouter(prefix="/api", tags=["chat"])


class HistoryMessage(BaseModel):
    role: str       # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[HistoryMessage] = []


class ChatResponse(BaseModel):
    message: str


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=422, detail="Message cannot be empty.")

    history = [{"role": m.role, "content": m.content} for m in request.history]

    reply = await chat_completion(request.message, history)
    return ChatResponse(message=reply)
