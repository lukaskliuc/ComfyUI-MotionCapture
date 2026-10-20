"""MotionCapture Nodes."""

import os

import folder_paths

# Apply configured paths before node imports capture directory constants.
for directory in ("input", "output", "temp"):
    configured = os.environ.get(f"MOTIONCAPTURE_{directory.upper()}_DIRECTORY")
    if configured:
        getattr(folder_paths, f"set_{directory}_directory")(configured)

# GPU nodes
from .load_model import LoadGVHMRModels
from .inference_node import GVHMRInference
from .save_smpl_node import SaveSMPL
from .fbx_loader_node import LoadFBXCharacter
from .fbx_preview_node import FBXPreview
from .fbx_animation_viewer_node import FBXAnimationViewer
from .smpl_to_bvh_node import SMPLtoBVH
from .bvh_viewer_node import BVHViewer
from .compare_smpl_bvh_node import CompareSMPLtoBVH
from .compare_skeletons_node import CompareSkeletons

# Blender nodes
from .retarget_node import SMPLToFBX
from .bvh_retarget_node import BVHtoFBX
from .smpl_retarget_node import SMPLRetargetToSMPL
from .smpl_to_mixamo_node import SMPLToMixamo
from .rest_pose_node import ExtractRestPose
from .glb_export_node import SMPLToGLB

# Viewer nodes
from .viewer_node import NODE_CLASS_MAPPINGS as viewer_mappings
from .viewer_node import NODE_DISPLAY_NAME_MAPPINGS as viewer_display
from .smpl_camera_viewer_node import NODE_CLASS_MAPPINGS as camera_viewer_mappings
from .smpl_camera_viewer_node import NODE_DISPLAY_NAME_MAPPINGS as camera_viewer_display

NODE_CLASS_MAPPINGS = {
    # GPU nodes
    "LoadGVHMRModels": LoadGVHMRModels,
    "GVHMRInference": GVHMRInference,
    "SaveSMPL": SaveSMPL,
    "LoadFBXCharacter": LoadFBXCharacter,
    "FBXPreview": FBXPreview,
    "FBXAnimationViewer": FBXAnimationViewer,
    "SMPLtoBVH": SMPLtoBVH,
    "BVHViewer": BVHViewer,
    "CompareSMPLtoBVH": CompareSMPLtoBVH,
    "CompareSkeletons": CompareSkeletons,
    # Blender nodes
    "SMPLToFBX": SMPLToFBX,
    "BVHtoFBX": BVHtoFBX,
    "SMPLRetargetToSMPL": SMPLRetargetToSMPL,
    "SMPLToMixamo": SMPLToMixamo,
    "ExtractRestPose": ExtractRestPose,
    "SMPLToGLB": SMPLToGLB,
    # Viewer nodes
    **viewer_mappings,
    **camera_viewer_mappings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    # GPU nodes
    "LoadGVHMRModels": "Load GVHMR Models",
    "GVHMRInference": "GVHMR Inference",
    "SaveSMPL": "Save SMPL Motion",
    "LoadFBXCharacter": "Load FBX Character",
    "FBXPreview": "FBX 3D Preview",
    "FBXAnimationViewer": "FBX Animation Viewer",
    "SMPLtoBVH": "SMPL to BVH Converter",
    "BVHViewer": "BVH Animation Viewer",
    "CompareSMPLtoBVH": "Compare SMPL vs BVH",
    "CompareSkeletons": "Compare Skeletons",
    # Blender nodes
    "SMPLToFBX": "SMPL to FBX Retargeting",
    "BVHtoFBX": "BVH to FBX Retargeter",
    "SMPLRetargetToSMPL": "SMPL to SMPL Retargeting",
    "SMPLToMixamo": "SMPL to Mixamo",
    "ExtractRestPose": "Extract Rest Pose",
    "SMPLToGLB": "SMPL to GLB Animation",
    # Viewer nodes
    **viewer_display,
    **camera_viewer_display,
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
