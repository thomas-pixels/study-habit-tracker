# Walking Skeleton — Plan

Red/Green TDD: for each task group, write the failing test first, watch it
fail (red), then write the minimal code to make it pass (green).

---

## Task group 1 — Project scaffolding & database init

### What gets built

A minimal Flask app that starts, connects to SQLite, and creates the
`study_sessions` table if it does not exist.

### Steps

- [ ] Create `requirements.txt` (Flask).
- [ ] Create `app.py` with a Flask app factory (`create_app()`), bound to
      `0.0.0.0` and a port in 1024–9499.
- [ ] Create `db.py` with `get_db()`, `close_db()`, and `init_db()`.
      `init_db()` runs a `CREATE TABLE IF NOT EXISTS` for `study_sessions`.
- [ ] Verify: `python -m pytest` runs and reports no failures (no tests yet).
- [ ] Verify: `python app.py` starts and creates `study_tracker.db` on disk.

---

## Task group 2 — Data access layer (tests first)

### What gets built

Two functions in `db.py`:

| Function | What it does |
|----------|--------------|
| `insert_session(subject, duration, note, date)` | Stores one row, returns the new `id` |
| `get_all_sessions()` | Returns all rows, newest first (`date DESC, id DESC`) |
| `delete_session(session_id)` | Deletes one row by `id` |

### Tests (red → green)

- [ ] Test: `insert_session` stores a row with all fields correctly.
- [ ] Test: `get_all_sessions` returns rows in newest-first order.
- [ ] Test: `delete_session` removes the row; `get_all_sessions` no longer
      includes it.
- [ ] Write passing code for all three.
- [ ] Check: tests pass (green), then refactor if needed.

---

## Task group 3 — Validation (tests first)

### What gets built

A `validate_session(subject, duration, note, date)` function that returns
`None` on success, or a friendly error string on failure.

### Validation rules

| Field | Rule | Error message (friendly) |
|-------|------|--------------------------|
| subject | must not be empty/whitespace | "Please enter a subject." |
| duration | must be a whole number > 0 and ≤ 1440 | "Duration must be between 1 and 1440 minutes." |
| date | must be present and non-empty | "Please choose a date." |

### Tests (red → green)

- [ ] Test: empty subject → returns an error mentioning "subject".
- [ ] Test: non-number duration → returns an error mentioning "duration".
- [ ] Test: zero / negative duration → returns an error mentioning "duration".
- [ ] Test: duration above 1440 → returns an error mentioning "duration".
- [ ] Test: valid data → returns `None`.
- [ ] Check: tests pass (green).

---

## Task group 4 — Routes (tests first)

### Routes in implementation order

| # | Method | Path | What it does | Template change |
|---|--------|------|--------------|-----------------|
| 1 | GET | `/` | Shows the log form + session list | First version of `index.html` with form and empty list |
| 2 | POST | `/log` | Validates input, stores if valid, re-renders list | Same `index.html`; new session appears at top of list |
| 3 | POST | `/delete/<id>` | Deletes the session by id, redirects to `/` | No template change — redirect back to `/` |

### Tests (red → green)

- [ ] Test: GET `/` returns 200 and contains the form fields (subject,
      duration, note, date).
- [ ] Test: POST `/log` with valid data returns 200, the new session appears
      in the page, and a row exists in the database.
- [ ] Test: POST `/log` with invalid data (empty subject) returns 200, shows
      an error message, and the database still has 0 rows.
- [ ] Test: POST `/delete/1` removes the session and redirects to `/`.
- [ ] Write passing route code.
- [ ] Check: tests pass (green).

---

## Task group 5 — Page template (HTML/CSS)

### Template changes per route

| Route | What the template shows |
|-------|------------------------|
| GET `/` (first load) | Form (subject, duration, note, date defaulting to today) + empty list placeholder |
| POST `/log` (valid) | Form cleared + session at the top of the list |
| POST `/log` (invalid) | Error message above the form + form values retained |
| POST `/delete/<id>` | Redirect to `/` — session gone from the list |

### Steps

- [ ] Build `templates/index.html`:
      - Log form with all four fields.
      - Session list (newest first) below the form.
      - Date field pre-fills with today's date (set server-side).
      - Error message area, shown only when there is an error.
      - "Delete" link on each session row (as a `POST` form for safety).
- [ ] Add minimal vanilla CSS (`static/style.css`) — clean, readable, no
      framework.
- [ ] Verify the form, list, error message, and delete link all render.

---

## Task group 6 — Manual end-to-end verification

- [ ] Run `python app.py`.
- [ ] Visit the page, log a session, confirm it appears in the list.
- [ ] Stop the server, restart it, confirm the session is still in the list.
- [ ] Submit an empty subject, confirm the error message appears.
- [ ] Click "Delete" on a session, confirm it disappears from the list.
- [ ] Bind to `0.0.0.0`, use the Codio public URL, and verify it responds
      before announcing the site is live (see AGENTS.md).

---

## General reminders

- Run `python -m pytest` after each task group.
- Run lint/type checks if configured (add `mypy` only if simple to set up).
- Do not add commentary/comments unless asked; keep code obvious.