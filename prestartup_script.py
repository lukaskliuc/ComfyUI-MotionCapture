from pathlib import Path

import folder_paths
from comfy_env import setup_env, copy_files

setup_env()

SCRIPT_DIR = Path(__file__).resolve().parent
INPUT_DIR = Path(folder_paths.get_input_directory())

# Seed examples without overwriting files edited by the user.
copy_files(SCRIPT_DIR / "assets", INPUT_DIR)
copy_files(SCRIPT_DIR / "assets", INPUT_DIR / "3d", "*.fbx")
