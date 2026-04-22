"""Job entry CRUD routes — all endpoints require authentication."""

from flask import Blueprint, g, jsonify, request

from backend.app.services import job_service
from backend.app.services.auth_service import require_auth

jobs_bp = Blueprint("jobs", __name__)


def _handle_files(data):
    """Upload all files from request.files and add to data['attachments']."""
    files = request.files.getlist("files")
    if not files:
        # fallback: single file field
        f = request.files.get("file")
        if f:
            files = [f]

    if files:
        from backend.app.services import file_service  # noqa: PLC0415
        attachments = []
        for f in files:
            if f and f.filename:
                result = file_service.upload(f)
                attachments.append({
                    "file_url": result["file_url"],
                    "file_public_id": result["file_public_id"],
                    "file_original_name": result["file_original_name"],
                })
        if attachments:
            data["attachments"] = attachments
    return data


@jobs_bp.route("/", methods=["GET"])
@require_auth
def list_jobs():
    entries = job_service.get_all(g.current_user.id)
    return jsonify(entries), 200


@jobs_bp.route("/", methods=["POST"])
@require_auth
def create_job():
    if request.content_type and "multipart/form-data" in request.content_type:
        data = dict(request.form)
    else:
        data = request.get_json(silent=True) or {}

    data = _handle_files(data)
    entry = job_service.create(g.current_user.id, data)
    return jsonify(entry), 201


@jobs_bp.route("/<int:entry_id>", methods=["GET"])
@require_auth
def get_job(entry_id):
    entry = job_service.get_one(g.current_user.id, entry_id)
    return jsonify(entry), 200


@jobs_bp.route("/<int:entry_id>", methods=["PUT"])
@require_auth
def update_job(entry_id):
    if request.content_type and "multipart/form-data" in request.content_type:
        data = dict(request.form)
    else:
        data = request.get_json(silent=True) or {}

    data = _handle_files(data)
    entry = job_service.update(g.current_user.id, entry_id, data)
    return jsonify(entry), 200


@jobs_bp.route("/<int:entry_id>", methods=["DELETE"])
@require_auth
def delete_job(entry_id):
    result = job_service.delete(g.current_user.id, entry_id)
    return jsonify(result), 200


@jobs_bp.route("/<int:entry_id>/attachments/<int:attachment_id>", methods=["DELETE"])
@require_auth
def delete_attachment(entry_id, attachment_id):
    result = job_service.delete_attachment(g.current_user.id, entry_id, attachment_id)
    return jsonify(result), 200
