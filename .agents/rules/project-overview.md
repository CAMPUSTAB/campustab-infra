# CampusTab Architecture Overview

CampusTab is a multi-component project that serves school notices grouped by interest, integrating functionality similar to Surfit as a Chrome extension.

## Tech Stack
- **API Server (`api`)**: Spring Boot applications running on Java 21 LTS using Gradle 8.14. Connects to PostgreSQL and Redis.
- **Data Service (`data-service`)**: Python FastAPI application for asynchronous data processing or crawling.
- **Chrome Extension (`extension`)**: The primary user interface. Built with Vite and React.
- **Admin Dashboard (`admin-web`)**: A separate web dashboard for administration. Built with Vite and React.
- **Infra Deploy (`infra-deploy`)**: Central orchestration directory housing all Docker Compose files and infrastructure configurations.

## Architecture & Communication
- The `api` acts as the primary data gateway for the `extension` and `admin-web`.
- The `data-service` can operate alongside the `api` for background tasks or specialized Python workflows.
- During development, `api`, `data-service`, `extension`, and `admin-web` can be run natively on the host while depending on `docker-compose.dev.yml` for database and caching.
- During production or full staging tests, `docker-compose.prod.yml` encapsulates the entire stack, spinning up backend containers and Nginx-served static React files.
