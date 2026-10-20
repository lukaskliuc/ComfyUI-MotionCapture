"""ComfyUI-MotionCapture: Motion capture from video for ComfyUI."""

import os

import folder_paths
from comfy_env import register_nodes

from .loaders import NODE_CLASS_MAPPINGS as loader_mappings
from .loaders import NODE_DISPLAY_NAME_MAPPINGS as loader_display
from .loaders import register_routes

# comfy-env copies the parent environment into metadata and execution workers.
for directory in ("input", "output", "temp"):
    os.environ[f"MOTIONCAPTURE_{directory.upper()}_DIRECTORY"] = folder_paths.get_directory_by_type(directory)

NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = register_nodes()
NODE_CLASS_MAPPINGS.update(loader_mappings)
NODE_DISPLAY_NAME_MAPPINGS.update(loader_display)
register_routes()

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
