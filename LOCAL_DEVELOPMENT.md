# 🪔 Local Development Guide - DrishyaMitra

## ✅ Project is Running!

### Backend Server
- **URL**: http://localhost:5000
- **Status**: ✅ Running
- **Database**: SQLite (drishyamitra.db)
- **Face Recognition**: ✅ DeepFace loaded successfully

### Frontend Server
- **URL**: http://localhost:3000
- **Status**: ✅ Running
- **API Connection**: http://localhost:5000

## 🚀 Quick Start Commands

### Start Backend
```bash
cd backend
venv/Scripts/python app.py
```

### Start Frontend
```bash
cd frontend
npm run dev
```

## 🛑 Stop Servers

To stop the servers, press `CTRL+C` in each terminal window.

## 📝 Access the Application

1. Open your browser
2. Go to: **http://localhost:3000**
3. Register a new account or login
4. Start uploading photos! 📸

## 🔧 Configuration

### Backend (.env)
- Database: SQLite (local file)
- Upload folder: `data/photos`
- JWT tokens configured
- Groq API for chat feature

### Frontend (.env)
- API URL: http://localhost:5000

## 📂 Project Structure

```
Drishyamitra/
├── backend/          # Flask API server
│   ├── app.py       # Main application
│   ├── models.py    # Database models
│   ├── routes/      # API endpoints
│   └── services/    # Business logic
├── frontend/        # React + Vite
│   ├── src/
│   │   ├── pages/   # All pages with Indian theme
│   │   └── components/
│   └── package.json
└── data/
    └── photos/      # Uploaded photos storage
```

## 🎨 Features

- ✅ Beautiful Indian-themed UI
- ✅ User authentication
- ✅ Photo upload & gallery
- ✅ Face recognition (local only - needs RAM)
- ✅ AI chat assistant
- ✅ People management
- ✅ Photo search & filtering

## 🐛 Troubleshooting

### Backend won't start
- Check if port 5000 is available
- Ensure virtual environment is activated
- Check database file permissions

### Frontend won't start
- Check if port 3000 is available
- Run `npm install` if needed
- Clear browser cache

### Face recognition not working
- This is normal - requires significant RAM
- Photos will upload but faces won't be detected
- All other features work fine

## 📱 Test the Application

1. **Register**: Create a new account at http://localhost:3000/register
2. **Login**: Sign in with your credentials
3. **Upload**: Go to Gallery and upload some photos
4. **Explore**: Check out the Dashboard, People, and Chat features

## 🙏 Enjoy DrishyaMitra!

Your traditional photo management system is ready to use locally.
