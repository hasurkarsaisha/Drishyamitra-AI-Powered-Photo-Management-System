# DrishyaMitra Deployment Guide

## 🚨 Pre-Deployment Checklist

### Critical Things to Remember

1. **This is a Complex Project** - You have:
   - ML models (TensorFlow, DeepFace) - ~500MB+ dependencies
   - Face recognition with embeddings storage
   - Image processing and storage
   - Real-time chat with Groq API
   - Email delivery with Gmail API
   - PostgreSQL database
   - React frontend with Vite

2. **Security First**:
   - ✅ Never commit `.env` files (already in .gitignore)
   - ✅ Generate new SECRET_KEY and JWT_SECRET_KEY for production
   - ✅ Use strong database passwords
   - ✅ Keep API keys secure (Groq, Gmail)
   - ✅ Enable HTTPS in production
   - ✅ Set CORS properly for your domain

3. **Resource Requirements**:
   - **RAM**: Minimum 2GB, Recommended 4GB+ (TensorFlow is memory-hungry)
   - **Storage**: 5GB+ (models, dependencies, photos)
   - **CPU**: 2+ cores recommended for face recognition
   - **Database**: PostgreSQL 12+ (SQLite only for development)

4. **Environment Variables** - Must configure:
   ```
   SECRET_KEY=<generate-new-one>
   JWT_SECRET_KEY=<generate-new-one>
   DATABASE_URL=postgresql://user:pass@host:5432/dbname
   GROQ_API_KEY=<your-groq-key>
   GMAIL_CLIENT_ID=<optional-for-email>
   GMAIL_CLIENT_SECRET=<optional-for-email>
   GMAIL_REFRESH_TOKEN=<optional-for-email>
   ```

5. **File Storage**:
   - Photos stored in `backend/data/photos/`
   - Need persistent volume or object storage (S3, Cloudinary)
   - Face embeddings stored in database

---

## 🎯 Recommended Deployment Platforms

### Option 1: Railway (Easiest for ML Projects) ⭐ RECOMMENDED
**Pros**:
- Handles large Docker images well
- Good for ML/AI projects
- PostgreSQL included
- Simple deployment from GitHub
- Reasonable pricing

**Cons**:
- Can be expensive at scale
- $5/month minimum

**Steps**:
1. Push code to GitHub
2. Connect Railway to your repo
3. Add PostgreSQL service
4. Set environment variables
5. Deploy backend and frontend separately

**Cost**: ~$20-50/month

---

### Option 2: Render (Good Balance)
**Pros**:
- Free tier available
- PostgreSQL included
- Docker support
- Auto-deploy from GitHub

**Cons**:
- Free tier spins down after inactivity
- Slower cold starts with ML models
- 512MB RAM on free tier (not enough for TensorFlow)

**Steps**:
1. Create Web Service for backend (Docker)
2. Create Static Site for frontend
3. Add PostgreSQL database
4. Configure environment variables

**Cost**: Free tier or $7-25/month

---

### Option 3: DigitalOcean App Platform
**Pros**:
- Predictable pricing
- Good performance
- Managed database
- Docker support

**Cons**:
- No free tier
- More expensive than others

**Cost**: ~$30-60/month

---

### Option 4: AWS (Most Scalable, Most Complex)
**Pros**:
- Highly scalable
- Full control
- S3 for photo storage
- RDS for database

**Cons**:
- Complex setup
- Requires DevOps knowledge
- Can be expensive if misconfigured

**Services Needed**:
- ECS/Fargate for containers
- RDS PostgreSQL
- S3 for photos
- CloudFront for frontend
- ALB for load balancing

**Cost**: $50-200+/month

---

### Option 5: Self-Hosted VPS (Most Control)
**Platforms**: DigitalOcean Droplets, Linode, Vultr, Hetzner

**Pros**:
- Full control
- Cost-effective
- Can use Docker Compose directly

**Cons**:
- You manage everything
- Security is your responsibility
- Need to handle backups

**Cost**: $10-40/month

---

## 🐳 Docker Deployment (Recommended Method)

### Prerequisites
```bash
# Install Docker and Docker Compose
# Windows: Docker Desktop
# Linux: docker.io and docker-compose
```

### Deployment Steps

1. **Update Environment Variables**:
```bash
cd backend
cp .env.example .env
# Edit .env with production values
```

2. **Build and Run**:
```bash
cd deployment
docker-compose up -d
```

3. **Check Status**:
```bash
docker-compose ps
docker-compose logs -f backend
```

