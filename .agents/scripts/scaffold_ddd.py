import os
import shutil

base_pkg = "/Volumes/Workspace/projects/campustab/api/src/main/java/com/campustab"

# 기존에 만들어진 레거시 구조(domain, controller, dto) 폴더 삭제
old_dirs = ["domain", "controller", "dto"]
for d in old_dirs:
    path = os.path.join(base_pkg, d)
    if os.path.exists(path):
        shutil.rmtree(path)

# DDD 구조 정의
domains = {
    "global": {
        "domain": ["BaseTimeEntity"],
        "infrastructure": [],
        "presentation": [],
        "application": []
    },
    "university": {
        "domain": ["University", "Department"],
        "infrastructure": ["UniversityRepository", "DepartmentRepository"],
        "presentation": ["UniversityController"],
        "application": ["UniversityService"]
    },
    "user": {
        "domain": ["User", "UserInterest", "Bookmark"],
        "infrastructure": ["UserRepository", "UserInterestRepository", "BookmarkRepository"],
        "presentation": ["UserController", "AuthController"],
        "application": ["UserService", "AuthService"]
    },
    "feed": {
        "domain": ["Feed", "Category", "Topic", "FeedTopic"],
        "infrastructure": ["FeedRepository", "CategoryRepository", "TopicRepository", "FeedTopicRepository"],
        "presentation": ["FeedController", "AdminFeedController"],
        "application": ["FeedService"]
    },
    "source": {
        "domain": ["Source"],
        "infrastructure": ["SourceRepository"],
        "presentation": ["AdminSourceController", "InternalCrawlController"],
        "application": ["SourceService"]
    },
    "system": {
        "domain": [],
        "infrastructure": [],
        "presentation": ["AdminSystemController"],
        "application": ["SystemService"]
    }
}

# 폴더 생성
for ddd_ctx, layers in domains.items():
    for layer in layers.keys():
        os.makedirs(os.path.join(base_pkg, ddd_ctx, layer), exist_ok=True)
    if ddd_ctx != "global" and ddd_ctx != "system":
        os.makedirs(os.path.join(base_pkg, ddd_ctx, "presentation", "dto"), exist_ok=True)

def write_java(filepath, content):
    with open(filepath, "w") as f:
        f.write(content)

# 1. Global (BaseTimeEntity)
write_java(os.path.join(base_pkg, "global/domain/BaseTimeEntity.java"), """package com.campustab.global.domain;

import jakarta.persistence.Column;
import jakarta.persistence.EntityListeners;
import jakarta.persistence.MappedSuperclass;
import lombok.Getter;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;

@Getter
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class BaseTimeEntity {
    @CreatedDate
    @Column(updatable = false, name = "created_at")
    private LocalDateTime createdAt;
}
""")

# 2. University Domain
write_java(os.path.join(base_pkg, "university/domain/University.java"), """package com.campustab.university.domain;

import com.campustab.global.domain.BaseTimeEntity;
import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "universities")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class University extends BaseTimeEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String domain;
}
""")

write_java(os.path.join(base_pkg, "university/domain/Department.java"), """package com.campustab.university.domain;

import com.campustab.global.domain.BaseTimeEntity;
import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "departments")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Department extends BaseTimeEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "university_id", nullable = false)
    private University university;
}
""")

# 3. Feed Domain
write_java(os.path.join(base_pkg, "feed/domain/Category.java"), """package com.campustab.feed.domain;

import com.campustab.global.domain.BaseTimeEntity;
import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "categories")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Category extends BaseTimeEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;
}
""")

write_java(os.path.join(base_pkg, "feed/domain/Topic.java"), """package com.campustab.feed.domain;

import com.campustab.global.domain.BaseTimeEntity;
import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "topics")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Topic extends BaseTimeEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "category_id", nullable = false)
    private Category category;
}
""")

