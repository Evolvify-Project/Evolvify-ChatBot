import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from services.speech_service import speech_service

router = APIRouter()

class TextToSpeechRequest(BaseModel):
    text: str

@router.post("/speech-to-text")
async def speech_to_text_endpoint(audio: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        temp_file = f"temp_{audio.filename}"
        with open(temp_file, "wb") as buffer:
            content = await audio.read()
            buffer.write(content)
        
        # Convert speech to text
        text = speech_service.speech_to_text(temp_file)
        
        # Clean up
        os.remove(temp_file)
        
        return {"transcription": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/text-to-speech")
async def text_to_speech_endpoint(request: TextToSpeechRequest):
    try:
        audio_file = speech_service.text_to_speech(request.text)
        return FileResponse(
            audio_file,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment; filename=speech.mp3"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))