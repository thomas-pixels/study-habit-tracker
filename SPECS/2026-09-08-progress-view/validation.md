# Progress View — Validation

## How we know this feature works

The progress view is done when all of the following hold.

### Automated tests

- `python -m pytest` exits 0 with no failing tests.
- Tests cover at minimum:
  - the streak message helper returns the right headline for streaks 0, 1,
    3, and 7+;
  - GET `/` shows the "Your progress" section;
  - GET `/` shows the streak headline once a session is logged;
  - GET `/` with no sessions shows "Start your streak today!";
  - all existing behaviors still pass (log, validate, delete, stats).

### Manual checks in the browser

1. **Add a record & see the progress view update.**
   - [x] Open the page: no sessions → "Start your streak today!" and an empty
     strip.
   - [x] Log a session for today → the streak headline counts it and today's box
     fills.
   - [x] Log sessions for several past days → the strip fills for those days and
     the headline counts them.

2. **Restart the server.**
   - [x] Stop and restart `python app.py`.
   - [x] The page still shows the same headline, strip, and session list (data
     persisted in SQLite).

3. **Invalid data still handled.**
   - [x] Submit an empty subject → error message, nothing stored.
   - [x] Submit duration "0" / "1441" → error message, nothing stored.

4. **Delete still works.**
   - [x] Delete a session → it disappears; strip/streak update accordingly.

### Layout check

- The main page shows, top to bottom: log form → "Your progress" (streak
  headline + 7-day strip) → hours per subject → session list.
- The page remains readable in a normal browser window.

## When it can be merged

- All automated tests pass.
- All manual checks pass.
- Any difference between the spec and the built result has been surfaced and
  approved by the user.
- The ROADMAP is updated to reflect the completed progress view.