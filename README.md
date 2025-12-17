# Hoops Graphs

NBA cumulative standings graphs updated weekly.

## Adding New Weekly Graphs

### 1. Generate the graphs

Run your standings plot script to create new images:
```bash
python -m src.scripts.standings_plot
```

### 2. Copy images to `img/standings/`

Name them:
- `nba-eastern-conference-cumulative-standings-YYYY-MM-DD.png`
- `nba-western-conference-cumulative-standings-YYYY-MM-DD.png`

### 3. Update `src/web/index.html`

Add a new `<article class="standings-week">` block **above** the previous week (newest first).

Update:
- `id="YYYY-MM-DD"`
- Week number in `<h2>`
- `datetime` and visible date in `<time>`
- All image `src` and `href` paths
- Alt text dates
- Figcaption (games played count)

### 4. Update `src/web/sitemap.xml`

Add new `<image:image>` entries for both conferences:
```xml
<image:image>
  <image:loc>https://hoopsgraphs.com/nba-standings/eastern-conference/YYYY-MM-DD.png</image:loc>
  <image:title>NBA Eastern Conference Cumulative Standings - Month DD, YYYY</image:title>
  <image:caption>Graph showing cumulative win-loss records for all 15 NBA Eastern Conference teams through Month DD, YYYY</image:caption>
</image:image>
```

Update `<lastmod>` to today's date.

### 5. Deploy

```bash
git add -A
git commit -m "Add week X standings"
git push heroku main
```

## URLs

- **Live site:** https://hoopsgraphs.com
- **Sitemap:** https://hoopsgraphs.com/sitemap.xml
- **Plausible:** Check your dashboard for analytics

## SEO Checklist

- [ ] Sitemap updated with new images
- [ ] Alt text includes date and conference
- [ ] Schema.org JSON-LD in `<head>` updated (optional but recommended)

