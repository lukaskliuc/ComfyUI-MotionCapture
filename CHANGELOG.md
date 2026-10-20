# Changelog

## 2026-10-20 — File loading and folder fixes

### Fixed

- Refresh SMPL, camera trajectory, Mixamo and BVH dropdowns without restarting
  ComfyUI. Use native refresh buttons and scan input/output subfolders.
- Run the four lightweight file loaders in ComfyUI so cached isolation metadata
  cannot freeze file lists or suppress file-change fingerprints. Keep the other
  18 nodes isolated and preserve existing node IDs, inputs and output types.
- Check selected files stay inside the configured input/output folders.
- Propagate configured input, output and temporary folders into metadata and
  execution workers, including ComfyUI Desktop installations.
- Resolve relative filenames in seven exporters against the configured output
  folder. Support absolute paths, legacy output/temp prefixes and Windows
  separators without creating duplicate output/output folders.
- Seed bundled examples into the configured input folder, including input/3d FBX
  assets, without overwriting existing files.

### Changed

- Vendor editable viewer source from upstream dev (68e8c9f) in javascript/ and
  register it through pyproject.toml. Remove generated-viewer copying and the
  comfy-3d-viewers dependency; retain comfy-env 0.3.89.
- Disable automatic Comfy registry publishing for this personal fork.
- Ignore local environments, generated data/log folders and the personal
  FIXES.md checklist.

### Validation

- Five regression tests pass, covering all four file loaders, refresh responses,
  fingerprints, nested paths, path containment, export paths and asset seeding.
- All 22 nodes register in the running Windows ComfyUI installation.
- Live SMPL-to-BVH and FBX rest-pose exports succeed using configured folders;
  newly exported files appear immediately through the refresh endpoint.
