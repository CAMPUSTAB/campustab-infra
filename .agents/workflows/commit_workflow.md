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
When a change is made, a new branch MUST be created in the corresponding repository with an appropriate prefix based on the change type.

### Supported Types:
- `feat` : A new feature (Branch prefix: `feature/`, Commit: `feat`)
- `fix` : A bug fix (Branch prefix: `fix/`, Commit: `fix`)
- `docs` : Documentation only changes (Branch prefix: `docs/`, Commit: `docs`)
- `style` : Changes that do not affect the meaning of the code (white-space, formatting, etc) (Branch prefix: `style/`, Commit: `style`)
- `refactor` : A code change that neither fixes a bug nor adds a feature (Branch prefix: `refactor/`, Commit: `refactor`)
- `test` : Adding missing tests or correcting existing tests (Branch prefix: `test/`, Commit: `test`)
- `chore` : Changes to the build process or auxiliary tools and libraries (Branch prefix: `chore/`, Commit: `chore`)

### Branch Naming Rule:
- **Format**: `<type_prefix>/<폴더명>-<기능명>`
- **Example**: `feature/api-oauth-login`, `fix/admin-web-dashboard-ui`, `chore/infra-deploy-update-deps`

## 2. Commit Message Convention
Commit messages follow a structural format indicating the affected folder and the change type.
- **Format**: `<type>(<폴더명>): <추가된 기능 설명>`
- **Example**: `feat(api): Add Google OAuth2 login`, `fix(extension): Resolve UI glitch`

## 3. Push Process (Auto Push)
A script is provided to automate change detection, branch creation, matching commit conventions, and pushing. The script will prompt you to review the commit message and branch before proceeding.

Use the included script: 
`../scripts/auto_push.sh <type> <feature_name> "<commit_message>"`

**Examples:**
- `./auto_push.sh feat "oauth" "Add OAuth2 login support"`
- `./auto_push.sh fix "typo" "Fix typo in login screen"`

You can bypass the confirmation prompt by adding the `-y` flag (useful for automated agents):
- `./auto_push.sh -y chore "dependencies" "Update npm packages"`
