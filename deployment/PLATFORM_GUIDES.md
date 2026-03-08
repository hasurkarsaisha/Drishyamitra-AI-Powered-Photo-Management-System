# Platform-Specific Deployment Guides

## 🚂 Railway Deployment (Recommended)

### Why Railway?
- Best for ML/AI projects with large dependencies
- Handles TensorFlow well
- Simple GitHub integration
- PostgreSQL included
- Good performance

### Steps:

1. **Prepare Repository**
```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

2. **Create Railway Project**
- Go to https://railway.app
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your DrishyaMitra repository

3. **Add PostgreSQL Database**
- In Railway dashboard, click "New"
- Select "Database" → "PostgreSQL"
- Note the connection string

4. **Configure Backend Service**
- Railway auto-detects Dockerfile in backend/
- Add environment variables:
  ```
  SECRET_KEY=<generate-new>
  JWT_SECRET_KEY=<generate-new>
  DATABASE_URL=${{Postgres.DATABASE_URL}}
  GROQ_API_KEY=<your-groq-key>
  FLASK_ENV=production
  ```
- Set root directory: `backend`
- Deploy

5. **Configure Frontend Service**
- Add new service from same repo
- Set root directory: `frontend`
- Add environment variable:
  ```
  VITE_API_URL=https://your-backend.railway.app
  ```
- Deploy

6. **Custom Domain (Optional)**
- Go to service settings
- Add custom domain
- Update DNS records

### Cost: ~$20-50/month

---

## 🎨 Render Deployment

### Why Render?
- Free tier available
- Simple setup
- Good documentation
- Auto-deploy from GitHub

### Steps:

1. **Create Web Service (Backend)**
- Go to https://render.com
- Click "New" → "Web Service"
- Connect GitHub repository
- Configure:
  ```
  Name: drishyamitra-backend
  Environment: Docker
  Region: Choose closest
  Branch: main
  Root Directory: backend
  ```
- Add environment variables (same as Railway)

2. **Create PostgreSQL Database**
- Click "New" → "PostgreSQL"
- Choose plan (free tier available)
- Copy internal database URL

3. **Update Backend Environment**
- Add DATABASE_URL with internal database URL
- This keeps database traffic internal (faster + free)

4. **Create Static Site (Frontend)**
- Click "New" → "Static Site"
- Connect same repository
- Configure:
  ```
  Name: drishyamitra-frontend
  Branch: main
  Root Directory: frontend
  Build Command: npm install && npm run build
  Publish Directory: dist
  ```
- Add environment variable:
  ```
  VITE_API_URL=https://drishyamitra-backend.onrender.com
  ```

5. **Important Notes**
- Free tier spins down after 15 min inactivity
- First request after spin-down takes 30-60 seconds
- Paid tier ($7/month) keeps service always on

### Cost: Free or $7-25/month

---

## 🌊 DigitalOcean App Platform

### Why DigitalOcean?
- Predictable pricing
- Good performance
- Managed database
- Simple scaling

### Steps:

1. **Create App**
- Go to https://cloud.digitalocean.com/apps
- Click "Create App"
- Connect GitHub repository

2. **Configure Backend Component**
```yaml
name: backend
source:
  repo: Copper369/laughing-waddle
  branch: main
  root_dir: /backend
dockerfile_path: backend/Dockerfile
instance_size: basic-xs
instance_count: 1
http_port: 5000
```

3. **Add Database**
- Add PostgreSQL database component
- Choose plan (starts at $15/month)

4. **Configure Frontend Component**
```yaml
name: frontend
source:
  repo: Copper369/laughing-waddle
  branch: main
  root_dir: /frontend
dockerfile_path: frontend/Dockerfile
instance_size: basic-xs
instance_count: 1
http_port: 80
```

5. **Set Environment Variables**
- Add all required variables in App Platform dashboard
- Use ${db.DATABASE_URL} for database connection

### Cost: ~$30-60/month

---

## ☁️ AWS Deployment (Advanced)

### Why AWS?
- Most scalable
- Full control
- Enterprise-grade
- Many services available

### Architecture:
```
CloudFront (CDN)
    ↓
ALB (Load Balancer)
    ↓
ECS Fargate (Backend Containers)
    ↓
RDS PostgreSQL (Database)
    ↓
S3 (Photo Storage)
```

### Steps:

1. **Create RDS PostgreSQL Database**
```bash
aws rds create-db-instance \
  --db-instance-identifier drishyamitra-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password <strong-password> \
  --allocated-storage 20
