"""Generate cumulative standings plot for a conference."""

import argparse
import json
from datetime import datetime
from pathlib import Path

import plotly.graph_objects as go
from PIL import Image
import numpy as np

from src.scrape.teams import TEAMS
from src.scrape.team_wins_losses import get_team_wins_losses_cached


# Team colors (primary colors)
TEAM_COLORS = {
    # Eastern Conference
    "atl": "#E03A3E",  # Hawks red
    "bos": "#007A33",  # Celtics green
    "bkn": "#000000",  # Nets black
    "cha": "#1D1160",  # Hornets purple
    "chi": "#CE1141",  # Bulls red
    "cle": "#860038",  # Cavaliers wine
    "det": "#C8102E",  # Pistons red
    "ind": "#002D62",  # Pacers blue
    "mia": "#98002E",  # Heat red
    "mil": "#00471B",  # Bucks green
    "ny": "#006BB6",   # Knicks blue
    "orl": "#0077C0",  # Magic blue
    "phi": "#006BB6",  # 76ers blue
    "tor": "#CE1141",  # Raptors red
    "wsh": "#002B5C",  # Wizards blue
    # Western Conference
    "dal": "#00538C",  # Mavericks blue
    "den": "#0E2240",  # Nuggets blue
    "gs": "#1D428A",   # Warriors blue
    "hou": "#CE1141",  # Rockets red
    "lac": "#C8102E",  # Clippers red
    "lal": "#552583",  # Lakers purple
    "mem": "#5D76A9",  # Grizzlies blue
    "min": "#0C2340",  # Timberwolves blue
    "no": "#0C2340",   # Pelicans blue
    "okc": "#007AC1",  # Thunder blue
    "phx": "#1D1160",  # Suns purple
    "por": "#E03A3E",  # Blazers red
    "sac": "#5A2D81",  # Kings purple
    "sa": "#C4CED4",   # Spurs silver
    "utah": "#002B5C", # Jazz blue
}

# Team display names
TEAM_NAMES = {
    "atl": "Hawks", "bos": "Celtics", "bkn": "Nets", "cha": "Hornets",
    "chi": "Bulls", "cle": "Cavaliers", "det": "Pistons", "ind": "Pacers",
    "mia": "Heat", "mil": "Bucks", "ny": "Knicks", "orl": "Magic",
    "phi": "76ers", "tor": "Raptors", "wsh": "Wizards",
    "dal": "Mavericks", "den": "Nuggets", "gs": "Warriors", "hou": "Rockets",
    "lac": "Clippers", "lal": "Lakers", "mem": "Grizzlies", "min": "Timberwolves",
    "no": "Pelicans", "okc": "Thunder", "phx": "Suns", "por": "Blazers",
    "sac": "Kings", "sa": "Spurs", "utah": "Jazz",
}


def get_conference_teams(conference: str) -> list[str]:
    """Get team abbreviations for a conference."""
    return [abbr for abbr, info in TEAMS.items() if info["conference"] == conference]


def get_cumulative_standings_cached(
    conference: str, cache_dir: Path = Path(".standings")
) -> dict:
    """Get cumulative standings data, using cache if available."""
    cache_dir.mkdir(exist_ok=True)
    cache_file = cache_dir / f"{conference}_data.json"

    if cache_file.exists():
        print(f"{conference} standings: cached")
        return json.loads(cache_file.read_text())

    data = compute_cumulative_standings(conference)
    cache_file.write_text(json.dumps(data, indent=2))
    return data


def compute_cumulative_standings(conference: str) -> dict:
    """Compute cumulative standings for all teams in a conference."""
    teams = get_conference_teams(conference)
    all_dates = set()
    team_data = {}

    # Collect all data
    for team in teams:
        results = get_team_wins_losses_cached(team)
        team_data[team] = results
        for game in results:
            all_dates.add(game["date"])

    # Sort dates
    sorted_dates = sorted(all_dates)

    # Build cumulative records
    standings = {}
    for team, results in team_data.items():
        cumulative = []
        record = 0  # wins - losses
        game_idx = 0
        games_by_date = {g["date"]: g["win"] for g in results}

        for date in sorted_dates:
            if date in games_by_date:
                record += 1 if games_by_date[date] else -1
            cumulative.append(record)

        standings[team] = cumulative

    return {
        "dates": sorted_dates,
        "standings": standings,
    }


