# Progress View — Plan

Red/Green TDD: write the failing test first (red), then minimal code to make
it pass (green).

## Task group 1 — Message helper (tests first)

### What gets built

A pure function (in `stats.py`) that turns a streak count into a friendly
headline + encouraging message. No Flask, easy to test.

| Streak | Headline | Encouraging message |
|--------|----------|---------------------|
| 0 | "Start your streak today!" | "Log a session to begin." |
| 1 | "You've studied 1 day in a row!" | "A great start — keep going!" |
| 2–6 | "You've studied N days in a row!" | "You're building the habit!" |
| 7+ | "You've studied N days in a row!" | "Amazing consistency!" |

### Tests (red → green)

- [ ] Test: streak 0 → headline "Start your streak today!".
- [ ] Test: streak 1 → headline contains "1 day", singular "day".
- [ ] Test: streak 3 → headline has "3", plural "days".
- [ ] Test: streak 3 → encouraging message for mid-range.
- [ ] Test: streak 10 → "7+" encouraging message.
- [ ] Check: tests pass (green).

## Task group 2 — Route test update (tests first)

### What gets built

The root renderer passes the message data to the template.

### Tests (red → green)

- [ ] Test: GET `/` returns the reworked page containing the word "Your
      progress".
- [ ] Test: with a logged session, GET `/` contains the streak headline
      ("days in a row!").
- [ ] Test: with no sessions, GET `/` contains "Start your streak today!".
- [ ] Update `_render_index` to pass the headline/message into the template.
- [ ] Check: all tests pass (green).

## Task group 3 — Template rework

### What gets built

`templates/index.html` reworked to a progress-led layout:

1. Log form (unchanged, at top).
2. **Progress section**:
   - `h2` "Your progress".
   - Streak headline (from the message helper).
   - Last-7-days strip with day labels and filled boxes.
   - Caption explaining the strip.
   - Encouraging message.
3. Hours-per-subject list (kept, below progress).
4. Session list (unchanged, below).

### Steps

- [ ] Reorder template sections into progress-led layout.
- [ ] Keep all existing elements (form, error, list, delete, hours).
- [ ] Verify the page renders for: 0 sessions, 1 session, many sessions.

## Task group 4 — Styling

- [ ] Style the streak headline and encouraging message (vanilla CSS).
- [ ] Keep the strip styling from before.
- [ ] Ensure the page stays readable at ~640px width.

## Task group 5 — Full-suite + manual verification

- [ ] `python -m pytest` — all tests pass (green).
- [ ] Run `python app.py`, verify through the Codio public URL.
- [ ] Manual checks (per validation.md):
      - log a session → headline updates, strip fills;
      - restart server → data and headline persist;
      - invalid submit → error, nothing stored;
      - delete → session gone, stats update.

## General reminders

- Run `python -m pytest` after each task group.
- Keep code simple and obvious; no clever tricks.
- No new dependencies.