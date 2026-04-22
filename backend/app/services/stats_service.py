"""Stats service — aggregate statistics for a user's job entries."""

from datetime import datetime

from backend.app.models.models import JobEntry, VALID_STATUSES


def get_stats(user_id):
    """Return aggregated stats for *user_id*."""
    entries = JobEntry.query.filter_by(user_id=user_id).all()

    total = len(entries)
    interview = sum(1 for e in entries if e.status == "Interview")
    offer = sum(1 for e in entries if e.status == "Offer")
    rejected = sum(1 for e in entries if e.status == "Rejected")

    by_status = {status: 0 for status in VALID_STATUSES}
    for entry in entries:
        if entry.status in by_status:
            by_status[entry.status] += 1

    monthly_counts = _compute_monthly_counts(entries)

    return {
        "total": total,
        "interview": interview,
        "offer": offer,
        "rejected": rejected,
        "by_status": by_status,
        "monthly_counts": monthly_counts,
        # Keep weekly_counts for backward compat (empty)
        "weekly_counts": [],
    }


def _compute_monthly_counts(entries):
    """Build a list of 12 monthly-count dicts, oldest first.

    Each bucket is one calendar month: {"month": "Jan 2025", "count": N}
    """
    now = datetime.utcnow()

    # Build the 12 month buckets (oldest first)
    months = []
    for i in range(11, -1, -1):
        # Go back i months from current month
        month = now.month - i
        year = now.year
        while month <= 0:
            month += 12
            year -= 1
        months.append((year, month))

    # Count entries per (year, month)
    counts = {(y, m): 0 for y, m in months}
    for entry in entries:
        created = entry.created_at
        if created is None:
            continue
        if hasattr(created, "tzinfo") and created.tzinfo is not None:
            created = created.replace(tzinfo=None)
        key = (created.year, created.month)
        if key in counts:
            counts[key] += 1

    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    return [
        {
            "month": f"{month_names[m - 1]} {y}",
            "count": counts[(y, m)],
        }
        for y, m in months
    ]
