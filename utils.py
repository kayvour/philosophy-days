"""utils.py
================
Helper functions for converting symbolic event rules into concrete dates.
Supports three rule types:
  • "fixed"          — same month/day every year
  • "nth_weekday"    — e.g. 3rd Thursday of November
  • "easter_offset"  — X days relative to Easter Sunday
"""
from __future__ import annotations

from datetime import date, timedelta
import calendar

# Weekday lookup for nth_weekday rule
WEEKDAY_LOOKUP = {
    "MON": 0,
    "TUE": 1,
    "WED": 2,
    "THU": 3,
    "FRI": 4,
    "SAT": 5,
    "SUN": 6,
}

# N‑th weekday of month helper

def nth_weekday_of_month(year: int, month: int, weekday: str, n: int) -> date:
    """Return the date of the *n*‑th <weekday> in <month>/<year>."""
    c = calendar.Calendar()
    idx = WEEKDAY_LOOKUP[weekday.upper()]

    valid_days = [
        week[idx]
        for week in c.monthdayscalendar(year, month)
        if week[idx] != 0
    ]

    if n < 1 or n > len(valid_days):
        raise ValueError(f"Month {month}/{year} does not have a {n}th {weekday}.")

    return date(year, month, valid_days[n - 1])

# Easter Sunday (Gregorian) — Meeus/Jones/Butcher algorithm

def easter_sunday(year: int) -> date:
    """Return Easter Sunday for a given Gregorian year."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)

# Core resolver

def resolve_event(ev: dict, year: int) -> date:
    """Convert a single event dictionary into a concrete `datetime.date`."""
    rule = ev.get("rule")

    if rule == "fixed":
        return date(year, ev["month"], ev["day"])

    if rule == "nth_weekday":
        return nth_weekday_of_month(
            year, ev["month"], ev["weekday"], ev["n"]
        )

    if rule == "easter_offset":
        return easter_sunday(year) + timedelta(days=ev["offset"])

    raise ValueError(
        f"Unsupported rule type: {rule!r} (event: {ev.get('name', '<unknown>')})"
    )
