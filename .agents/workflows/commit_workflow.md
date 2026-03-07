---
description: Branch strategy, commit message rules, folder-specific push process
---

# Multi-Repo Git Workflow

This project is managed efficiently using a multi-repo approach. Each major module has its own Git repository instead of a single root repository.

## Repositories
- `admin-web/`
- `api/`
- `infra-deploy/`
- `data-service/`
- `extension/`

## 1. Branch Strategy
When a new feature is added, a new branch MUST be created in the corresponding repository.
- **Naming Rule**: `feature/폴더명-기능명`
- **Example**: `feature/api-oauth-login`, `feature/admin-web-dashboard-ui`

## 2. Commit Message Convention
Commit messages follow a structural format indicating the affected folder.
- **Format**: `feat(폴더명): 추가된 기능 설명`
- **Example**: `feat(api): Add Google OAuth2 login`

## 3. Push Process (Auto Push)
A script is provided to automate change detection, branch creation, matching commit conventions, and pushing:
1. Detect which directories have modified files (`git status`).
2. Generate the appropriate branch `feature/폴더명-기능명`.
3. Stage changes (`git add .`) and commit with `feat(폴더명): <commit_message>`.
4. Push to remote.

Use the included script: `../scripts/auto_push.sh <feature_name> "<commit_message>"`
