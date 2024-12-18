from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.gemini_service import gemini_service

router = APIRouter()

class ChatMessage(BaseModel):
    message: str

@router.post("/chat")
async def chat_endpoint(message: ChatMessage):
    try:
        response = await gemini_service.get_response(message.message)
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))