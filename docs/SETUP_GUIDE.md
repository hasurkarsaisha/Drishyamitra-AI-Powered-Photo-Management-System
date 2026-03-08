# DrishyaMitra - Setup Guide

## Prerequisites

Before running the application, ensure you have:

1. **Python 3.12** installed
2. **Node.js 18+** and npm installed
3. **PostgreSQL 18** installed (at D:\Postgres)
4. **Git** (for version control)

## Quick Start (Windows)

### Step 1: Start PostgreSQL

PostgreSQL must be running before starting the application.

**Option A: Using the helper script (Recommended)**
```bash
# Right-click and "Run as Administrator"
start_postgres.bat
```

**Option B: Using PowerShell (as Administrator)**
```powershell
Start-Service postgresql-x64-18
```

**Option C: Manual start**
```bash
D:\Postgres\bin\pg_ctl.exe start -D "D:\Postgres\data"
```

### Step 2: Run Initial Setup

This creates the database, installs dependencies, and configures environment files:

```bash
setup.bat
```

This script will:
- Create `.env` files from examples
- Check PostgreSQL status
- Create the `drishyamitra` database
- Install Python dependencies in virtual environment
- Install Node.js dependencies

### Step 3: Configure API Keys (Important!)

Edit `backend/.env` and add your API keys:

```env
# Required for Chat Feature
GROQ_API_KEY=your_groq_api_key_here

# Optional for Email Delivery
GMAIL_CLIENT_ID=your_gmail_client_id
GMAIL_CLIENT_SECRET=your_gmail_client_secret
GMAIL_REFRESH_TOKEN=your_gmail_refresh_token
```

### Step 4: Start the Application

```bash
start.bat
```

This will:
- Verify PostgreSQL is running
- Start the backend server (http://localhost:5000)
- Start the frontend server (http://localhost:3000)
- Open the application in your browser

## Troubleshooting

### PostgreSQL Connection Error

If you see: `connection to server at "localhost" (::1), port 5432 failed`

**Solution:**
1. Check if PostgreSQL is running:
   ```bash
   sc query postgresql-x64-18
   ```
2. Start it if stopped:
   ```bash
   start_postgres.bat  # Run as Administrator
   ```

### TensorFlow/DeepFace Import Error

If you see: `AttributeError: module 'tensorflow' has no attribute '__version__'`

**Solution:**
```bash
cd backend
venv\Scripts\activate
pip uninstall tensorflow tensorflow-intel -y
pip install tensorflow==2.16.2
pip install --upgrade deepface
```

### Database Already Exists

If `setup_postgres.py` says database exists, that's fine! The script will skip creation.

### Port Already in Use

If port 5000 or 3000 is already in use:

**Backend (5000):**
- Edit `backend/app.py` and change the port
- Update `frontend/.env` with new backend URL

**Frontend (3000):**
- Vite will automatically use the next available port

## Manual Setup (Alternative)

If the batch scripts don't work, follow these steps:

### 1. Start PostgreSQL
```bash
net start postgresql-x64-18
```

### 2. Create Database
```bash
python setup_postgres.py
```

### 3. Setup Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### 4. Setup Frontend (in new terminal)
```bash
cd frontend
npm install
npm run dev
```

## Docker Setup (Alternative)

If you prefer Docker:

```bash
docker-compose up --build
```

Note: The docker-compose.yml currently uses SQLite. To use PostgreSQL with Docker, you'll need to add a PostgreSQL service to docker-compose.yml.

## File Structure

```
DrishyaMitra/
├── setup.bat              # Initial setup script
├── start_postgres.bat     # PostgreSQL starter (admin required)
├── start.bat              # Application starter
├── setup_postgres.py      # Database initialization
├── backend/
│   ├── .env              # Backend configuration (create from .env.example)
│   ├── app.py            # Flask application
│   ├── requirements.txt  # Python dependencies
│   └── venv/             # Virtual environment (created by setup)
├── frontend/
│   ├── .env              # Frontend configuration (create from .env.example)
│   ├── package.json      # Node dependencies
│   └── node_modules/     # Dependencies (created by setup)
└── docker-compose.yml    # Docker configuration
```

## Next Steps

After successful setup:

1. Register a new user account
2. Upload photos
3. Label faces for recognition
4. Use the chat feature to search photos
5. Share photos via email delivery

## Getting API Keys

### Groq API (Required for Chat)
1. Visit https://console.groq.com
2. Sign up for free account
3. Go to "API Keys" section
4. Create new API key
5. Copy to `backend/.env`

### Gmail API (Optional for Email Delivery)
1. Visit https://console.cloud.google.com
2. Create new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Run `python get_gmail_token.py` to get refresh token
6. Copy credentials to `backend/.env`

## Support

For issues or questions, check:
- SYSTEM_STATUS.md - Current system status
- FACE_MATCHING_STATUS.md - Face recognition details
- Backend logs in the terminal
- Frontend console in browser DevTools
