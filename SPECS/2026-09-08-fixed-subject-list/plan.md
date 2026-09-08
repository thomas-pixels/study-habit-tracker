# Fixed Subject List — Plan

Red/Green TDD: write the failing test first (red), then minimal code to make
it pass (green).

## Task group 1 — Subject list + validation (tests first)

### What gets built

In `validation.py`:

- A constant `SUBJECTS` — the fixed, ordered list of allowed subjects.
- `validate_session` is extended so an unknown subject is invalid.

### Tests (red → green)

- [x] Test: `SUBJECTS` is a non-empty list of strings, no duplicates.
- [x] Test: a subject in `SUBJECTS` passes validation.
- [x] Test: a subject not in `SUBJECTS` fails with a message mentioning
      "subject".
- [x] Test: existing rules still pass (empty subject, bad duration, bad
      date) — update the loop in `test_validation.py` to use a valid subject
      from the list.
- [x] Check: tests pass (green).

## Task group 2 — Route passes the list (tests first)

### What gets built

`routes.py` passes `validation.SUBJECTS` into the template render.

### Tests (red → green)

- [x] Test: GET `/` page source contains an `<option>` per subject (e.g.
      `value="Math"`).
- [x] Check: tests pass (green).

## Task group 3 — Template change

### What gets built

`templates/index.html`: replace the text `<input id="subject">` with a
`<select id="subject">` rendering one `<option>` per subject, with the first
subject preselected. The list comes from the template variable, not
hard-coded.

When re-rendering after an invalid submit, keep the submitted subject
selected if it has a value.

### Steps

- [x] Replace the input with a select in the template.
- [x] Options rendered from the passed-in list.
- [x] First subject is `selected` by default; if `form.subject` was
      submitted, that one is selected instead.
- [x] Verify form still works with a valid selection.

## Task group 4 — Styling

- [x] Ensure the `<select>` matches the input styling (width, padding) in
      `static/style.css`.

## Task group 5 — Full suite + manual verification

- [x] `python -m pytest` — all tests pass (green).
- [x] Run the server, verify through the Codio public URL.
- [x] Manual checks (per validation.md): pick a subject, log, confirm; try a
      non-listed value is rejected.

## General reminders

- Run `python -m pytest` after each task group.
- Keep code simple and obvious; no clever tricks.
- No new dependencies.