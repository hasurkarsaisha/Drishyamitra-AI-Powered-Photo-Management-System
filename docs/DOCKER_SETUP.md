# Docker Setup Guide

## Why Docker?

Docker eliminates all the manual setup headaches:
- ✅ No need to install Python, Node.js, or PostgreSQL manually
- ✅ No dependency conflicts or version issues
- ✅ Everything runs in isolated containers
- ✅ One command to start everything
- ✅ Works the same on any machine

## Prerequisites

1. **Install Docker Desktop**
   - Download from: https://www.docker.com/products/docker-desktop
   - Install and start Docker Desktop
   - Make sure Docker is running (check system tray icon)

## Quick Start

### 1. Configure Environment

Make sure your `.env` files are set up:

```bash
# backend/.env should have:
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/drishyamitra
GROQ_API_KEY=your_groq_api_key_here
```

### 2. Start Everything

**Option A: Using the batch file (Recommended)**
```bash
docker-start.bat
```

**Option B: Using docker-compose directly**
```bash
docker-compose up --build
```

This will:
1. Start PostgreSQL database
2. Build and start the backend
3. Build and start the frontend

### 3. Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- PostgreSQL: localhost:5432

### 4. Stop Everything

Press `Ctrl+C` in the terminal, or run:
```bash
docker-stop.bat
```

Or:
```bash
docker-compose down
```

## What's Running?

- **postgres** - PostgreSQL 16 database
- **backend** - Python Flask API (port 5000)
- **frontend** - React app with Nginx (port 3000)

## Data Persistence

Your data is stored in Docker volumes:
- `postgres_data` - Database data (persists between restarts)
- `./backend/data` - Uploaded photos (mounted from host)

## Useful Commands

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f postgres
```

### Restart a service
```bash
docker-compose restart backend
```

### Rebuild after code changes
```bash
docker-compose up --build
```

### Clean everything (including database)
```bash
docker-compose down -v
```

### Access database directly
```bash
docker exec -it drishyamitra-postgres psql -U postgres -d drishyamitra
```

### Run backend commands
```bash
docker exec -it drishyamitra-backend python reprocess_all_photos.py
```

## Troubleshooting

### Port already in use
If you get "port already in use" errors:
1. Stop any manually running backend/frontend/postgres
2. Or change ports in docker-compose.yml

### Docker not starting
1. Make sure Docker Desktop is running
2. Check Docker Desktop settings
3. Restart Docker Desktop

### Database connection errors
1. Wait 10-15 seconds for PostgreSQL to fully start
2. Check logs: `docker-compose logs postgres`

### Build errors
1. Make sure .env files exist
2. Check Docker has enough resources (Settings > Resources)
3. Try: `docker-compose down` then `docker-compose up --build`

## Advantages Over Manual Setup

| Manual Setup | Docker Setup |
|--------------|--------------|
| Install Python 3.12 | ✅ Included |
| Install Node.js 18+ | ✅ Included |
| Install PostgreSQL | ✅ Included |
| Manage virtual environments | ✅ Automatic |
| Fix dependency conflicts | ✅ No conflicts |
| Start 3 services manually | ✅ One command |
| Platform-specific issues | ✅ Works everywhere |

## Migrating from Manual to Docker

If you have existing data:

1. Export your PostgreSQL data:
```bash
pg_dump -U postgres drishyamitra > backup.sql
```

2. Start Docker setup:
```bash
docker-compose up -d postgres
```

3. Import data:
```bash
docker exec -i drishyamitra-postgres psql -U postgres drishyamitra < backup.sql
```

4. Start everything:
```bash
docker-compose up
```

## Development Workflow

1. Make code changes in your editor
2. For backend changes: `docker-compose restart backend`
3. For frontend changes: `docker-compose up --build frontend`
4. Database changes persist automatically

## Production Deployment

For production, update docker-compose.yml:
- Change `FLASK_ENV=production`
- Add proper secrets management
- Use nginx reverse proxy
- Add SSL certificates
- Set up backups for postgres_data volume
