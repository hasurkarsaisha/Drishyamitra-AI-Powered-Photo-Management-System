# 🚀 Vercel Frontend Deployment Guide

## Why Vercel for Frontend?
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Perfect for React/Vite apps
- ✅ Auto-deploys on git push
- ✅ Much faster than Railway for static sites

## Prerequisites
1. ✅ Backend deployed on Railway (get the URL)
2. ✅ Code pushed to GitHub: `Copper369/laughing-waddle`
3. ✅ Vercel account (sign up with GitHub)

## Step-by-Step Deployment

### Step 1: Get Your Backend URL
From Railway:
1. Go to your backend service
2. Settings → Networking
3. Generate Domain (port 5000)
4. Copy the URL (e.g., `https://backend-production-xxxx.up.railway.app`)

### Step 2: Sign Up for Vercel
1. Go to https://vercel.com
2. Click "Sign Up"
3. Choose "Continue with GitHub"
4. Authorize Vercel

### Step 3: Import Your Project
1. Click "Add New..." → "Project"
2. Import `Copper369/laughing-waddle`
3. Click "Import"

### Step 4: Configure Project Settings

#### Framework Preset:
- Select: **Vite**

#### Root Directory:
- Click "Edit"
- Set to: `frontend`
- Click "Continue"

#### Build Settings:
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

#### Environment Variables:
Click "Add" and add:

```
VITE_API_URL=https://your-backend-url.up.railway.app
```

**Important**: Replace with your actual Railway backend URL!

### Step 5: Deploy
1. Click "Deploy"
2. Wait 2-3 minutes for build
3. Vercel will give you a URL like: `https://laughing-waddle.vercel.app`

### Step 6: Update Backend CORS
Now that you have the Vercel URL, update Railway backend:

1. Go to Railway → Backend service → Variables
2. Update `FRONTEND_URL`:
   ```
   FRONTEND_URL=https://laughing-waddle.vercel.app
   ```
3. Backend will auto-redeploy

## Verification

### Test Your Deployment:
1. Visit your Vercel URL
2. Should see login page
3. Open browser console (F12)
4. Try to register/login
5. Check for CORS errors (should be none)

### Expected URLs:
- **Frontend**: `https://laughing-waddle.vercel.app`
- **Backend**: `https://backend-production-xxxx.up.railway.app`

## Configuration Files

### vercel.json (Root of repo)
```json
{
  "version": 2,
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### Environment Variables in Vercel:
```
VITE_API_URL=https://your-backend-railway-url.up.railway.app
```

## Common Issues & Fixes

### Issue: Build Fails - "Cannot find module"
**Fix**: 
- Check Root Directory is set to `frontend`
- Verify package.json exists in frontend folder

### Issue: Blank Page After Deploy
**Fix**:
- Check browser console for errors
- Verify VITE_API_URL is set correctly
- Check Output Directory is `dist` not `build`

### Issue: API Calls Fail (CORS Error)
**Fix**:
- Update Railway backend FRONTEND_URL variable
- Make sure it matches your Vercel URL exactly
- Include https:// protocol

### Issue: 404 on Page Refresh
**Fix**:
- Verify vercel.json has rewrites configuration
- Should redirect all routes to index.html

### Issue: Environment Variable Not Working
**Fix**:
- Must start with `VITE_` prefix
- Redeploy after adding variables
- Check in browser: `console.log(import.meta.env.VITE_API_URL)`

## Custom Domain (Optional)

### Add Your Own Domain:
1. In Vercel project → Settings → Domains
2. Add your domain (e.g., `drishyamitra.com`)
3. Update DNS records as instructed
4. Update Railway backend FRONTEND_URL to your custom domain

## Automatic Deployments

Vercel automatically deploys when you:
- Push to `main` branch → Production deployment
- Push to other branches → Preview deployment
- Open Pull Request → Preview deployment

## Environment Variables for Different Environments

### Production:
```
VITE_API_URL=https://backend-production.up.railway.app
```

### Preview/Development:
```
VITE_API_URL=http://localhost:5000
```

You can set different values for Production vs Preview in Vercel settings.

## Monitoring & Analytics

### View Deployment Logs:
1. Go to Vercel Dashboard
2. Click on your project
3. Click on a deployment
4. View build logs and runtime logs

### Analytics (Optional):
1. Vercel → Project → Analytics
2. Enable Web Analytics
3. See visitor stats, performance metrics

## Cost

### Vercel Pricing:
- **Hobby (Free)**: 
  - 100GB bandwidth/month
  - Unlimited deployments
  - Perfect for personal projects
  
- **Pro ($20/month)**:
  - 1TB bandwidth
  - Better performance
  - Team features

For this project, **Free tier is sufficient**!

## Comparison: Vercel vs Railway Frontend

| Feature | Vercel | Railway |
|---------|--------|---------|
| Speed | ⚡ Very Fast | 🐢 Slower |
| Cost | 💰 Free | 💰 ~$5/month |
| CDN | ✅ Global | ❌ Single region |
| Build Time | 2-3 min | 5-8 min |
| Best For | Static sites | Full-stack apps |

**Recommendation**: Use Vercel for frontend, Railway for backend!

## Troubleshooting Checklist

Before asking for help, verify:
- [ ] Root directory set to `frontend`
- [ ] Framework preset is `Vite`
- [ ] Output directory is `dist`
- [ ] VITE_API_URL environment variable is set
- [ ] Backend URL includes `https://`
- [ ] Railway backend has correct FRONTEND_URL
- [ ] No CORS errors in browser console

## Quick Commands

### Test Build Locally:
```bash
cd frontend
npm install
npm run build
npm run preview
```

### Check Environment Variables:
Add to any component:
```javascript
console.log('API URL:', import.meta.env.VITE_API_URL);
```

## Support Resources

- Vercel Docs: https://vercel.com/docs
- Vercel Discord: https://vercel.com/discord
- Vite Docs: https://vitejs.dev
- Project Issues: https://github.com/Copper369/laughing-waddle/issues

## Success Checklist

Your deployment is successful when:
- ✅ Vercel build completes without errors
- ✅ Frontend loads at Vercel URL
- ✅ Can see login page
- ✅ Can register new user
- ✅ Can login successfully
- ✅ Can upload photos
- ✅ No CORS errors in console
- ✅ All features work as expected

---

**Pro Tip**: Vercel provides preview URLs for every branch and PR - great for testing!

## Next Steps After Deployment

1. Test all features thoroughly
2. Add custom domain (optional)
3. Enable Vercel Analytics
4. Set up monitoring
5. Share your app! 🎉
