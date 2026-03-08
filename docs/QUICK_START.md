# Quick Start Guide

## Before Running start.bat

You must complete these steps in order:

### 1️⃣ Start PostgreSQL (Run as Administrator)
```bash
start_postgres.bat
```
OR manually:
```bash
net start postgresql-x64-18
```

### 2️⃣ Run Initial Setup
```bash
setup.bat
```
This will:
- Create .env files
- Create PostgreSQL database
- Install all dependencies

### 3️⃣ Configure API Keys
Edit `backend/.env` and add:
```env
GROQ_API_KEY=your_key_here
```

### 4️⃣ Start Application
```bash
start.bat
```

## Files Created

- **setup.bat** - Run this ONCE for initial setup
- **start_postgres.bat** - Start PostgreSQL (needs admin)
- **start.bat** - Start the application (run this every time)
- **setup_postgres.py** - Database initialization script

## Troubleshooting

**PostgreSQL not running?**
→ Run `start_postgres.bat` as Administrator

**Database connection error?**
→ Run `python setup_postgres.py`

**Missing dependencies?**
→ Run `setup.bat` again

**TensorFlow errors?**
→ Already fixed in backend/services/face_recognition.py
→ Dependencies updated in backend/requirements.txt
