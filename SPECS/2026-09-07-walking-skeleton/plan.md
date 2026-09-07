# Walking Skeleton — Plan

Red/Green TDD: for each task group, write the failing test first, watch it
fail (red), then write the minimal code to make it pass (green).

## Task group 1 — Project scaffolding

- [ ] Create `requirements.txt` with Flask.
- [ ] Create the app entry point `app.py` (a Flask app factory, e.g.
      `create_app()`), bound to `0.0.0.0` and a port in 1024–9499 so it is
      reachable via the Codio public URL.
- [ ] Set up the SQLite database module (`db.py`): open/connect using the
      built-in `sqlite3` module.
- [ ] Create the `study_sessions` table (via a small init function or schema
      applied on startup).
- [ ] Check: `python -m pytest` runs and reports no failures.

## Task group 2 — In-memory-free data access layer (tests first)

- [ ] Write test: inserting a session into `study_sessions` stores a row with
      id, subject, duration, note, date.
- [ ] Write test: fetching all sessions returns them newest-first.
- [ ] Write passing code for both.
- [ ] Check: tests pass (green), then refactor if needed.

## Task group 3 — Validation (tests first)

- [ ] Write test: subject empty → invalid.
- [ ] Write test: duration not a positive whole number → invalid.
- [ ] Write passing validation code (returns error message on invalid).
- [ ] Check: tests pass (green).

## Task group 4 — Routes (tests first)

- [ ] Write test: GET `/` returns 200 and shows the form.
- [ ] Write test: POST a valid session redirects (or re-renders) and the new
      session appears in the list.
- [ ] Write test: POST an invalid session shows an error message and stores
      nothing.
- [ ] Write passing route code.
- [ ] Check: tests pass (green).

## Task group 5 — Page template (HTML/CSS/JS)

- [ ] Minimal page: log form + session list, newest first.
- [ ] Date field pre-fills with today's date (server-side default).
- [ ] Friendly error message shown for invalid submissions.
- [ ] Clean, readable styling with vanilla CSS only.

## Task group 6 — Manual end-to-end verification

- [ ] Run the server (`python app.py`).
- [ ] Visit the page, log a session, confirm it appears in the list.
- [ ] Confirm data survives a server restart (stored in SQLite).
- [ ] Bind to `0.0.0.0`, use the Codio public URL, and verify it responds
      before announcing the site is live (see AGENTS.md).

## General reminders

- Run `python -m pytest` after each task group.
- Run lint/type checks if configured (TECH.md calls for strict typing; add a
  `mypy` or similar check only if it is simple to set up).
- Do not add commentary/comments unless asked; keep code obvious.