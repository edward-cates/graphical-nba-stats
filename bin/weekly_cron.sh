#!/usr/bin/env bash
# Weekly update on agent-box: render graphs, update the site, push to GitHub, deploy to app-host.
# crontab: 0 14 * * 2 ~/code/heroku/graphical-nba-stats/bin/weekly_cron.sh >> ~/logs/hoopsgraphs.log 2>&1
set -euo pipefail
cd "$(dirname "$0")/.."
echo "=== $(date -u +%FT%TZ)"

# Chrome for Testing has no linux-arm64 build; kaleido renders with Playwright's Chromium instead.
export BROWSER_PATH=$(ls -d ~/.cache/ms-playwright/chromium-*/chrome-linux*/chrome | tail -1)
export PATH="$PWD/.venv/bin:$PATH"

git pull -q --rebase origin main
python scripts/weekly_update.py
git add -A img src
git commit -qm "Add week $(grep -oE '<h2>Week [0-9]+' src/web/nba-standings.html | head -1 | grep -oE '[0-9]+') graphs"
git push -q origin main

git -C ~/code/app-host pull -q --rebase
~/code/app-host/deploy.sh nba
command -v zipper-post >/dev/null && zipper-post "hoopsgraphs.com updated: $(git log -1 --format=%s)" || true
