import os
import tempfile
from gtts import gTTS
import speech_recognition as sr
from config import settings

class SpeechService:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def speech_to_text(self, audio_file) -> str:
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
                return self.recognizer.recognize_google(audio)
        except Exception as e:
            raise Exception(f"Error in speech recognition: {str(e)}")

    def text_to_speech(self, text: str) -> str:
        try:
            # Create a temporary file for the audio
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                tts = gTTS(text=text, lang='en')
                tts.save(fp.name)
                return fp.name
        except Exception as e:
            raise Exception(f"Error in text to speech conversion: {str(e)}")

speech_service = SpeechService()