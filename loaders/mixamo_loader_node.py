"""
LoadMixamoCharacter Node - Load Mixamo-rigged FBX characters.

Searches both input and output folders for .fbx files.
"""

import os
import logging

from comfy_api.latest import io

from .shared_utils import resolve_file_path, list_files, file_fingerprint

log = logging.getLogger("motioncapture")


class LoadMixamoCharacter(io.ComfyNode):
    """
    Load a Mixamo-rigged FBX character.

    Searches both input and output folders for .fbx files.
    Returns the resolved file path.
    """

    @classmethod
    def define_schema(cls):
        fbx_files = cls._get_fbx_files()
        if not fbx_files:
            fbx_files = ["No .fbx files found"]
        return io.Schema(
            node_id="LoadMixamoCharacter",
            display_name="Load Mixamo Character",
            category="MotionCapture/Mixamo",
            inputs=[
                io.Combo.Input("fbx_file", options=fbx_files,
                               remote=io.RemoteOptions(route="/motioncapture/files/mixamo", refresh_button=True),
                               tooltip="FBX file containing Mixamo-rigged character"),
            ],
            outputs=[
                io.String.Output(display_name="fbx_path"),
                io.String.Output(display_name="info"),
            ],
        )

    @staticmethod
    def _get_fbx_files():
        return list_files('*.[fF][bB][xX]')

    @classmethod
    def fingerprint_inputs(cls, **kwargs):
        fbx_file = kwargs.get("fbx_file")
        try:
            return file_fingerprint(resolve_file_path(fbx_file))
        except FileNotFoundError:
            return fbx_file

    @classmethod
    def execute(cls, fbx_file):
        full_path = resolve_file_path(fbx_file)

        file_size = os.path.getsize(full_path) / (1024 * 1024)  # MB
        source = "output" if fbx_file.startswith("[output] ") else "input"

        info = (
            f"Mixamo Character Loaded\n"
            f"File: {fbx_file}\n"
            f"Source: {source}\n"
            f"Full path: {full_path}\n"
            f"Size: {file_size:.2f} MB\n"
        )

        log.info("Selected: %s", full_path)
        return io.NodeOutput(full_path, info)


NODE_CLASS_MAPPINGS = {
    "LoadMixamoCharacter": LoadMixamoCharacter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadMixamoCharacter": "Load Mixamo Character",
}
