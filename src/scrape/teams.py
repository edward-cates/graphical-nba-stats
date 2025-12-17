from src.scrape.team_wins_losses import get_team_wins_losses_cached

# NBA team abbreviations (as used by ESPN) with metadata
TEAMS = {
    # Eastern Conference
    "atl": {"conference": "east"},  # Atlanta Hawks
    "bos": {"conference": "east"},  # Boston Celtics
    "bkn": {"conference": "east"},  # Brooklyn Nets
    "cha": {"conference": "east"},  # Charlotte Hornets
    "chi": {"conference": "east"},  # Chicago Bulls
    "cle": {"conference": "east"},  # Cleveland Cavaliers
    "det": {"conference": "east"},  # Detroit Pistons
    "ind": {"conference": "east"},  # Indiana Pacers
    "mia": {"conference": "east"},  # Miami Heat
    "mil": {"conference": "east"},  # Milwaukee Bucks
    "ny":  {"conference": "east"},  # New York Knicks
    "orl": {"conference": "east"},  # Orlando Magic
    "phi": {"conference": "east"},  # Philadelphia 76ers
    "tor": {"conference": "east"},  # Toronto Raptors
    "wsh": {"conference": "east"},  # Washington Wizards
    # Western Conference
    "dal": {"conference": "west"},  # Dallas Mavericks
    "den": {"conference": "west"},  # Denver Nuggets
    "gs":  {"conference": "west"},  # Golden State Warriors
    "hou": {"conference": "west"},  # Houston Rockets
    "lac": {"conference": "west"},  # Los Angeles Clippers
    "lal": {"conference": "west"},  # Los Angeles Lakers
    "mem": {"conference": "west"},  # Memphis Grizzlies
    "min": {"conference": "west"},  # Minnesota Timberwolves
    "no":  {"conference": "west"},  # New Orleans Pelicans
    "okc": {"conference": "west"},  # Oklahoma City Thunder
    "phx": {"conference": "west"},  # Phoenix Suns
    "por": {"conference": "west"},  # Portland Trail Blazers
    "sac": {"conference": "west"},  # Sacramento Kings
    "sa":  {"conference": "west"},  # San Antonio Spurs
    "utah": {"conference": "west"}, # Utah Jazz
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