```

2. **Create S3 Bucket for Photos**
```bash
aws s3 mb s3://drishyamitra-photos
aws s3api put-bucket-cors --bucket drishyamitra-photos --cors-configuration file://cors.json
```

3. **Build and Push Docker Images**
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Create repositories
aws ecr create-repository --repository-name drishyamitra-backend
aws ecr create-repository --repository-name drishyamitra-frontend

# Build and push
docker build -t drishyamitra-backend ./backend
docker tag drishyamitra-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/drishyamitra-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/drishyamitra-backend:latest

docker build -t drishyamitra-frontend ./frontend
docker tag drishyamitra-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/drishyamitra-frontend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/drishyamitra-frontend:latest
```

4. **Create ECS Cluster and Services**
- Use AWS Console or Terraform
- Configure task definitions
- Set up ALB
- Configure auto-scaling

5. **Set Up CloudFront**
- Create distribution for frontend
- Configure S3 as origin
- Enable HTTPS

### Cost: $50-200+/month (highly variable)

---

## 🖥️ VPS Deployment (Self-Hosted)

### Why VPS?
- Full control
- Cost-effective
- Learn DevOps
- No vendor lock-in

### Recommended Providers:
- DigitalOcean Droplets ($12-24/month)
- Linode ($10-20/month)
- Vultr ($12-24/month)
- Hetzner ($5-15/month, EU only)

### Steps:

1. **Create VPS**
- Choose Ubuntu 22.04 LTS
- Minimum: 4GB RAM, 2 CPU, 80GB SSD
- Enable backups

2. **Initial Server Setup**
```bash
# SSH into server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Create non-root user
adduser deploy
usermod -aG sudo deploy
su - deploy

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. **Configure Firewall**
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

4. **Clone Repository**
```bash
cd /home/deploy
git clone https://github.com/Copper369/laughing-waddle.git
cd laughing-waddle
```

5. **Configure Environment**
```bash
cd backend
cp .env.example .env
nano .env  # Edit with production values
```

6. **Deploy with Docker Compose**
```bash
cd deployment
docker-compose up -d
```

7. **Set Up Nginx Reverse Proxy**
```bash
sudo apt install nginx certbot python3-certbot-nginx

# Create Nginx config
sudo nano /etc/nginx/sites-available/drishyamitra
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/drishyamitra /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

8. **Set Up Auto-Restart**
```bash
# Create systemd service
sudo nano /etc/systemd/system/drishyamitra.service
```

```ini
[Unit]
Description=DrishyaMitra Application
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/deploy/DrishyaMitra/deployment
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
User=deploy

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable drishyamitra
sudo systemctl start drishyamitra
```

9. **Set Up Backups**
```bash
# Create backup script
nano ~/backup.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/deploy/backups"

# Backup database
docker-compose exec -T postgres pg_dump -U postgres drishyamitra > $BACKUP_DIR/db_$DATE.sql

# Backup photos
tar -czf $BACKUP_DIR/photos_$DATE.tar.gz /home/deploy/DrishyaMitra/backend/data/photos/

# Keep only last 7 days
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

```bash
chmod +x ~/backup.sh

# Add to crontab (daily at 2 AM)
crontab -e
0 2 * * * /home/deploy/backup.sh
```

### Cost: $10-40/month

---

## 📊 Platform Comparison

| Platform | Ease | Cost | Performance | Scalability | ML Support |
|----------|------|------|-------------|-------------|------------|
| Railway | ⭐⭐⭐⭐⭐ | $$ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Render | ⭐⭐⭐⭐ | $ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| DigitalOcean | ⭐⭐⭐⭐ | $$ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| AWS | ⭐⭐ | $$$ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| VPS | ⭐⭐⭐ | $ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 🎯 Recommendation

**For Beginners**: Start with Railway
**For Budget**: Use Render free tier or cheap VPS
**For Learning**: Self-host on VPS
**For Scale**: AWS or DigitalOcean
**For ML Projects**: Railway or AWS

---

## 🆘 Common Issues

### Issue: Out of Memory
**Solution**: Upgrade to 4GB+ RAM or use swap file

### Issue: Slow Face Recognition
**Solution**: Use GPU instance or optimize batch processing

### Issue: Database Connection Timeout
**Solution**: Check firewall, use internal URLs when possible

### Issue: Docker Build Fails
**Solution**: Increase Docker memory limit to 4GB+

---

## 📞 Need Help?

- Check main deployment guide: docs/DEPLOYMENT_GUIDE.md
- Review checklist: docs/PRE_DEPLOYMENT_CHECKLIST.md
- Open issue: https://github.com/Copper369/laughing-waddle/issues
