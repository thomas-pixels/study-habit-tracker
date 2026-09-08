# Walking Skeleton — Requirements

## Context

This is the first step in the ROADMAP: the thinnest end-to-end slice of the
Study Habit Tracker that works. Today the app has no code at all, so this
feature builds the very first working version.

The goal is a complete loop: the student fills in a form, submits it, sees it
appear in the list, and can delete it. Everything else (last-7-days strip,
streak, hours per subject) comes in later steps and is not part of this spec.

## Scope

In scope:

- A single web page with a "Log a study session" form and a session list.
- Form fields: subject (free text), duration (minutes), note (optional), date
  (defaults to today, changeable).
- On submit, validation runs; if valid, the session is stored in the SQLite
  database and appears in the list on the same page.
- On submit, if invalid, a friendly error message appears and nothing is
  stored.
- A "Delete" link on each session that removes it from the database and the
  list.
- Data survives a server restart (SQLite on disk).
- Simple vanilla HTML/CSS/JS; no frameworks.

Out of scope (later steps):

- Last-7-days strip, streak counter, total hours per subject.
- Editing a session (changing its fields after logging).
- Any styling beyond clean, readable basics.

## User story

> As a student, I can log a study session (subject, minutes, optional note,
> date) and see it appear in the list, then delete it if I made a mistake —
> and the data is still there after a restart.

---

## Entities to store

One entity: **Study Session**.

### Required fields

| Field | Type | Constraint | Example |
|-------|------|------------|---------|
| `id` | INTEGER | Primary key, auto-increment, set by the database | `1` |
| `subject` | TEXT | Not empty after trimming whitespace | `"Math"` |
| `duration` | INTEGER | Greater than zero, at most 1440 (one day in minutes) | `60` |
| `note` | TEXT | Optional; may be empty or blank | `"Reviewed algebra"` |
| `date` | TEXT | Not empty; stored as `YYYY-MM-DD` | `"2026-09-07"` |

### Constraints

- **subject:** must not be empty or whitespace only.
- **duration:** must be a whole number, greater than zero, at most 1440.
- **date:** must be present and in `YYYY-MM-DD` format.
- **note:** no constraint; a blank note is allowed.

---

## What the user sees after each action

### Log a study session (valid form)

- The page refreshes.
- The new session appears at the top of the list (newest first).
- The form is shown again, ready for the next session.

### Log a study session (invalid form)

- A friendly error message appears near the form (e.g. "Please enter a
  subject.").
- Nothing is stored in the database.
- The form values the student entered are kept in the form so they do not
  have to retype everything.

### Delete a session

- The student clicks "Delete" on a session row.
- A confirmation page (or a `POST` request) removes the session from the
  database.
- The page reloads and the session is gone from the list.

---

## Behaviour after a server restart

The SQLite database is a file on disk (`study_tracker.db`). When the server
stops and starts again, all saved sessions are still there and appear in the
list as before.

---

## Data model (SQLite)

Single table, one row per session:

```
Table: study_sessions
- id:        INTEGER PRIMARY KEY AUTOINCREMENT
- subject:   TEXT    NOT NULL
- duration:  INTEGER NOT NULL
- note:      TEXT
- date:      TEXT    NOT NULL  (YYYY-MM-DD)
```

Uses Python's built-in `sqlite3` module. No ORM.

## Constraints

- Flask for the server, vanilla HTML/CSS/JS for the page.
- SQLite for storage (data survives restarts).
- Red/Green TDD: tests are written before the feature code.
- Business logic stays separate from logging logic (logging via decorators).