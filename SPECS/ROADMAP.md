# ROADMAP

## Current state

The core app is built and working. A student can:

- log a study session (subject, duration, note, date);
- see it appear in the session list;
- delete a session;
- see a last-7-days strip, a streak counter, and total hours per subject.

All 26 automated tests pass (`python -m pytest`).

## Next steps (in order)

1. **Walking skeleton** — log a study session and see it appear on the page.
   This is the thinnest end-to-end slice that works. ✅ Done
2. **Last-7-days strip** — show a row of boxes for the last 7 days, filled for
   days a study session was logged. ✅ Done
3. **Streak counter** — show how many days in a row the student studied.
   ✅ Done
4. **Total hours per subject** — show where the student's study time goes.
   ✅ Done

Remaining polish before closing this milestone:

- Manual end-to-end check in the browser (add a session, restart the server,
  confirm data persists, delete a session).
- Update the walking-skeleton feature-spec checkboxes in
  `SPECS/2026-09-07-walking-skeleton/` to match reality.

## Next ideas (after the core app is stable)

- Combine the strip + streak + hours into a clearer daily "progress view."
  ✅ Done (2026-09-08)
- Cap subject names to a fixed list to avoid typos ("Math" vs "maths").
  ✅ Done (2026-09-08)

## Long-term vision

A simple, reliable study-habit tracker that a student opens after each
session to log it, and that gives them a clear daily view of their progress.
The app stays small, clean, and easy to learn from.