def create_placeholder_logo(size: int = 40) -> Image.Image:
    """Create a circular placeholder logo."""
    img = Image.new("RGBA", (size, size), (200, 200, 200, 255))
    # Create circular mask
    mask = Image.new("L", (size, size), 0)
    from PIL import ImageDraw
    draw = ImageDraw.Draw(mask)
    draw.ellipse([0, 0, size - 1, size - 1], fill=255)
    
    # Apply mask
    result = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    result.paste(img, mask=mask)
    return result


def generate_standings_plot(conference: str, output_dir: Path = Path(".standings")):
    """Generate and save the standings plot."""
    output_dir.mkdir(exist_ok=True)

    data = get_cumulative_standings_cached(conference)
    dates = data["dates"]
    standings = data["standings"]

    # Convert dates to datetime for better x-axis formatting
    date_labels = [datetime.strptime(f"20{d}", "%Y-%m-%d") for d in dates]

    # Sort teams by final standing for legend order
    final_standings = [(team, records[-1]) for team, records in standings.items()]
    sorted_teams = sorted(final_standings, key=lambda x: -x[1])

    # Create figure with dark theme
    fig = go.Figure()

    # Add traces for each team
    for team, _ in sorted_teams:
        records = standings[team]
        color = TEAM_COLORS.get(team, "#888888")
        name = TEAM_NAMES.get(team, team.upper())

        fig.add_trace(go.Scatter(
            x=date_labels,
            y=records,
            mode="lines",
            name=f"{name}",
            line=dict(color=color, width=3),
            hovertemplate=f"<b>{name}</b><br>Date: %{{x|%b %d}}<br>Record: %{{y:+d}}<extra></extra>",
        ))

        # Add team logo placeholder at the end
        fig.add_layout_image(
            dict(
                source="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAAhklEQVR4nO3XwQnAIBBFUVNZ+i/NNpJNIIEQnYxzzrsL/gcuIiIiIiIiIiIiIiLy/wCbmWXvPfYBM8u991xrrWut9d577LVWSillZlZKKXPOmXOuta611tra2lprjTHGGGOMY4wx7rXWvdZac865995z773XXnvtvffce++19lprrWuttfa31vrRJ0h0OhqZqgoAAAAASUVORK5CYII=",
                xref="x",
                yref="y",
                x=date_labels[-1],
                y=records[-1],
                sizex=86400000 * 2,  # 2 days in milliseconds
                sizey=1.5,
                xanchor="left",
                yanchor="middle",
                opacity=0.9,
                layer="above",
            )
        )

    # Style the chart
    conference_name = "Eastern" if conference == "east" else "Western"
    
    fig.update_layout(
        title=dict(
            text=f"<b>NBA {conference_name} Conference Standings</b><br><sup>2024-25 Season • Cumulative Record (Wins - Losses)</sup>",
            font=dict(size=28, color="#E8E8E8", family="Helvetica Neue, Arial"),
            x=0.5,
            xanchor="center",
        ),
        font=dict(family="Helvetica Neue, Arial", color="#CCCCCC"),
        plot_bgcolor="#1a1a2e",
        paper_bgcolor="#0f0f23",
        xaxis=dict(
            title="",
            showgrid=True,
            gridcolor="#2a2a4a",
            gridwidth=1,
            tickformat="%b %d",
            tickfont=dict(size=12, color="#AAAAAA"),
            linecolor="#3a3a5a",
            tickangle=-45,
        ),
        yaxis=dict(
            title=dict(text="Games Over/Under .500", font=dict(size=14, color="#CCCCCC")),
            showgrid=True,
            gridcolor="#2a2a4a",
            gridwidth=1,
            zeroline=True,
            zerolinecolor="#4a4a6a",
            zerolinewidth=2,
            tickfont=dict(size=12, color="#AAAAAA"),
            linecolor="#3a3a5a",
        ),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02,
            bgcolor="rgba(15, 15, 35, 0.9)",
            bordercolor="#3a3a5a",
            borderwidth=1,
            font=dict(size=11),
        ),
        margin=dict(l=60, r=180, t=100, b=80),
        width=1400,
        height=900,
        hovermode="x unified",
    )

    # Add .500 line annotation
    fig.add_annotation(
        x=date_labels[0],
        y=0,
        text=".500",
        showarrow=False,
        font=dict(size=11, color="#666666"),
        xanchor="right",
        xshift=-10,
    )

    # Save to PNG
    output_path = output_dir / f"{conference}_standings.png"
    fig.write_image(str(output_path), scale=2)
    print(f"Saved: {output_path}")

    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate NBA conference standings plot")
    parser.add_argument(
        "conference",
        choices=["east", "west"],
        help="Conference to generate standings for",
    )
    args = parser.parse_args()

    generate_standings_plot(args.conference)

