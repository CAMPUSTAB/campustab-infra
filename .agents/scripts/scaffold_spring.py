import os

base_pkg = "/Volumes/Workspace/projects/campustab/api/src/main/java/com/campustab"
dirs = ["domain/entity", "domain/repository", "controller/api", "controller/admin", "controller/internal", "dto"]

for d in dirs:
    os.makedirs(os.path.join(base_pkg, d), exist_ok=True)

entities = [
    "University", "Department", "User", "Category", 
    "Topic", "UserInterest", "Source", "Feed", "FeedTopic", "Bookmark"
]

for e in entities:
    # Entity
    with open(os.path.join(base_pkg, f"domain/entity/{e}.java"), "w") as f:
        f.write(f"""package com.campustab.domain.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import lombok.Getter;
import lombok.Setter;

@Entity
@Getter
@Setter
public class {e} {{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
}}
""")
    # Repository
    with open(os.path.join(base_pkg, f"domain/repository/{e}Repository.java"), "w") as f:
        f.write(f"""package com.campustab.domain.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.campustab.domain.entity.{e};

public interface {e}Repository extends JpaRepository<{e}, Long> {{
}}
""")

controllers = {
    "api": ["AuthController", "FeedController", "UserController", "BookmarkController", "UniversityController"],
    "admin": ["AdminSourceController", "AdminFeedController", "AdminSystemController"],
    "internal": ["InternalCrawlController"]
}

for pkg, ctrls in controllers.items():
    for c in ctrls:
        with open(os.path.join(base_pkg, f"controller/{pkg}/{c}.java"), "w") as f:
            f.write(f"""package com.campustab.controller.{pkg};

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/v1")
@RequiredArgsConstructor
public class {c} {{
}}
""")

print("✅ Spring Boot (api) scaffolding generated successfully.")
