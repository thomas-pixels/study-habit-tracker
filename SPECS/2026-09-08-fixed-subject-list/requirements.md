# Fixed Subject List — Requirements

## Context

Today the log form has a free-text subject box, so a student can type
"Math", "maths", or "Maht" — three different spellings that the stats and
progress view treat as three different subjects. The ROADMAP notes this as a
known improvement: "Cap subject names to a fixed list to avoid typos."

This feature replaces the subject text box with a **dropdown of fixed
subjects**, so every logged session is consistent and the stats group
cleanly.

## Scope

In scope:

- The log form's subject field becomes a dropdown (`<select>`) of fixed
  subjects.
- A single source of truth for the subject list, shared by the form (and
  validation, so only listed subjects are accepted).
- Validation rejects a subject that is not in the list.
- The first subject in the list is preselected, so a valid submission is
  always possible.

Out of scope:

- Changing how existing sessions are stored or displayed. Old sessions with
  free-text subjects (e.g. "Maths") are left exactly as they are — no data
  migration.
- Changing the session list, delete, stats, or progress view.
- Coloured badges or per-subject styling.

## User story

> As a student, when I log a session I pick my subject from a clear list, so
> the app never mixes up typos of the same subject.

## Decisions (made with the user)

| Question | Decision |
|----------|----------|
| How is the subject entered? | Dropdown only, no free-text option |
| What subjects are in the list? | A fixed common list (below) |
| What happens to existing data? | Left alone — no migration |
| How far does the change reach? | Only the form and validation |

## The fixed subject list

Single source of truth (a Python constant, e.g. `validation.SUBJECTS`):

```
Math
Science
History
English
Languages
Computer Science
```

The list is ordered by frequency of use; the first item ("Math") is the
default selection in the form.

## Functional requirements

1. GET `/` renders the subject field as a `<select>` with one `<option>` per
   subject from the fixed list. The list is passed to the template from the
   server (the template never hard-codes it).
2. The first subject is preselected by default.
3. POST `/log` with a subject that is in the list behaves exactly as today
   (valid → stored).
4. POST `/log` with a subject that is **not** in the list is invalid: a
   friendly error message appears and nothing is stored.
5. The session list, delete, stats, and progress view are unchanged.
6. Sessions already in the database keep their original subject text.

## Data model

Unchanged: SQLite `study_sessions` table (id, subject, duration, note, date).
`subject` remains a TEXT column; the fixed list is enforced by the
application, not by the database.

## Constraints

- Flask server, vanilla HTML/CSS/JS — no frameworks.
- SQLite for storage.
- Red/Green TDD: tests before code.
- Logging via decorators (business logic separate from logging).
- Simple, obvious code a beginner can read.