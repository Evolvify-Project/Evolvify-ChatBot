import React, { useState, useRef } from 'react';
import { Mic, Send, Square } from 'lucide-react';

interface ChatInputProps {
  onSendMessage: (message: string, isVoice?: boolean) => void;
  isRecording: boolean;
  onStartRecording: () => void;
  onStopRecording: () => void;
}

export const ChatInput: React.FC<ChatInputProps> = ({
  onSendMessage,
  isRecording,
  onStartRecording,
  onStopRecording,
}) => {
  const [message, setMessage] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      onSendMessage(message);
      setMessage('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-2 p-4 border-t bg-white">
      <input
        ref={inputRef}
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Type your message..."
        className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        disabled={isRecording}
      />
      <button
        type="button"
        onClick={isRecording ? onStopRecording : onStartRecording}
        className={`p-2 rounded-full transition-colors ${
          isRecording 
            ? 'bg-red-100 text-red-600 hover:bg-red-200' 
            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
        }`}
      >
        {isRecording ? <Square size={20} /> : <Mic size={20} />}
      </button>
      <button
        type="submit"
        disabled={!message.trim() || isRecording}
        className="p-2 rounded-full bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <Send size={20} />
      </button>
    </form>
  );
}