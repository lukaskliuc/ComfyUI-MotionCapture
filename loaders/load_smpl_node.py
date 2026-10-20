"""
LoadSMPLParams Node - Load SMPL params from disk.

Loads smpl_params_*.npz files from ComfyUI output folder.
"""

import logging

from comfy_api.latest import io

from .shared_utils import resolve_file_path, list_files, file_fingerprint

log = logging.getLogger("motioncapture")


class LoadSMPLParams(io.ComfyNode):
    """
    Select an SMPL params .npz file (smpl_params_*.npz).

    Searches both input and output folders.
    Returns the resolved file path.
    """

    @classmethod
    def define_schema(cls):
        npz_files = cls.get_npz_files()
        if not npz_files:
            npz_files = ["No smpl_params files found"]
        return io.Schema(
            node_id="LoadSMPL",
            display_name="Load SMPL Params",
            category="MotionCapture/SMPL",
            inputs=[
                io.Combo.Input("file_path", options=npz_files,
                               remote=io.RemoteOptions(route="/motioncapture/files/smpl", refresh_button=True),
                               tooltip="NPZ file containing SMPL parameters (smpl_params_*.npz from GVHMR Inference)"),
            ],
            outputs=[
                io.String.Output(display_name="file_path"),
            ],
        )

    @staticmethod
    def get_npz_files():
        return list_files('smpl_params_*.npz')

    @classmethod
    def fingerprint_inputs(cls, **kwargs):
        file_path = kwargs.get("file_path")
        try:
            return file_fingerprint(resolve_file_path(file_path))
        except FileNotFoundError:
            return file_path

    @classmethod
    def execute(cls, file_path):
        full_path = resolve_file_path(file_path)
        log.info("Selected: %s", full_path)
        return io.NodeOutput(full_path)


NODE_CLASS_MAPPINGS = {
    "LoadSMPL": LoadSMPLParams,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadSMPL": "Load SMPL Params",
}
