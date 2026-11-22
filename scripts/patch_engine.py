#!/usr/bin/env python3
"""Patch upstream renderer so all visuals are staged beneath Remotion's public directory."""
from pathlib import Path

target = Path("engine/src/render.ts")
source = target.read_text(encoding="utf-8")
needle = """        // Stage assets from workspace/<id>/ to staging/<id>/ for Remotion staticFile()
        if (assetWorkspaceDir && sceneData.assetNamespace) {
            const publicRoot = resolveRuntimePublicPath();
            const jobPublicDir = path.join(publicRoot, path.basename(assetWorkspaceDir));
            if (fs.existsSync(assetWorkspaceDir) && assetWorkspaceDir !== jobPublicDir) {
                fs.rmSync(jobPublicDir, { recursive: true, force: true });
                fs.mkdirSync(jobPublicDir, { recursive: true });
                copyRecursiveSync(assetWorkspaceDir, jobPublicDir);
                stagingDir = jobPublicDir;
                console.log(`📦 [RENDER] Staged assets: ${assetWorkspaceDir} → ${jobPublicDir}`);
            }
        }
"""
replacement = needle + """
        // Keep every visual beneath Remotion public/. Acquired cache images can live
        // outside assetWorkspaceDir, so copy them individually into this job's staging folder.
        if (stagingDir) {
            const visualDir = path.join(stagingDir, "visuals");
            fs.mkdirSync(visualDir, { recursive: true });
            for (let i = 0; i < sceneData.scenes.length; i++) {
                const visualPath = sceneData.scenes[i].visual?.localPath;
                if (!visualPath) continue;
                const absolutePath = path.isAbsolute(visualPath)
                    ? visualPath
                    : path.resolve(assetWorkspaceDir || outputDir, visualPath);
                if (!fs.existsSync(absolutePath) || !fs.statSync(absolutePath).isFile()) {
                    continue;
                }
                const extension = path.extname(absolutePath) || ".jpg";
                const filename = `scene_${i + 1}${extension}`;
                fs.copyFileSync(absolutePath, path.join(visualDir, filename));
                sceneData.scenes[i].visual.localPath = path.posix.join(
                    path.basename(assetWorkspaceDir || stagingDir),
                    "visuals",
                    filename
                );
            }
        }
"""
if (needle not in source):
    raise SystemExit("Expected renderer staging block was not found; refusing to patch unknown upstream source.")
start = source.find("Keep every visual beneath Remotion public/.")
if start < 0:
    if "Remotion staticFile() only accepts paths relative to public/." in source:
        # Replace the earlier, incomplete path-rewrite patch with robust per-scene staging.
        begin = source.find("        // Remotion staticFile() only accepts paths relative to public/.")
        end = source.find("\n        console.log(`📋 [RENDER] Loaded", begin)
        if begin < 0 or end < 0:
            raise SystemExit("Could not locate earlier patch boundaries.")
        source = source[:begin] + replacement[len(needle):] + source[end:]
    else:
        source = source.replace(needle, replacement, 1)
    target.write_text(source, encoding="utf-8")
    print("Patched renderer to copy visuals into public/ and use relative paths.")
else:
    print("Robust renderer asset patch already present.")
