#!/usr/bin/env python3
"""The World — 21 November 2026.

Hand-in program for the news-image-20261121 bounty. It takes the
front-page collage in image.jpg, checks that it is a well-formed JPEG
under one mebibyte, and copies it byte-for-byte to /output/entry.png.

Pure standard library only; no third-party packages are used.
"""

import argparse
import hashlib
import os
import struct
import sys

SOURCE_NAME = "image.jpg"
DEFAULT_DESTINATION = "/output/entry.png"
MAX_BYTES = 1024 * 1024

JPEG_SOI = b"\xff\xd8"
JPEG_EOI = b"\xff\xd9"


def read_source(path):
    """Return the raw bytes of the source image, or raise ValueError."""
    if not os.path.isfile(path):
        raise ValueError("source image not found: %s" % path)
    size = os.path.getsize(path)
    if size == 0:
        raise ValueError("source image is empty: %s" % path)
    if size > MAX_BYTES:
        raise ValueError(
            "source image is %d bytes, over the %d byte limit"
            % (size, MAX_BYTES)
        )
    with open(path, "rb") as handle:
        return handle.read()


def check_jpeg(data, path):
    """Raise ValueError unless data looks like a complete JPEG."""
    if not data.startswith(JPEG_SOI):
        raise ValueError("%s does not start with a JPEG SOI marker" % path)
    if not data.endswith(JPEG_EOI):
        raise ValueError(
            "%s is truncated: %d bytes read but no JPEG EOI marker "
            "at the end (last two bytes %s)"
            % (path, len(data), data[-2:].hex())
        )
    width, height = jpeg_dimensions(data)
    if width <= 0 or height <= 0:
        raise ValueError("%s has no readable SOF dimensions" % path)
    return width, height


def jpeg_dimensions(data):
    """Scan JPEG markers for the first SOF segment and return (w, h)."""
    pos = 2
    end = len(data)
    while pos + 4 <= end:
        if data[pos] != 0xFF:
            pos += 1
            continue
        marker = data[pos + 1]
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        if pos + 4 > end:
            break
        length = struct.unpack(">H", data[pos + 2 : pos + 4])[0]
        if length < 2 or pos + 2 + length > end:
            break
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            height, width = struct.unpack(">HH", data[pos + 5 : pos + 9])
            return width, height
        pos += 2 + length
    return 0, 0


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def build_parser():
    parser = argparse.ArgumentParser(
        description="Validate the 21 November 2026 front page and copy it "
        "to the grader output path."
    )
    parser.add_argument(
        "--source",
        default=SOURCE_NAME,
        help="input JPEG file (default: %(default)s)",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_DESTINATION,
        help="destination path for the validated copy (default: %(default)s)",
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    source_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.source)
    try:
        data = read_source(source_path)
        width, height = check_jpeg(data, source_path)
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    digest = sha256_hex(data)
    dest_dir = os.path.dirname(os.path.abspath(args.output))
    os.makedirs(dest_dir, exist_ok=True)
    with open(args.output, "wb") as handle:
        handle.write(data)
    with open(args.output, "rb") as handle:
        if sha256_hex(handle.read()) != digest:
            print("error: copy failed the sha256 check", file=sys.stderr)
            return 1
    print(
        "ok: %s (%dx%d, %d bytes, sha256 %s) -> %s"
        % (source_path, width, height, len(data), digest, args.output)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
