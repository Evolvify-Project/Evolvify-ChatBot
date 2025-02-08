import { useState, useRef, useEffect } from 'react';
import { ChatMessage } from './components/ChatMessage';
import { ChatInput } from './components/ChatInput';
import { useVoiceRecording } from './hooks/useVoiceRecording';
import { sendMessage, sendVoiceMessage } from './services/api';
import type { Message } from './types/chat';

function App() {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Hello! How can I help you today?' }
  ]);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const { isRecording, startRecording, stopRecording, getAudioBlob } = useVoiceRecording();

  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (content: string, isVoice = false) => {
    if (!content.trim()) return;

    setIsLoading(true);
    // Add user message
    const userMessage: Message = { role: 'user', content, isVoice };
    setMessages(prev => [...prev, userMessage]);

    try {
      // Get bot response
      const response = await sendMessage(content);
      
      // Add bot message
      const botMessage: Message = { role: 'assistant', content: response.message };
      setMessages(prev => [...prev, botMessage]);

      // If it was a voice message, speak the response
      if (isVoice && !isSpeaking) {
        setIsSpeaking(true);
        // The backend will handle TTS and return audio
        // You can play it here using the Audio API
        setIsSpeaking(false);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please try again.' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleVoiceMessage = async () => {
    const audioBlob = await getAudioBlob();
    if (audioBlob) {
      try {
        const response = await sendVoiceMessage(audioBlob);
        handleSendMessage(response.transcription, true);
      } catch (error) {
        console.error('Error sending voice message:', error);
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: 'Sorry, I had trouble processing your voice message. Please try again.' 
        }]);
      }
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <header className="bg-white border-b p-4 shadow-sm">
        <h1 className="text-xl font-semibold text-gray-800">Evolvify Chat</h1>
      </header>

      <main className="flex-1 overflow-hidden">
        <div 
          ref={chatContainerRef}
          className="h-full overflow-y-auto px-4 py-6 space-y-4"
        >
          {messages.map((message, index) => (
            <ChatMessage 
              key={index} 
              message={message} 
            />
          ))}
          {isLoading && (
            <div className="flex justify-center">
              <div className="animate-pulse text-gray-500">Thinking...</div>
            </div>
          )}
        </div>
      </main>

      <ChatInput
        onSendMessage={handleSendMessage}
        isRecording={isRecording}
        onStartRecording={startRecording}
        onStopRecording={() => {
          stopRecording();
          handleVoiceMessage();
        }}
      />
    </div>
  );
}

export default App;