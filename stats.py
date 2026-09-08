"""Derived statistics: last-7-days strip, streak, hours per subject.

These are computed from the sessions in the database, never stored.
Pure logic — no Flask — so they are easy to test.
"""

from datetime import date, timedelta

from log import logged


def _studied_dates(sessions):
    """Return the set of dates (YYYY-MM-DD) that have at least one session."""
    return {row["date"] for row in sessions}


@logged
def last_7_days_strip(sessions, today=None):
    """Return the last 7 days as (date, studied) pairs, oldest first."""
    today = today or date.today().isoformat()
    today_date = date.fromisoformat(today)
    studied = _studied_dates(sessions)
    result = []
    for days_ago in range(6, -1, -1):
        day = (today_date - timedelta(days=days_ago)).isoformat()
        result.append((day, day in studied))
    return result


@logged
def streak(sessions, today=None):
    """Return how many consecutive study days end on today (or yesterday).

    A day with no session breaks the streak. If today is not logged yet but
    yesterday was, the streak counts from yesterday — the day is not over.
    """
    today = today or date.today().isoformat()
    studied = _studied_dates(sessions)

    current = date.fromisoformat(today)
    if current.isoformat() not in studied:
        # Today not logged yet — the streak may still be alive from yesterday.
        current = current - timedelta(days=1)

    count = 0
    while current.isoformat() in studied:
        count += 1
        current = current - timedelta(days=1)
    return count


@logged
def hours_per_subject(sessions):
    """Return [(subject, total_hours), ...] sorted by hours, highest first.

    Total hours = sum of durations (minutes) / 60, rounded to 1 decimal.
    """
    minutes_by_subject = {}
    for row in sessions:
        subject = row["subject"]
        minutes_by_subject[subject] = minutes_by_subject.get(subject, 0) + row["duration"]

    hours = [(s, round(m / 60, 1)) for s, m in minutes_by_subject.items()]
    return sorted(hours, key=lambda pair: pair[1], reverse=True)


@logged
def streak_message(streak_count):
    """Return (headline, encouraging_message) for a streak count."""
    if streak_count == 0:
        return "Start your streak today!", "Log a session to begin."

    word = "day" if streak_count == 1 else "days"
    headline = f"You've studied {streak_count} {word} in a row!"

    if streak_count == 1:
        message = "A great start — keep going!"
    elif streak_count < 7:
        message = "You're building the habit!"
    else:
        message = "Amazing consistency!"

    return headline, message