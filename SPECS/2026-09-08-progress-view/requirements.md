# Progress View — Requirements

## Context

The core app is built and working: a student can log, list, and delete study
sessions, and the page shows a last-7-days strip, a streak counter, and total
hours per subject. These three pieces of feedback are currently separate
sections on the page.

This feature reorganizes the main page into one clear **progress view**: the
streak as a headline, the 7-day strip as the visual, then the session list.
The goal is that a student understands their progress at a glance (MISSION:
"see, at a glance, a true picture of how consistent they have been").

No new pages are added. The main page is reworked.

## Scope

In scope:

- Reorganize the main page (`/`) into a single progress-led layout:
  - **Streak headline** — e.g. "You've studied 3 days in a row!"
  - **Last-7-days strip** — the existing row of 7 boxes with day labels
  - **Encouraging message** — a short, friendly line tied to the streak
    (aligned with the MISSION value "helpful, not punishing")
  - **Session list** — unchanged, below the progress section
- The log form stays exactly where it is (top), so logging is still fast.
- Existing behavior (log, validate, delete, error messages, data surviving
  restarts) is unchanged.

Out of scope:

- The hours-per-subject list: it stays on the page in its current form or is
  moved below the progress section (it is not part of the headline view).
- A separate `/progress` page.
- Any change to the data model, validation, or routes beyond re-rendering.

## User story

> As a student, when I open the app I immediately see how I'm doing — my
> streak and my last 7 days together — before I see the session list.

## Decisions (made with the user)

| Question | Decision |
|----------|----------|
| Where does the combined view live? | Main page rework (no new pages) |
| What is the headline? | Streak counter |
| What is the visual? | Last-7-days strip (kept) |
| Can the layout change? | Yes — the page is being reworked |

## Functional requirements

1. GET `/` renders the reworked page:
   - Log form (unchanged, at top).
   - Progress section:
     - Streak headline (e.g. "You've studied 3 days in a row!"; for 0 days,
       "Start your streak today!").
     - Last-7-days strip with day labels and filled/empty boxes.
     - A short encouraging message based on the streak.
   - Session list (unchanged) below.
   - Hours-per-subject list kept on the page (below the progress section).
2. All existing behaviors are preserved:
   - Valid POST `/log` stores the session and re-renders with the updated
     streak/strip.
   - Invalid POST `/log` shows the error, stores nothing.
   - POST `/delete/<id>` deletes and redirects to `/`.
3. No changes to the data model, validation rules, or the stats functions
   unless tests require it.

## Data model

Unchanged: SQLite `study_sessions` table (id, subject, duration, note, date).
The progress view is derived from these rows by the existing `stats.py`
functions (`streak`, `last_7_days_strip`, `hours_per_subject`).

## Constraints

- Flask server, vanilla HTML/CSS/JS — no frameworks.
- SQLite for storage.
- Red/Green TDD: tests before code.
- Logging via decorators (business logic separate from logging).
- Plain, simple code a beginner can read.