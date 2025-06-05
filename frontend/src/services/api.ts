import { Model, Message } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || '';
const WS_BASE_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8000';

export const ChatService = {
  async getModels(): Promise<Model[]> {
    const response = await fetch(`${API_BASE_URL}/api/models`);
    return response.json();
  },

  async sendMessage(modelId: string, messages: Message[]): Promise<string> {
    const response = await fetch(`${API_BASE_URL}/api/chat/completions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        model_id: modelId, 
        messages: messages.map(m => ({ 
          role: m.role, 
          content: m.content 
        })) 
      })
    });
    const data = await response.json();
    return data.message;
  },

  connectWebSocket(
    onMessage: (chunk: string) => void,
    onComplete: () => void
  ): WebSocket {
    const ws = new WebSocket(`${WS_BASE_URL}/api/chat/stream`);
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'chunk') {
        onMessage(data.content);
      } else if (data.type === 'done') {
        onComplete();
      }
    };
    
    return ws;
  }
};
