# Study Habit Tracker

*Log what you study, and see your progress — one session at a time.*

A simple, friendly website where students log their study sessions and get an
honest, at-a-glance picture of how consistent they have been. Built by
students, for students — no clutter, no jargon, just the truth about your
studying.

## The problem it solves

It is hard to build a study habit when you don't know what you actually do.
Most of us guess: "I probably studied enough this week." The tracker removes
the guesswork. It answers three simple questions:

- **How much** have I been studying?
- **How often** — am I staying consistent, day to day?
- **On what subjects** does my study time actually go?

The goal is not to judge or to punish missed days. It is to give each student
a clear, honest picture so they can build confidence and keep going.

## The solution

A single-page Flask app with one job: let a student log a study session
(subject, minutes, note, date) and immediately see their progress update.

Instead of a complicated dashboard, the page shows a **progress view** right
at the top:

- a **streak headline** with an encouraging message ("You've studied 3 days in
  a row!" / "Start your streak today!"),
- a **last-7-days strip** — one small box per day, filled if you studied that
  day,
- **total hours per subject** — a simple list that shows where your time goes.

Below that is the full **session list**, formatted newest first, with a
one-click delete button. Form inputs are validated server-side, and sessions
are stored in SQLite so they survive server restarts.

## Key features

- **Log a study session** — pick a subject from a fixed dropdown (so "math"
  and "Maths" can never become two different subjects), enter the minutes, an
  optional note, and the date.
- **Streak counter with friendly messages** — counts consecutive study days
  (today counts even if you log late; a missed day breaks the streak).
- **Last-7-days strip** — see which of the last 7 days you studied, at a
  glance.
- **Total hours per subject** — a running total of where your study time goes,
  highest first.
- **Session list with delete** — every session appears newest first, and can
  be removed with one click.
- **Friendly validation** — empty subjects, out-of-range durations, and
  non-listed subjects are caught with a clear message; nothing bad is stored.
- **Data that persists** — everything is saved to a SQLite file on disk, so a
  server restart never loses your sessions.

## Tech stack

| Layer | What we use |
|-------|-------------|
| Backend | Python 3 + Flask (a Blueprint for routes, an app factory) |
| Frontend | Vanilla HTML + CSS, rendered by Jinja templates — no JavaScript, no frameworks, no build tools |
| Database | SQLite via Python's built-in `sqlite3` module — no ORM |
| Testing | pytest (37 tests) with Flask's test client and a temporary database per test |
| Logging | A `@logged` decorator in `log.py`, kept separate from business logic |

There is deliberately **no React, no npm, no CSS framework, and no ORM**. The
code stays small and obvious, so a beginner can read the whole app in one
sitting.

## Database design

A single table stores one study session per row:

```sql
CREATE TABLE study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    duration INTEGER NOT NULL,   -- minutes studied (a whole number)
    note TEXT,                   -- what they did (optional)
    date TEXT NOT NULL           -- the day it happened (YYYY-MM-DD)
);
```

| Column | Type | Purpose |
|--------|------|---------|
| `id` | INTEGER | Unique id per session (also used by Delete) |
| `subject` | TEXT | Subject studied — from a fixed list in `validation.SUBJECTS` |
| `duration` | INTEGER | Minutes studied, validated between 1 and 1440 |
| `note` | TEXT | Optional note about what they did |
| `date` | TEXT | Day the session happened, stored as `YYYY-MM-DD` |

The progress statistics are **derived, never stored** — they are computed on
every page load in `stats.py`:

- **Days studied** = the set of unique `date` values with at least one session.
- **Streak** = walking backwards from today, count consecutive dates that have
  at least one session (if today isn't logged yet, the streak is still alive
  from yesterday).
- **Hours per subject** = sum of `duration` per `subject`, divided by 60.
- **Last-7-days strip** = the previous 7 dates, marked studied or not.

## Project structure

```
study_tracker.db        the SQLite database file (created on first run)
app.py                  Flask app factory + entry point (python app.py)
db.py                   SQLite helpers: init, insert, get, delete
routes.py               HTTP routes: GET /, POST /log, POST /delete/<id>
validation.py           Pure validation logic + the fixed SUBJECTS list
stats.py                Pure logic: strip, streak, hours, streak messages
log.py                  The @logged decorator (decoupled logging)
templates/index.html    The single page (Jinja template)
static/style.css        All the styling (vanilla CSS)
tests/                  pytest suite — each test uses its own temp database
SPECS/                  Mission, tech standards, roadmap, and feature specs
```

## Running it

```bash
pip install -r requirements.txt   # Flask + pytest
python app.py                     # starts the server on port 3000
```

Then open `http://localhost:3000/` (in a Codio box, the live URL is
`https://${CODIO_HOSTNAME}-3000.codio.io/`). Run the test suite with:

```bash
python -m pytest
```

## How it was built

The project follows the constitution in `SPECS/`:

1. **Walking skeleton first** — the thinnest working slice (log a session, see
   it appear) was built before any extra features.
2. **Red/Green TDD** — every feature started with failing tests, then minimal
   code to make them pass, then the full suite went green.
3. **Spec-driven** — each feature was written up in `SPECS/<date>-<feature>/`
   (requirements, plan, validation) and implemented straight from it.

Every idea on the roadmap is implemented and verified: walking skeleton,
last-7-days strip, streak counter, hours per subject, the progress view, and
the fixed subject list.

## What I learned

- **TDD makes features feel small.** Writing the test first forced me to
  define "done" before writing any code. Features that sounded big (streak,
  progress view) turned into a handful of small green steps. Seeing a test go
  from red to green is genuinely motivating — it's proof, not a guess.
- **Pure logic is easy to test; glue code is not.** The streak, validation,
  and hours math live in `stats.py` and `validation.py` with no Flask
  imports — they work on plain lists and strings. The routes only fetch data,
  call the logic, and render the template. That split is what makes 37 tests
  fast and reliable.
- **SQLite needs no setup and no ORM.** A few parameterized `INSERT`/`SELECT`
  statements were enough, and `?` placeholders handled escaping safely. A
  whole database is just one file — restart the server and the data is still
  there.
- **Small obvious code beats clever code.** Vanilla HTML and CSS, one
  blueprint, a decorator for logging — nothing clever anywhere. Because of
  that, I can still read every line of this project months later.
- **Specs catch design questions early.** Writing requirements.md first made
  us answer "what if someone types 'maths'?" and "what happens to old data?"
  before writing code, not during a bug hunt.
- **The boring parts matter.** Validation (duration between 1 and 1440, a
  fixed subject list), friendly error messages, and tests for them — those are
  the things that make an app feel trustworthy.

---

Project constitution: `SPECS/MISSION.md`, `SPECS/TECH.md`, `SPECS/ROADMAP.md`.