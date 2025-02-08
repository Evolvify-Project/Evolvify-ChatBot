import os
import tempfile
from pathlib import Path
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import logging
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpeechService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Create uploads directory if it doesn't exist
        Path(settings.AUDIO_UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

    def _convert_to_wav(self, input_file: str) -> str:
        """Convert audio file to WAV format for speech recognition."""
        try:
            # Log the input file details
            logger.info(f"Converting file: {input_file}")
            logger.info(f"File exists: {os.path.exists(input_file)}")
            
            # Read the audio file
            audio = AudioSegment.from_file(input_file, format='webm')
            
            # Create temporary WAV file
            wav_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False).name
            logger.info(f"Converting to WAV: {wav_file}")
            
            # Export to WAV format
            audio.export(wav_file, format='wav')
            logger.info("Conversion successful")
            
            return wav_file
        except Exception as e:
            logger.error(f"Error converting audio: {str(e)}")
            raise Exception(f"Error converting audio: {str(e)}")

    def speech_to_text(self, audio_file: str) -> str:
        """Convert speech to text with improved error handling and audio processing."""
        wav_file = None
        try:
            logger.info(f"Processing audio file: {audio_file}")
            
            # Convert to WAV if needed
            file_ext = os.path.splitext(audio_file)[1].lower()
            if file_ext != '.wav':
                wav_file = self._convert_to_wav(audio_file)
            else:
                wav_file = audio_file

            logger.info(f"Using WAV file: {wav_file}")

            with sr.AudioFile(wav_file) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source)
                # Record audio with higher timeout
                audio = self.recognizer.record(source)
                
                # Try multiple recognition services
                try:
                    text = self.recognizer.recognize_google(audio)
                    logger.info("Successfully transcribed audio")
                    return text
                except sr.UnknownValueError:
                    logger.error("Could not understand audio")
                    raise Exception("Could not understand audio")
                except sr.RequestError as e:
                    logger.error(f"Speech recognition service error: {str(e)}")
                    raise Exception("Speech recognition service unavailable")
        except Exception as e:
            logger.error(f"Error in speech recognition: {str(e)}")
            raise Exception(f"Error in speech recognition: {str(e)}")
        finally:
            # Cleanup temporary files
            if wav_file and wav_file != audio_file:
                try:
                    os.unlink(wav_file)
                    logger.info(f"Cleaned up temporary file: {wav_file}")
                except Exception as e:
                    logger.error(f"Error cleaning up file: {str(e)}")

    def text_to_speech(self, text: str) -> str:
        """Convert text to speech with improved quality and error handling."""
        try:
            # Create a temporary file with a unique name
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                tts = gTTS(text=text, lang='en', slow=False)
                tts.save(fp.name)
                return fp.name
        except Exception as e:
            logger.error(f"Error in text to speech conversion: {str(e)}")
            raise Exception(f"Error in text to speech conversion: {str(e)}")

speech_service = SpeechService()