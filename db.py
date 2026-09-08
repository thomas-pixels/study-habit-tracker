"""Database helpers for the Study Habit Tracker.

Uses Python's built-in sqlite3 module. No ORM.
"""

import sqlite3

from flask import current_app, g

from log import logged

from log import logged


def get_db():
    """Return one database connection per request (stored in Flask's g)."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_error=None):
    """Close the database connection when the request ends."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create the study_sessions table if it does not exist yet."""
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            duration INTEGER NOT NULL,
            note TEXT,
            date TEXT NOT NULL
        )
        """
    )
    db.commit()


@logged
def insert_session(subject: str, duration: int, note: str, date: str) -> int:
    """Store one study session and return its new id."""
    db = get_db()
    cursor = db.execute(
        "INSERT INTO study_sessions (subject, duration, note, date) "
        "VALUES (?, ?, ?, ?)",
        (subject, duration, note, date),
    )
    db.commit()
    return cursor.lastrowid


@logged
def get_session(session_id: int):
    """Return one study session by id, or None if it does not exist."""
    db = get_db()
    row = db.execute(
        "SELECT id, subject, duration, note, date FROM study_sessions "
        "WHERE id = ?",
        (session_id,),
    ).fetchone()
    return row


@logged
def get_all_sessions():
    """Return all study sessions, newest first (by date, then by newest id)."""
    db = get_db()
    rows = db.execute(
        "SELECT id, subject, duration, note, date FROM study_sessions "
        "ORDER BY date DESC, id DESC"
    ).fetchall()
    return rows


@logged
def delete_session(session_id: int) -> None:
    """Delete one study session by id."""
    db = get_db()
    db.execute("DELETE FROM study_sessions WHERE id = ?", (session_id,))
    db.commit()