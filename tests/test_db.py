"""Tests for the data access layer (tests written first — Red)."""

import db


def test_insert_session_stores_a_row(app):
    with app.app_context():
        session_id = db.insert_session("Math", 60, "Algebra homework", "2026-09-07")
        row = db.get_session(session_id)

    assert session_id > 0
    assert row["subject"] == "Math"
    assert row["duration"] == 60
    assert row["note"] == "Algebra homework"
    assert row["date"] == "2026-09-07"


def test_get_all_sessions_returns_newest_first(app):
    with app.app_context():
        db.insert_session("Math", 60, "note", "2026-09-05")
        db.insert_session("History", 45, "note", "2026-09-06")
        db.insert_session("Science", 30, "note", "2026-09-07")
        rows = db.get_all_sessions()

    assert [row["subject"] for row in rows] == ["Science", "History", "Math"]


def test_delete_session_removes_the_row(app):
    with app.app_context():
        session_id = db.insert_session("Math", 60, "note", "2026-09-07")
        db.delete_session(session_id)
        rows = db.get_all_sessions()

    assert rows == []