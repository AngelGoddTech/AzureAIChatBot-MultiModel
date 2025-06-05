# Architecture Overview

This document describes the architecture of the Azure AI Chatbot application.

## Components

1. **Frontend**: React application with TypeScript
2. **Backend**: FastAPI Python application
3. **AI Services**: Azure OpenAI and Azure AI Foundry
4. **Infrastructure**: Azure Web App Services

## Data Flow

1. User sends message through React UI
2. WebSocket connection streams to FastAPI backend
3. Backend calls appropriate Azure AI service
4. Response streams back through WebSocket
5. UI updates in real-time
