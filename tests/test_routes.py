"""Tests for the HTTP routes (tests written first — Red)."""


def test_get_root_shows_the_form(client):
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'name="subject"' in html
    assert 'name="duration"' in html
    assert 'name="note"' in html
    assert 'name="date"' in html


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