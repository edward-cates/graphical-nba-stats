#!/usr/bin/env bash
# Manual run from agent-box (the schedule lives in GitHub Actions): render graphs, update the site,
# push to GitHub and deploy to app-host right away.
set -euo pipefail
cd "$(dirname "$0")/.."
echo "=== $(date -u +%FT%TZ)"

# Chrome for Testing has no linux-arm64 build; kaleido renders with Playwright's Chromium instead.
export BROWSER_PATH=$(ls -d ~/.cache/ms-playwright/chromium-*/chrome-linux*/chrome | tail -1)
export PATH="$PWD/.venv/bin:$HOME/.local/bin:/usr/local/bin:$PATH"

# Cron has no session secrets; load GH_TOKEN from SSM and hand it to git.
eval "$(agent-secrets)"
git config credential.helper '!f() { echo username=x-access-token; echo "password=$GH_TOKEN"; }; f'

git pull -q --rebase origin main
python scripts/weekly_update.py
git add -A img src
git commit -qm "Add week $(grep -m1 -oE '<h2>Week [0-9]+' src/web/nba-standings.html | sed 's/.*Week //') graphs"
git push -q origin main

git -C ~/code/app-host pull -q --rebase
~/code/app-host/deploy.sh nba
command -v zipper-post >/dev/null && zipper-post "hoopsgraphs.com updated: $(git log -1 --format=%s)" || true
