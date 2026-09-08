# Walking Skeleton — Validation

## How we know this feature works

The walking skeleton is done when all four of the following checks pass.

---

### 1. Add a record and confirm it appears in the UI

- [ ] Run `python app.py` and visit `http://localhost:3000/`.
- [ ] Fill in the form: subject = "Math", duration = 60, note = "Algebra
      homework", date = today's date.
- [ ] Click "Log session".
- [ ] The page reloads and a new row appears in the list with subject "Math",
      duration "60 min", note "Algebra homework", and today's date.
- [ ] Confirm the database file `study_tracker.db` now contains one row
      (checked via a simple test or sqlite3 command line).

### 2. Stop the server, restart it, confirm the record is still there

- [ ] Stop the server (Ctrl-C).
- [ ] Run `python app.py` again.
- [ ] Visit the page — the "Math / 60 min" session is still in the list.
- [ ] This confirms the SQLite file is written to disk and survives restarts.

### 3. Submit invalid data and confirm the error is handled

- [ ] On the same page, submit the form with an **empty subject** (duration
      and date filled in).
- [ ] The page reloads with an error message near the form (e.g. "Please
      enter a subject.").
- [ ] No new row is added — the list still shows only the original "Math"
      session.
- [ ] Repeat with duration = "abc": an error appears and nothing is stored.
- [ ] Repeat with duration = "0": an error appears and nothing is stored.
- [ ] Repeat with duration = "1441": an error appears and nothing is stored.

### 4. Delete a record and confirm it is gone

- [ ] On the list, click "Delete" next to the "Math" session.
- [ ] The page reloads and the list is empty (the session is gone).
- [ ] Check `study_tracker.db` directly — the table is empty.

---

## Automated tests

In addition to the manual checks above, `python -m pytest` must exit 0 with
no failing tests. Tests cover at minimum:

- Storing a session inserts a row with all fields.
- Fetching sessions returns them newest-first.
- Deleting a session removes it from the database.
- Empty subject is rejected.
- Non-integer / zero / negative / >1440 duration is rejected.
- A valid POST adds the session and it appears in the HTML response.
- An invalid POST shows an error and stores nothing.

## When it can be merged

- All four manual checks pass.
- `python -m pytest` exits 0.
- The user has reviewed the result and approves.