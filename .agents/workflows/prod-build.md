---
description: Build and start the entire CampusTab production stack
---

# Production Build Workflow

This workflow spins up the entire CampusTab ecosystem inside Docker containers using the production multi-stage builds.

// turbo-all

1. Navigate to the infra directory and start the production stack. Wait for the build and the dependencies.
```bash
cd /Volumes/Workspace/projects/campustab/infra-deploy
docker compose -f docker-compose.prod.yml up -d --build
```

2. Verify the containers are running and healthy.
```bash
cd /Volumes/Workspace/projects/campustab/infra-deploy
docker compose -f docker-compose.prod.yml ps
```
