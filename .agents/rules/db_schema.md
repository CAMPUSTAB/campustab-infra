# CampusTab Database Schema (ERD)

The database is designed for PostgreSQL. It handles user management, university/department metadata, flexible content curation via Categories/Topics, and source management for crawlers.

## PostgreSQL ERD (Mermaid)

```mermaid
erDiagram
    UNIVERSITIES {
        bigint id PK
        varchar name "e.g., 한국대학교"
        varchar domain "e.g., hankook.ac.kr"
        timestamp created_at
    }

    DEPARTMENTS {
        bigint id PK
        bigint university_id FK
        varchar name "e.g., 컴퓨터공학과"
        timestamp created_at
    }

    USERS {
        bigint id PK
        varchar email "Unique"
        varchar password_hash
        varchar role "USER, ADMIN"
        bigint university_id FK "Nullable"
        bigint department_id FK "Nullable"
        timestamp created_at
    }

    CATEGORIES {
        bigint id PK
        varchar name "e.g., 개발, 디자인"
        timestamp created_at
    }

    TOPICS {
        bigint id PK
        bigint category_id FK
        varchar name "e.g., Frontend, Spring"
        timestamp created_at
    }

    USER_INTERESTS {
        bigint user_id FK
        bigint topic_id FK
        timestamp created_at
    }

    SOURCES {
        bigint id PK
        varchar name "해당 크롤링 소스명"
        varchar url "타겟 URL"
        varchar type "RSS, CRAWL, NOTICE"
        varchar css_selector "Nullable (for HTML crawling)"
        varchar schedule_cron "크롤링 주기"
        boolean is_active
        bigint department_id FK "Nullable (학과 공지사항인 경우 연결)"
        timestamp created_at
    }

    FEEDS {
        bigint id PK
        bigint source_id FK
        varchar title
        text summary
        varchar content_url
        varchar image_url "Nullable"
        timestamp published_at
        tsvector search_vector "PostgreSQL Full-Text Search용 벡터 칼럼"
        timestamp created_at
    }

    FEED_TOPICS {
        bigint feed_id FK
        bigint topic_id FK
    }

    BOOKMARKS {
        bigint user_id FK
        bigint feed_id FK
        timestamp created_at
    }

    UNIVERSITIES ||--o{ DEPARTMENTS : has
    UNIVERSITIES ||--o{ USERS : belongs_to
    DEPARTMENTS ||--o{ USERS : belongs_to
    DEPARTMENTS ||--o{ SOURCES : "can have specific notice sources"
    
    CATEGORIES ||--o{ TOPICS : contains
    USERS ||--o{ USER_INTERESTS : has
    TOPICS ||--o{ USER_INTERESTS : selected_by
    
    SOURCES ||--o{ FEEDS : generates
    FEEDS ||--o{ FEED_TOPICS : tagged_with
    TOPICS ||--o{ FEED_TOPICS : applied_to
    
    USERS ||--o{ BOOKMARKS : saves
    FEEDS ||--o{ BOOKMARKS : saved_by
```

## Table Details & PostgreSQL Search Optimization
- **Full-Text Search (FTS)**: `FEEDS` 테이블에 `tsvector` 타입의 `search_vector` 컬럼을 둡니다. 이는 트리거를 통해 `title`, `summary`, 연관 `TOPICS.name` 등이 병합되어 자동 업데이트됩니다.
- **Indexes**: 
  - `FEEDS.search_vector`에 **GIN (Generalized Inverted Index)**를 생성하여 텍스트 검색 성능을 극대화합니다.
  - `FEEDS.published_at` 컬럼에 B-Tree 인덱스를 생성하여 최신 순 정렬 조회를 가속합니다.
  - `USER_INTERESTS`, `BOOKMARKS`, `FEED_TOPICS` 복합키(PK)에 대한 기본 인덱싱.
