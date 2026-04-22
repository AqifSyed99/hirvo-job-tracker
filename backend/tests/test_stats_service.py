"""Unit tests for stats_service.get_stats."""

from datetime import datetime, timedelta

import pytest

from backend.app import db
from backend.app.models.models import JobEntry, User, VALID_STATUSES
from backend.app.services import stats_service


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_user(email="test@example.com"):
    user = User(email=email, password_hash="hashed")
    db.session.add(user)
    db.session.flush()
    return user


def _make_entry(user_id, status="Applied", created_at=None):
    entry = JobEntry(
        user_id=user_id,
        company_name="Acme",
        job_title="Engineer",
        status=status,
    )
    if created_at is not None:
        entry.created_at = created_at
    db.session.add(entry)
    db.session.flush()
    return entry


# ---------------------------------------------------------------------------
# Tests: zero entries
# ---------------------------------------------------------------------------


def test_get_stats_empty_user(app, db):
    """User with no entries returns all-zero stats and 12 weekly buckets."""
    with app.app_context():
        user = _make_user()
        stats = stats_service.get_stats(user.id)

    assert stats["total"] == 0
    assert stats["interview"] == 0
    assert stats["offer"] == 0
    assert stats["rejected"] == 0
    assert all(v == 0 for v in stats["by_status"].values())
    assert len(stats["weekly_counts"]) == 12
    assert all(w["count"] == 0 for w in stats["weekly_counts"])


# ---------------------------------------------------------------------------
# Tests: by_status always has all 6 keys
# ---------------------------------------------------------------------------


def test_by_status_has_all_six_keys(app, db):
    """by_status always contains all six valid statuses."""
    with app.app_context():
        user = _make_user("keys@example.com")
        _make_entry(user.id, status="Applied")
        stats = stats_service.get_stats(user.id)

    assert set(stats["by_status"].keys()) == set(VALID_STATUSES)


# ---------------------------------------------------------------------------
# Tests: counts match inserted entries
# ---------------------------------------------------------------------------


def test_total_count(app, db):
    """total equals the number of entries for the user."""
    with app.app_context():
        user = _make_user("total@example.com")
        for _ in range(5):
            _make_entry(user.id, status="Applied")
        stats = stats_service.get_stats(user.id)

    assert stats["total"] == 5


def test_interview_count(app, db):
    """interview count matches entries with status 'Interview'."""
    with app.app_context():
        user = _make_user("interview@example.com")
        _make_entry(user.id, status="Interview")
        _make_entry(user.id, status="Interview")
        _make_entry(user.id, status="Applied")
        stats = stats_service.get_stats(user.id)

    assert stats["interview"] == 2


def test_offer_count(app, db):
    """offer count matches entries with status 'Offer'."""
    with app.app_context():
        user = _make_user("offer@example.com")
        _make_entry(user.id, status="Offer")
        _make_entry(user.id, status="Applied")
        stats = stats_service.get_stats(user.id)

    assert stats["offer"] == 1


def test_rejected_count(app, db):
    """rejected count matches entries with status 'Rejected'."""
    with app.app_context():
        user = _make_user("rejected@example.com")
        _make_entry(user.id, status="Rejected")
        _make_entry(user.id, status="Rejected")
        _make_entry(user.id, status="Rejected")
        stats = stats_service.get_stats(user.id)

    assert stats["rejected"] == 3


def test_by_status_counts(app, db):
    """by_status counts match the actual distribution of statuses."""
    with app.app_context():
        user = _make_user("bystatus@example.com")
        _make_entry(user.id, status="Applied")
        _make_entry(user.id, status="Applied")
        _make_entry(user.id, status="Phone Screen")
        _make_entry(user.id, status="Interview")
        _make_entry(user.id, status="Offer")
        _make_entry(user.id, status="Rejected")
        _make_entry(user.id, status="Withdrawn")
        stats = stats_service.get_stats(user.id)

    bs = stats["by_status"]
    assert bs["Applied"] == 2
    assert bs["Phone Screen"] == 1
    assert bs["Interview"] == 1
    assert bs["Offer"] == 1
    assert bs["Rejected"] == 1
    assert bs["Withdrawn"] == 1


# ---------------------------------------------------------------------------
# Tests: user isolation
# ---------------------------------------------------------------------------


def test_stats_isolated_per_user(app, db):
    """Stats for one user do not include entries from another user."""
    with app.app_context():
        user_a = _make_user("usera@example.com")
        user_b = _make_user("userb@example.com")
        for _ in range(3):
            _make_entry(user_a.id, status="Applied")
        _make_entry(user_b.id, status="Offer")

        stats_a = stats_service.get_stats(user_a.id)
        stats_b = stats_service.get_stats(user_b.id)

    assert stats_a["total"] == 3
    assert stats_b["total"] == 1
    assert stats_b["offer"] == 1


# ---------------------------------------------------------------------------
# Tests: weekly_counts structure
# ---------------------------------------------------------------------------


def test_weekly_counts_always_12(app, db):
    """weekly_counts always has exactly 12 entries."""
    with app.app_context():
        user = _make_user("weekly@example.com")
        stats = stats_service.get_stats(user.id)

    assert len(stats["weekly_counts"]) == 12


def test_weekly_counts_chronological_order(app, db):
    """weekly_counts are in chronological order (oldest first)."""
    with app.app_context():
        user = _make_user("chrono@example.com")
        stats = stats_service.get_stats(user.id)

    weeks = [w["week"] for w in stats["weekly_counts"]]
    assert weeks == sorted(weeks)


def test_weekly_counts_format(app, db):
    """Each weekly_counts entry has 'week' (YYYY-WXX) and 'count' keys."""
    import re
    pattern = re.compile(r"^\d{4}-W\d{2}$")

    with app.app_context():
        user = _make_user("format@example.com")
        stats = stats_service.get_stats(user.id)

    for item in stats["weekly_counts"]:
        assert "week" in item
        assert "count" in item
        assert pattern.match(item["week"]), (
            f"Week label '{item['week']}' does not match YYYY-WXX"
        )


def test_weekly_counts_current_week_entry(app, db):
    """An entry created this week appears in the last weekly bucket."""
    with app.app_context():
        user = _make_user("thisweek@example.com")
        now = datetime.utcnow()
        _make_entry(user.id, status="Applied", created_at=now)
        stats = stats_service.get_stats(user.id)

    # The last bucket is the current week
    last_bucket = stats["weekly_counts"][-1]
    assert last_bucket["count"] >= 1


def test_weekly_counts_old_entry_excluded(app, db):
    """An entry older than 12 weeks is not counted in weekly_counts."""
    with app.app_context():
        user = _make_user("oldentry@example.com")
        old_date = datetime.utcnow() - timedelta(weeks=13)
        _make_entry(user.id, status="Applied", created_at=old_date)
        stats = stats_service.get_stats(user.id)

    total_weekly = sum(w["count"] for w in stats["weekly_counts"])
    # The entry is older than 12 weeks so it should not appear in weekly_counts
    assert total_weekly == 0
    # But it still counts toward total
    assert stats["total"] == 1
