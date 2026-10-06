"""
Safe Local Metadata Inspector and Stripper Service
Extracts EXIF and media metadata from voluntarily uploaded local images,
analyzes geolocation/camera leakage, and allows generating an EXIF-stripped sanitized copy.
Privacy Guarantee: Runs 100% locally; no external network calls; temporary files wiped after use.
"""

import io
from typing import Dict, Any, Optional
from PIL import Image, ExifTags


def _convert_to_degrees(value) -> Optional[float]:
    """Helper to convert the GPS coordinates stored in the EXIF to degrees in float format."""
    try:
        # Handles Rational/tuple format from PIL
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        return d + (m / 60.0) + (s / 3600.0)
    except Exception:
        return None


def inspect_image_metadata(file_bytes: bytes, filename: str) -> Dict[str, Any]:
    """
    Parses EXIF tags from image bytes locally without internet access.
    Detects GPS, device model, software, timestamp, and serial numbers.
    """
    result = {
        "filename": filename,
        "format": "Unknown",
        "size_bytes": len(file_bytes),
        "dimensions": None,
        "has_exif": False,
        "metadata": {},
        "gps_data": None,
        "privacy_leak_warnings": []
    }

    try:
        image = Image.open(io.BytesIO(file_bytes))
        result["format"] = image.format
        result["dimensions"] = f"{image.width} x {image.height}"

        exif_raw = image.getexif()
        if not exif_raw:
            return result

        result["has_exif"] = True
        raw_dict = {}

        for tag_id, val in exif_raw.items():
            tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
            # Omit huge byte payloads (like embedded thumbnail)
            if isinstance(val, (bytes, bytearray)) and len(val) > 200:
                raw_dict[tag_name] = f"<{len(val)} bytes binary data>"
            else:
                raw_dict[tag_name] = str(val)

        # Inspect GPS IFD specifically if available
        gps_info = {}
        gps_ifd = exif_raw.get_ifd(ExifTags.IFD.GPSInfo) if hasattr(exif_raw, "get_ifd") else None

        if gps_ifd:
            for tag_id, val in gps_ifd.items():
                tag_name = ExifTags.GPSTAGS.get(tag_id, str(tag_id))
                gps_info[tag_name] = str(val)

            # Try parsing latitude and longitude
            lat_val = gps_ifd.get(2)  # GPSLatitude
            lat_ref = gps_ifd.get(1)  # GPSLatitudeRef
            lon_val = gps_ifd.get(4)  # GPSLongitude
            lon_ref = gps_ifd.get(3)  # GPSLongitudeRef

            if lat_val and lon_val:
                lat = _convert_to_degrees(lat_val)
                lon = _convert_to_degrees(lon_val)
                if lat is not None and lon is not None:
                    if lat_ref == "S":
                        lat = -lat
                    if lon_ref == "W":
                        lon = -lon
                    result["gps_data"] = {
                        "latitude": round(lat, 6),
                        "longitude": round(lon, 6),
                        "raw_tags": gps_info
                    }
                    result["privacy_leak_warnings"].append(
                        f"CRITICAL: Embedded GPS coordinates detected ({round(lat, 4)}, {round(lon, 4)}). "
                        "Anyone with this photo can determine your exact physical location."
                    )

        result["metadata"] = raw_dict

        # Check for device model
        if "Model" in raw_dict or "Make" in raw_dict:
            device = f"{raw_dict.get('Make', '')} {raw_dict.get('Model', '')}".strip()
            result["privacy_leak_warnings"].append(
                f"DEVICE REVEALED: Camera hardware identified as '{device}'. "
                "Can assist device-fingerprinting and targeted exploit selection."
            )

        # Check for timestamp
        if "DateTime" in raw_dict or "DateTimeOriginal" in raw_dict:
            ts = raw_dict.get("DateTimeOriginal", raw_dict.get("DateTime"))
            result["privacy_leak_warnings"].append(
                f"TIMESTAMP REVEALED: Photo captured at {ts}. Discloses your daily schedule and activity times."
            )

    except Exception as e:
        result["error"] = str(e)

    return result


def strip_image_metadata(file_bytes: bytes, output_format: str = "PNG") -> bytes:
    """
    Creates a sanitized copy of an image by redrawing pixel data
    onto a fresh image canvas without carrying over any EXIF or GPS tags.
    """
    image = Image.open(io.BytesIO(file_bytes))
    # Create clean image canvas with same mode & dimensions
    clean_image = Image.new(image.mode, image.size)
    clean_image.putdata(list(image.getdata()))

    out_buffer = io.BytesIO()
    # Save in specified format without EXIF
    fmt = output_format.upper()
    if fmt not in ["PNG", "JPEG", "WEBP"]:
        fmt = "PNG"

    clean_image.save(out_buffer, format=fmt)
    return out_buffer.getvalue()
