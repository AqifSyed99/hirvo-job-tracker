"""File proxy route — streams Cloudinary files through the backend."""

import time
import requests
import cloudinary
import cloudinary.utils
from flask import Blueprint, Response, abort, request, current_app

proxy_bp = Blueprint("proxy", __name__)


def _configure_cloudinary():
    cloudinary.config(
        cloud_name=current_app.config.get("CLOUDINARY_CLOUD_NAME"),
        api_key=current_app.config.get("CLOUDINARY_API_KEY"),
        api_secret=current_app.config.get("CLOUDINARY_API_SECRET"),
    )


def _fix_pdf_url(url):
    """
    Cloudinary sometimes stores PDFs under /image/upload/ which returns 401.
    Convert to /raw/upload/ for direct access.
    """
    if url.endswith(".pdf") and "/image/upload/" in url:
        return url.replace("/image/upload/", "/raw/upload/")
    return url


def _make_signed_url(url):
    """Generate a signed Cloudinary URL valid for 1 hour."""
    try:
        parts = url.split("/")
        upload_idx = next((i for i, p in enumerate(parts) if p == "upload"), -1)
        if upload_idx < 0:
            return url

        resource_type = parts[upload_idx - 1]  # image, video, raw
        after_upload = parts[upload_idx + 1:]

        # Skip version segment (v1234567)
        if after_upload and after_upload[0].startswith("v") and after_upload[0][1:].isdigit():
            after_upload = after_upload[1:]

        public_id = "/".join(after_upload)

        signed_url, _ = cloudinary.utils.cloudinary_url(
            public_id,
            resource_type=resource_type,
            sign_url=True,
            expires_at=int(time.time()) + 3600,
            secure=True,
        )
        return signed_url
    except Exception as e:
        print(f"Signing error: {e}")
        return url


@proxy_bp.route("/file", methods=["GET"])
def proxy_file():
    file_url = request.args.get("url", "")

    if not file_url:
        abort(400, "Missing url parameter")

    if "cloudinary.com" not in file_url:
        abort(403, "Only Cloudinary URLs are allowed")

    _configure_cloudinary()

    # Generate signed URL (keep original resource type)
    fetch_url = _make_signed_url(file_url)

    try:
        upstream = requests.get(fetch_url, timeout=30, stream=True)
        # If signed URL fails, try raw resource type for PDFs
        if upstream.status_code == 401 and file_url.endswith(".pdf"):
            raw_url = file_url.replace("/image/upload/", "/raw/upload/")
            raw_signed = _make_signed_url(raw_url)
            upstream = requests.get(raw_signed, timeout=30, stream=True)
        upstream.raise_for_status()
    except requests.RequestException as exc:
        abort(502, f"Failed to fetch file: {exc}")

    content_type = upstream.headers.get("Content-Type", "application/octet-stream")
    # Force PDF content type for .pdf files
    if file_url.endswith(".pdf"):
        content_type = "application/pdf"

    def generate():
        for chunk in upstream.iter_content(chunk_size=8192):
            yield chunk

    response = Response(generate(), status=upstream.status_code, content_type=content_type)
    response.headers.pop("X-Frame-Options", None)
    response.headers.pop("Content-Security-Policy", None)
    response.headers.pop("Content-Disposition", None)  # Remove any attachment disposition
    response.headers["Content-Disposition"] = "inline"
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response
