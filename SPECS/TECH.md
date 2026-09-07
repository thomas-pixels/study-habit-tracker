# TECH

## Stack (what we use)

- **Python Flask** for the backend (the server that runs the app).
- **Vanilla HTML, CSS, and JavaScript** for the frontend (what the user sees).
- No frameworks or libraries (no React, no CSS frameworks, no npm packages).
- **SQLite database** — study sessions are stored in a single SQLite table.
  Data is saved to disk and survives server restarts.

## Architecture principles

- **Walking skeleton.** Start with the thinnest end-to-end slice that works,
  then grow features on it. Avoid building too much before seeing it work.
- **Simplicity over complexity.** Prefer the simplest solution that works.
  Pick the obvious approach over clever tricks.
- **DRY (Don't Repeat Yourself).** If the same code appears more than once,
  pull it into one reusable piece.

## Engineering standards

- **Red/Green TDD.** Write a failing test first (red), watch it fail, then
  write the minimal code to make it pass (green), and refactor as needed.
- **Spec-driven development.** All work starts from a written specification;
  code must trace back to an approved spec.
- **Strict models over loose logic.** Define clear shapes for our data (e.g. a
  single `study_sessions` table with columns subject, duration, note, date)
  instead of ad-hoc parsing and custom logic.
- **Decoupled logging.** Keep logging separate from business logic.
- **Strict typing.** Type-safety is not traded away for convenience.
