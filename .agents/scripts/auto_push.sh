#!/usr/bin/env bash

# Usage: ./auto_push.sh [-y] <type> <feature_name> <commit_message>
# Example: ./auto_push.sh feat "login" "Add OAuth2 login support"
# Allowed types: feat, fix, docs, style, refactor, test, chore

AUTO_CONFIRM=false

if [ "$1" == "-y" ]; then
    AUTO_CONFIRM=true
    shift
fi

if [ "$#" -lt 3 ]; then
    echo "Usage: $0 [-y] <type> <feature_name> <commit_message>"
    echo "Types: feat, fix, docs, style, refactor, test, chore"
    echo "Example: $0 feat \"login\" \"Add OAuth2 login support\""
    exit 1
fi

TYPE=$1
FEATURE_NAME=$2
COMMIT_MESSAGE=$3

# Map type to branch prefix
case $TYPE in
    feat)
        BRANCH_PREFIX="feature"
        ;;
    fix|docs|style|refactor|test|chore)
        BRANCH_PREFIX="$TYPE"
        ;;
    *)
        echo "Error: Invalid type '$TYPE'. Allowed types: feat, fix, docs, style, refactor, test, chore"
        exit 1
        ;;
esac

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
DIRS=("admin-web" "api" "infra-deploy" "data-service" "extension")

for DIR in "${DIRS[@]}"; do
    if [ -d "$PROJECT_ROOT/$DIR/.git" ]; then
        cd "$PROJECT_ROOT/$DIR" || continue
        
        # Check if there are any changes
        if [[ -n $(git status -s) ]]; then
            echo ""
            echo "================================================"
            echo "🚀 Changes detected in: $DIR"
            git status -s
            echo "------------------------------------------------"
            
            BRANCH_NAME="${BRANCH_PREFIX}/${DIR}-${FEATURE_NAME}"
            FULL_COMMIT_MSG="${TYPE}(${DIR}): ${COMMIT_MESSAGE}"
            
            echo "📌 Target Branch: $BRANCH_NAME"
            echo "📌 Commit Message: $FULL_COMMIT_MSG"
            echo "================================================"
            
            if [ "$AUTO_CONFIRM" = false ]; then
                read -p "🤔 Do you want to commit and push these changes? (y/N): " confirm
                if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
                    echo "⏭  Skipping $DIR..."
                    continue
                fi
            fi
            
            # Create and checkout branch
            if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
                git checkout "$BRANCH_NAME"
            else
                git checkout -b "$BRANCH_NAME"
            fi
            
            echo "📝 Committing changes..."
            git add .
            git commit -m "$FULL_COMMIT_MSG"
            
            echo "⬆️ Pushing to remote..."
            git push -u origin "$BRANCH_NAME"
            
            echo "✅ Successfully pushed $DIR"
        fi
    fi
done

echo ""
echo "🎉 All changed repositories have been processed."
