"""Job entry service — CRUD operations for JobEntry records."""

from flask import abort

from backend.app import db
from backend.app.models.models import JobEntry, JobAttachment, VALID_STATUSES

_REQUIRED_FIELDS = ("company_name", "job_title", "status", "platform")

_UPDATABLE_FIELDS = (
    "company_name",
    "job_title",
    "status",
    "platform",
    "contact_person",
    "work_type",
    "employment_type",
    "application_date",
    "location",
    "salary_min",
    "salary_max",
    "job_url",
    "notes",
    "file_url",
    "file_public_id",
    "file_original_name",
)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def get_all(user_id):
    """Return all job entries for *user_id*, newest first."""
    entries = (
        JobEntry.query
        .filter_by(user_id=user_id)
        .order_by(JobEntry.created_at.desc())
        .all()
    )
    return [_entry_to_dict(e) for e in entries]


def get_one(user_id, entry_id):
    """Return a single job entry dict, enforcing ownership.

    Aborts with 404 if the entry does not exist, 403 if it belongs to a
    different user.
    """
    entry = JobEntry.query.get(entry_id)
    if entry is None:
        abort(404, "Job entry not found")
    if entry.user_id != user_id:
        abort(403, "Access forbidden")
    return _entry_to_dict(entry)


def create(user_id, data):
    """Validate *data* and insert a new JobEntry for *user_id*.

    Required fields: company_name, job_title, status.
    Aborts with 400 on validation failure.
    Returns the new entry as a dict.
    """
    data = data or {}

    # Required field validation
    for field in _REQUIRED_FIELDS:
        if not data.get(field):
            abort(400, f"Missing required field: {field}")

    # Status validation
    if data["status"] not in VALID_STATUSES:
        abort(
            400,
            f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}",
        )

    # Salary range validation
    _validate_salary_range(data)

    entry = JobEntry(
        user_id=user_id,
        company_name=data["company_name"],
        job_title=data["job_title"],
        status=data["status"],
        platform=data.get("platform"),
        contact_person=data.get("contact_person"),
        work_type=data.get("work_type"),
        employment_type=data.get("employment_type"),
        application_date=data.get("application_date"),
        location=data.get("location"),
        salary_min=data.get("salary_min"),
        salary_max=data.get("salary_max"),
        job_url=data.get("job_url"),
        notes=data.get("notes"),
        file_url=data.get("file_url"),
        file_public_id=data.get("file_public_id"),
        file_original_name=data.get("file_original_name"),
    )
    db.session.add(entry)
    db.session.flush()  # get entry.id before commit

    # Handle multiple attachments
    attachments = data.get("attachments", [])
    for att in attachments:
        attachment = JobAttachment(
            job_entry_id=entry.id,
            file_url=att["file_url"],
            file_public_id=att.get("file_public_id"),
            file_original_name=att.get("file_original_name"),
        )
        db.session.add(attachment)

    db.session.commit()
    return _entry_to_dict(entry)


def update(user_id, entry_id, data):
    """Partially update a job entry, enforcing ownership.

    Only fields present in *data* are updated.
    Aborts with 400 on validation failure, 403/404 on ownership/existence.
    Returns the updated entry as a dict.
    """
    data = data or {}

    # Fetch the raw ORM object (not the dict) for mutation
    entry = JobEntry.query.get(entry_id)
    if entry is None:
        abort(404, "Job entry not found")
    if entry.user_id != user_id:
        abort(403, "Access forbidden")

    # Status validation (only if provided)
    if "status" in data and data["status"] not in VALID_STATUSES:
        abort(
            400,
            f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}",
        )

    # Salary range validation (only if both are present after merge)
    merged_min = data.get("salary_min", entry.salary_min)
    merged_max = data.get("salary_max", entry.salary_max)
    if merged_min is not None and merged_max is not None:
        try:
            if float(merged_min) > float(merged_max):
                abort(
                    400,
                    "salary_min must be less than or equal to salary_max",
                )
        except (TypeError, ValueError):
            abort(400, "Invalid salary values")

    for field in _UPDATABLE_FIELDS:
        if field in data:
            setattr(entry, field, data[field])

    # Handle new attachments added during edit
    new_attachments = data.get("attachments", [])
    for att in new_attachments:
        attachment = JobAttachment(
            job_entry_id=entry.id,
            file_url=att["file_url"],
            file_public_id=att.get("file_public_id"),
            file_original_name=att.get("file_original_name"),
        )
        db.session.add(attachment)

    db.session.commit()
    return _entry_to_dict(entry)


def delete(user_id, entry_id):
    """Delete a job entry and all its attachments."""
    entry = JobEntry.query.get(entry_id)
    if entry is None:
        abort(404, "Job entry not found")
    if entry.user_id != user_id:
        abort(403, "Access forbidden")

    from backend.app.services import file_service  # noqa: PLC0415
    # Delete all attachments from Cloudinary
    for att in entry.attachments:
        if att.file_public_id:
            file_service.delete(att.file_public_id)
    # Delete legacy single file
    if entry.file_public_id:
        file_service.delete(entry.file_public_id)

    db.session.delete(entry)
    db.session.commit()
    return {"message": "Job entry deleted"}


def delete_attachment(user_id, entry_id, attachment_id):
    """Delete a single attachment from a job entry."""
    entry = JobEntry.query.get(entry_id)
    if entry is None:
        abort(404, "Job entry not found")
    if entry.user_id != user_id:
        abort(403, "Access forbidden")

    att = JobAttachment.query.get(attachment_id)
    if att is None or att.job_entry_id != entry_id:
        abort(404, "Attachment not found")

    from backend.app.services import file_service  # noqa: PLC0415
    if att.file_public_id:
        file_service.delete(att.file_public_id)

    db.session.delete(att)
    db.session.commit()
    return {"message": "Attachment deleted"}


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _validate_salary_range(data):
    """Abort 400 if both salary fields are present and min > max."""
    salary_min = data.get("salary_min")
    salary_max = data.get("salary_max")
    if salary_min is not None and salary_max is not None:
        try:
            if float(salary_min) > float(salary_max):
                abort(
                    400,
                    "salary_min must be less than or equal to salary_max",
                )
        except (TypeError, ValueError):
            abort(400, "Invalid salary values")


def _entry_to_dict(entry):
    """Serialize a JobEntry ORM object to a JSON-safe dict."""
    def _date(val):
        return val.isoformat() if val is not None else None

    def _decimal(val):
        return float(val) if val is not None else None

    return {
        "id": entry.id,
        "user_id": entry.user_id,
        "company_name": entry.company_name,
        "job_title": entry.job_title,
        "status": entry.status,
        "platform": entry.platform,
        "contact_person": entry.contact_person,
        "work_type": entry.work_type,
        "employment_type": entry.employment_type,
        "application_date": _date(entry.application_date),
        "location": entry.location,
        "salary_min": _decimal(entry.salary_min),
        "salary_max": _decimal(entry.salary_max),
        "job_url": entry.job_url,
        "notes": entry.notes,
        "file_url": entry.file_url,
        "file_public_id": entry.file_public_id,
        "file_original_name": entry.file_original_name,
        "attachments": [
            {
                "id": a.id,
                "file_url": a.file_url,
                "file_public_id": a.file_public_id,
                "file_original_name": a.file_original_name,
            }
            for a in entry.attachments
        ],
        "created_at": _date(entry.created_at),
        "updated_at": _date(entry.updated_at),
    }
