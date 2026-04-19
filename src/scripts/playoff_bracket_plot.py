"""2025-26 NBA playoff bracket with regular-season H2H records.

Round 1 matchups are current; later rounds are PROJECTIONS that advance
whichever team won the regular-season series (higher seed breaks ties).
Every box shows the regular-season head-to-head record.
"""

import json
from dataclasses import dataclass
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib.patches import FancyBboxPatch, Rectangle

from src.scrape.team_wins_losses import get_team_wins_losses_cached
from src.scrape.teams import TEAMS

BRACKET_DATA = Path(__file__).resolve().parent.parent / "data" / "playoff_bracket.json"


@dataclass
class Matchup:
    seed_a: int
    team_a: str
    seed_b: int
    team_b: str
    note: str = ""


def load_round1() -> tuple[list[Matchup], list[Matchup]]:
    data = json.loads(BRACKET_DATA.read_text())
    west = [Matchup(**m) for m in data["west_r1"]]
    east = [Matchup(**m) for m in data["east_r1"]]
    return west, east


def compute_h2h(team_a: str, team_b: str) -> tuple[int, int]:
    results = get_team_wins_losses_cached(team_a)
    a_wins = sum(1 for g in results if g["opponent_abbrev"] == team_b and g["win"])
    b_wins = sum(1 for g in results if g["opponent_abbrev"] == team_b and not g["win"])
    return a_wins, b_wins


def h2h_winner(m: Matchup) -> tuple[int, str]:
    wa, wb = compute_h2h(m.team_a, m.team_b)
    if wa > wb:
        return m.seed_a, m.team_a
    if wb > wa:
        return m.seed_b, m.team_b
    return (m.seed_a, m.team_a) if m.seed_a < m.seed_b else (m.seed_b, m.team_b)


def project_next_round(pairs: list[Matchup]) -> list[Matchup]:
    out = []
    for i in range(0, len(pairs), 2):
        s1, t1 = h2h_winner(pairs[i])
        s2, t2 = h2h_winner(pairs[i + 1])
        if s1 <= s2:
            out.append(Matchup(s1, t1, s2, t2))
        else:
            out.append(Matchup(s2, t2, s1, t1))
    return out


# ───────── theme ─────────

BG            = "#0a0f1c"
BG_PANEL      = "#0f1627"
CARD_FG       = "#1a2338"
CARD_FG_PROJ  = "#141c30"
CARD_BORDER   = "#2a344c"
FINALS_BORDER = "#f59e0b"
TEXT_PRIMARY  = "#f1f5f9"
TEXT_SECOND   = "#cbd5e1"
TEXT_MUTED    = "#64748b"
TEXT_DIM      = "#475569"
GOLD          = "#fbbf24"
WEST_HUE      = "#ef4444"
EAST_HUE      = "#60a5fa"
DIVIDER       = "#2a344c"
CONNECTOR     = "#3a4560"

BOX_W = 2.75
BOX_H = 1.70


def draw_team_row(ax, team, seed, wins, x_center, y, is_winner, logo_zoom):
    team_color = TEAMS[team]["color"]

    # Winner accent bar
    if is_winner:
        ax.add_patch(Rectangle(
            (x_center - BOX_W / 2 + 0.045, y - 0.30),
            0.07, 0.54,
            facecolor=team_color, edgecolor="none", zorder=3,
        ))

    # Seed
    seed_color = TEXT_SECOND if is_winner else TEXT_DIM
    ax.text(x_center - BOX_W / 2 + 0.25, y, str(seed),
            ha="center", va="center", fontsize=19,
            color=seed_color, fontweight="bold", zorder=4)

    # Logo (slightly dimmed for losers)
    logo_path = Path("img/logos") / f"{team}.png"
    if logo_path.exists():
        img = mpimg.imread(logo_path)
        alpha = 1.0 if is_winner else 0.45
        im = OffsetImage(img, zoom=logo_zoom, alpha=alpha)
        ab = AnnotationBbox(im, (x_center - BOX_W / 2 + 0.60, y),
                            frameon=False, pad=0)
        ax.add_artist(ab)

    # Team name
    name_color = TEXT_PRIMARY if is_winner else TEXT_MUTED
    name_weight = "bold" if is_winner else "normal"
    ax.text(x_center - BOX_W / 2 + 0.95, y, TEAMS[team]["name"],
            ha="left", va="center", fontsize=22,
            color=name_color, fontweight=name_weight, zorder=4)

    # Win count — white for winners (team color used for the side bar instead)
    win_color = TEXT_PRIMARY if is_winner else TEXT_DIM
    ax.text(x_center + BOX_W / 2 - 0.18, y, str(wins),
            ha="right", va="center", fontsize=34,
            color=win_color, fontweight="bold", zorder=4)


