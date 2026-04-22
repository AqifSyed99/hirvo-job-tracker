from flask import Blueprint, jsonify, request

from backend.app.services import auth_service

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user account."""
    data = request.get_json(silent=True) or {}
    email = data.get("email", "")
    password = data.get("password", "")
    full_name = data.get("full_name", "")

    user = auth_service.register(email, password, full_name)
    return jsonify(user), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate and receive a JWT."""
    data = request.get_json(silent=True) or {}
    email = data.get("email", "")
    password = data.get("password", "")

    result = auth_service.login(email, password)
    return jsonify(result), 200
