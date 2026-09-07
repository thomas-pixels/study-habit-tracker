# Walking Skeleton — Validation

## How we know this feature works

The walking skeleton is done when all of the following hold:

1. **Automated tests pass.**

   - `python -m pytest` exits with status 0 and no failing tests.
   - Tests cover, at minimum:
     - storing a session inserts a row with all fields;
     - fetching sessions returns them newest-first;
     - empty subject is rejected;
     - non-positive / non-integer duration is rejected;
     - a valid POST adds the session and it appears in the list;
     - an invalid POST shows an error and stores nothing.

2. **Manual check in the browser.**

   - The page at `/` shows the log form and the session list.
   - The date field is pre-filled with today's date.
   - Entering a valid session (subject + minutes, optional note) and
     submitting makes it appear in the list, newest first.
   - Submitting an empty subject or a bad duration shows a friendly error
     message and adds nothing to the list.
   - Restarting the server keeps the logged sessions (stored in SQLite).

3. **The app works through the Codio public URL.**

   - The server is bound to `0.0.0.0`, the public URL responds to a request
     (`curl`), and the URL is announced to the user (per AGENTS.md).

4. **Specs still match the code.**

   - Any difference between what was built and the specs is surfaced, and the
     specs (SPECS/ + feature spec) are updated only after the user approves.

## When it can be merged

- All tests pass.
- The manual browser check succeeds.
- The user has reviewed and approved the feature spec and the built result.