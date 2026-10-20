"""File selection shared by the loaders and their refresh endpoints."""

from pathlib import Path

import folder_paths


def list_files(pattern, legacy_prefix=False):
    files = []
    for source in ("input", "output"):
        directory = Path(folder_paths.get_directory_by_type(source))
        prefix = f"{source}/" if legacy_prefix else ("[output] " if source == "output" else "")
        files.extend(
            prefix + path.relative_to(directory).as_posix()
            for path in sorted(directory.rglob(pattern))
            if path.is_file() and folder_paths.is_within_directory(str(directory), str(path))
        )
    return files


def resolve_file_path(file_path):
    source = "output" if file_path.startswith("[output] ") else "input"
    name = file_path[len("[output] "):] if source == "output" else file_path
    directory = folder_paths.get_directory_by_type(source)
    path = Path(directory) / name.replace("\\", "/")
    if not folder_paths.is_within_directory(directory, str(path)):
        raise ValueError(f"Invalid file path: {file_path!r}")
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")
    return str(path.resolve())


def resolve_bvh_path(file_path):
    name = file_path.replace("\\", "/")
    if name.startswith("output/"):
        name = "[output] " + name[len("output/"):]
    elif name.startswith("input/"):
        name = name[len("input/"):]
    return resolve_file_path(name)


def file_fingerprint(file_path):
    stat = Path(file_path).stat()
    return stat.st_mtime_ns, stat.st_size
