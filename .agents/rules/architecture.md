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

---

## API Specifications

All endpoints conventionally prefix with `/api/v1`.

### Group A: Internal Communication (Spring Scheduler -> FastAPI)
Spring의 스케줄러가 크롤링 주기가 도래한 소스를 파악하여 FastAPI(Data Service)로 크롤링을 위임합니다.

| Method | URI | Description | Request Body | Response Body |
|--------|-----|-------------|--------------|---------------|
| `POST` | `/internal/crawl` | 특정 Source의 크롤링 즉시 트리거 | `{"source_id": 1, "url": "...", "css_selector": "..."}` | `{"status": "queued/success", "job_id": "..."}` |
| `GET` | `/internal/crawl/{job_id}` | (Optional) 특정 크롤링 작업 상태 확인 | - | `{"job_id": "...", "status": "completed", "items_crawled": 12}` |

> **Note**: FastAPI가 크롤링 완료 후 Feeds 테이블에 **직접 INSERT**하므로, Spring으로 데이터를 다시 회신할 필요가 없습니다.

---

### Group B: Client API (React Extension -> Spring Boot)
크롬 익스텐션에서 일반 유저가 호출하는 API입니다. JWT Token (Header: `Authorization: Bearer <token>`) 인증이 필요합니다.

| Method | URI | Description | Request Body | Response Body (Summary) |
|--------|-----|-------------|--------------|-------------------------|
| **[Auth]** |
| `POST` | `/auth/login` | 이메일/비밀번호 로그인 | `{"email": "", "password": ""}` | `{"access_token": "...", "refresh_token": "..."}` |
| `POST` | `/auth/register` | 신규 회원가입 | `{"email": "", "password": ""}` | `{"id": 1, "email": "..."}` |
| **[Feeds]** |
| `GET`  | `/feeds` | 메인 피드 목록 (내 관심사, 학교 공지 우선 정렬) | - (Query: `?page=0&size=20`) | `{"content": [{feed obj}], "total": 100}` |
| `GET`  | `/feeds/category/{id}` | 특정 카테고리의 최신 피드 조회 | - | `{"content": [{feed obj}]}` |
| `GET`  | `/feeds/topic/{id}` | 특정 토픽의 최신 피드 조회 | - | `{"content": [{feed obj}]}` |
| `GET`  | `/feeds/search` | Full-Text Search를 이용한 피드 검색 | - (Query: `?q={keyword}`) | `{"content": [{feed obj}]}` |
| **[User]** |
| `GET`  | `/users/me` | 내 프로필 및 설정 조회 | - | `{"id": 1, "university": {}, "departments": {}, "interests": []}` |
| `PUT`  | `/users/me` | 학교/학과 정보 수정 | `{"university_id": 1, "department_id": 5}` | `{"status": "success"}` |
| `PUT`  | `/users/me/interests` | 내 관심사(Topics) 덮어쓰기 업데이트 | `{"topic_ids": [1, 3, 5]}` | `{"status": "success"}` |
| **[Bookmarks]** |
| `GET`  | `/bookmarks` | 내 북마크 목록 조회 | - (Query: `?page=0&size=20`) | `{"content": [{feed obj}]}` |
| `POST` | `/bookmarks/{feedId}` | 특정 피드 북마크 추가 | - | `{"status": "success"}` |
| `DELETE`| `/bookmarks/{feedId}` | 북마크 취소 | - | `{"status": "success"}` |
| **[University]** |
| `GET` | `/universities` | 가입 가능한 대학교 목록 조회 | - | `[{"id": 1, "name": "..."}]` |
| `GET` | `/universities/{id}/departments` | 특정 대학교의 학과 목록 조회 (Select Box) | - | `[{"id": 1, "name": "..."}]` |

---

### Group C: Admin API (React Admin -> Spring Boot)
관리자 대시보드에서 호출하며, Spring Security 상 `ROLE_ADMIN` 권한이 필수입니다.

| Method | URI | Description | Request Body | Response Body (Summary) |
|--------|-----|-------------|--------------|-------------------------|
| **[Source Management]** |
| `GET` | `/admin/sources` | 크롤링 Source 전체 목록 조회 | - | `[{"id": 1, "name": "...", "type": "...", "is_active": true}]` |
| `POST` | `/admin/sources` | 새 소스 추가 | `{"name": "", "url": "", "type": "", "css_selector": "", "schedule_cron": "", "department_id": null}` | `{"id": 2, "status": "created"}` |
| `PUT` | `/admin/sources/{id}` | 소스 정보 수정 | `{"url": "...", "is_active": false...}` | `{"status": "success"}` |
| `DELETE` | `/admin/sources/{id}` | 소스 삭제 | - | `{"status": "success"}` |
| **[Feed Management]** |
| `GET` | `/admin/feeds` | 전체 피드 조회 및 관리용 (상태 필터 포함) | - (Query: `?source_id=1&page=0`) | `{"content": [{feed obj}]}` |
| `DELETE` | `/admin/feeds/{id}` | 특정 스팸/오류 피드 강제 삭제 | - | `{"status": "success"}` |
| **[System Control]** |
| `POST` | `/admin/system/trigger-crawl/{sourceId}`| 즉시 크롤링 수동 실행 (Spring이 FastAPI 호출)| - | `{"status": "triggered_to_data_service"}` |
