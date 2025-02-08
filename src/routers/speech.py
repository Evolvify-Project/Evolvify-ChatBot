import os
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from services.speech_service import speech_service
from pathlib import Path
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class TextToSpeechRequest(BaseModel):
    text: str

@router.post("/speech-to-text")
async def speech_to_text_endpoint(audio: UploadFile = File(...)):
    if not audio.filename:
        raise HTTPException(status_code=400, detail="No audio file provided")

    temp_path = None
    try:
        # Log incoming request
        logger.info(f"Received audio file: {audio.filename}")
        
        # Save uploaded file with original extension
        suffix = Path(audio.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            content = await audio.read()
            temp_file.write(content)
            temp_path = temp_file.name
            logger.info(f"Saved temporary file: {temp_path}")

        # Convert speech to text
        text = speech_service.speech_to_text(temp_path)
        logger.info("Successfully processed audio")

        return {"transcription": text}
    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup
        if temp_path:
            try:
                os.unlink(temp_path)
                logger.info(f"Cleaned up temporary file: {temp_path}")
            except Exception as e:
                logger.error(f"Error cleaning up file: {str(e)}")

@router.post("/text-to-speech")
async def text_to_speech_endpoint(request: TextToSpeechRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="No text provided")

    try:
        logger.info("Processing text-to-speech request")
        audio_file = speech_service.text_to_speech(request.text)
        
        return FileResponse(
            audio_file,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f"attachment; filename=speech.mp3"
            },
            background=lambda: os.unlink(audio_file)
        )
    except Exception as e:
        logger.error(f"Error in text-to-speech: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))