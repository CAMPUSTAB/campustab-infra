---
description: Start the CampusTab environment for local development
---

# Local Development Workflow

This workflow guides you through spinning up the CampusTab project for local development with Hot Module Replacement (HMR) and fast iteration.

// turbo-all

1. Navigate to the infra directory and start the local databases (PostgreSQL and Redis) using Docker Compose.
```bash
cd /Volumes/Workspace/projects/campustab/infra-deploy
docker compose -f docker-compose.dev.yml up -d
```

2. Start the Spring Boot API Server
```bash
cd /Volumes/Workspace/projects/campustab/api
./gradlew bootRun
```

3. (In a new terminal) Start the FastAPI Data Service
```bash
cd /Volumes/Workspace/projects/campustab/data-service
# (Activate python venv if applicable)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

4. (In a new terminal) Start the Chrome Extension React Server
```bash
cd /Volumes/Workspace/projects/campustab/extension
npm run dev
```

5. (In a new terminal) Start the Admin Dashboard React Server
```bash
cd /Volumes/Workspace/projects/campustab/admin-web
npm run dev
```
