"""Tests for the HTTP routes (tests written first — Red)."""

import validation


def test_get_root_shows_the_form(client):
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'name="subject"' in html
    assert 'name="duration"' in html
    assert 'name="note"' in html
    assert 'name="date"' in html


def test_form_has_one_option_per_subject_from_the_list(client):
    html = client.get("/").get_data(as_text=True)

    for subject in validation.SUBJECTS:
        assert f"value=\"{subject}\"" in html


def test_post_log_subject_not_in_list_is_rejected(client):
    response = client.post(
        "/log",
        data={"subject": "Maths", "duration": "60", "note": "note", "date": "2026-09-07"},
    )

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Please pick a subject from the list." in html


def test_post_log_valid_session_appears_in_list(client):
    response = client.post(
        "/log",
        data={
            "subject": "Math",
            "duration": "60",
            "note": "Algebra homework",
            "date": "2026-09-07",
        },
    )

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Math" in html
    assert "60" in html
    assert "Algebra homework" in html
    assert "2026-09-07" in html


def test_page_shows_streak_strip_and_hours(client):
    # Log sessions on two consecutive days ending today, so the streak is 2
    # and the headline uses the plural "days in a row!".
    client.post(
        "/log",
        data={
            "subject": "History",
            "duration": "45",
            "note": "note",
            "date": "2026-09-07",
        },
    )
    client.post(
        "/log",
        data={
            "subject": "Math",
            "duration": "60",
            "note": "note",
            "date": "2026-09-08",
        },
    )
    html = client.get("/").get_data(as_text=True)

    assert "Your progress" in html
    assert "days in a row!" in html
    assert "Last 7 days" in html
    assert "Total hours per subject" in html
    assert "Math" in html


def test_page_shows_start_message_when_no_sessions(client):
    html = client.get("/").get_data(as_text=True)

    assert "Your progress" in html
    assert "Start your streak today!" in html
    assert "Log a session to begin." in html


def test_post_log_invalid_session_shows_error_and_stores_nothing(client):
    response = client.post(
        "/log",
        data={"subject": "", "duration": "60", "note": "note", "date": "2026-09-07"},
    )

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Please enter a subject." in html


def test_post_delete_removes_session(client):
    # First, log a session so there is one to delete.
    client.post(
        "/log",
        data={
            "subject": "Math",
            "duration": "60",
            "note": "note",
            "date": "2026-09-07",
        },
    )

    response = client.post("/delete/1")

    assert response.status_code == 302  # redirect back to /
    page = client.get("/")
    assert "No sessions logged yet." in page.get_data(as_text=True)