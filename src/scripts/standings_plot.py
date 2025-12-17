"""Generate cumulative standings plot for a conference."""

import argparse
import base64
import json
from pathlib import Path

import plotly.graph_objects as go

from src.scrape.teams import TEAMS
from src.scrape.team_wins_losses import get_team_wins_losses_cached

# Logo directory
LOGO_DIR = Path("img/logos")


def get_logo_base64(team: str) -> str | None:
    """Load team logo and return as base64 data URI."""
    logo_path = LOGO_DIR / f"{team}.png"
    if not logo_path.exists():
        return None
    with open(logo_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{b64}"


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
    standings = {}

    for team in teams:
        results = get_team_wins_losses_cached(team)
        sorted_results = sorted(results, key=lambda g: g["date"])
        
        cumulative = [0]
        record = 0
        for game in sorted_results:
            record += 1 if game["win"] else -1
            cumulative.append(record)
        
        standings[team] = cumulative

    return {"standings": standings}


def generate_standings_plot(conference: str, output_dir: Path = Path(".standings")):
    """Generate and save the standings plot."""
    output_dir.mkdir(exist_ok=True)

    data = get_cumulative_standings_cached(conference)
    standings = data["standings"]

    # Sort by final standing
    final_standings = [(team, records[-1]) for team, records in standings.items()]
    sorted_teams = sorted(final_standings, key=lambda x: -x[1])

    # Clean colors
    bg_color = "#ffffff"
    plot_bg = "#fafafa"
    grid_color = "#e5e5e5"
    text_color = "#1f2937"
    muted_text = "#6b7280"

    # Mobile-friendly portrait - tighter
    chart_w, chart_h = 1200, 1350

    fig = go.Figure()

    # Draw lines (worst first so best render on top)
    for team, _ in reversed(sorted_teams):
        records = standings[team]
        game_nums = list(range(len(records)))
        team_info = TEAMS[team]
        color = team_info["color"]
        color2 = team_info["color2"]
        name = team_info["name"]

        # Stroke outline
        fig.add_trace(go.Scatter(
            x=game_nums, y=records,
            mode="lines",
            line=dict(color=color2, width=5, shape="spline", smoothing=0.3),
            hoverinfo="skip",
            showlegend=False,
        ))

        # Main line
        fig.add_trace(go.Scatter(
            x=game_nums, y=records,
            mode="lines",
            name=name,
            line=dict(color=color, width=2.5, shape="spline", smoothing=0.3),
            hovertemplate=f"<b>{name}</b><br>Game %{{x}}<br>%{{y:+d}}<extra></extra>",
            showlegend=False,
        ))

    # Endpoint markers
    for team, final_record in sorted_teams:
        records = standings[team]
        game_count = len(records) - 1
        team_info = TEAMS[team]
        color = team_info["color"]
        color2 = team_info["color2"]
        
        fig.add_trace(go.Scatter(
            x=[game_count], y=[final_record],
            mode="markers",
            marker=dict(size=12, color=color, line=dict(color=color2, width=2)),
            hoverinfo="skip",
            showlegend=False,
        ))

    conference_name = "Eastern" if conference == "east" else "Western"

    # Legend positioning - small gap below subtitle, tight bottom
    num_teams = len(sorted_teams)
    legend_top = 0.97
    legend_bottom = 0.04
    legend_spacing = (legend_top - legend_bottom) / (num_teams - 1)

    fig.update_layout(
        font=dict(family="Arial, Helvetica, sans-serif", color=text_color),
        plot_bgcolor=plot_bg,
        paper_bgcolor=bg_color,
        xaxis=dict(
            title=dict(text="Games Played", font=dict(size=16, color=muted_text)),
            showgrid=True,
            gridcolor=grid_color,
            tickfont=dict(size=14, color=muted_text),
            linecolor=grid_color,
            dtick=5,
            zeroline=False,
        ),
        yaxis=dict(
            title=dict(text="Games Over .500", font=dict(size=16, color=muted_text)),
            showgrid=True,
            gridcolor=grid_color,
            zeroline=True,
            zerolinecolor="#9ca3af",
            zerolinewidth=2,
            tickfont=dict(size=14, color=muted_text),
            linecolor=grid_color,
            domain=[legend_bottom, legend_top],
        ),
        showlegend=False,
        margin=dict(l=65, r=210, t=70, b=25),
        width=chart_w,
        height=chart_h,
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#e5e5e5",
            font=dict(size=14, color=text_color),
        ),
    )

    # Title - centered between image top and plot
    fig.add_annotation(
        x=0.0, y=1.04,
        xref="paper", yref="paper",
        text=f"<b>NBA {conference_name} Conference</b>",
        showarrow=False,
        font=dict(size=32, color=text_color),
        xanchor="left",
    )

    # Subtitle
    fig.add_annotation(
        x=0.0, y=1.005,
        xref="paper", yref="paper",
        text="2025-26 Season · Cumulative Record",
        showarrow=False,
        font=dict(size=16, color=muted_text),
        xanchor="left",
    )

    # .500 label
    fig.add_annotation(
        x=0, y=0,
        text=".500",
        showarrow=False,
        font=dict(size=13, color=muted_text),
        xanchor="right",
        xshift=-8,
    )

    # Legend on right with logos
    for i, (team, record) in enumerate(sorted_teams):
        team_info = TEAMS[team]
        name = team_info["name"]
        y_pos = legend_top - (i * legend_spacing)
        
        # Team logo (base64 for static export)
        logo_b64 = get_logo_base64(team)
        if logo_b64:
            fig.add_layout_image(
                dict(
                    source=logo_b64,
                    xref="paper", yref="paper",
                    x=1.02, y=y_pos,
                    sizex=0.045, sizey=0.045,
                    xanchor="left", yanchor="middle",
                )
            )
        
        # Team name
        fig.add_annotation(
            x=1.075, y=y_pos,
            xref="paper", yref="paper",
            text=name,
            showarrow=False,
            font=dict(size=15, color=text_color),
            xanchor="left", yanchor="middle",
        )
        
        # Record
        record_sign = "+" if record > 0 else ""
        record_color = "#059669" if record > 0 else ("#dc2626" if record < 0 else muted_text)
        fig.add_annotation(
            x=1.18, y=y_pos,
            xref="paper", yref="paper",
            text=f"<b>{record_sign}{record}</b>",
            showarrow=False,
            font=dict(size=14, color=record_color),
            xanchor="right", yanchor="middle",
        )

    # Save
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
