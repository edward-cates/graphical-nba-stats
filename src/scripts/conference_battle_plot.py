"""Generate East vs West conference battle plot."""

import base64
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import plotly.graph_objects as go

from src.scrape.teams import TEAMS
from src.scrape.team_wins_losses import get_team_wins_losses_cached

# Logo directory
LOGO_DIR = Path("img/logos")


def get_logo_base64(name: str) -> str | None:
    """Load logo and return as base64 data URI."""
    logo_path = LOGO_DIR / f"{name}.png"
    if not logo_path.exists():
        return None
    with open(logo_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{b64}"


def get_cache_date_suffix() -> str:
    """Get today's date as YY-MM-DD for cache filename."""
    return datetime.now().strftime("%y-%m-%d")


def compute_conference_battle() -> dict:
    """Compute East vs West daily results."""
    # Get all teams grouped by conference
    east_teams = [abbr for abbr, info in TEAMS.items() if info["conference"] == "east"]
    west_teams = [abbr for abbr, info in TEAMS.items() if info["conference"] == "west"]
    
    # Track wins by date: east_wins[date] = number of East wins over West that day
    daily_east_wins = defaultdict(int)
    daily_west_wins = defaultdict(int)
    
    # Process all East team games
    for team in east_teams:
        results = get_team_wins_losses_cached(team)
        for game in results:
            opp = game["opponent_abbrev"]
            # Only count inter-conference games
            if opp in west_teams:
                date = game["date"]
                if game["win"]:
                    daily_east_wins[date] += 1
                else:
                    daily_west_wins[date] += 1
    
    # Get all dates sorted
    all_dates = sorted(set(daily_east_wins.keys()) | set(daily_west_wins.keys()))
    
    # Build cumulative series
    cumulative = []
    running_total = 0
    for date in all_dates:
        east_w = daily_east_wins[date]
        west_w = daily_west_wins[date]
        running_total += east_w - west_w
        cumulative.append({
            "date": date,
            "east_wins": east_w,
            "west_wins": west_w,
            "cumulative": running_total,
        })
    
    return {
        "daily": cumulative,
        "total_east": sum(daily_east_wins.values()),
        "total_west": sum(daily_west_wins.values()),
    }


def get_conference_battle_cached(cache_dir: Path = Path(".conference_battle")) -> dict:
    """Get conference battle data, using cache if available."""
    cache_dir.mkdir(exist_ok=True)
    date_suffix = get_cache_date_suffix()
    cache_file = cache_dir / f"battle_data-{date_suffix}.json"

    if cache_file.exists():
        print("conference-battle: cached")
        return json.loads(cache_file.read_text())

    print("conference-battle: computing...")
    data = compute_conference_battle()
    cache_file.write_text(json.dumps(data, indent=2))
    return data


def parse_date(date_str: str) -> datetime:
    """Parse date string YY-MM-DD to datetime."""
    return datetime.strptime(date_str, "%y-%m-%d")


def generate_conference_battle_plot(output_dir: Path = Path(".conference_battle")):
    """Generate and save the conference battle plot."""
    output_dir.mkdir(exist_ok=True)

    data = get_conference_battle_cached(output_dir)
    daily = data["daily"]
    total_east = data["total_east"]
    total_west = data["total_west"]

    if not daily:
        print("No inter-conference games found")
        return None

    # Parse dates and values
    dates = [parse_date(d["date"]) for d in daily]
    cumulative = [d["cumulative"] for d in daily]

    # Colors - vibrant 2025 palette
    bg_color = "#ffffff"
    plot_bg = "#fafafa"
    grid_color = "#e5e5e5"
    text_color = "#1f2937"
    muted_text = "#6b7280"
    east_color = "#2563eb"  # Vibrant blue
    west_color = "#ef4444"  # Vibrant red
    line_color = "#0f172a"  # Rich dark slate

    fig = go.Figure()

    # Create positive and negative fill arrays (clamped to zero)
    pos_y = [max(0, v) for v in cumulative]
    neg_y = [min(0, v) for v in cumulative]

    # Fill for East winning (positive, blue) - vivid
    fig.add_trace(go.Scatter(
        x=dates,
        y=pos_y,
        fill='tozeroy',
        fillcolor='rgba(37, 99, 235, 0.5)',
        line=dict(width=0),
        hoverinfo='skip',
        showlegend=False,
    ))

    # Fill for West winning (negative, red) - vivid
    fig.add_trace(go.Scatter(
        x=dates,
        y=neg_y,
        fill='tozeroy',
        fillcolor='rgba(239, 68, 68, 0.5)',
        line=dict(width=0),
        hoverinfo='skip',
        showlegend=False,
    ))

    # Main line - linear
    fig.add_trace(go.Scatter(
        x=dates,
        y=cumulative,
        mode='lines',
        line=dict(color=line_color, width=2.5),
        hovertemplate="<b>%{x|%b %d}</b><br>East %{customdata}<extra></extra>",
        customdata=[f"+{v}" if v > 0 else str(v) for v in cumulative],
        showlegend=False,
    ))

    # End marker with glow effect
    final_val = cumulative[-1]
    marker_color = east_color if final_val > 0 else (west_color if final_val < 0 else muted_text)
    fig.add_trace(go.Scatter(
        x=[dates[-1]],
        y=[final_val],
        mode='markers',
        marker=dict(size=12, color=marker_color, line=dict(color='white', width=2.5)),
        hoverinfo='skip',
        showlegend=False,
    ))

    chart_w, chart_h = 900, 450

    fig.update_layout(
        font=dict(family="Arial, Helvetica, sans-serif", color=text_color),
        plot_bgcolor=plot_bg,
        paper_bgcolor=bg_color,
        xaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            tickfont=dict(size=11, color=muted_text),
            linecolor=grid_color,
            tickformat="%b %d",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            zeroline=True,
            zerolinecolor="#9ca3af",
            zerolinewidth=1.5,
            tickfont=dict(size=11, color=muted_text),
            linecolor=grid_color,
        ),
        showlegend=False,
        margin=dict(l=45, r=20, t=80, b=35),
        width=chart_w,
        height=chart_h,
        hovermode="x unified",
    )

    # Title - more prominent
    today = datetime.now().strftime("%B %d, %Y")
    fig.add_annotation(
        x=0.0, y=1.14,
        xref="paper", yref="paper",
        text="<b>East vs West</b>",
        showarrow=False,
        font=dict(size=24, color=text_color, family="Arial, Helvetica, sans-serif"),
        xanchor="left",
    )
    fig.add_annotation(
        x=0.0, y=1.05,
        xref="paper", yref="paper",
        text=f"2025–26 Season  ·  {today}",
        showarrow=False,
        font=dict(size=13, color=muted_text, family="Arial, Helvetica, sans-serif"),
        xanchor="left",
    )

    # Current record annotation - bold and prominent
    fig.add_annotation(
        x=0.88, y=1.10,
        xref="paper", yref="paper",
        text=f"<b>{total_east}–{total_west}</b>",
        showarrow=False,
        font=dict(size=26, color=text_color, family="Arial, Helvetica, sans-serif"),
        xanchor="center",
        yanchor="middle",
    )

    # Text watermarks - EAST at top, WEST at bottom, both centered
    fig.add_annotation(
        x=0.5, y=0.97,
        xref="paper", yref="paper",
        text="EAST",
        showarrow=False,
        font=dict(size=40, color=east_color, family="Arial Black, Arial, sans-serif"),
        opacity=0.15,
        xanchor="center",
        yanchor="top",
    )
    
    fig.add_annotation(
        x=0.5, y=0.03,
        xref="paper", yref="paper",
        text="WEST",
        showarrow=False,
        font=dict(size=40, color=west_color, family="Arial Black, Arial, sans-serif"),
        opacity=0.15,
        xanchor="center",
        yanchor="bottom",
    )
    
    # Conference logos flanking the record - tight to record
    east_logo = get_logo_base64("east")
    west_logo = get_logo_base64("west")
    logo_y = 1.10
    logo_size = 0.10
    
    if east_logo:
        fig.add_layout_image(dict(
            source=east_logo,
            xref="paper",
            yref="paper",
            x=0.82,
            y=logo_y,
            sizex=logo_size,
            sizey=logo_size,
            xanchor="right",
            yanchor="middle",
        ))
    
    if west_logo:
        fig.add_layout_image(dict(
            source=west_logo,
            xref="paper",
            yref="paper",
            x=0.94,
            y=logo_y,
            sizex=logo_size,
            sizey=logo_size,
            xanchor="left",
            yanchor="middle",
        ))

    # Save
    output_path = output_dir / "conference_battle.png"
    fig.write_image(str(output_path), scale=2)
    print(f"Saved: {output_path}")

    return output_path


if __name__ == "__main__":
    generate_conference_battle_plot()

