"""
Metadata Inspection and Sanitization Routes
Allows users to voluntarily inspect image EXIF/GPS metadata locally
and download an EXIF-sanitized sanitized copy.
Privacy Guarantee: Zero external requests; in-memory processing only.
"""

from flask import Blueprint, request, jsonify, Response
from backend.services.metadata_inspector import inspect_image_metadata, strip_image_metadata

metadata_bp = Blueprint("metadata", __name__, url_prefix="/api/metadata")


@metadata_bp.route("/inspect", methods=["POST"])
def inspect_image():
    """
    Accepts an uploaded image, parses embedded EXIF/GPS tags locally in-memory,
    and returns detected privacy leakage risks.
    """
    if "image" not in request.files:
        return jsonify({"success": False, "error": "No image file provided in request."}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected."}), 400

    file_bytes = file.read()
    if len(file_bytes) > 25 * 1024 * 1024:  # 25 MB max
        return jsonify({"success": False, "error": "File size exceeds 25MB limit."}), 400

    results = inspect_image_metadata(file_bytes, file.filename)
    return jsonify({
        "success": True,
        "results": results
    })


@metadata_bp.route("/strip", methods=["POST"])
def strip_metadata():
    """
    Strips all EXIF, GPS, camera model, and timestamp metadata from an uploaded image,
    returning a clean sanitized PNG/JPEG stream.
    """
    if "image" not in request.files:
        return jsonify({"success": False, "error": "No image file provided."}), 400

    file = request.files["image"]
    format_opt = request.form.get("format", "PNG").upper()
    file_bytes = file.read()

    try:
        clean_bytes = strip_image_metadata(file_bytes, output_format=format_opt)
        mime = "image/png" if format_opt == "PNG" else "image/jpeg"
        clean_filename = f"sanitized_{file.filename.rsplit('.', 1)[0]}.{format_opt.lower()}"
        return Response(
            clean_bytes,
            mimetype=mime,
            headers={"Content-Disposition": f"attachment; filename={clean_filename}"}
        )
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to sanitize image: {str(e)}"}), 500
