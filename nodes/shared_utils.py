"""Shared utility functions for MotionCapture nodes."""

from pathlib import Path

import folder_paths


def next_sequential_filename(directory, prefix, ext):
    """Find the next sequential filename like prefix_0001.ext, prefix_0002.ext, etc."""
    existing = sorted(directory.glob(f"{prefix}_*{ext}"))
    max_num = 0
    for f in existing:
        stem = f.stem
        suffix = stem[len(prefix) + 1:]
        try:
            max_num = max(max_num, int(suffix))
        except ValueError:
            pass
    return f"{prefix}_{max_num + 1:04d}{ext}"


def resolve_output_path(filename):
    """Resolve export names against ComfyUI's configured output or temp folder."""
    path = Path(str(filename).replace("\\", "/"))
    if path.is_absolute():
        return path
    directory = folder_paths.get_output_directory()
    if path.parts and path.parts[0] in ("output", "temp"):
        directory = folder_paths.get_directory_by_type(path.parts[0])
        path = Path(*path.parts[1:])
    return Path(directory) / path
