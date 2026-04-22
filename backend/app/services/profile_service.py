"""Profile service — get and update the authenticated user's profile."""

from flask import abort, current_app

from backend.app import db
from backend.app.models.models import User


def _user_to_dict(user):
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "phone": user.phone,
        "ic_number": user.ic_number,
        "avatar_url": user.avatar_url,
        "address": user.address,
        "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else None,
    }


def get_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, "User not found")
    return _user_to_dict(user)


def update_profile(user_id, data):
    user = User.query.get(user_id)
    if not user:
        abort(404, "User not found")

    updatable = ["full_name", "phone", "ic_number", "address", "date_of_birth",
                 "avatar_url", "avatar_public_id"]
    for field in updatable:
        if field in data:
            setattr(user, field, data[field] or None)

    db.session.commit()
    return _user_to_dict(user)