def draw_matchup(ax, matchup: Matchup, x_center: float, y_center: float,
                 projected: bool, is_finals: bool = False,
                 logo_zoom: float = 0.42):
    wa, wb = compute_h2h(matchup.team_a, matchup.team_b)

    fc = CARD_FG_PROJ if projected else CARD_FG
    ec = FINALS_BORDER if is_finals else CARD_BORDER
    lw = 2.0 if is_finals else 1.1

    ax.add_patch(FancyBboxPatch(
        (x_center - BOX_W / 2, y_center - BOX_H / 2), BOX_W, BOX_H,
        boxstyle="round,pad=0.01,rounding_size=0.06",
        linewidth=lw, edgecolor=ec, facecolor=fc, zorder=1,
    ))

    # "REG. SEASON H2H" ribbon
    label_color = GOLD if is_finals else "#94a3b8"
    ax.text(x_center, y_center + BOX_H / 2 - 0.18,
            "REG. SEASON H2H",
            ha="center", va="center", fontsize=11,
            color=label_color, fontweight="bold", zorder=4)

    # Divider between team rows
    ax.plot([x_center - BOX_W / 2 + 0.10, x_center + BOX_W / 2 - 0.10],
            [y_center - 0.14, y_center - 0.14],
            color=DIVIDER, lw=0.8, zorder=2)

    draw_team_row(ax, matchup.team_a, matchup.seed_a, wa,
                  x_center, y_center + 0.26,
                  is_winner=(wa > wb), logo_zoom=logo_zoom)
    draw_team_row(ax, matchup.team_b, matchup.seed_b, wb,
                  x_center, y_center - 0.48,
                  is_winner=(wb > wa), logo_zoom=logo_zoom)

    # Bottom note
    if matchup.note:
        ax.text(x_center, y_center - BOX_H / 2 - 0.10, matchup.note,
                ha="center", va="top", fontsize=12, color=TEXT_SECOND,
                style="italic")
    elif projected:
        ax.text(x_center, y_center - BOX_H / 2 - 0.10, "projected",
                ha="center", va="top", fontsize=11, color=TEXT_MUTED,
                style="italic")


def draw_connector(ax, x1, y1, x2, y2):
    xmid = (x1 + x2) / 2
    ax.plot([x1, xmid, xmid, x2], [y1, y1, y2, y2],
            color=CONNECTOR, lw=1.4, zorder=0, solid_capstyle="round")


