"""Profile routes — get and update the authenticated user's profile."""

from flask import Blueprint, g, jsonify, request

from backend.app.services import profile_service
from backend.app.services.auth_service import require_auth

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/", methods=["GET"])
@require_auth
def get_profile():
    profile = profile_service.get_profile(g.current_user.id)
    return jsonify(profile), 200


@profile_bp.route("/", methods=["PUT"])
@require_auth
def update_profile():
    data = request.get_json(silent=True) or {}

    # Handle avatar upload if file is present
    file = request.files.get("avatar")
    if file:
        from backend.app.services import file_service  # noqa: PLC0415
        upload_result = file_service.upload(file)
        data["avatar_url"] = upload_result["file_url"]
        data["avatar_public_id"] = upload_result["file_public_id"]

    profile = profile_service.update_profile(g.current_user.id, data)
    return jsonify(profile), 200


@profile_bp.route("/avatar", methods=["POST"])
@require_auth
def upload_avatar():
    file = request.files.get("avatar")
    if not file:
        from flask import abort
        abort(400, "No avatar file provided")

    from backend.app.services import file_service  # noqa: PLC0415
    upload_result = file_service.upload(file)

    data = {
        "avatar_url": upload_result["file_url"],
        "avatar_public_id": upload_result["file_public_id"],
    }
    profile = profile_service.update_profile(g.current_user.id, data)
    return jsonify(profile), 200
