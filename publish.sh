#!/usr/bin/env bash
set -euo pipefail

REPO_NAME=${1:-github-portfolio}
GIT_URL="git@github.com:xavierdscott01/${REPO_NAME}.git"

echo "Creating local git repo and pushing to $GIT_URL"
git init
git add .
git commit -m "feat: initial portfolio"
git branch -M main
git remote add origin "$GIT_URL" || true
git push -u origin main

echo "Done. If the remote doesn't exist yet, create https://github.com/xavierdscott01/${REPO_NAME} and rerun this script."