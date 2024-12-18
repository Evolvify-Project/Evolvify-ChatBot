import axios from 'axios';

const API_URL = 'http://localhost:8000/api';  // Updated API URL to include /api prefix

export const sendMessage = async (message: string) => {
  try {
    const response = await axios.post(`${API_URL}/chat`, { message });
    return response.data;
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
};

export const sendVoiceMessage = async (audioBlob: Blob) => {
  try {
    const formData = new FormData();
    formData.append('audio', audioBlob);
    
    const response = await axios.post(`${API_URL}/speech-to-text`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error sending voice message:', error);
    throw error;
  }
};