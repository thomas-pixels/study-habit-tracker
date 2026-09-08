"""Tests for form validation (tests written first — Red)."""

import validation


def test_valid_data_returns_none():
    error = validation.validate_session("Math", "60", "note", "2026-09-07")
    assert error is None


def test_empty_subject_is_invalid():
    error = validation.validate_session("", "60", "note", "2026-09-07")
    assert error is not None
    assert "subject" in error.lower()


def test_whitespace_subject_is_invalid():
    error = validation.validate_session("   ", "60", "note", "2026-09-07")
    assert error is not None
    assert "subject" in error.lower()


def test_non_number_duration_is_invalid():
    error = validation.validate_session("Math", "abc", "note", "2026-09-07")
    assert error is not None
    assert "duration" in error.lower()


def test_zero_duration_is_invalid():
    error = validation.validate_session("Math", "0", "note", "2026-09-07")
    assert error is not None
    assert "duration" in error.lower()


def test_negative_duration_is_invalid():
    error = validation.validate_session("Math", "-10", "note", "2026-09-07")
    assert error is not None
    assert "duration" in error.lower()


def test_duration_above_1440_is_invalid():
    error = validation.validate_session("Math", "1441", "note", "2026-09-07")
    assert error is not None
    assert "duration" in error.lower()


def test_missing_date_is_invalid():
    error = validation.validate_session("Math", "60", "note", "")
    assert error is not None
    assert "date" in error.lower()


# --- Fixed subject list -----------------------------------------------------


def test_subjects_list_is_non_empty_and_unique():
    assert len(validation.SUBJECTS) > 0
    assert len(validation.SUBJECTS) == len(set(validation.SUBJECTS))


def test_subject_from_the_list_passes():
    for subject in validation.SUBJECTS:
        assert validation.validate_session(subject, "60", "note", "2026-09-07") is None


def test_subject_not_in_the_list_is_invalid():
    error = validation.validate_session("Maths", "60", "note", "2026-09-07")
    assert error is not None
    assert "subject" in error.lower()