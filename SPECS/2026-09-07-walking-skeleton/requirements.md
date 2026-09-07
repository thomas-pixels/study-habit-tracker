# Walking Skeleton — Requirements

## Context

This is the first step in the ROADMAP: the thinnest end-to-end slice of the
Study Habit Tracker that works. Today the app has no code at all, so this
feature builds the very first working version.

The goal is one small loop: the student fills in a form, submits it, and sees
the session appear on the page. Everything else (last-7-days strip, streak,
hours per subject) comes in later steps and is **not** part of this spec.

## Scope

In scope:

- A single web page with a "Log a study session" form.
- Form fields: subject (free text), duration (minutes), note (optional), date
  (defaults to today, changeable).
- On submit, basic validation is checked; if valid, the session is stored in
  the SQLite database.
- The page also shows a chronological list of all logged sessions (newest
  first), so the student can see their session appear.
- Simple vanilla HTML/CSS/JS; no frameworks.

Out of scope (later steps):

- Last-7-days strip, streak counter, total hours per subject.
- Any editing or deleting of sessions.
- Any styling beyond clean, readable basics.

## User story

> As a student, I can log a study session (subject, minutes, optional note,
> date) and immediately see it in the list on the page, so I know the app
> works end to end.

## Decisions (made with the user)

| Question | Decision |
|----------|----------|
| How is the subject entered? | Free-text field |
| How is the date handled? | Defaults to today, changeable |
| What does "see it appear" mean? | A chronological list on the same page |
| How strict is validation? | Basic checks on submit |

## Functional requirements

1. The app serves one page at `/` that contains the log form and the session
   list.
2. The form has a subject text field, a duration number field, an optional
   note field, and a date field that pre-fills with today's date.
3. Submitting a **valid** form stores the session in the `study_sessions`
   table and re-renders the page with the new session in the list.
4. Submitting an **invalid** form shows a friendly error message and does not
   store anything. Validation rules:
   - subject: non-empty
   - duration: a positive whole number (minutes)
5. The list shows all sessions, newest first, with subject, duration, note,
   and date visible.

## Data model

Single SQLite table, one row per session:

```
Table: study_sessions
- id:        INTEGER PRIMARY KEY AUTOINCREMENT
- subject:   TEXT    NOT NULL
- duration:  INTEGER NOT NULL
- note:      TEXT    (optional, may be empty)
- date:      TEXT    NOT NULL  (YYYY-MM-DD)
```

Uses Python's built-in `sqlite3` module. No ORM.

## Constraints

- Flask for the server, vanilla HTML/CSS/JS for the page.
- SQLite for storage (data survives restarts).
- Red/Green TDD: tests are written before the feature code.
- Business logic stays separate from logging logic (logging via decorators).