# Evolvify Chat

A modern, real-time chat application with voice capabilities powered by React and FastAPI. This application combines text and voice interactions with AI responses using Google's Gemini model.

## ✨ Features

- 💬 Real-time text chat interface
- 🎤 Voice message support
- 🤖 AI-powered responses using Gemini
- 🗣️ Speech-to-text and text-to-speech capabilities
- 📱 Responsive design
- ⚡ Fast and efficient communication

## 🚀 Tech Stack

### Frontend

- React 18
- TypeScript
- Tailwind CSS
- Vite
- Axios
- Lucide Icons

### Backend

- FastAPI
- Python 3.8+
- Google Generative AI
- Speech Recognition
- gTTS (Google Text-to-Speech)

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- Node.js (v18 or higher)
- Python (3.8 or higher)
- pip (Python package manager)
- Google Cloud API key for Gemini
- ffmpeg for audio conversion

## 🛠️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/evolvify-chat.git
   cd evolvify-chat
   ```

2. **Install Frontend Dependencies**

   ```bash
   npm install
   ```

3. **Install Backend Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEYS=your_google_api_key_here
   ```

## 🚀 Running the Application

1. **Start the Backend Server**

   ```bash
   cd src
   python main.py
   ```

   The backend will start on `http://localhost:8000`

2. **Start the Frontend Development Server**
   ```bash
   npm run dev
   ```
   The frontend will start on `http://localhost:5173`

## 🎯 Usage

1. **Text Chat**

   - Type your message in the input field
   - Press Enter or click the Send button
   - Receive AI-powered responses

2. **Voice Messages**
   - Click the microphone icon to start recording
   - Speak your message
   - Click the stop button to send
   - Receive both text and audio responses

## 📚 API Documentation

### Chat Endpoints

#### Send Text Message
```http
POST /api/chat
Content-Type: application/json

{
  "message": "Your message here"
}
```

**Response**
```json
{
  "message": "AI response text"
}
```

### Speech Endpoints

#### Speech to Text
```http
POST /api/speech-to-text
Content-Type: multipart/form-data

Form Data:
- audio: <audio_file>
```

**Response**
```json
{
  "transcription": "Transcribed text from audio"
}
```

#### Text to Speech
```http
POST /api/text-to-speech
Content-Type: application/json

{
  "text": "Text to convert to speech"
}
```

**Response**
- Content-Type: audio/mpeg
- File: speech.mp3

### Error Responses

All endpoints may return the following error response:

```json
{
  "detail": "Error message description"
}
```

Status codes:
- 200: Success
- 400: Bad Request
- 500: Internal Server Error

## 🔧 Project Structure

```
evolvify-chat/
├── src/
│   ├── components/        # React components
│   ├── hooks/            # Custom React hooks
│   ├── services/         # API and service functions
│   ├── types/            # TypeScript type definitions
│   ├── routers/          # FastAPI route handlers
│   └── main.py          # Python backend entry point
├── public/              # Static assets
└── package.json        # Project dependencies
```
