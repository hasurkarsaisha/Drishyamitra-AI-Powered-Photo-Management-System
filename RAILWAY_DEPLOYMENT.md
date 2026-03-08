# 🚂 Railway Deployment Guide - Quick Setup

## Step 1: Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub
3. Authorize Railway to access your repositories

## Step 2: Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose: `Copper369/laughing-waddle`
4. Railway will detect your repository

## Step 3: Add PostgreSQL Database
1. In your project, click "New"
2. Select "Database" → "Add PostgreSQL"
3. Database will be created automatically
4. Note: Railway will create a `DATABASE_URL` variable

## Step 4: Deploy Backend Service

### Configure Backend:
1. Click "New" → "GitHub Repo" → Select your repo again
2. Settings to configure:
   - **Service Name**: `backend`
   - **Root Directory**: `backend`
   - **Builder**: Dockerfile (auto-detected)

### Add Environment Variables:
Click on backend service → Variables → Add these:

```
SECRET_KEY=<generate-new-one>
JWT_SECRET_KEY=<generate-new-one>
DATABASE_URL=${{Postgres.DATABASE_URL}}
GROQ_API_KEY=<your-groq-api-key>
FLASK_ENV=production
UPLOAD_FOLDER=data/photos
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,heic,webp
MAX_CONTENT_LENGTH=16777216
```

### Generate Secrets (Run on your computer):
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
Run this twice - once for SECRET_KEY, once for JWT_SECRET_KEY

### Get Groq API Key:
1. Go to https://console.groq.com
2. Sign up (free)
3. Go to "API Keys"
4. Create new key
5. Copy and paste as GROQ_API_KEY

## Step 5: Deploy Frontend Service

### Configure Frontend:
1. Click "New" → "GitHub Repo" → Select your repo again
2. Settings to configure:
   - **Service Name**: `frontend`
   - **Root Directory**: `frontend`
   - **Builder**: Dockerfile (auto-detected)

### Add Environment Variable:
Click on frontend service → Variables → Add:

```
VITE_API_URL=https://backend-production-xxxx.up.railway.app
```

**Important**: Replace with your actual backend URL from Railway
- Find it in: Backend service → Settings → Domains
- Copy the Railway-provided domain

## Step 6: Deploy!
1. Both services will start building automatically
2. Wait 5-10 minutes for first build (TensorFlow is large)
3. Check logs for any errors

## Step 7: Add Custom Domain (Optional)
1. Click on frontend service
2. Go to Settings → Domains
3. Click "Generate Domain" for free Railway domain
4. Or add your custom domain

## 🎯 What Files Railway Needs

Railway automatically uses these files from your repo:

### Backend:
- ✅ `backend/Dockerfile` - Builds the backend container
- ✅ `backend/requirements.txt` - Python dependencies
- ✅ `backend/app.py` - Main application
- ✅ `backend/.env.example` - Template (you add real values in Railway)

### Frontend:
- ✅ `frontend/Dockerfile` - Builds the frontend container
- ✅ `frontend/package.json` - Node dependencies
- ✅ `frontend/nginx.conf` - Web server config
- ✅ `frontend/.env.example` - Template (you add real values in Railway)

### You DON'T need to upload:
- ❌ `.env` files (set variables in Railway dashboard)
- ❌ `node_modules/` (Railway installs them)
- ❌ `venv/` (Railway creates it)
- ❌ Database files (Railway provides PostgreSQL)
- ❌ Photos (will be stored in Railway volumes)

## 📋 Environment Variables Checklist

### Backend Variables (Required):
- [ ] SECRET_KEY - Generate new one
- [ ] JWT_SECRET_KEY - Generate new one
- [ ] DATABASE_URL - Use `${{Postgres.DATABASE_URL}}`
- [ ] GROQ_API_KEY - Get from Groq console
- [ ] FLASK_ENV - Set to `production`

### Frontend Variables (Required):
- [ ] VITE_API_URL - Your backend Railway URL

### Optional (for email delivery):
- [ ] GMAIL_CLIENT_ID
- [ ] GMAIL_CLIENT_SECRET
- [ ] GMAIL_REFRESH_TOKEN

## 🔍 How to Check if It's Working

### Backend Health Check:
Visit: `https://your-backend-url.railway.app/`

Should return:
```json
{
  "message": "Drishyamitra API",
  "version": "1.0.0",
  "status": "running"
}
```

### Frontend Check:
Visit: `https://your-frontend-url.railway.app/`

Should show the login page

## 🐛 Troubleshooting

### Build Fails:
- Check logs in Railway dashboard
- Verify Dockerfile paths are correct
- Ensure all dependencies in requirements.txt

### Backend Won't Start:
- Check environment variables are set
- Verify DATABASE_URL is correct
- Check logs for Python errors

### Frontend Can't Connect:
- Verify VITE_API_URL points to backend
- Check CORS settings
- Ensure backend is running

### Out of Memory:
- Upgrade Railway plan (need 4GB+ RAM)
- TensorFlow needs significant memory

## 💰 Cost Estimate

Railway charges based on usage:

- **Starter Plan**: $5/month minimum
- **Backend**: ~$15-20/month (needs more resources)
- **Frontend**: ~$5/month
- **PostgreSQL**: ~$5-10/month
- **Total**: ~$25-35/month

First $5 is free credit!

## 🎉 You're Done!

Once deployed:
1. Visit your frontend URL
2. Register a new account
3. Upload photos
4. Test face recognition
5. Try AI chat

## 📞 Need Help?

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Project Issues: https://github.com/Copper369/laughing-waddle/issues

---

**Pro Tip**: Railway auto-deploys on every git push to main branch!
