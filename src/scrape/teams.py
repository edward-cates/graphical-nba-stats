from src.scrape.team_wins_losses import get_team_wins_losses_cached

# NBA team abbreviations (as used by ESPN) with metadata
# Colors optimized for visibility on dark backgrounds, using official team colors
TEAMS = {
    # Eastern Conference
    "atl": {"name": "Hawks", "color": "#E03A3E", "color2": "#C1D32F", "conference": "east"},  # Red + Volt Green
    "bos": {"name": "Celtics", "color": "#007A33", "color2": "#BA9653", "conference": "east"},  # Green + Gold
    "bkn": {"name": "Nets", "color": "#000000", "color2": "#A1A1A4", "conference": "east"},  # Black + Gray
    "cha": {"name": "Hornets", "color": "#1D1160", "color2": "#00788C", "conference": "east"},  # Purple + Teal
    "chi": {"name": "Bulls", "color": "#CE1141", "color2": "#000000", "conference": "east"},  # Red + Black
    "cle": {"name": "Cavaliers", "color": "#FFB81C", "color2": "#6F263D", "conference": "east"},  # Gold + Wine
    "det": {"name": "Pistons", "color": "#C8102E", "color2": "#1D42BA", "conference": "east"},  # Red + Blue
    "ind": {"name": "Pacers", "color": "#FDBB30", "color2": "#002D62", "conference": "east"},  # Gold + Navy
    "mia": {"name": "Heat", "color": "#98002E", "color2": "#000000", "conference": "east"},  # Red + Black
    "mil": {"name": "Bucks", "color": "#00471B", "color2": "#552582", "conference": "east"},  # Green + Purple
    "ny": {"name": "Knicks", "color": "#F58426", "color2": "#006BB6", "conference": "east"},  # Orange + Blue
    "orl": {"name": "Magic", "color": "#0077C0", "color2": "#C4CED4", "conference": "east"},  # Blue + Silver
    "phi": {"name": "76ers", "color": "#006BB6", "color2": "#ED174C", "conference": "east"},  # Blue + Red
    "tor": {"name": "Raptors", "color": "#CE1141", "color2": "#5D2E8C", "conference": "east"},  # Red + Purple
    "wsh": {"name": "Wizards", "color": "#002B5C", "color2": "#E31837", "conference": "east"},  # Blue + Red
    # Western Conference
    "dal": {"name": "Mavericks", "color": "#B8C4CA", "color2": "#00538C", "conference": "west"},  # Silver + Blue
    "den": {"name": "Nuggets", "color": "#0E2240", "color2": "#FEC524", "conference": "west"},  # Blue + Yellow
    "gs": {"name": "Warriors", "color": "#FFC72C", "color2": "#1D428A", "conference": "west"},  # Gold + Blue
    "hou": {"name": "Rockets", "color": "#CE1141", "color2": "#C4CED4", "conference": "west"},  # Red + Silver
    "lac": {"name": "Clippers", "color": "#C8102E", "color2": "#1D428A", "conference": "west"},  # Red + Blue
    "lal": {"name": "Lakers", "color": "#FDB927", "color2": "#552583", "conference": "west"},  # Gold + Purple
    "mem": {"name": "Grizzlies", "color": "#5D76A9", "color2": "#12173F", "conference": "west"},  # Memphis Blue + Navy
    "min": {"name": "Wolves", "color": "#236192", "color2": "#0C2340", "conference": "west"},  # Lake Blue + Midnight Blue
    "no": {"name": "Pelicans", "color": "#0C2340", "color2": "#85714D", "conference": "west"},  # Blue + Gold-Brown
    "okc": {"name": "Thunder", "color": "#007AC1", "color2": "#EF3B24", "conference": "west"},  # Blue + Orange
    "phx": {"name": "Suns", "color": "#E56020", "color2": "#1D1160", "conference": "west"},  # Orange + Purple
    "por": {"name": "Blazers", "color": "#000000", "color2": "#E03A3E", "conference": "west"},  # Black + Red
    "sac": {"name": "Kings", "color": "#5A2D81", "color2": "#63727A", "conference": "west"},  # Purple + Gray
    "sa": {"name": "Spurs", "color": "#C4CED4", "color2": "#000000", "conference": "west"},  # Silver + Black
    "utah": {"name": "Jazz", "color": "#00471B", "color2": "#F9A01B", "conference": "west"},  # Green + Yellow
}


if __name__ == "__main__":
    for team in TEAMS.keys():
        try:
            print(f"Scraping {team}...")
            results = get_team_wins_losses_cached(team)
            print(f"{team}: {len(results)} games")
        except Exception as e:
            print(f"{team}: {e}")
            continue
