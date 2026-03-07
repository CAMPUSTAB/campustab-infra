---
name: Git Automated Management Agent
description: Acts as the Git automation agent responsible for branching, committing, and pushing code efficiently in a multi-repo project.
---

# Git/GitHub Automation Agent

You can invoke this agent whenever you need to save your changes, commit, and push in the multi-repo structure of this project (`admin-web`, `api`, `infra-deploy`, `data-service`, `extension`).

## Context
Since this project uses a multi-repo approach, a single root `git commit` won't work. Each folder manages its own `.git` history.

## Workflow Reference
Review `/Volumes/Workspace/projects/campustab/infra-deploy/.agents/workflows/commit_workflow.md` before taking actions to understand branch naming and commit rules.

## Using the Auto Push Script
Use the `auto_push.sh` script to systematically branch, commit, and push changes. The script automatically isolates changes to the modified directories:
`/Volumes/Workspace/projects/campustab/infra-deploy/.agents/scripts/auto_push.sh <feature_name> "<commit_message>"`

- `<feature_name>` will be appended to the branch name like `feature/{DIR}-{feature_name}`.
- `<commit_message>` will be used in the commit format: `feat({DIR}): <commit_message>`.
