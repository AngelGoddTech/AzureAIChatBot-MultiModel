from fastapi import FastAPI, WebSocket, HTTPException, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, AsyncGenerator
from datetime import datetime
import json
import asyncio
import os
from openai import AsyncAzureOpenAI
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model_id: str
    messages: List[Message]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000
    stream: Optional[bool] = True

class ChatResponse(BaseModel):
    model_id: str
    message: str
    timestamp: datetime = datetime.now()

class ModelInfo(BaseModel):
    id: str
    name: str
    type: str
    description: str
    capabilities: List[str] = []

# Configuration
class Settings:
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY", "")
    AZURE_OPENAI_API_VERSION = "2024-02-01"
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    
    AVAILABLE_MODELS = {
        "gpt-4": {
            "name": "GPT-4",
            "type": "openai",
            "description": "Most capable GPT-4 model for complex tasks",
            "capabilities": ["chat", "reasoning", "code", "analysis"]
        },
        "gpt-35-turbo": {
            "name": "GPT-3.5 Turbo",
            "type": "openai",
            "description": "Fast and efficient for most tasks",
            "capabilities": ["chat", "reasoning", "code"]
        }
    }

settings = Settings()

# Initialize FastAPI app
app = FastAPI(
    title="Azure Multi-Model Chatbot API",
    version="1.0.0",
    description="API for chatbot supporting multiple Azure AI models"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Azure AI Service
class AzureAIService:
    def __init__(self):
        if settings.AZURE_OPENAI_KEY and settings.AZURE_OPENAI_ENDPOINT:
            self.openai_client = AsyncAzureOpenAI(
                api_key=settings.AZURE_OPENAI_KEY,
                api_version=settings.AZURE_OPENAI_API_VERSION,
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
            )
        else:
            self.openai_client = None
            logger.warning("Azure OpenAI credentials not configured")
    
    async def chat_completion_stream(
        self, 
        model_id: str, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> AsyncGenerator[str, None]:
        try:
            if model_id in ["gpt-4", "gpt-35-turbo"] and self.openai_client:
                stream = await self.openai_client.chat.completions.create(
                    model=model_id,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True
                )
                
                async for chunk in stream:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            else:
                # Demo response for when Azure OpenAI is not configured
                response = f"This is a demo response from {model_id}. Configure Azure OpenAI to use real models."
                for word in response.split():
                    yield word + " "
                    await asyncio.sleep(0.05)
                
        except Exception as e:
            logger.error(f"Error in chat completion: {str(e)}")
            yield f"Error: {str(e)}"

# Initialize AI service
ai_service = AzureAIService()

# Connection manager for WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_json(self, websocket: WebSocket, data: dict):
        await websocket.send_json(data)

manager = ConnectionManager()

# Routes
@app.get("/")
async def root():
    return {
        "message": "Azure Multi-Model Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "models": "/api/models",
            "chat": "/api/chat/completions",
            "websocket": "/api/chat/stream"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "chatbot-api"
    }

@app.get("/api/models", response_model=List[ModelInfo])
async def get_available_models():
    models = []
    for model_id, info in settings.AVAILABLE_MODELS.items():
        models.append(ModelInfo(
            id=model_id,
            name=info["name"],
            type=info["type"],
            description=info["description"],
            capabilities=info["capabilities"]
        ))
    return models

@app.post("/api/chat/completions", response_model=ChatResponse)
async def create_chat_completion(request: ChatRequest):
    try:
        messages = [msg.dict() for msg in request.messages]
        response = ""
        
        async for chunk in ai_service.chat_completion_stream(
            model_id=request.model_id,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        ):
            response += chunk
        
        return ChatResponse(
            model_id=request.model_id,
            message=response
        )
        
    except Exception as e:
        logger.error(f"Error in chat completion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/api/chat/stream")
async def websocket_chat_stream(websocket: WebSocket):
    await manager.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            request_data = json.loads(data)
            
            logger.info(f"Received request for model: {request_data.get('model_id')}")
            
            try:
                async for chunk in ai_service.chat_completion_stream(
                    model_id=request_data["model_id"],
                    messages=request_data["messages"],
                    temperature=request_data.get("temperature", 0.7),
                    max_tokens=request_data.get("max_tokens", 1000)
                ):
                    await manager.send_json(websocket, {
                        "type": "chunk",
                        "content": chunk
                    })
                
                await manager.send_json(websocket, {
                    "type": "done"
                })
                
            except Exception as e:
                logger.error(f"Error during streaming: {str(e)}")
                await manager.send_json(websocket, {
                    "type": "error",
                    "message": str(e)
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
