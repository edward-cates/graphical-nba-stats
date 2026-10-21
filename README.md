# Hoops Graphs

Simple NBA visualizations that inexplicably don't exist anywhere online—Google, ESPN, Reddit, etc. The goal is to fill this gap and rank highly in Google Image Search for terms like "nba standings over time", "nba head to head", "east vs west nba".

## SEO Philosophy

- **Hardcoded URLs**: Every image URL is explicit and permanent. Never use dynamic routing.
- **Never change existing URLs**: Once an image is published, its URL is frozen forever. Existing images already rank in Google Image Search.
- **Dated snapshots**: All graphs are weekly snapshots with dates in filenames. We preserve history, never overwrite.
- **SEO-friendly naming**: Filenames and URLs contain keywords people actually search for.
- **Stable `/latest` URLs**: Each graph type has a `/latest.png` URL that always serves the current week's image. These accumulate SEO value over time as stable entry points.

## Site Structure

```
/                     → Current week dashboard (latest of each graph type)
/nba-standings        → All standings history (East + West)
/nba-head-to-head     → All head-to-head history
/nba-east-vs-west     → All east-vs-west history
```

Each graph type gets its own page for keyword authority. The homepage shows the latest week only.

## Graph Types

### 1. Conference Standings (East & West)

Cumulative win-loss progression for all 15 teams in each conference.

**Generate:**
```bash
make standings-east
make standings-west
```

**Output:** `.standings/east_standings.png`, `.standings/west_standings.png`

**Copy to:**
- `img/standings/nba-eastern-conference-cumulative-standings-YYYY-MM-DD.png`
- `img/standings/nba-western-conference-cumulative-standings-YYYY-MM-DD.png`

**SEO URLs:**
- `https://hoopsgraphs.com/nba-standings/eastern-conference/YYYY-MM-DD.png`
- `https://hoopsgraphs.com/nba-standings/western-conference/YYYY-MM-DD.png`
- `https://hoopsgraphs.com/nba-standings/eastern-conference/latest.png` (always current)
- `https://hoopsgraphs.com/nba-standings/western-conference/latest.png` (always current)

### 2. Head-to-Head

30×30 heatmap showing every team's record against every other team.

**Generate:**
```bash
make head-to-head
```

**Output:** `.head_to_head/head_to_head.png`

**Copy to:** `img/head-to-head/nba-head-to-head-YYYY-MM-DD.png`

**SEO URLs:**
- `https://hoopsgraphs.com/nba-head-to-head/YYYY-MM-DD.png`
- `https://hoopsgraphs.com/nba-head-to-head/latest.png` (always current)

### 3. East vs West

Cumulative inter-conference record showing which conference is winning.

**Generate:**
```bash
make east-vs-west
```

**Output:** `.conference_battle/conference_battle.png`

**Copy to:** `img/east-vs-west/nba-east-vs-west-YYYY-MM-DD.png`

**SEO URLs:**
- `https://hoopsgraphs.com/nba-east-vs-west/YYYY-MM-DD.png`
- `https://hoopsgraphs.com/nba-east-vs-west/latest.png` (always current)

## Weekly Update Workflow

Automated: agent-box runs `bin/weekly_cron.sh` every Tuesday 14:00 UTC (crontab). It runs
`scripts/weekly_update.py` (render graphs, copy dated images, add routes/archive entries/sitemap
images, point `/latest` at the new week), commits, pushes to GitHub and deploys with
`~/code/app-host/deploy.sh nba`. Log: `~/logs/hoopsgraphs.log` on agent-box.

Data comes from ESPN's schedule JSON (`site.api.espn.com/.../teams/<abbrev>/schedule`); the
HTML schedule page returns an empty 202 to cloud IPs. Graphs render with plotly/kaleido, which
needs Chrome: on the ARM box that's Playwright's Chromium (`uvx playwright install --with-deps chromium`).

## New Season

Run once before the first weekly update of a season:

```bash
python scripts/new_season.py 2025-26 2026-27
```

It copies each archive page to `/<page>/<old-season>/` (e.g. `/nba-standings/2025-26/`), empties
the live pages, adds a "Past seasons" link, moves the old dated images to the archived pages in the
sitemap, and drops the playoff bracket from the homepage. No image URL ever changes. Graph titles
and alt text take the season from `src/season.py`.

## URLs

- **Live site:** https://hoopsgraphs.com
- **Sitemap:** https://hoopsgraphs.com/sitemap.xml

## SEO Checklist

- [ ] All new images copied with SEO filenames
- [ ] Hardcoded dated routes added to `main.py`
- [ ] `/latest` routes updated to point to new week's images
- [ ] `index.html` date strings updated (3 section-meta elements)
- [ ] Archive HTML pages updated with new graphs
- [ ] Sitemap updated with new dated images (under correct page URL)
