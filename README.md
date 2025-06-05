# AzureAIChatBot-MultiModel

A production-ready multi-model AI chatbot powered by Azure AI Foundry and Azure OpenAI, deployed on Azure Web App Services.

![Azure Architecture](https://img.shields.io/badge/Azure-0089D0?style=for-the-badge&logo=microsoft-azure&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)

## 🌟 Features

- **Multi-Model Support**: Seamlessly switch between GPT-4, GPT-3.5 Turbo, and custom Azure AI models
- **Real-time Streaming**: WebSocket-based streaming for responsive conversations
- **Scalable Architecture**: Built for Azure Web App Services with horizontal scaling
- **Modern UI**: React-based interface with TypeScript and Tailwind CSS
- **Production Ready**: Includes monitoring, logging, error handling, and security best practices

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Azure Web App Service                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐         ┌─────────────────────────┐   │
│  │   React Frontend │         │   FastAPI Backend       │   │
│  │   (TypeScript)   │ <────> │   (Python 3.11)         │   │
│  └─────────────────┘         └──────────┬──────────────┘   │
│                                         │                    │
└─────────────────────────────────────────┼───────────────────┘
                                         │
                              ┌──────────┴──────────┐
                              │ Azure AI Services   │
                              │ - GPT-4            │
                              │ - GPT-3.5 Turbo    │
                              │ - Custom Models    │
                              └────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker Desktop
- Azure CLI
- Azure subscription with AI services

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/AzureAIChatBot-MultiModel.git
   cd AzureAIChatBot-MultiModel
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your Azure credentials
   uvicorn app.main:app --reload
   ```

3. **Set up the frontend**
   ```bash
   cd ../frontend
   npm install
   cp .env.example .env.local
   # Edit .env.local with your API endpoint
   npm start
   ```

4. **Run with Docker Compose**
   ```bash
   docker-compose -f docker-compose.dev.yml up
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 📦 Deployment

### Azure Web App Deployment

1. Set up Azure resources:
   ```bash
   az webapp create --name your-chatbot-app --resource-group your-rg --plan your-plan
   ```

2. Configure GitHub Actions secrets in your repository

3. Push to main branch to trigger automatic deployment

### Environment Variables

See `.env.example` files in both backend and frontend directories for required configuration.

## 🧪 Testing

```bash
# Backend tests
cd backend && pytest

# Frontend tests
cd frontend && npm test

# E2E tests
npm run test:e2e
```

## 📖 Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [API Documentation](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Contributing Guidelines](docs/CONTRIBUTING.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔒 Security

For security concerns, please review our [Security Policy](SECURITY.md).

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Azure AI Team for the excellent AI services
- FastAPI community for the amazing framework
- React team for the powerful frontend library
