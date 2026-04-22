import logging
import os

import cloudinary
import cloudinary.uploader
from flask import abort, current_app

logger = logging.getLogger(__name__)

ALLOWED_MIME_TYPES = {"application/pdf", "image/png", "image/jpeg"}
ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


def _configure_cloudinary():
    """Configure Cloudinary using the current Flask app config."""
    cloudinary.config(
        cloud_name=current_app.config.get("CLOUDINARY_CLOUD_NAME"),
        api_key=current_app.config.get("CLOUDINARY_API_KEY"),
        api_secret=current_app.config.get("CLOUDINARY_API_SECRET"),
    )


def upload(file):
    """Upload a file to Cloudinary.

    Args:
        file: A Werkzeug FileStorage object.

    Returns:
        dict with keys ``file_url`` and ``file_public_id``.

    Raises:
        HTTPException 400 if the file type or size is invalid.
        HTTPException 502 if the Cloudinary upload fails.
    """
    # --- Validate MIME type and extension ---
    mime_type = file.mimetype or ""
    filename = file.filename or ""
    _, ext = os.path.splitext(filename.lower())

    if mime_type not in ALLOWED_MIME_TYPES or ext not in ALLOWED_EXTENSIONS:
        abort(400, "File type not allowed. Accepted: PDF, PNG, JPG, JPEG")

    # --- Validate file size ---
    content = file.read()
    if len(content) > MAX_FILE_SIZE_BYTES:
        abort(400, "File size exceeds 10 MB limit")
    file.seek(0)

    # --- Upload to Cloudinary ---
    _configure_cloudinary()

    # Use 'auto' resource type — Cloudinary will detect the correct type
    try:
        result = cloudinary.uploader.upload(
            file,
            resource_type="auto",
            folder="job-tracker",
        )
    except Exception as exc:
        logger.error("Cloudinary upload error: %s", exc)
        abort(502, f"File upload failed: {exc}")

    return {
        "file_url": result["secure_url"],
        "file_public_id": result["public_id"],
        "file_original_name": filename,
    }


def delete(public_id):
    """Delete a file from Cloudinary by its public ID.

    Errors are logged but not re-raised — deletion is best-effort.
    """
    _configure_cloudinary()

    try:
        # Try raw first (for PDFs), then image
        result = cloudinary.uploader.destroy(public_id, resource_type="raw")
        if result.get("result") != "ok":
            cloudinary.uploader.destroy(public_id, resource_type="image")
    except Exception as exc:
        logger.error("Cloudinary delete error for public_id '%s': %s", public_id, exc)
