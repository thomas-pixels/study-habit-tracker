"""Form validation for the Study Habit Tracker.

Pure logic, no Flask or HTML — easy to test.
Returns None when the input is valid, or a friendly error message.
"""

from log import logged

MAX_MINUTES = 1440

# Fixed list of allowed subjects, in frequency-of-use order.
# The form renders a dropdown from this list; the first item is the default.
SUBJECTS = [
    "Math",
    "Science",
    "History",
    "English",
    "Languages",
    "Computer Science",
]


@logged
def validate_session(subject: str, duration: str, note: str, date: str) -> str | None:
    """Return a friendly error message, or None if the input is valid."""
    if subject is None or subject.strip() == "":
        return "Please enter a subject."

    if subject not in SUBJECTS:
        return "Please pick a subject from the list."

    try:
        minutes = int(duration)
    except (TypeError, ValueError):
        return "Duration must be a whole number of minutes."

    if minutes <= 0 or minutes > MAX_MINUTES:
        return f"Duration must be between 1 and {MAX_MINUTES} minutes."

    if date is None or date.strip() == "":
        return "Please choose a date."

    return None