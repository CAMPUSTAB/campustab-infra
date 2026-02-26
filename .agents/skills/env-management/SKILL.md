---
name: Environment Management Guide
description: Instructions on how environment variables are decoupled and managed across CampusTab environments.
---

# Environment Management Guide

CampusTab uses a decoupled environment configuration strategy divided by 'dev' and 'prod' profiles to prevent accidental exposure and improve DX.

## 1. Frontend Environments (`extension` & `admin-web`)
Both Vite+React projects use `.env` files.
- **Local Dev (`.env.development`)**: Variables used when running `npm run dev`. Points to `localhost` (e.g., `VITE_API_BASE_URL=http://localhost:8080`).
- **Production (`.env.production`)**: Variables hardbaked into the static JS bundles during `npm run build` or the Docker build process. Points to the actual domain.
- **DO NOT** commit real secrets or production domains to `.env.example`.

## 2. Backend API (`api`)
Spring Boot configuration is managed via YAML profiles in `api/src/main/resources/`.
- **`application-dev.yaml`**: Connects to the host's `localhost`. Used when running `./gradlew bootRun`.
- **`application-prod.yaml`**: Connects to Docker services (host names: `db`, `redis`). Activated in docker-compose.
- **`application.yaml`**: Houses common secrets (JWT, Flyway configs). Defaults to `dev`.

## 3. Infrastructure (`infra-deploy`)
- Database credentials and other central secrets are passed to `docker-compose*.yml` via the `infra-deploy/.env` file. These values trickle down to the Spring Boot app when running in Prod mode.
