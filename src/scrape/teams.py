from src.scrape.team_wins_losses import get_team_wins_losses_cached

# NBA team abbreviations (as used by ESPN) with metadata
# Colors optimized for visibility on dark backgrounds, using official team colors
TEAMS = {
    # Eastern Conference
    "atl": {"name": "Hawks", "color": "#E03A3E", "color2": "#C1D32F", "conference": "east"},  # Red + Volt Green
    "bos": {"name": "Celtics", "color": "#007A33", "color2": "#BA9653", "conference": "east"},  # Green + Gold
    "bkn": {"name": "Nets", "color": "#000000", "color2": "#FFFFFF", "conference": "east"},  # Black + White
    "cha": {"name": "Hornets", "color": "#1D1160", "color2": "#00788C", "conference": "east"},  # Purple + Teal
    "chi": {"name": "Bulls", "color": "#CE1141", "color2": "#000000", "conference": "east"},  # Red + Black
    "cle": {"name": "Cavaliers", "color": "#FFB81C", "color2": "#6F263D", "conference": "east"},  # Gold + Wine
    "det": {"name": "Pistons", "color": "#C8102E", "color2": "#1D42BA", "conference": "east"},  # Red + Blue
    "ind": {"name": "Pacers", "color": "#FDBB30", "color2": "#002D62", "conference": "east"},  # Gold + Navy
    "mia": {"name": "Heat", "color": "#F9A01B", "color2": "#98002E", "conference": "east"},  # Yellow/Orange + Red
    "mil": {"name": "Bucks", "color": "#00471B", "color2": "#EEE1C6", "conference": "east"},  # Green + Cream
    "ny": {"name": "Knicks", "color": "#F58426", "color2": "#006BB6", "conference": "east"},  # Orange + Blue
    "orl": {"name": "Magic", "color": "#0077C0", "color2": "#C4CED4", "conference": "east"},  # Blue + Silver
    "phi": {"name": "76ers", "color": "#006BB6", "color2": "#ED174C", "conference": "east"},  # Blue + Red
    "tor": {"name": "Raptors", "color": "#CE1141", "color2": "#A1A1A4", "conference": "east"},  # Red + Silver
    "wsh": {"name": "Wizards", "color": "#E31837", "color2": "#002B5C", "conference": "east"},  # Red + Navy
    # Western Conference
    "dal": {"name": "Mavericks", "color": "#00538C", "color2": "#B8C4CA", "conference": "west"},  # Blue + Silver
    "den": {"name": "Nuggets", "color": "#FEC524", "color2": "#0E2240", "conference": "west"},  # Gold + Navy
    "gs": {"name": "Warriors", "color": "#FFC72C", "color2": "#1D428A", "conference": "west"},  # Gold + Blue
    "hou": {"name": "Rockets", "color": "#CE1141", "color2": "#C4CED4", "conference": "west"},  # Red + Silver
    "lac": {"name": "Clippers", "color": "#C8102E", "color2": "#1D428A", "conference": "west"},  # Red + Blue
    "lal": {"name": "Lakers", "color": "#FDB927", "color2": "#552583", "conference": "west"},  # Gold + Purple
    "mem": {"name": "Grizzlies", "color": "#5D76A9", "color2": "#12173F", "conference": "west"},  # Memphis Blue + Navy
    "min": {"name": "Timberwolves", "color": "#78BE20", "color2": "#0C2340", "conference": "west"},  # Aurora Green + Navy
    "no": {"name": "Pelicans", "color": "#85714D", "color2": "#0C2340", "conference": "west"},  # Gold + Navy
    "okc": {"name": "Thunder", "color": "#007AC1", "color2": "#EF3B24", "conference": "west"},  # Blue + Orange
    "phx": {"name": "Suns", "color": "#E56020", "color2": "#1D1160", "conference": "west"},  # Orange + Purple
    "por": {"name": "Blazers", "color": "#E03A3E", "color2": "#000000", "conference": "west"},  # Red + Black
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
