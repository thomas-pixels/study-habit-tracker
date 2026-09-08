# Fixed Subject List — Validation

## How we know this feature works

The fixed subject list is done when all of the following hold.

### Automated tests

- `python -m pytest` exits 0 with no failing tests.
- Tests cover at minimum:
  - `SUBJECTS` is a non-empty list of unique strings;
  - a subject in the list passes validation;
  - a subject not in the list is rejected with a friendly error;
  - all existing validation rules and route behaviours still pass.

### Manual checks in the browser

1. **The form uses a dropdown.**
   - [x] Open the page — the subject field is a dropdown, not a text box.
   - [x] Every subject from the fixed list is present as an option.
   - [x] The first subject is preselected.

2. **Logging still works.**
   - [x] Pick a subject, enter a duration, submit → session appears in the
     list with the chosen subject.

3. **Non-listed subjects are rejected.**
   - [x] Send a request with subject "Maths" (not in the list) → a friendly
     error appears and nothing is stored.

4. **Existing sessions are untouched.**
   - [x] Sessions logged before this change still appear with their original
     subject text.

### When it can be merged

- All automated tests pass.
- All manual checks pass.
- Any difference between the spec and the built result is surfaced and
  approved by the user.
- The ROADMAP is updated to mark the subject-list idea done.