write_java(os.path.join(base_pkg, "feed/domain/Feed.java"), """package com.campustab.feed.domain;

import com.campustab.global.domain.BaseTimeEntity;
import com.campustab.source.domain.Source;
import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Entity
@Table(name = "feeds")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Feed extends BaseTimeEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "source_id", nullable = false)
    private Source source;

    @Column(nullable = false)
    private String title;

    @Column(columnDefinition = "TEXT")
    private String summary;

    @Column(name = "content_url", nullable = false)
    private String contentUrl;

    @Column(name = "image_url")
    private String imageUrl;

    @Column(name = "published_at")
    private LocalDateTime publishedAt;

    @Column(name = "search_vector", columnDefinition = "tsvector", insertable = false, updatable = false)
    private String searchVector;
}
""")

write_java(os.path.join(base_pkg, "feed/domain/FeedTopic.java"), """package com.campustab.feed.domain;

import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "feed_topics")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class FeedTopic {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "feed_id", nullable = false)
    private Feed feed;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "topic_id", nullable = false)
    private Topic topic;
}
""")

# 4. User Domain
write_java(os.path.join(base_pkg, "user/domain/User.java"), """package com.campustab.user.domain;

import com.campustab.global.domain.BaseTimeEntity;
import com.campustab.university.domain.University;
import com.campustab.university.domain.Department;
import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "users")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class User extends BaseTimeEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false, name = "password_hash")
    private String passwordHash;

    @Column(nullable = false)
    private String role; 

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "university_id")
    private University university;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "department_id")
    private Department department;
}
""")

write_java(os.path.join(base_pkg, "user/domain/UserInterest.java"), """package com.campustab.user.domain;

import com.campustab.global.domain.BaseTimeEntity;
import com.campustab.feed.domain.Topic;
import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "user_interests")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class UserInterest extends BaseTimeEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "topic_id", nullable = false)
    private Topic topic;
}
""")

write_java(os.path.join(base_pkg, "user/domain/Bookmark.java"), """package com.campustab.user.domain;

import com.campustab.global.domain.BaseTimeEntity;
import com.campustab.feed.domain.Feed;
import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "bookmarks")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Bookmark extends BaseTimeEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "feed_id", nullable = false)
    private Feed feed;
}
""")

# 5. Source Domain
write_java(os.path.join(base_pkg, "source/domain/Source.java"), """package com.campustab.source.domain;

import com.campustab.global.domain.BaseTimeEntity;
import com.campustab.university.domain.Department;
import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "sources")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Source extends BaseTimeEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String url;

    @Column(nullable = false)
    private String type;

    @Column(name = "css_selector")
    private String cssSelector;

    @Column(name = "schedule_cron", nullable = false)
    private String scheduleCron;

    @Column(name = "is_active", nullable = false)
    private boolean isActive = true;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "department_id")
    private Department department;
}
""")

# DTO, Repository, Service, Controller 생성을 위한 헬퍼 루프
for ddd_ctx, layers in domains.items():
    # Repositories
    for repo in layers["infrastructure"]:
        entity_name = repo.replace("Repository", "")
        write_java(os.path.join(base_pkg, f"{ddd_ctx}/infrastructure/{repo}.java"), f"""package com.campustab.{ddd_ctx}.infrastructure;

import org.springframework.data.jpa.repository.JpaRepository;
import com.campustab.{ddd_ctx}.domain.{entity_name};

public interface {repo} extends JpaRepository<{entity_name}, Long> {{
}}
""")
    # Services
    for svc in layers["application"]:
        write_java(os.path.join(base_pkg, f"{ddd_ctx}/application/{svc}.java"), f"""package com.campustab.{ddd_ctx}.application;

import org.springframework.stereotype.Service;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class {svc} {{
}}
""")
    # Controllers
    for ctrl in layers["presentation"]:
        write_java(os.path.join(base_pkg, f"{ddd_ctx}/presentation/{ctrl}.java"), f"""package com.campustab.{ddd_ctx}.presentation;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/v1")
@RequiredArgsConstructor
public class {ctrl} {{
}}
""")

print("✅ Spring Boot DDD structure refactoring finished successfully.")
