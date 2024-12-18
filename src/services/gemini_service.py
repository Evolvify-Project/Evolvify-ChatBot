import google.generativeai as genai
from config import settings

class GeminiService:
    def __init__(self):
        self.api_keys = settings.GOOGLE_API_KEYS.split()
        self.current_key_index = 0
        self._initialize_client()

    def _initialize_client(self):
        genai.configure(api_key=self.api_keys[self.current_key_index])
        self.model = genai.GenerativeModel(settings.MODEL_NAME)
        self.chat = self.model.start_chat(history=[])

    def _rotate_api_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        self._initialize_client()

    async def get_response(self, message: str) -> str:
        try:
            response = await self.chat.send_message_async(message)
            return response.text
        except Exception as e:
            if "quota exceeded" in str(e).lower():
                self._rotate_api_key()
                return await self.get_response(message)
            raise e

gemini_service = GeminiService()