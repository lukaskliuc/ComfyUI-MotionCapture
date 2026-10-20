
import logging
from pathlib import Path

from comfy_api.latest import io

from .shared_utils import list_files, resolve_bvh_path, file_fingerprint

log = logging.getLogger("motioncapture")

class LoadBVHFromFolder(io.ComfyNode):
    """
    Load a BVH file from a specific folder (input or output) using a dropdown menu.
    """

    @classmethod
    def define_schema(cls):
        files = list_files("*.[bB][vV][hH]", legacy_prefix=True)

        if not files:
            files = ["None"]

        return io.Schema(
            node_id="LoadBVHFromFolder",
            display_name="Load BVH (Dropdown)",
            category="MotionCapture/BVH",
            inputs=[
                io.Combo.Input("bvh_file", options=files,
                               remote=io.RemoteOptions(route="/motioncapture/files/bvh", refresh_button=True)),
            ],
            outputs=[
                io.Custom("BVH_DATA").Output(display_name="bvh_data"),
            ],
        )

    @classmethod
    def execute(cls, bvh_file: str) -> io.NodeOutput:
        if bvh_file == "None":
            return io.NodeOutput({})

        file_path = Path(resolve_bvh_path(bvh_file))

        with open(file_path, 'r') as f:
            content = f.read()

        # Parse basic info from content to populate bvh_data
        # Simple parsing to get frame count and FPS
        num_frames = 0
        frame_time = 0.033333

        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith("Frames:"):
                try:
                    num_frames = int(line.split(":")[1].strip())
                except Exception as e:
                    log.debug("Failed to parse BVH frame count: %s", e)
            elif line.startswith("Frame Time:"):
                try:
                    frame_time = float(line.split(":")[1].strip())
                except Exception as e:
                    log.debug("Failed to parse BVH frame time: %s", e)

        fps = int(round(1.0 / frame_time)) if frame_time > 0 else 30

        bvh_data = {
            "file_path": str(file_path.absolute()),
            "num_frames": num_frames,
            "fps": fps,
            "content": content # Store raw content if needed
        }

        return io.NodeOutput(bvh_data)

    @classmethod
    def fingerprint_inputs(cls, **kwargs):
        bvh_file = kwargs.get("bvh_file")
        if bvh_file == "None":
            return bvh_file
        try:
            return file_fingerprint(resolve_bvh_path(bvh_file))
        except FileNotFoundError:
            return bvh_file

NODE_CLASS_MAPPINGS = {
    "LoadBVHFromFolder": LoadBVHFromFolder,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadBVHFromFolder": "Load BVH (Dropdown)",
}
