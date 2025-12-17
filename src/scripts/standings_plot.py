"""Generate cumulative standings plot for a conference."""

import argparse
import json
from pathlib import Path

import plotly.graph_objects as go

from src.scrape.teams import TEAMS
from src.scrape.team_wins_losses import get_team_wins_losses_cached


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
    """Compute cumulative standings for all teams in a conference.
    
    Returns game-by-game record for each team, starting at (0, 0).
    """
    teams = get_conference_teams(conference)
    standings = {}

    for team in teams:
        results = get_team_wins_losses_cached(team)
        # Sort by date to ensure chronological order
        sorted_results = sorted(results, key=lambda g: g["date"])
        
        # Build cumulative record starting at 0
        cumulative = [0]  # Start at origin
        record = 0
        for game in sorted_results:
            record += 1 if game["win"] else -1
            cumulative.append(record)
        
        standings[team] = cumulative

    return {
        "standings": standings,
    }


def generate_standings_plot(conference: str, output_dir: Path = Path(".standings")):
    """Generate and save the standings plot."""
    output_dir.mkdir(exist_ok=True)

    data = get_cumulative_standings_cached(conference)
    standings = data["standings"]

    # Sort teams by final standing for legend order
    final_standings = [(team, records[-1]) for team, records in standings.items()]
    sorted_teams = sorted(final_standings, key=lambda x: -x[1])

    # Light theme colors
    bg_color = "#ffffff"
    plot_bg = "#f8f9fa"
    grid_color = "rgba(0, 0, 0, 0.08)"
    text_color = "#1a1a1a"
    muted_text = "#6b7280"

    fig = go.Figure()

    # Add traces in reverse order so top teams render on top
    for team, _ in reversed(sorted_teams):
        records = standings[team]
        game_nums = list(range(len(records)))
        team_info = TEAMS[team]
        color = team_info["color"]
        color2 = team_info["color2"]
        name = team_info["name"]

        # Outline layer (secondary color)
        fig.add_trace(go.Scatter(
            x=game_nums,
            y=records,
            mode="lines",
            line=dict(color=color2, width=6, shape="spline", smoothing=0.3),
            hoverinfo="skip",
            showlegend=False,
        ))

        # Main line - thicker
        fig.add_trace(go.Scatter(
            x=game_nums,
            y=records,
            mode="lines",
            name=name,
            line=dict(color=color, width=3, shape="spline", smoothing=0.3),
            hovertemplate=f"<b>{name}</b><br>Game %{{x}}<br>Record: %{{y:+d}}<extra></extra>",
            showlegend=False,
        ))

    # Add endpoint markers for each team
    for team, final_record in sorted_teams:
        records = standings[team]
        game_count = len(records) - 1
        team_info = TEAMS[team]
        color = team_info["color"]
        color2 = team_info["color2"]
        
        fig.add_trace(go.Scatter(
            x=[game_count],
            y=[final_record],
            mode="markers",
            marker=dict(
                size=10,
                color=color,
                line=dict(color=color2, width=2),
            ),
            hoverinfo="skip",
            showlegend=False,
        ))

    # Style the chart
    conference_name = "Eastern" if conference == "east" else "Western"
    legend_top = 0.91
    legend_spacing = 0.053
    
    # Chart dimensions for circle aspect ratio correction
    chart_w, chart_h = 1400, 900
    
    fig.update_layout(
        font=dict(family="Arial, sans-serif", color=text_color),
        plot_bgcolor=plot_bg,
        paper_bgcolor=bg_color,
        xaxis=dict(
            title=dict(text="Games Played", font=dict(size=14, color=muted_text)),
            showgrid=True,
            gridcolor=grid_color,
            tickfont=dict(size=12, color=muted_text),
            linecolor="rgba(0,0,0,0)",
            dtick=5,
        ),
        yaxis=dict(
            title=dict(text="Games Over .500", font=dict(size=14, color=muted_text)),
            showgrid=True,
            gridcolor=grid_color,
            zeroline=True,
            zerolinecolor="rgba(0,0,0,0.2)",
            zerolinewidth=2,
            tickfont=dict(size=12, color=muted_text),
            linecolor="rgba(0,0,0,0)",
        ),
        showlegend=False,
        margin=dict(l=70, r=200, t=110, b=60),
        width=chart_w,
        height=chart_h,
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="rgba(255, 255, 255, 0.95)",
            bordercolor="rgba(0,0,0,0.1)",
            font=dict(size=14, color=text_color, family="Arial"),
        ),
    )
    
    # Title - separate annotation for proper spacing
    fig.add_annotation(
        x=0.0, y=1.07,
        xref="paper", yref="paper",
        text=f"<b>NBA {conference_name} Conference</b>",
        showarrow=False,
        font=dict(size=30, color=text_color, family="Arial, sans-serif"),
        xanchor="left", yanchor="bottom",
    )
    
    # Subtitle - with proper gap
    fig.add_annotation(
        x=0.0, y=1.015,
        xref="paper", yref="paper",
        text="2025-26 Season · Cumulative Record",
        showarrow=False,
        font=dict(size=16, color=muted_text, family="Arial, sans-serif"),
        xanchor="left", yanchor="bottom",
    )

    # Add custom legend with circles
    # Circle size in pixels, corrected for aspect ratio
    circle_r_px = 12
    x_r = circle_r_px / chart_w
    y_r = circle_r_px / chart_h
    
    for i, (team, record) in enumerate(sorted_teams):
        team_info = TEAMS[team]
        color = team_info["color"]
        color2 = team_info["color2"]
        name = team_info["name"]
        y_pos = legend_top - (i * legend_spacing)
        x_center = 1.025
        
        # True circle (aspect-ratio corrected)
        fig.add_shape(
            type="circle",
            xref="paper", yref="paper",
            x0=x_center - x_r, y0=y_pos - y_r,
            x1=x_center + x_r, y1=y_pos + y_r,
            fillcolor=color,
            line=dict(color=color2, width=2),
        )
        
        # Team name - bigger
        fig.add_annotation(
            x=1.05, y=y_pos,
            xref="paper", yref="paper",
            text=name,
            showarrow=False,
            font=dict(size=15, color=text_color, family="Arial, sans-serif"),
            xanchor="left",
            yanchor="middle",
        )
        
        # Record - bigger, bold
        record_sign = "+" if record > 0 else ""
        record_color = "#059669" if record > 0 else ("#dc2626" if record < 0 else muted_text)
        fig.add_annotation(
            x=1.15, y=y_pos,
            xref="paper", yref="paper",
            text=f"<b>{record_sign}{record}</b>",
            showarrow=False,
            font=dict(size=14, color=record_color, family="Arial, sans-serif"),
            xanchor="right",
            yanchor="middle",
        )

    # Add .500 line label
    fig.add_annotation(
        x=0, y=0,
        text=".500",
        showarrow=False,
        font=dict(size=12, color=muted_text),
        xanchor="right",
        xshift=-8,
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
