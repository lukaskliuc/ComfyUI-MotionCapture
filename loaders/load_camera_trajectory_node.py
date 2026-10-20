"""
LoadCameraTrajectory Node - Load camera trajectory from disk.

Loads camera_trajectory_*.npz files from ComfyUI output folder.
"""

import logging

from comfy_api.latest import io

from .shared_utils import resolve_file_path, list_files, file_fingerprint

log = logging.getLogger("motioncapture")


class LoadCameraTrajectory(io.ComfyNode):
    """
    Select a camera trajectory .npz file (camera_trajectory_*.npz).

    Searches both input and output folders.
    Returns the resolved file path.
    """

    @classmethod
    def define_schema(cls):
        npz_files = cls.get_npz_files()
        if not npz_files:
            npz_files = ["No camera_trajectory files found"]
        return io.Schema(
            node_id="LoadCameraTrajectory",
            display_name="Load Camera Trajectory",
            category="MotionCapture/SMPL",
            inputs=[
                io.Combo.Input("file_path", options=npz_files,
                               remote=io.RemoteOptions(route="/motioncapture/files/camera", refresh_button=True),
                               tooltip="NPZ file containing camera trajectory (camera_trajectory_*.npz from GVHMR moving camera)"),
            ],
            outputs=[
                io.String.Output(display_name="camera_npz_path"),
            ],
        )

    @staticmethod
    def get_npz_files():
        return list_files('camera_trajectory_*.npz')

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
    "LoadCameraTrajectory": LoadCameraTrajectory,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadCameraTrajectory": "Load Camera Trajectory",
}
