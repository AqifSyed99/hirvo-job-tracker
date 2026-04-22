"""Stats routes — dashboard aggregate statistics."""

from flask import Blueprint, g, jsonify

from backend.app.services import stats_service
from backend.app.services.auth_service import require_auth

stats_bp = Blueprint("stats", __name__)


@stats_bp.route("/", methods=["GET"])
@require_auth
def get_stats():
    """Return aggregated stats for the authenticated user."""
    stats = stats_service.get_stats(g.current_user.id)
    return jsonify(stats), 200
