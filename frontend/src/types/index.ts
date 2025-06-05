export interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface Model {
  id: string;
  name: string;
  type: string;
  description: string;
  capabilities: string[];
}