4. **Initialize Database**:
```bash
docker-compose exec backend python -c "from app import create_app; from models import db; app = create_app(); app.app_context().push(); db.create_all()"
```

---

## 📦 Manual Deployment (Without Docker)

### Backend Setup

1. **Install Python 3.12**:
```bash
python --version  # Should be 3.12.x
```

2. **Create Virtual Environment**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install Dependencies**:
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

4. **Configure Environment**:
```bash
cp .env.example .env
# Edit .env with production values
```

5. **Initialize Database**:
```bash
python -c "from app import create_app; from models import db; app = create_app(); app.app_context().push(); db.create_all()"
```

6. **Run Backend**:
```bash
# Development
python app.py

# Production (use gunicorn)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### Frontend Setup

1. **Install Node.js 18+**:
```bash
node --version  # Should be 18.x or higher
```

2. **Install Dependencies**:
```bash
cd frontend
npm install
```

3. **Configure Environment**:
```bash
cp .env.example .env
# Set VITE_API_URL to your backend URL
```

4. **Build for Production**:
```bash
npm run build
```

5. **Serve Frontend**:
```bash
# Option 1: Using serve
npm install -g serve
serve -s dist -p 3000

# Option 2: Using nginx (recommended)
# Copy dist/ contents to /var/www/html
```

---

## 🗄️ Database Migration

### From SQLite to PostgreSQL

1. **Export SQLite Data**:
```bash
cd backend
python scripts/export_sqlite.py
```

2. **Import to PostgreSQL**:
```bash
python scripts/import_postgres.py
```

3. **Update DATABASE_URL** in `.env`:
```
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

---

## 📸 Photo Storage Solutions

### Option 1: Local Storage (Simple)
- Store in `backend/data/photos/`
- Use Docker volumes for persistence
- Good for small deployments

### Option 2: AWS S3 (Scalable)
- Unlimited storage
- CDN integration
- Need to modify code to use boto3

### Option 3: Cloudinary (Easy)
- Image optimization included
- Free tier: 25GB storage
- Simple API integration

---

## 🔒 Production Security Checklist

- [ ] Generate new SECRET_KEY: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- [ ] Generate new JWT_SECRET_KEY
- [ ] Use strong database password
- [ ] Enable HTTPS (Let's Encrypt)
- [ ] Set proper CORS origins
- [ ] Disable Flask debug mode
- [ ] Set up database backups
- [ ] Configure rate limiting
- [ ] Set up monitoring (Sentry, LogRocket)
- [ ] Enable firewall rules
- [ ] Regular security updates

---

## 🚀 Quick Deploy Commands

### Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Render
```bash
# Connect GitHub repo in Render dashboard
# Add render.yaml for configuration
```

### Docker Compose (VPS)
```bash
# Clone repo on server
git clone https://github.com/Copper369/laughing-waddle.git
cd laughing-waddle/deployment

# Configure environment
cd ../backend
cp .env.example .env
nano .env  # Edit with production values

# Deploy
cd ../deployment
docker-compose up -d
```

---

## 📊 Monitoring & Maintenance

### Health Checks
```bash
# Backend health
curl http://your-domain.com/

# Database connection
docker-compose exec backend python -c "from models import db; from app import create_app; app = create_app(); app.app_context().push(); print('DB OK' if db.engine.connect() else 'DB FAIL')"
```

### Logs
```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Application logs
tail -f backend/app.log
```

### Backups
```bash
# Database backup
docker-compose exec postgres pg_dump -U postgres drishyamitra > backup_$(date +%Y%m%d).sql

# Photo backup
tar -czf photos_backup_$(date +%Y%m%d).tar.gz backend/data/photos/
```

---

## 🆘 Troubleshooting

### TensorFlow Issues
- Ensure 2GB+ RAM available
- Use tensorflow-cpu if no GPU
- Check Python version compatibility (3.12)

### Face Recognition Slow
- Increase worker processes
- Use GPU if available
- Consider caching embeddings

### Database Connection Errors
- Check DATABASE_URL format
- Verify PostgreSQL is running
- Check firewall rules

### Photo Upload Fails
- Check UPLOAD_FOLDER permissions
- Verify MAX_CONTENT_LENGTH setting
- Check disk space

---

## 📞 Support

- GitHub Issues: https://github.com/Copper369/laughing-waddle/issues
- Documentation: See docs/ folder

---

**Remember**: Start with Railway or Render for easiest deployment. Move to AWS/VPS when you need more control or scale.
