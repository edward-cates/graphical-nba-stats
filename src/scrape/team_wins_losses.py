import json
from datetime import datetime
from pathlib import Path
from typing import TypedDict

import requests
import pytz

EASTERN = pytz.timezone("US/Eastern")


class GameResult(TypedDict):
    date: str
    opponent: str
    opponent_abbrev: str
    win: bool


def get_team_wins_losses(team_abbreviation: str) -> list[GameResult]:
    """Fetch completed regular-season wins/losses for a team from ESPN's schedule JSON.

    (The HTML schedule page returns an empty 202 to cloud IPs, so we use the API it's built on.)
    """
    url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{team_abbreviation}/schedule"
    response = requests.get(url, params={"seasontype": 2}, timeout=30)
    response.raise_for_status()

    results = []
    for event in response.json().get("events", []):
        competition = event["competitions"][0]
        if not competition["status"]["type"]["completed"]:
            continue
        us = them = None
        for competitor in competition["competitors"]:
            if competitor["team"]["abbreviation"].lower() == team_abbreviation:
                us = competitor
            else:
                them = competitor
        if us is None or them is None:
            continue

        # Game dates are UTC; night games belong to the previous US calendar day.
        tipoff = datetime.fromisoformat(event["date"].replace("Z", "+00:00")).astimezone(EASTERN)
        results.append({
            "date": tipoff.strftime("%y-%m-%d"),
            "opponent": them["team"].get("shortDisplayName", ""),
            "opponent_abbrev": them["team"]["abbreviation"].lower(),
            "win": bool(us.get("winner")),
        })

    return results


def get_cache_date_suffix() -> str:
    """Get today's date as YY-MM-DD for cache filename."""
    return datetime.now().strftime("%y-%m-%d")


def get_team_wins_losses_cached(
    team_abbreviation: str, cache_dir: Path = Path(".teams")
) -> list[GameResult]:
    """Get wins/losses for a team, using cache if available."""
    cache_dir.mkdir(exist_ok=True)
    date_suffix = get_cache_date_suffix()
    cache_file = cache_dir / f"{team_abbreviation}-{date_suffix}.json"

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