def main():
    fig, ax = plt.subplots(figsize=(26, 15), dpi=160)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 17)
    ax.set_ylim(-0.8, 10.8)
    ax.axis("off")

    # ── Title band ──────────────────────────────────────────────
    ax.add_patch(Rectangle((0, 9.55), 17, 1.25,
                           facecolor=BG_PANEL, edgecolor="none", zorder=0))
    ax.text(8.5, 10.35, "2025–26 NBA PLAYOFFS",
            ha="center", va="center", fontsize=40, fontweight="bold",
            color=TEXT_PRIMARY, zorder=2)
    ax.text(8.5, 9.83,
            "Projected bracket · every box shows the two teams' "
            "regular-season head-to-head record",
            ha="center", va="center", fontsize=15, color=TEXT_SECOND,
            zorder=2)

    # ── Columns ─────────────────────────────────────────────────
    x_west = [1.55, 5.00]
    x_cf = 8.5
    x_east = [15.45, 12.00]

    round_labels = [
        (x_west[0],  "FIRST ROUND"),
        (x_west[1],  "CONF. SEMIS"),
        (x_cf,       "CONFERENCE FINALS"),
        (x_east[1],  "CONF. SEMIS"),
        (x_east[0],  "FIRST ROUND"),
    ]
    for x, label in round_labels:
        ax.text(x, 9.10, label, ha="center", va="center",
                fontsize=14, color=TEXT_SECOND, fontweight="bold")

    ax.text(x_west[0], 8.70, "WESTERN CONFERENCE", ha="center", va="center",
            fontsize=14, color=WEST_HUE, fontweight="bold")
    ax.text(x_east[0], 8.70, "EASTERN CONFERENCE", ha="center", va="center",
            fontsize=14, color=EAST_HUE, fontweight="bold")

    # ── Y positions ─────────────────────────────────────────────
    y_r1 = [7.4, 5.2, 3.0, 0.8]
    y_r2 = [(y_r1[0] + y_r1[1]) / 2, (y_r1[2] + y_r1[3]) / 2]
    # Two conf-finals boxes stacked in the center
    y_cf_west = (y_r2[0] + y_r2[1]) / 2 + 1.2
    y_cf_east = (y_r2[0] + y_r2[1]) / 2 - 1.2

    # ── Projections ─────────────────────────────────────────────
    west_r1, east_r1 = load_round1()
    west_r2 = project_next_round(west_r1)
    west_cf = project_next_round(west_r2)
    east_r2 = project_next_round(east_r1)
    east_cf = project_next_round(east_r2)

    # ── Connectors ──────────────────────────────────────────────
    for i in range(4):
        draw_connector(ax,
                       x_west[0] + BOX_W / 2, y_r1[i],
                       x_west[1] - BOX_W / 2, y_r2[i // 2])
        draw_connector(ax,
                       x_east[0] - BOX_W / 2, y_r1[i],
                       x_east[1] + BOX_W / 2, y_r2[i // 2])
    for i in range(2):
        draw_connector(ax,
                       x_west[1] + BOX_W / 2, y_r2[i],
                       x_cf - BOX_W / 2, y_cf_west)
        draw_connector(ax,
                       x_east[1] - BOX_W / 2, y_r2[i],
                       x_cf + BOX_W / 2, y_cf_east)

    # ── Cards ───────────────────────────────────────────────────
    for m, y in zip(west_r1, y_r1):
        draw_matchup(ax, m, x_west[0], y, projected=False)
    for m, y in zip(east_r1, y_r1):
        draw_matchup(ax, m, x_east[0], y, projected=False)
    for m, y in zip(west_r2, y_r2):
        draw_matchup(ax, m, x_west[1], y, projected=True)
    for m, y in zip(east_r2, y_r2):
        draw_matchup(ax, m, x_east[1], y, projected=True)
    draw_matchup(ax, west_cf[0], x_cf, y_cf_west, projected=True,
                 logo_zoom=0.32)
    draw_matchup(ax, east_cf[0], x_cf, y_cf_east, projected=True,
                 logo_zoom=0.32)

    # Footer credit
    ax.text(8.5, -0.55, "hoopsgraphs.com",
            ha="center", va="center", fontsize=9,
            color=TEXT_DIM, fontweight="bold", alpha=0.7)

    out_dir = Path(".bracket")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "playoff_bracket.png"
    plt.savefig(out_path, dpi=160, bbox_inches="tight",
                facecolor=BG, pad_inches=0.25)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
