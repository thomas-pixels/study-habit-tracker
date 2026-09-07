# Study Habit Tracker — Design

## Project Overview

- **App Name:** Study Habit Tracker
- **Target User:** Students who want to build consistent study habits
- **Core Problem:** Not knowing how much, how often, or on what subjects you
  actually study
- **Purpose:** Help students track, visualize, and improve their study habits
  over time

## Core Requirements

- Log a study session by entering subject, duration (minutes), and a short
  note about what was studied
- View a **last-7-days strip** — a simple row of boxes for the last 7 days,
  filled if a study session was logged that day
- See a streak counter showing how many days in a row the student studied
- See total hours per subject to understand where study time goes

---

## Non-Goals

- No user registration or login system (single-user local application)
- No mobile app or responsive mobile framework
- No email or SMS notifications
- No third-party API integrations
- No export functionality (PDF, CSV, etc.)
- No social features (sharing, leaderboards, etc.)

## Tech Stack

- **Backend:** Python Flask (the server that runs the app)
- **Frontend:** Vanilla HTML, CSS, and JavaScript (no frameworks or libraries)
- **Data storage:** SQLite database — study sessions live in a single table
  and are saved to disk, so data survives server restarts.

## Database Requirements

Each requirement states the question the data must answer to make that
feature work:

1. **Log a study session** — The user enters a subject, a duration (in
   minutes), an optional note, and a date. Question it answers: *what did the
   student study, for how long, and on what day?*
2. **Last-7-days strip** — Show which days recently had study. Question it
   answers: *which of the last 7 days have at least one study session
   logged?*
3. **Streak counter** — Show consistency over time. Question it answers:
   *going back from today, how many consecutive days have a study session
   logged?* (A day with no session breaks the streak.)
4. **Total hours per subject** — Show where time goes. Question it answers:
   *for each subject, what is the sum of all session durations, converted to
   hours?*

## Schema (SQLite)

The app stores **one study session per row** in a single `study_sessions`
table:

```
Table: study_sessions
- id:        INTEGER PRIMARY KEY  # unique id per session
- subject:   TEXT                 # e.g. "Math", "History"
- duration:  INTEGER              # minutes studied (a whole number)
- note:      TEXT                 # what they did (optional)
- date:      TEXT                 # the day the session happened (YYYY-MM-DD)
```

Example rows:

| id | subject | duration | note | date |
|----|---------|----------|------|------|
| 1 | Math | 60 | Reviewed algebra homework | 2026-09-07 |
| 2 | History | 45 | Read chapter 5 | 2026-09-06 |

The fields:

| Field | Type | What it stores | Used to answer |
|-------|------|----------------|----------------|
| `id` | INTEGER | Unique number for each session | identifying/sorting sessions |
| `subject` | TEXT | The subject studied | hours per subject |
| `duration` | INTEGER | Minutes studied (whole number) | hours per subject (sum) |
| `note` | TEXT | What they did (optional) | showing the log |
| `date` | TEXT | Day the session happened | last-7-days strip, streak |

### Derived calculations (not stored)

These are computed from the `study_sessions` table, never stored in it:

- **Hours per subject** = sum of `duration` for each `subject`, divided by 60.
- **Which days studied** = the set of unique `date` values.
- **Streak** = walking back from today, count consecutive `date` values with
  at least one session.

Data is saved to disk in the SQLite database, so it survives server restarts.

## Development Approach

- **Walking skeleton first:** get the thinnest end-to-end slice working (log a
  session and see it appear), then build the strip, streak, and hours-per
  subject on top of it.
- **Red/Green TDD:** write a failing test first, then the minimal code to make
  it pass.
- **Simplicity over complexity:** prefer the simplest solution that works.

## Where to Find More

- **Mission & scope:** `SPECS/MISSION.md`
- **Tech & standards:** `SPECS/TECH.md`
- **Roadmap:** `SPECS/ROADMAP.md`
