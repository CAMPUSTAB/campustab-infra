#!/usr/bin/env bash

# Usage: ./auto_push.sh <feature_name> <commit_message>
# Example: ./auto_push.sh "login" "Add OAuth2 login support"

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <feature_name> <commit_message>"
    echo "Example: $0 \"login\" \"Add OAuth2 login support\""
    exit 1
fi

FEATURE_NAME=$1
COMMIT_MESSAGE=$2

# 프로젝트 루트 디렉토리 (스크립트 위치부터 계산: infra-deploy/.agents/scripts -> ../../../)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"

DIRS=("admin-web" "api" "infra-deploy" "data-service" "extension")

for DIR in "${DIRS[@]}"; do
    if [ -d "$PROJECT_ROOT/$DIR/.git" ]; then
        cd "$PROJECT_ROOT/$DIR" || continue
        
        # Check if there are any changes
        if [[ -n $(git status -s) ]]; then
            echo "------------------------------------------------"
            echo "🚀 Changes detected in: $DIR"
            
            # Create and checkout feature branch
            BRANCH_NAME="feature/${DIR}-${FEATURE_NAME}"
            
            # Check if branch exists, if not create it
            if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
                git checkout "$BRANCH_NAME"
            else
                git checkout -b "$BRANCH_NAME"
            fi
            
            echo "📝 Committing changes..."
            git add .
            git commit -m "feat(${DIR}): ${COMMIT_MESSAGE}"
            
            echo "⬆️ Pushing to remote..."
            git push -u origin "$BRANCH_NAME"
            
            echo "✅ Successfully pushed $DIR"
        fi
    fi
done

echo "------------------------------------------------"
echo "🎉 All changed repositories have been processed."
