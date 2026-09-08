"""Tests for derived statistics (tests written first — Red).

Session rows look like sqlite3.Row objects with keys
subject, duration, note, date. In these tests we use plain dictionaries
with the same keys.
"""

import stats

FIXED_TODAY = "2026-09-07"  # a Monday


def sessions(*records):
    """Build valid session dicts for tests."""
    return [
        {"id": i, "subject": subj, "duration": dur, "note": "n", "date": d}
        for i, (subj, dur, d) in enumerate(records, start=1)
    ]


# --- Last-7-days strip -----------------------------------------------------


def test_last_7_days_returns_study_dates():
    result = stats.last_7_days_strip(
        sessions(("Math", 30, "2026-09-04"), ("History", 45, "2026-09-07")),
        today="2026-09-07",
    )

    # 2026-09-01 .. 2026-09-07, studied only on the 4th and 7th.
    assert result == [
        ("2026-09-01", False),
        ("2026-09-02", False),
        ("2026-09-03", False),
        ("2026-09-04", True),
        ("2026-09-05", False),
        ("2026-09-06", False),
        ("2026-09-07", True),
    ]


def test_last_7_days_all_empty_when_no_sessions():
    result = stats.last_7_days_strip([], today="2026-09-07")
    assert all(studied is False for _, studied in result)
    assert len(result) == 7


def test_last_7_days_ignores_old_sessions():
    result = stats.last_7_days_strip(
        sessions(("Math", 30, "2026-08-20")), today="2026-09-07"
    )
    assert all(studied is False for _, studied in result)


# --- Streak counter ---------------------------------------------------------


def test_streak_counts_consecutive_days_including_today():
    result = stats.streak(
        sessions(
            ("Math", 30, "2026-09-05"),
            ("History", 45, "2026-09-06"),
            ("Science", 40, "2026-09-07"),
        ),
        today="2026-09-07",
    )
    assert result == 3


def test_streak_stops_at_a_gap():
    result = stats.streak(
        sessions(
            ("Math", 30, "2026-09-05"),
            ("History", 45, "2026-09-07"),
        ),
        today="2026-09-07",
    )
    assert result == 1


def test_streak_counts_from_yesterday_when_today_not_logged_yet():
    result = stats.streak(
        sessions(
            ("Math", 30, "2026-09-06"),
            ("History", 45, "2026-09-07"),
        ),
        today="2026-09-08",
    )
    # Today (the 8th) is not logged yet, but yesterday was part of a streak.
    assert result == 2


def test_streak_zero_when_no_recent_study():
    result = stats.streak(
        sessions(("Math", 30, "2026-08-20")), today="2026-09-07"
    )
    assert result == 0


def test_streak_zero_when_nothing_logged():
    assert stats.streak([], today="2026-09-07") == 0


# --- Total hours per subject ------------------------------------------------


def test_hours_per_subject_sums_minutes_and_converts():
    result = stats.hours_per_subject(
        sessions(
            ("Math", 60, "2026-09-05"),
            ("Math", 30, "2026-09-06"),
            ("History", 45, "2026-09-05"),
        )
    )
    assert dict(result) == {"Math": 1.5, "History": 0.8}


def test_hours_per_subject_empty():
    assert stats.hours_per_subject([]) == []


# --- Streak messages --------------------------------------------------------


def test_streak_message_zero():
    headline, message = stats.streak_message(0)
    assert headline == "Start your streak today!"
    assert message == "Log a session to begin."


def test_streak_message_one_uses_singular():
    headline, message = stats.streak_message(1)
    assert headline == "You've studied 1 day in a row!"
    assert "keep going" in message.lower()


def test_streak_message_three_uses_plural():
    headline, _ = stats.streak_message(3)
    assert headline == "You've studied 3 days in a row!"


def test_streak_message_mid_range_encourages():
    _, message = stats.streak_message(3)
    assert "habit" in message.lower()


def test_streak_message_high_range():
    headline, message = stats.streak_message(10)
    assert headline == "You've studied 10 days in a row!"
    assert "amazing" in message.lower()