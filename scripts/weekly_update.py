#!/usr/bin/env python3
"""Weekly update: generates graphs, copies images, updates all site files."""

import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def fatal(msg: str):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def human_date(dt: datetime) -> str:
    return f"{dt.strftime('%B')} {dt.day}, {dt.year}"


def insert_after(content: str, marker: str, insertion: str) -> str:
    idx = content.find(marker)
    if idx == -1:
        fatal(f"Marker not found: {marker!r}")
    end = idx + len(marker)
    return content[:end] + insertion + content[end:]


def insert_after_in_section(content: str, section_marker: str, after_tag: str, insertion: str) -> str:
    section_idx = content.find(section_marker)
    if section_idx == -1:
        fatal(f"Section not found: {section_marker!r}")
    tag_idx = content.find(after_tag, section_idx)
    if tag_idx == -1:
        fatal(f"Tag not found after section {section_marker!r}: {after_tag!r}")
    end = tag_idx + len(after_tag)
    return content[:end] + insertion + content[end:]


def generate_graphs():
    targets = [
        ("East standings", "standings-east"),
        ("West standings", "standings-west"),
        ("Head-to-head", "head-to-head"),
        ("East vs West", "east-vs-west"),
    ]
    for label, target in targets:
        print(f"  {label}...")
        result = subprocess.run(["make", target], cwd=ROOT, capture_output=True, text=True)
        if result.returncode != 0:
            print(result.stdout, file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            fatal(f"Graph generation failed: {label}")


def copy_images(date: str):
    copies = [
        (".standings/east_standings.png", f"img/standings/nba-eastern-conference-cumulative-standings-{date}.png"),
        (".standings/west_standings.png", f"img/standings/nba-western-conference-cumulative-standings-{date}.png"),
        (".head_to_head/head_to_head.png", f"img/head-to-head/nba-head-to-head-{date}.png"),
        (".conference_battle/conference_battle.png", f"img/east-vs-west/nba-east-vs-west-{date}.png"),
    ]
    for src, dst in copies:
        src_path = ROOT / src
        if not src_path.exists():
            fatal(f"Generated image not found: {src}")
        shutil.copy2(src_path, ROOT / dst)


def update_main_py(date: str, date_under: str, prev_date: str):
    path = ROOT / "src" / "main.py"
    content = path.read_text()

    routes = [
        (
            "# STANDINGS - Eastern Conference",
            f'''@app.get("/nba-standings/eastern-conference/{date}.png")
async def standings_east_{date_under}():
    return FileResponse(
        "img/standings/nba-eastern-conference-cumulative-standings-{date}.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )''',
        ),
        (
            "# STANDINGS - Western Conference",
            f'''@app.get("/nba-standings/western-conference/{date}.png")
async def standings_west_{date_under}():
    return FileResponse(
        "img/standings/nba-western-conference-cumulative-standings-{date}.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )''',
        ),
        (
            "# HEAD-TO-HEAD",
            f'''@app.get("/nba-head-to-head/{date}.png")
async def head_to_head_{date_under}():
    return FileResponse(
        "img/head-to-head/nba-head-to-head-{date}.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )''',
        ),
        (
            "# EAST VS WEST",
            f'''@app.get("/nba-east-vs-west/{date}.png")
async def east_vs_west_{date_under}():
    return FileResponse(
        "img/east-vs-west/nba-east-vs-west-{date}.png",
        media_type="image/png",
        headers=CACHE_HEADERS,
    )''',
        ),
    ]

    for section_marker, route_block in routes:
        idx = content.find(section_marker)
        if idx == -1:
            fatal(f"Section not found in main.py: {section_marker}")
        app_idx = content.find("@app.get", idx + len(section_marker))
        if app_idx == -1:
            fatal(f"No @app.get found after section: {section_marker}")
        content = content[:app_idx] + route_block + "\n\n\n" + content[app_idx:]

    latest_patterns = [
        (r'(async def standings_east_latest\(\):\s+return FileResponse\(\s+"img/standings/nba-eastern-conference-cumulative-standings-)\d{4}-\d{2}-\d{2}(\.png")',
         rf'\g<1>{date}\g<2>'),
        (r'(async def standings_west_latest\(\):\s+return FileResponse\(\s+"img/standings/nba-western-conference-cumulative-standings-)\d{4}-\d{2}-\d{2}(\.png")',
         rf'\g<1>{date}\g<2>'),
        (r'(async def head_to_head_latest\(\):\s+return FileResponse\(\s+"img/head-to-head/nba-head-to-head-)\d{4}-\d{2}-\d{2}(\.png")',
         rf'\g<1>{date}\g<2>'),
        (r'(async def east_vs_west_latest\(\):\s+return FileResponse\(\s+"img/east-vs-west/nba-east-vs-west-)\d{4}-\d{2}-\d{2}(\.png")',
         rf'\g<1>{date}\g<2>'),
    ]

    for pattern, replacement in latest_patterns:
        content, n = re.subn(pattern, replacement, content)
        if n != 1:
            fatal(f"Expected 1 replacement for latest route, got {n}")

    path.write_text(content)


def update_index_html(date_human: str, prev_date_human: str, week: int, prev_week: int):
    path = ROOT / "src" / "web" / "index.html"
    content = path.read_text()

    old_standings = f'<p class="section-meta">Week {prev_week} · {prev_date_human}</p>'
    new_standings = f'<p class="section-meta">Week {week} · {date_human}</p>'
    if old_standings not in content:
        fatal(f"Could not find standings section-meta in index.html")
    content = content.replace(old_standings, new_standings)

    old_meta = f'<p class="section-meta">{prev_date_human}</p>'
    new_meta = f'<p class="section-meta">{date_human}</p>'
    count = content.count(old_meta)
    if count != 2:
        fatal(f"Expected 2 date-only section-meta in index.html, found {count}")
    content = content.replace(old_meta, new_meta)

    path.write_text(content)


def update_standings_html(date: str, date_human: str, week: int, games: str):
    path = ROOT / "src" / "web" / "nba-standings.html"
    content = path.read_text()

    block = f'''
        <!-- Week {week}: {date_human} -->
        <article class="standings-week" id="{date}">
            <header class="week-header">
                <h2>Week {week}</h2>
                <time datetime="{date}">{date_human}</time>
            </header>

            <div class="standings-grid">
                <article class="standings-card">
                    <figure>
                        <a href="/nba-standings/eastern-conference/{date}.png" title="View full size">
                            <div class="card-header">
                                <h3>Eastern Conference</h3>
                                <span class="conference-badge east">East</span>
                            </div>
                            <img
                                src="/nba-standings/eastern-conference/{date}.png"
                                alt="NBA Eastern Conference Cumulative Standings Graph {date_human} - Shows win-loss record progression for all 15 Eastern Conference teams through the 2025-26 NBA season"
                                width="1200"
                                height="800"
                                loading="lazy"
                            >
                        </a>
                        <figcaption class="card-footer">
                            Games over .500 through {games} games played
                        </figcaption>
                    </figure>
                </article>

                <article class="standings-card">
                    <figure>
                        <a href="/nba-standings/western-conference/{date}.png" title="View full size">
                            <div class="card-header">
                                <h3>Western Conference</h3>
                                <span class="conference-badge west">West</span>
                            </div>
                            <img
                                src="/nba-standings/western-conference/{date}.png"
                                alt="NBA Western Conference Cumulative Standings Graph {date_human} - Shows win-loss record progression for all 15 Western Conference teams through the 2025-26 NBA season"
                                width="1200"
                                height="800"
                                loading="lazy"
                            >
                        </a>
                        <figcaption class="card-footer">
                            Games over .500 through {games} games played
                        </figcaption>
                    </figure>
                </article>
            </div>
        </article>
        '''

    content = insert_after(content, "<main>\n", block)
    path.write_text(content)


def update_head_to_head_html(date: str, date_human: str, week: int):
    path = ROOT / "src" / "web" / "nba-head-to-head.html"
    content = path.read_text()

    block = f'''
        <!-- {date_human} -->
        <article class="graph-week" id="{date}">
            <header class="week-header">
                <h2>Week {week}</h2>
                <time datetime="{date}">{date_human}</time>
            </header>

            <article class="graph-card">
                <figure>
                    <a href="/nba-head-to-head/{date}.png" title="View full size">
                        <img
                            src="/nba-head-to-head/{date}.png"
                            alt="NBA Head-to-Head Records Heatmap {date_human} - Shows every team's record against every other team in the 2025-26 NBA season"
                            width="1000"
                            height="1000"
                            loading="lazy"
                        >
                    </a>
                    <figcaption class="card-footer">
                        Every team's record against every other team
                    </figcaption>
                </figure>
            </article>
        </article>
        '''

    content = insert_after(content, "<main>\n", block)
    path.write_text(content)


def update_east_vs_west_html(date: str, date_human: str, week: int):
    path = ROOT / "src" / "web" / "nba-east-vs-west.html"
    content = path.read_text()

    block = f'''
        <!-- {date_human} -->
        <article class="graph-week" id="{date}">
            <header class="week-header">
                <h2>Week {week}</h2>
                <time datetime="{date}">{date_human}</time>
            </header>

            <article class="graph-card">
                <figure>
                    <a href="/nba-east-vs-west/{date}.png" title="View full size">
                        <img
                            src="/nba-east-vs-west/{date}.png"
                            alt="NBA East vs West Conference Battle {date_human} - Shows cumulative inter-conference record throughout the 2025-26 NBA season"
                            width="900"
                            height="450"
                            loading="lazy"
                        >
                    </a>
                    <figcaption class="card-footer">
                        Cumulative inter-conference record
                    </figcaption>
                </figure>
            </article>
        </article>
        '''

    content = insert_after(content, "<main>\n", block)
    path.write_text(content)


def update_sitemap(date: str, date_human: str, prev_date: str):
    path = ROOT / "src" / "web" / "sitemap.xml"
    content = path.read_text()

    content = content.replace(f"<lastmod>{prev_date}</lastmod>", f"<lastmod>{date}</lastmod>")

    homepage_images = f"""
    <image:image>
      <image:loc>https://hoopsgraphs.com/nba-standings/eastern-conference/{date}.png</image:loc>
      <image:title>NBA Eastern Conference Standings Over Time - {date_human}</image:title>
      <image:caption>Graph showing NBA Eastern Conference standings over time through {date_human}</image:caption>
    </image:image>
    <image:image>
      <image:loc>https://hoopsgraphs.com/nba-standings/western-conference/{date}.png</image:loc>
      <image:title>NBA Western Conference Standings Over Time - {date_human}</image:title>
      <image:caption>Graph showing NBA Western Conference standings over time through {date_human}</image:caption>
    </image:image>
    <image:image>
      <image:loc>https://hoopsgraphs.com/nba-head-to-head/{date}.png</image:loc>
      <image:title>NBA Head-to-Head Records - {date_human}</image:title>
      <image:caption>Heatmap showing every NBA team's record against every other team through {date_human}</image:caption>
    </image:image>
    <image:image>
      <image:loc>https://hoopsgraphs.com/nba-east-vs-west/{date}.png</image:loc>
      <image:title>NBA East vs West Conference Battle - {date_human}</image:title>
      <image:caption>Graph showing cumulative inter-conference record between East and West through {date_human}</image:caption>
    </image:image>"""
    content = insert_after_in_section(content, "<!-- Homepage -->", "<priority>1.0</priority>", homepage_images)

    standings_images = f"""
    <image:image>
      <image:loc>https://hoopsgraphs.com/nba-standings/eastern-conference/{date}.png</image:loc>
      <image:title>NBA Eastern Conference Standings Over Time - {date_human}</image:title>
      <image:caption>Graph showing NBA Eastern Conference standings over time through {date_human}</image:caption>
    </image:image>
    <image:image>
      <image:loc>https://hoopsgraphs.com/nba-standings/western-conference/{date}.png</image:loc>
      <image:title>NBA Western Conference Standings Over Time - {date_human}</image:title>
      <image:caption>Graph showing NBA Western Conference standings over time through {date_human}</image:caption>
    </image:image>"""
    content = insert_after_in_section(content, "<!-- Standings Archive -->", "<priority>0.9</priority>", standings_images)

    h2h_images = f"""
    <image:image>
      <image:loc>https://hoopsgraphs.com/nba-head-to-head/{date}.png</image:loc>
      <image:title>NBA Head-to-Head Records - {date_human}</image:title>
      <image:caption>Heatmap showing every NBA team's record against every other team through {date_human}</image:caption>
    </image:image>"""
    content = insert_after_in_section(content, "<!-- Head-to-Head Archive -->", "<priority>0.9</priority>", h2h_images)

    evw_images = f"""
    <image:image>
      <image:loc>https://hoopsgraphs.com/nba-east-vs-west/{date}.png</image:loc>
      <image:title>NBA East vs West Conference Battle - {date_human}</image:title>
      <image:caption>Graph showing cumulative inter-conference record between East and West through {date_human}</image:caption>
    </image:image>"""
    content = insert_after_in_section(content, "<!-- East vs West Archive -->", "<priority>0.9</priority>", evw_images)

    path.write_text(content)


def main():
    date_str = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y-%m-%d")

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        fatal(f"Invalid date format: {date_str}. Expected YYYY-MM-DD.")

    DATE = date.strftime("%Y-%m-%d")
    DATE_UNDER = DATE.replace("-", "_")
    DATE_HUMAN = human_date(date)

    main_py = (ROOT / "src" / "main.py").read_text()
    m = re.search(r'async def standings_east_latest\b.*?standings-(\d{4}-\d{2}-\d{2})\.png', main_py, re.DOTALL)
    if not m:
        fatal("Could not find previous date in main.py latest route")
    PREV_DATE = m.group(1)
    prev = datetime.strptime(PREV_DATE, "%Y-%m-%d")
    PREV_DATE_HUMAN = human_date(prev)

    if DATE == PREV_DATE:
        fatal(f"Date {DATE} already exists in the site")

    standings_html = (ROOT / "src" / "web" / "nba-standings.html").read_text()
    m = re.search(r'<h2>Week (\d+)</h2>', standings_html)
    if not m:
        fatal("Could not find week number in nba-standings.html")
    PREV_WEEK = int(m.group(1))
    WEEK = PREV_WEEK + 1
    GAMES = f"~{WEEK * 3}"

    print(f"Week {WEEK}: {DATE} ({DATE_HUMAN})")
    print(f"Previous: Week {PREV_WEEK}, {PREV_DATE}")
    print()

    print("Generating graphs...")
    generate_graphs()
    print()

    print("Copying images...")
    copy_images(DATE)
    print()

    print("Updating site files...")
    update_main_py(DATE, DATE_UNDER, PREV_DATE)
    update_index_html(DATE_HUMAN, PREV_DATE_HUMAN, WEEK, PREV_WEEK)
    update_standings_html(DATE, DATE_HUMAN, WEEK, GAMES)
    update_head_to_head_html(DATE, DATE_HUMAN, WEEK)
    update_east_vs_west_html(DATE, DATE_HUMAN, WEEK)
    update_sitemap(DATE, DATE_HUMAN, PREV_DATE)
    print()

    print("Done!")


if __name__ == "__main__":
    main()
