"""HTTP routes for the Study Habit Tracker."""

from datetime import date

from flask import Blueprint, redirect, render_template, request

import db
import validation
from log import logged

bp = Blueprint("main", __name__)


@bp.route("/")
@logged
def index():
    """Show the log form and the session list, newest first."""
    sessions = db.get_all_sessions()
    today = date.today().isoformat()
    return render_template("index.html", sessions=sessions, error=None, form=None, today=today)


@bp.route("/log", methods=["POST"])
@logged
def log_session():
    """Validate the form, store the session if valid, re-render the page."""
    subject = request.form.get("subject", "")
    duration = request.form.get("duration", "")
    note = request.form.get("note", "")
    session_date = request.form.get("date", "")

    error = validation.validate_session(subject, duration, note, session_date)

    if error is None:
        db.insert_session(subject.strip(), int(duration), note, session_date)
        sessions = db.get_all_sessions()
        return render_template(
            "index.html", sessions=sessions, error=None, form=None, today=date.today().isoformat()
        )

    sessions = db.get_all_sessions()
    form_data = {
        "subject": subject,
        "duration": duration,
        "note": note,
        "date": session_date,
    }
    return render_template(
        "index.html", sessions=sessions, error=error, form=form_data, today=date.today().isoformat()
    )


@bp.route("/delete/<int:session_id>", methods=["POST"])
@logged
def delete_session(session_id: int):
    """Delete one session, then redirect back to the home page."""
    db.delete_session(session_id)
    return redirect("/")