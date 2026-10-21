#!/usr/bin/env python3
"""Start a new season: archive last season's weekly pages under /<page>/<season>/ and reset the live pages.

Every image URL stays exactly where it is; only the pages that list them move.
Usage: python scripts/new_season.py 2025-26 2026-27
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "src" / "web"
MAIN_PY = ROOT / "src" / "main.py"
SITEMAP = WEB / "sitemap.xml"

MARKER = "        <!-- Add new weeks ABOVE this comment, newest first -->\n"
PAGES = {
    "nba-standings": "Standings Archive",
    "nba-head-to-head": "Head-to-Head Archive",
    "nba-east-vs-west": "East vs West Archive",
}


def fatal(msg: str):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def both_dashes(text: str, old: str, new: str) -> str:
    return text.replace(old, new).replace(old.replace("-", "–"), new.replace("-", "–"))


def archive_page(slug: str, old: str, new: str):
    path = WEB / f"{slug}.html"
    content = path.read_text()
    if MARKER not in content:
        fatal(f"Marker missing in {path.name}")

    # Archive copy: same weeks, its own URL, labelled as a past season.
    archive = content.replace(f'https://hoopsgraphs.com/{slug}/"', f'https://hoopsgraphs.com/{slug}/{old}/"')
    archive = re.sub(r"(<h1>)(.*?)(</h1>)", rf"\g<1>{old.replace('-', '–')} \g<2>\g<3>", archive, count=1)
    archive = re.sub(r'(<a href="/">Home</a> → )([^<\n]+)', rf'\g<1><a href="/{slug}/">\g<2></a> → {old.replace("-", "–")}', archive, count=1)
    (WEB / f"{slug}-{old}.html").write_text(archive)

    # Live page: drop the weeks, point labels at the new season, link to the archive.
    start = content.index("<main>\n") + len("<main>\n")
    end = content.index(MARKER)
    past = re.search(r'<nav class="past-seasons">.*?</nav>\n', content[end:], re.DOTALL)
    links = f'<a href="/{slug}/{old}/">{old.replace("-", "–")} season</a>'
    if past:
        nav = past.group(0).replace("Past seasons: ", f"Past seasons: {links} · ")
        content = content[:end] + content[end:].replace(past.group(0), "")
    else:
        nav = f'<nav class="past-seasons">Past seasons: {links}</nav>\n'
    content = both_dashes(content[:start], old, new) + "\n" + MARKER + f"        {nav}" + both_dashes(content[end + len(MARKER):], old, new)
    content = re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content="https://hoopsgraphs.com/[^"]*/)\d{4}-\d{2}-\d{2}\.png"',
                     r'\g<1>latest.png"', content)
    content = content.replace('<meta property="og:image" content="https://hoopsgraphs.com/nba-standings/latest.png"',
                              '<meta property="og:image" content="https://hoopsgraphs.com/nba-standings/eastern-conference/latest.png"')
    content = content.replace('<meta name="twitter:image" content="https://hoopsgraphs.com/nba-standings/latest.png"',
                              '<meta name="twitter:image" content="https://hoopsgraphs.com/nba-standings/eastern-conference/latest.png"')
    path.write_text(content)


def add_routes(old: str):
    content = MAIN_PY.read_text()
    marker = "@app.get(\"/sitemap.xml\")"
    block = ""
    for slug in PAGES:
        func = f"{slug.replace('-', '_')}_{old.replace('-', '_')}"
        block += f'''@app.get("/{slug}/{old}/", response_class=HTMLResponse)
async def {func}():
    with open("src/web/{slug}-{old}.html", "r") as f:
        return f.read()


'''
    MAIN_PY.write_text(content.replace(marker, block + marker, 1))


def update_index(old: str, new: str):
    path = WEB / "index.html"
    content = path.read_text()
    # The playoff bracket belongs to the season that just ended; its page stays up, off the homepage.
    content = re.sub(r"        <!-- PLAYOFF BRACKET SECTION -->.*?</section>\n\s*\n?", "", content, count=1, flags=re.DOTALL)
    content = re.sub(r'\s*<details class="faq-item">\s*<summary>What does the playoff bracket show.*?</details>', "", content, count=1, flags=re.DOTALL)
    content = re.sub(r'\s*\{\s*"@type": "Question",\s*"name": "What does the playoff bracket show.*?\}\s*\},', "", content, count=1, flags=re.DOTALL)
    content = content.replace("playoff bracket with regular-season H2H, standings, head-to-head, and conference battle",
                              "standings over time, East vs West, and head-to-head records")
    content = content.replace("Playoff Bracket, Standings, Head-to-Head, East vs West", "Standings Over Time, East vs West, Head-to-Head")
    content = content.replace("playoff bracket with regular-season head-to-head records, standings over time", "standings over time")
    content = content.replace("NBA playoff bracket, NBA playoffs regular season head to head, ", "")
    path.write_text(both_dashes(content, old, new))


def update_sitemap(old: str):
    content = SITEMAP.read_text()
    # Homepage only shows /latest images; dated ones live on the archive pages.
    home_start = content.index("<!-- Homepage -->")
    home_end = content.index("<!-- Latest URLs", home_start)
    first_img = content.index("<image:image>", home_start)
    if first_img < home_end:
        content = content[:first_img] + content[home_end:]

    for slug, label in PAGES.items():
        section = f"<!-- {label} -->"
        start = content.index(section)
        end = content.index("</url>", start) + len("</url>")
        old_block = content[start:end]
        archived = old_block.replace(section, f"<!-- {label} {old} -->").replace(
            f"<loc>https://hoopsgraphs.com/{slug}/</loc>", f"<loc>https://hoopsgraphs.com/{slug}/{old}/</loc>")
        archived = re.sub(r"<changefreq>weekly</changefreq>", "<changefreq>yearly</changefreq>", archived)
        archived = re.sub(r"<priority>0\.9</priority>", "<priority>0.6</priority>", archived)
        fresh = re.sub(r"\s*<image:image>.*?</image:image>", "", old_block, flags=re.DOTALL)
        content = content[:start] + fresh + "\n\n  " + archived + content[end:]
    SITEMAP.write_text(content)


def main():
    if len(sys.argv) != 3 or not all(re.fullmatch(r"\d{4}-\d{2}", s) for s in sys.argv[1:]):
        fatal("Usage: new_season.py OLD NEW   e.g. 2025-26 2026-27")
    old, new = sys.argv[1:]
    if (WEB / f"nba-standings-{old}.html").exists():
        fatal(f"{old} is already archived")
    for slug in PAGES:
        archive_page(slug, old, new)
    add_routes(old)
    update_index(old, new)
    update_sitemap(old)
    print(f"Archived {old}; live pages now say {new}.")


if __name__ == "__main__":
    main()
