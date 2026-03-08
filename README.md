# 📸 DrishyaMitra - AI-Powered Photo Management System

An intelligent photo management system with face recognition, AI-powered search, and smart delivery features.

## ✨ Features

- 🔐 **User Authentication** - Secure JWT-based authentication
- 📤 **Photo Upload & Management** - Upload, organize, and manage your photos
- 🤖 **Face Recognition** - Automatic face detection and recognition using DeepFace
- 👥 **People Management** - Label and organize photos by people
- 💬 **AI Chat** - Natural language photo search powered by Groq AI
- 📧 **Smart Delivery** - Send photos via email using Gmail API
- 🔍 **Advanced Search** - Search by date, people, and natural language queries
- 📊 **Dashboard** - Overview of your photo collection

## 🚀 Quick Start

### Prerequisites
- Python 3.12
- Node.js 18+
- PostgreSQL 12+ (production) or SQLite (development)
- Docker & Docker Compose (optional)

### Option 1: Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/Copper369/laughing-waddle.git
cd laughing-waddle

# Configure environment
cd backend
cp .env.example .env
# Edit .env with your API keys

# Start services
cd ../deployment
docker-compose up -d

# Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
```

### Option 2: Manual Setup

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Run backend
python app.py
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with backend URL

# Run development server
npm run dev

# Or build for production
npm run build
```

## 📚 Documentation

- [Setup Guide](docs/SETUP_GUIDE.md) - Detailed local setup instructions
- [Docker Setup](docs/DOCKER_SETUP.md) - Docker deployment guide
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) - Production deployment instructions
- [Project Structure](docs/PROJECT_STRUCTURE.md) - Codebase organization
- [Pre-Deployment Checklist](docs/PRE_DEPLOYMENT_CHECKLIST.md) - Before you deploy
- [Quick Start](docs/QUICK_START.md) - Get started quickly

## 🛠️ Technology Stack

### Backend
- Flask 3.0 - Web framework
- SQLAlchemy - ORM
- DeepFace + TensorFlow - Face recognition
- Groq API - AI chat
- Gmail API - Email delivery
- PostgreSQL - Database (production)

### Frontend
- React 18 - UI framework
- Vite - Build tool
- Tailwind CSS - Styling
- Axios - HTTP client
- React Router - Routing

### DevOps
- Docker & Docker Compose
- Nginx - Web server
- PostgreSQL 16 - Database

## 🔑 Required API Keys

1. **Groq API** (Required for chat feature)
   - Sign up: https://console.groq.com
   - Get API key from dashboard
   - Add to backend/.env as `GROQ_API_KEY`

2. **Gmail API** (Optional, for email delivery)
   - Enable Gmail API in Google Cloud Console
   - Create OAuth credentials
   - Run `python get_gmail_token.py` to get refresh token
   - Add credentials to backend/.env

## 📦 Project Structure

```
DrishyaMitra/
├── backend/          # Flask API server
├── frontend/         # React frontend
├── scripts/          # Utility scripts
├── deployment/       # Deployment files
├── docs/            # Documentation
└── Data-shots/      # Sample photos
```

See [Project Structure](docs/PROJECT_STRUCTURE.md) for detailed breakdown.

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/

# Frontend build test
cd frontend
npm run build
```

## 🚀 Deployment

### Recommended Platforms
1. **Railway** - Easiest for ML projects (Recommended)
2. **Render** - Good free tier
3. **DigitalOcean** - Predictable pricing
4. **AWS** - Most scalable
5. **VPS** - Most control

See [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) for detailed instructions.

### Pre-Deployment Checklist
- [ ] Generate production secrets
- [ ] Configure PostgreSQL database
- [ ] Set up API keys (Groq, Gmail)
- [ ] Configure file storage
- [ ] Enable HTTPS
- [ ] Set up monitoring

See [Pre-Deployment Checklist](docs/PRE_DEPLOYMENT_CHECKLIST.md) for complete list.

## 🔒 Security

- JWT-based authentication
- Password hashing with Werkzeug
- CORS protection
- Environment variable management
- SQL injection prevention (SQLAlchemy)
- XSS prevention (React)

## 📊 System Requirements

### Development
- RAM: 2GB minimum
- Storage: 5GB
- CPU: 2 cores

### Production
- RAM: 4GB+ recommended (TensorFlow is memory-intensive)
- Storage: 10GB+ (models + photos)
- CPU: 2+ cores
- Database: PostgreSQL 12+

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Known Issues

- TensorFlow requires significant RAM (2GB+)
- Face recognition can be slow on CPU-only systems
- Gmail API requires OAuth setup

## 🔮 Future Enhancements

- [ ] WhatsApp delivery integration
- [ ] Video support
- [ ] Mobile app
- [ ] Cloud storage integration (S3, Cloudinary)
- [ ] Advanced face clustering
- [ ] Photo editing features
- [ ] Shared albums
- [ ] Timeline view

## 📞 Support

- GitHub Issues: [Report a bug](https://github.com/Copper369/laughing-waddle/issues)
- Documentation: See `docs/` folder

## 🙏 Acknowledgments

- DeepFace for face recognition
- Groq for AI chat capabilities
- Flask and React communities
- All contributors

---

**Made with ❤️ by Ayush Karnewar**

⭐ Star this repo if you find it helpful!
