import json
import re
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def get_team_wins_losses(team_abbreviation: str) -> list[dict]:
    """Scrape wins/losses for a team from ESPN."""
    url = f"https://www.espn.com/nba/team/schedule/_/name/{team_abbreviation}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")

    if table is None:
        raise ValueError("No table found on page")

    # Extract season years from h1 (e.g. "Memphis Grizzlies Schedule 2025-26")
    h1 = table.find_previous("h1")
    season_match = re.search(r"(\d{4})-(\d{2})", h1.get_text() if h1 else "")
    if season_match:
        first_year = int(season_match.group(1))
        second_year = 2000 + int(season_match.group(2))
    else:
        # Fallback to current season
        now = datetime.now()
        first_year = now.year if now.month >= 10 else now.year - 1
        second_year = first_year + 1

    results = []
    for row in table.find_all("tr"):
        # Check if this is a completed game (has W or L symbol)
        symbol = row.find(attrs={"data-testid": "symbol"})
        if not symbol:
            continue

        date_elem = row.find(attrs={"data-testid": "date"})
        if not date_elem:
            continue

        date_text = date_elem.get_text(strip=True)  # e.g. "Wed, Oct 22"
        win = symbol.get_text(strip=True) == "W"

        # Parse the date (add dummy year to avoid deprecation warning)
        try:
            parsed = datetime.strptime(f"{date_text} 2000", "%a, %b %d %Y")
            # Determine year based on month
            year = first_year if parsed.month >= 10 else second_year
            date_str = f"{year % 100:02d}-{parsed.month:02d}-{parsed.day:02d}"
            results.append({"date": date_str, "win": win})
        except ValueError:
            continue  # Skip unparseable dates

    return results


def get_team_wins_losses_cached(
    team_abbreviation: str, cache_dir: Path = Path(".teams")
) -> list[dict]:
    """Get wins/losses for a team, using cache if available."""
    cache_dir.mkdir(exist_ok=True)
    cache_file = cache_dir / f"{team_abbreviation}.json"

    if cache_file.exists():
        print(f"{team_abbreviation}: cached")
        return json.loads(cache_file.read_text())

    results = get_team_wins_losses(team_abbreviation)
    cache_file.write_text(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    results = get_team_wins_losses_cached("mem")
    for game in results:
        print(f"{game['date']}: {'W' if game['win'] else 'L'}")

