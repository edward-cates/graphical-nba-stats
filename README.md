# Hoops Graphs

Simple NBA visualizations that inexplicably don't exist anywhere online—Google, ESPN, Reddit, etc. The goal is to fill this gap and rank highly in Google Image Search for terms like "nba standings over time", "nba head to head", "east vs west nba".

## SEO Philosophy

- **Hardcoded URLs**: Every image URL is explicit and permanent. Never use dynamic routing.
- **Never change existing URLs**: Once an image is published, its URL is frozen forever. Existing images already rank in Google Image Search.
- **Dated snapshots**: All graphs are weekly snapshots with dates in filenames. We preserve history, never overwrite.
- **SEO-friendly naming**: Filenames and URLs contain keywords people actually search for.

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

### 2. Head-to-Head

30×30 heatmap showing every team's record against every other team.

**Generate:**
```bash
make head-to-head
```

**Output:** `.head_to_head/head_to_head.png`

**Copy to:** `img/head-to-head/nba-head-to-head-YYYY-MM-DD.png`

**SEO URL:** `https://hoopsgraphs.com/nba-head-to-head/YYYY-MM-DD.png`

### 3. East vs West

Cumulative inter-conference record showing which conference is winning.

**Generate:**
```bash
make east-vs-west
```

**Output:** `.conference_battle/conference_battle.png`

**Copy to:** `img/east-vs-west/nba-east-vs-west-YYYY-MM-DD.png`

**SEO URL:** `https://hoopsgraphs.com/nba-east-vs-west/YYYY-MM-DD.png`

## Weekly Update Workflow

### 1. Generate all graphs

```bash
make standings-east
make standings-west
make head-to-head
make east-vs-west
```

### 2. Copy to `img/` with SEO filenames

Use today's date (YYYY-MM-DD format):

```bash
cp .standings/east_standings.png img/standings/nba-eastern-conference-cumulative-standings-YYYY-MM-DD.png
cp .standings/west_standings.png img/standings/nba-western-conference-cumulative-standings-YYYY-MM-DD.png
cp .head_to_head/head_to_head.png img/head-to-head/nba-head-to-head-YYYY-MM-DD.png
cp .conference_battle/conference_battle.png img/east-vs-west/nba-east-vs-west-YYYY-MM-DD.png
```

### 3. Add hardcoded routes to `src/main.py`

For each new image, add an explicit route:

```python
@app.get("/nba-standings/eastern-conference/YYYY-MM-DD.png")
async def standings_east_YYYY_MM_DD():
    return FileResponse("img/standings/nba-eastern-conference-cumulative-standings-YYYY-MM-DD.png", ...)
```

### 4. Update HTML pages

- `src/web/index.html` — Update current week dashboard
- `src/web/nba-standings.html` — Add new week to standings archive
- `src/web/nba-head-to-head.html` — Add new week to head-to-head archive
- `src/web/nba-east-vs-west.html` — Add new week to east-vs-west archive

### 5. Update `src/web/sitemap.xml`

Add `<image:image>` entries for all new images under the appropriate `<url>`. Update `<lastmod>` to today's date.

### 6. Deploy

```bash
git add -A
git commit -m "Add week X graphs"
git push heroku main
```

## URLs

- **Live site:** https://hoopsgraphs.com
- **Sitemap:** https://hoopsgraphs.com/sitemap.xml

## SEO Checklist

- [ ] All new images copied with SEO filenames
- [ ] Hardcoded routes added to `main.py`
- [ ] Sitemap updated with new images (under correct page URL)
- [ ] Alt text includes date and graph type
- [ ] All HTML pages updated with new graphs
