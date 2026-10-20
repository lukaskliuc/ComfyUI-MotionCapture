"""Lightweight file loaders run in ComfyUI so schemas and fingerprints stay live."""

from aiohttp import web
from server import PromptServer

from .load_smpl_node import LoadSMPLParams
from .load_camera_trajectory_node import LoadCameraTrajectory
from .mixamo_loader_node import LoadMixamoCharacter
from .bvh_loader_node import LoadBVHFromFolder
from .shared_utils import list_files

NODE_CLASS_MAPPINGS = {
    "LoadSMPL": LoadSMPLParams,
    "LoadCameraTrajectory": LoadCameraTrajectory,
    "LoadMixamoCharacter": LoadMixamoCharacter,
    "LoadBVHFromFolder": LoadBVHFromFolder,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadSMPL": "Load SMPL Params",
    "LoadCameraTrajectory": "Load Camera Trajectory",
    "LoadMixamoCharacter": "Load Mixamo Character",
    "LoadBVHFromFolder": "Load BVH (Dropdown)",
}


def register_routes():
    @PromptServer.instance.routes.get("/motioncapture/files/{kind}")
    async def files(request):
        kind = request.match_info["kind"]
        if kind == "smpl":
            options = LoadSMPLParams.get_npz_files() or ["No smpl_params files found"]
        elif kind == "camera":
            options = LoadCameraTrajectory.get_npz_files() or ["No camera_trajectory files found"]
        elif kind == "mixamo":
            options = LoadMixamoCharacter._get_fbx_files() or ["No .fbx files found"]
        elif kind == "bvh":
            options = list_files("*.[bB][vV][hH]", legacy_prefix=True) or ["None"]
        else:
            raise web.HTTPNotFound()
        return web.json_response(options)
