# Railway Deployment Checklist

## ✅ Pre-Deployment Verification

### Repository Status
- [x] Code pushed to GitHub: `Copper369/laughing-waddle`
- [x] No secrets in git history
- [x] .gitignore properly configured
- [x] All sensitive files excluded

### Backend Files Ready
- [x] `backend/Dockerfile` - Container configuration
- [x] `backend/requirements.txt` - Python dependencies
- [x] `backend/railway.json` - Railway configuration
- [x] `backend/start.sh` - Startup script
- [x] `backend/app.py` - Main application
- [x] `backend/config.py` - Configuration with PostgreSQL fix
- [x] `backend/.env.example` - Environment template
- [x] CORS configured for dynamic frontend URL

### Frontend Files Ready
- [x] `frontend/Dockerfile` - Container configuration
- [x] `frontend/package.json` - Node dependencies
- [x] `frontend/nginx.conf` - Web server config
- [x] `frontend/.env.example` - Environment template

## 🚀 Railway Deployment Steps

### Step 1: Create Railway Project
1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose: `Copper369/laughing-waddle`

### Step 2: Add PostgreSQL Database
1. In project, click "+ New"
2. Select "Database" → "Add PostgreSQL"
3. Wait for database to provision
4. Note: `DATABASE_URL` variable is auto-created

### Step 3: Deploy Backend Service

#### Create Backend Service:
1. Click "+ New" → "GitHub Repo"
2. Select `Copper369/laughing-waddle`
3. Configure:
   - **Service Name**: `backend`
   - **Root Directory**: `/backend`
   - **Builder**: Dockerfile (auto-detected)

#### Add Backend Environment Variables:
Go to backend service → Variables tab → Raw Editor:

```env
SECRET_KEY=<generate-with-command-below>
JWT_SECRET_KEY=<generate-with-command-below>
DATABASE_URL=${{Postgres.DATABASE_URL}}
GROQ_API_KEY=<get-from-groq-console>
FLASK_ENV=production
FRONTEND_URL=${{frontend.RAILWAY_PUBLIC_DOMAIN}}
UPLOAD_FOLDER=data/photos
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,heic,webp
MAX_CONTENT_LENGTH=104857600
```

#### Generate Secrets (run locally):
```bash
# For SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# For JWT_SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Get Groq API Key:
1. Visit https://console.groq.com
2. Sign up (free tier available)
3. Navigate to "API Keys"
4. Click "Create API Key"
5. Copy the key (starts with `gsk_`)

### Step 4: Deploy Frontend Service

#### Create Frontend Service:
1. Click "+ New" → "GitHub Repo"
2. Select `Copper369/laughing-waddle`
3. Configure:
   - **Service Name**: `frontend`
   - **Root Directory**: `/frontend`
   - **Builder**: Dockerfile (auto-detected)

#### Add Frontend Environment Variables:
Go to frontend service → Variables tab:

```env
VITE_API_URL=https://${{backend.RAILWAY_PUBLIC_DOMAIN}}
```

Or use the actual backend URL:
```env
VITE_API_URL=https://backend-production-xxxx.up.railway.app
```

### Step 5: Generate Public Domains
1. Click on backend service → Settings → Networking
2. Click "Generate Domain" (gets a Railway subdomain)
3. Copy the backend URL
4. Click on frontend service → Settings → Networking
5. Click "Generate Domain"
6. Update frontend's `VITE_API_URL` if needed

### Step 6: Monitor Deployment
1. Check backend logs for successful startup
2. Check frontend logs for build completion
3. Visit backend URL: should show API info
4. Visit frontend URL: should show login page

## 🔍 Verification Steps

### Backend Health Check
Visit: `https://your-backend-url.railway.app/`

Expected response:
```json
{
  "message": "Drishyamitra API",
  "version": "1.0.0",
  "status": "running",
  "endpoints": {...}
}
```

### Database Connection
Check backend logs for:
```
Starting application on port 5000
```

No database connection errors.

### Frontend Connection
1. Visit frontend URL
2. Should see login page
3. Open browser console (F12)
4. Check for CORS errors (should be none)

## 🐛 Common Issues & Fixes

### Issue: Build Fails - Out of Memory
**Solution**: 
- Upgrade Railway plan to at least 4GB RAM
- TensorFlow requires significant memory

### Issue: Backend Won't Start
**Check**:
- All environment variables are set
- DATABASE_URL is correct
- GROQ_API_KEY is valid
- Check logs for Python errors

### Issue: Frontend Can't Connect to Backend
**Check**:
- VITE_API_URL points to correct backend URL
- Backend CORS includes frontend URL
- Both services are running

### Issue: Database Connection Error
**Check**:
- PostgreSQL service is running
- DATABASE_URL variable is set
- Config.py has postgres:// → postgresql:// fix

### Issue: 502 Bad Gateway
**Check**:
- Backend is listening on correct port
- start.sh uses $PORT variable
- Gunicorn is running

## 📊 Expected Build Times

- **Backend First Build**: 8-12 minutes (TensorFlow is large)
- **Frontend First Build**: 3-5 minutes
- **Subsequent Builds**: 2-4 minutes (cached layers)

## 💰 Cost Estimate

Railway pricing (as of 2024):
- **Hobby Plan**: $5/month (includes $5 credit)
- **Backend**: ~$15-20/month (needs 4GB RAM)
- **Frontend**: ~$5/month
- **PostgreSQL**: ~$5-10/month
- **Total**: ~$25-35/month

First $5 is free!

## 🎯 Post-Deployment Tasks

### Test Core Features:
- [ ] User registration
- [ ] User login
- [ ] Photo upload
- [ ] Face detection
- [ ] Face labeling
- [ ] Photo search
- [ ] AI chat
- [ ] Email delivery (if configured)

### Optional Enhancements:
- [ ] Add custom domain
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Add SSL certificate (auto with Railway)
- [ ] Set up CI/CD (auto with Railway)

## 📞 Support Resources

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Project Issues: https://github.com/Copper369/laughing-waddle/issues
- Railway Status: https://status.railway.app

## 🎉 Success Criteria

Your deployment is successful when:
- ✅ Backend responds at `/` endpoint
- ✅ Frontend loads login page
- ✅ Can register new user
- ✅ Can login
- ✅ Can upload photos
- ✅ Face detection works
- ✅ AI chat responds
- ✅ No CORS errors in console

---

**Note**: Railway auto-deploys on every push to main branch!
