import re
from datetime import datetime, timedelta
from functools import wraps

import bcrypt
import jwt
from flask import abort, current_app, g, request

from backend.app import db
from backend.app.models.models import User

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def register(email, password, full_name=None):
    """Register a new user."""
    if not email or not _EMAIL_RE.match(email):
        abort(400, "Invalid email address")

    if not password or len(password) < 8:
        abort(400, "Password must be at least 8 characters")

    existing = User.query.filter_by(email=email).first()
    if existing is not None:
        abort(409, "Email already registered")

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    user = User(email=email, password_hash=password_hash, full_name=full_name or None)
    db.session.add(user)
    db.session.commit()

    return {"id": user.id, "email": user.email}


def login(email, password):
    """Authenticate a user and return a signed JWT.

    Looks up the user by email, verifies the password, issues a JWT valid for
    24 hours, and returns a dict with the token and basic user info.
    """
    user = User.query.filter_by(email=email).first()
    if user is None:
        abort(401, "Invalid credentials")

    if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
        abort(401, "Invalid credentials")

    payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(hours=24),
    }
    token = jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")

    return {
        "token": token,
        "user": {"id": user.id, "email": user.email, "full_name": user.full_name},
    }


def require_auth(f):
    """Decorator that enforces JWT authentication on a route.

    Extracts the Bearer token from the Authorization header, decodes and
    validates it, looks up the corresponding user, and stores the user in
    ``flask.g.current_user`` before calling the wrapped function.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header or not auth_header.startswith("Bearer "):
            abort(401, "Missing or invalid Authorization header")

        token = auth_header[len("Bearer "):]

        try:
            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET"],
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError:
            abort(401, "Token has expired")
        except jwt.InvalidTokenError:
            abort(401, "Invalid token")

        user = User.query.get(payload.get("user_id"))
        if user is None:
            abort(401, "User not found")

        g.current_user = user
        return f(*args, **kwargs)

    return decorated
