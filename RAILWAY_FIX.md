# Railway Deployment Fix - "Error: creating build plan with Railpack"

## Problem
Railway is trying to use Railpack (auto-detection) instead of the Dockerfile.

## Solution: Configure in Railway Dashboard

### Step 1: Delete Current Service
1. Go to your Railway project
2. Click on the failed backend service
3. Go to Settings → Danger Zone
4. Click "Remove Service"

### Step 2: Create New Service with Correct Settings
1. Click "+ New" → "GitHub Repo"
2. Select `Copper369/laughing-waddle`
3. **IMPORTANT**: Configure these settings BEFORE deploying:

#### Service Settings:
- **Service Name**: `backend`
- **Root Directory**: `/backend` or `backend` (try both if one fails)

#### Build Settings (CRITICAL):
1. Go to Settings → Build
2. **Builder**: Select "Dockerfile" from dropdown
3. **Dockerfile Path**: `Dockerfile` (relative to root directory)
4. **Build Command**: Leave empty (Dockerfile handles it)

#### Deploy Settings:
1. Go to Settings → Deploy
2. **Start Command**: `/app/start.sh`
3. **Watch Paths**: `backend/**`

### Step 3: Add Environment Variables
Go to Variables tab and add:

```env
SECRET_KEY=<generate-new>
JWT_SECRET_KEY=<generate-new>
DATABASE_URL=${{Postgres.DATABASE_URL}}
GROQ_API_KEY=<your-groq-key>
FLASK_ENV=production
FRONTEND_URL=http://localhost:3000
UPLOAD_FOLDER=data/photos
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,heic,webp
MAX_CONTENT_LENGTH=104857600
```

### Step 4: Deploy
1. Click "Deploy" or trigger deployment
2. Watch logs for successful build

## Alternative: Use Railway CLI

If dashboard method doesn't work, use Railway CLI:

### Install Railway CLI:
```bash
# Windows (PowerShell)
iwr https://railway.app/install.ps1 | iex

# Mac/Linux
curl -fsSL https://railway.app/install.sh | sh
```

### Deploy via CLI:
```bash
# Login
railway login

# Link to project
railway link

# Set root directory
railway up --service backend --dockerfile backend/Dockerfile
```

## Alternative 2: Simplify Dockerfile Detection

If Railway still can't find the Dockerfile, try this:

### Option A: Move railway.json to root
Currently: `backend/railway.json`
Move to: `railway.json` (root of repo)

Update content:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "backend/Dockerfile"
  },
  "deploy": {
    "startCommand": "/app/start.sh",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Option B: Remove railway.json entirely
Delete `backend/railway.json` and configure everything in Railway dashboard.

## Verification

After deployment, check:
1. Build logs show "Building Dockerfile"
2. No "Railpack" or "Nixpacks" mentioned
3. Python dependencies installing
4. TensorFlow downloading
5. Server starts on port 5000

## Common Issues

### Issue: "Dockerfile not found"
**Fix**: 
- Verify Root Directory is set to `backend`
- Dockerfile path should be just `Dockerfile` (not `backend/Dockerfile`)

### Issue: "Builder not specified"
**Fix**:
- In Settings → Build, explicitly select "Dockerfile" from dropdown
- Don't rely on auto-detection

### Issue: Still using Railpack
**Fix**:
- Delete service completely
- Create new service
- Set builder BEFORE first deployment

## Expected Build Output

You should see:
```
Building Dockerfile...
Step 1/10 : FROM python:3.11-slim
Step 2/10 : WORKDIR /app
...
Successfully built
Starting deployment...
```

NOT:
```
Error: creating build plan with Railpack
```

## Need More Help?

If still failing:
1. Share full build logs
2. Check Railway Status: https://status.railway.app
3. Try Railway Discord: https://discord.gg/railway
4. Check if Dockerfile builds locally:
   ```bash
   cd backend
   docker build -t test-backend .
   docker run -p 5000:5000 test-backend
   ```
