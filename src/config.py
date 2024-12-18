import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    GOOGLE_API_KEYS: str = os.getenv("GOOGLE_API_KEYS", "")
    MODEL_NAME: str = "gemini-1.5-flash"
    AUDIO_UPLOAD_DIR: str = "uploads"
    
    class Config:
        env_file = ".env"

settings = Settings()