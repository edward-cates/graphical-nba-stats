"""Generate head-to-head differential heatmap for all NBA teams."""

import base64
import json
from datetime import datetime
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from src.scrape.teams import TEAMS
from src.scrape.team_wins_losses import get_team_wins_losses_cached

# Logo directory
LOGO_DIR = Path("img/logos")


def get_cache_date_suffix() -> str:
    """Get today's date as YY-MM-DD for cache filename."""
    return datetime.now().strftime("%y-%m-%d")


def get_logo_base64(team: str) -> str | None:
    """Load team logo and return as base64 data URI."""
    logo_path = LOGO_DIR / f"{team}.png"
    if not logo_path.exists():
        return None
    with open(logo_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{b64}"


def compute_head_to_head() -> dict:
    """Compute head-to-head records for all teams."""
    all_teams = list(TEAMS.keys())
    
    # wins[team_a][team_b] = number of wins team_a has over team_b
    wins = {team: {opp: 0 for opp in all_teams} for team in all_teams}
    
    # Track total wins for sorting
    total_wins = {team: 0 for team in all_teams}
    
    for team in all_teams:
        results = get_team_wins_losses_cached(team)
        for game in results:
            if game["win"]:
                total_wins[team] += 1
                opp = game["opponent_abbrev"]
                if opp in wins[team]:
                    wins[team][opp] += 1
    
    return {
        "wins": wins,
        "total_wins": total_wins,
    }


def get_head_to_head_cached(cache_dir: Path = Path(".head_to_head")) -> dict:
    """Get head-to-head data, using cache if available."""
    cache_dir.mkdir(exist_ok=True)
    date_suffix = get_cache_date_suffix()
    cache_file = cache_dir / f"h2h_data-{date_suffix}.json"

    if cache_file.exists():
        print("head-to-head: cached")
        return json.loads(cache_file.read_text())

    print("head-to-head: computing...")
    data = compute_head_to_head()
    cache_file.write_text(json.dumps(data, indent=2))
    return data


def generate_head_to_head_plot(output_dir: Path = Path(".head_to_head")):
    """Generate and save the head-to-head heatmap."""
    output_dir.mkdir(exist_ok=True)

    data = get_head_to_head_cached(output_dir)
    wins = data["wins"]
    total_wins = data["total_wins"]

    # Sort teams by total wins (best first)
    sorted_teams = sorted(total_wins.keys(), key=lambda t: -total_wins[t])
    n = len(sorted_teams)

    # Build matrices
    diff_matrix = np.zeros((n, n))
    wins_a_matrix = np.zeros((n, n), dtype=int)
    wins_b_matrix = np.zeros((n, n), dtype=int)
    
    for i, team_a in enumerate(sorted_teams):
        for j, team_b in enumerate(sorted_teams):
            w_a = wins[team_a][team_b]
            w_b = wins[team_b][team_a]
            wins_a_matrix[i, j] = w_a
            wins_b_matrix[i, j] = w_b
            diff_matrix[i, j] = w_a - w_b

    # Colors
    bg_color = "#ffffff"
    text_color = "#1f2937"
    unplayed_color = "#1a1a1a"

    # Build custom z values and colors for each cell
    # We need to handle unplayed cells specially
    z_display = []
    colors = []
    annotations = []
    
    for i in range(n):
        z_row = []
        color_row = []
        for j in range(n):
            w_a = wins_a_matrix[i, j]
            w_b = wins_b_matrix[i, j]
            diff = diff_matrix[i, j]
            played = (w_a + w_b) > 0 and i != j
            
            if not played:
                z_row.append(None)  # Will use special color
                color_row.append(unplayed_color)
            else:
                z_row.append(diff)
                # Color based on differential
                if diff > 0:
                    # Green shades
                    intensity = min(abs(diff) / 3, 1)
                    r = int(240 - intensity * 180)
                    g = int(250 - intensity * 60)
                    b = int(240 - intensity * 180)
                    color_row.append(f"rgb({r},{g},{b})")
                elif diff < 0:
                    # Red shades
                    intensity = min(abs(diff) / 3, 1)
                    r = int(250 - intensity * 30)
                    g = int(240 - intensity * 160)
                    b = int(240 - intensity * 160)
                    color_row.append(f"rgb({r},{g},{b})")
                else:
                    color_row.append("#f0f0f0")
                
                # Add annotation for record
                font_color = "#ffffff" if abs(diff) >= 2 else text_color
                annotations.append(dict(
                    x=j,
                    y=i,
                    text=f"{w_a}-{w_b}",
                    showarrow=False,
                    font=dict(size=10, color=font_color, family="Arial"),
                    xref="x",
                    yref="y",
                ))
        
        z_display.append(z_row)
        colors.append(color_row)

    # Create figure with custom colored cells using shapes
    fig = go.Figure()

    # Draw colored rectangles for each cell
    shapes = []
    for i in range(n):
        for j in range(n):
            shapes.append(dict(
                type="rect",
                x0=j - 0.5,
                x1=j + 0.5,
                y0=i - 0.5,
                y1=i + 0.5,
                fillcolor=colors[i][j],
                line=dict(color="#e0e0e0", width=0.5),
                layer="below",
            ))

    # Hover text
    hover_text = []
    for i, team_a in enumerate(sorted_teams):
        row = []
        for j, team_b in enumerate(sorted_teams):
            w_a = wins_a_matrix[i, j]
            w_b = wins_b_matrix[i, j]
            if i == j:
                row.append("")
            elif (w_a + w_b) == 0:
                row.append(f"{TEAMS[team_a]['name']} vs {TEAMS[team_b]['name']}: not played yet")
            else:
                row.append(f"{TEAMS[team_a]['name']} {w_a}-{w_b} vs {TEAMS[team_b]['name']}")
        hover_text.append(row)

    # Invisible heatmap for hover functionality
    fig.add_trace(go.Heatmap(
        z=[[0] * n for _ in range(n)],
        x=list(range(n)),
        y=list(range(n)),
        text=hover_text,
        hovertemplate="%{text}<extra></extra>",
        showscale=False,
        opacity=0,
    ))

    # Layout
    chart_size = 1000
    
    fig.update_layout(
        shapes=shapes,
        annotations=annotations,
        font=dict(family="Arial, Helvetica, sans-serif", color=text_color),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-1.8, n - 0.5],
            constrain="domain",
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[n + 0.8, -0.5],
            scaleanchor="x",
            constrain="domain",
        ),
        width=chart_size,
        height=chart_size,
        margin=dict(l=5, r=5, t=50, b=5),
    )

    # Title - clean and understated
    today = datetime.now().strftime("%B %d, %Y")
    fig.add_annotation(
        x=0.5,
        y=1.045,
        xref="paper",
        yref="paper",
        text="Head-to-Head",
        showarrow=False,
        font=dict(
            size=18,
            color=text_color,
            family="Arial, Helvetica, sans-serif",
        ),
        xanchor="center",
    )
    fig.add_annotation(
        x=0.5,
        y=1.018,
        xref="paper",
        yref="paper",
        text=f"2025–26 Season  ·  {today}",
        showarrow=False,
        font=dict(
            size=11,
            color="#6b7280",
            family="Arial, Helvetica, sans-serif",
        ),
        xanchor="center",
    )

    # Add logos on axes using data coordinates
    logo_size_data = 0.9  # Size in data units (slightly smaller than 1 cell)
    
    for idx, team in enumerate(sorted_teams):
        logo_b64 = get_logo_base64(team)
        if logo_b64:
            # Y-axis logo (left side)
            fig.add_layout_image(dict(
                source=logo_b64,
                xref="x",
                yref="y",
                x=-1.0,
                y=idx,
                sizex=logo_size_data,
                sizey=logo_size_data,
                xanchor="center",
                yanchor="middle",
            ))
            
            # X-axis logo (bottom)
            fig.add_layout_image(dict(
                source=logo_b64,
                xref="x",
                yref="y",
                x=idx,
                y=n,
                sizex=logo_size_data,
                sizey=logo_size_data,
                xanchor="center",
                yanchor="middle",
            ))

    # Save
    output_path = output_dir / "head_to_head.png"
    fig.write_image(str(output_path), scale=2)
    print(f"Saved: {output_path}")

    return output_path


if __name__ == "__main__":
    generate_head_to_head_plot()
