from datetime import date


def season_years(today: date | None = None) -> tuple[int, int]:
    """(2026, 2027) for the 2026-27 season. A new season starts in August, before the October tip-off."""
    today = today or date.today()
    first = today.year if today.month >= 8 else today.year - 1
    return first, first + 1


def season_label(dash: str = "-") -> str:
    """'2026-27' (pass dash='–' for the typographic en dash used in graph titles)."""
    first, second = season_years()
    return f"{first}{dash}{second % 100:02d}"
