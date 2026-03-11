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

    print()
    print(f"[1] FRONTEND → BACKEND | POST /api/chat received")
    print(f"    message : '{request.message}'")
    print(f"    history : {len(request.history)} previous turn(s)")
    print()

    history = [{"role": m.role, "content": m.content} for m in request.history]

    print()
    print(f"[2] BACKEND | History converted, calling LLM service...")
    print()

    reply = await chat_completion(request.message, history)

    print()
    print(f"[9] LLM SERVICE → BACKEND | Got final reply: '{reply}'")
    print()

    print()
    print(f"[10] BACKEND → FRONTEND | Sending ChatResponse back to Angular")
    print()

    return ChatResponse(message=reply)
