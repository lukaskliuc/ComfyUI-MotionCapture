"""Run with ComfyUI's Python: python -m unittest discover -s <extension>/tests."""

import asyncio
import importlib.util
import json
from pathlib import Path
import runpy
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

from aiohttp import web
import comfy_env
import folder_paths

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


routes = web.RouteTableDef()
server = types.ModuleType("server")
server.PromptServer = types.SimpleNamespace(instance=types.SimpleNamespace(routes=routes))
with patch.dict(sys.modules, {"server": server}):
    loaders = load_module("motioncapture_test_loaders", ROOT / "loaders/__init__.py")
    loaders.register_routes()
paths = load_module("motioncapture_test_paths", ROOT / "nodes/shared_utils.py")


class FilePathsTest(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.base = Path(self.scratch.name)
        for source in ("input", "output", "temp"):
            old = folder_paths.get_directory_by_type(source)
            setter = getattr(folder_paths, f"set_{source}_directory")
            self.addCleanup(setter, old)
            directory = self.base / ("configured_" + source)
            directory.mkdir()
            setter(str(directory))
        self.input = Path(folder_paths.get_input_directory())
        self.output = Path(folder_paths.get_output_directory())
        self.temp = Path(folder_paths.get_temp_directory())

    def write(self, source, name, content="test"):
        path = source / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def test_loaders_refresh_and_resolve_configured_folders(self):
        cases = (
            ("LoadSMPL", "file_path", "nested/smpl_params_new.npz", "smpl"),
            ("LoadCameraTrajectory", "file_path", "nested/camera_trajectory_new.npz", "camera"),
            ("LoadMixamoCharacter", "fbx_file", "3d/character.FBX", "mixamo"),
            ("LoadBVHFromFolder", "bvh_file", "nested/motion.bvh", "bvh"),
        )
        for node_id, argument, filename, route in cases:
            with self.subTest(node=node_id):
                node = loaders.NODE_CLASS_MAPPINGS[node_id]
                label = ("output/" if route == "bvh" else "[output] ") + filename
                before = node.INPUT_TYPES()["required"][argument]
                self.assertNotIn(label, before[1]["options"])
                path = self.write(self.output, filename, "Frames: 2\nFrame Time: 0.04\n")
                after = node.INPUT_TYPES()["required"][argument]
                self.assertIn(label, after[1]["options"])
                self.assertEqual(after[1]["remote"]["route"], f"/motioncapture/files/{route}")
                self.assertTrue(after[1]["remote"]["refresh_button"])
                request = types.SimpleNamespace(match_info={"kind": route})
                response = asyncio.run(routes[0].handler(request))
                self.assertIn(label, json.loads(response.body))
                loaded = node.execute(**{argument: label})[0]
                self.assertEqual(loaded["file_path"] if route == "bvh" else loaded, str(path.resolve()))
                if route == "bvh":
                    self.assertEqual((loaded["num_frames"], loaded["fps"]), (2, 25))
                fingerprint = node.fingerprint_inputs(**{argument: label})
                path.write_text("changed file with different size")
                self.assertNotEqual(fingerprint, node.fingerprint_inputs(**{argument: label}))
                path.unlink()
                self.assertNotIn(label, node.INPUT_TYPES()["required"][argument][1]["options"])

    def test_input_output_labels_and_windows_paths(self):
        self.write(self.input, "nested/smpl_params_same.npz")
        output = self.write(self.output, "nested/smpl_params_same.npz")
        self.assertEqual(loaders.LoadSMPLParams.get_npz_files(), [
            "nested/smpl_params_same.npz", "[output] nested/smpl_params_same.npz"])
        self.assertEqual(loaders.LoadSMPLParams.execute("[output] nested\\smpl_params_same.npz")[0], str(output.resolve()))
        bvh = self.write(self.input, "nested/demo.bvh", "Frames: 1\nFrame Time: 0.02\n")
        self.assertEqual(loaders.LoadBVHFromFolder.execute("input\\nested\\demo.bvh")[0]["file_path"], str(bvh.resolve()))

    def test_loader_rejects_paths_outside_selected_folder(self):
        outside = self.write(self.base, "smpl_params_secret.npz")
        for label in ("../smpl_params_secret.npz", str(outside), "[output] ../smpl_params_secret.npz"):
            with self.subTest(label=label), self.assertRaises(ValueError):
                loaders.LoadSMPLParams.execute(label)
        with self.assertRaises(FileNotFoundError):
            loaders.LoadMixamoCharacter.execute("missing.fbx")

    def test_output_paths_preserve_absolute_and_strip_legacy_prefix(self):
        for name in ("motion.fbx", "output/motion.fbx", "output\\motion.fbx"):
            with self.subTest(name=name):
                self.assertEqual(paths.resolve_output_path(name), self.output / "motion.fbx")
        self.assertEqual(paths.resolve_output_path("nested/motion.npz"), self.output / "nested/motion.npz")
        self.assertEqual(paths.resolve_output_path("temp\\preview.fbx"), self.temp / "preview.fbx")
        absolute = self.base / "explicit.fbx"
        self.assertEqual(paths.resolve_output_path(str(absolute)), absolute)

    def test_asset_seeding_uses_configured_input_and_preserves_existing(self):
        custom = self.write(self.input, "3d/mixamo.fbx", "user edited asset")
        with patch.object(comfy_env, "setup_env"):
            runpy.run_path(str(ROOT / "prestartup_script.py"))
        self.assertEqual(custom.read_text(), "user edited asset")
        self.assertTrue((self.input / "smpl_params_example.npz").is_file())
        self.assertTrue((self.input / "mixamo.fbx").is_file())


if __name__ == "__main__":
    unittest.main()
