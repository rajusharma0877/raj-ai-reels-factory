#!/usr/bin/env python3
"""Patch the pinned-at-run upstream renderer so Remotion receives public-relative asset paths."""
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
        // Remotion staticFile() only accepts paths relative to public/. The acquired
        // scene data may contain absolute cache paths; map them to the staged copy.
        if (stagingDir && assetWorkspaceDir) {
            for (const scene of sceneData.scenes) {
                const localPath = scene.visual?.localPath;
                if (!localPath) continue;
                const absolutePath = path.isAbsolute(localPath)
                    ? localPath
                    : path.resolve(assetWorkspaceDir, localPath);
                const relativeToWorkspace = path.relative(assetWorkspaceDir, absolutePath);
                if (!relativeToWorkspace.startsWith("..") && !path.isAbsolute(relativeToWorkspace)) {
                    scene.visual.localPath = path.posix.join(
                        path.basename(assetWorkspaceDir),
                        relativeToWorkspace.split(path.sep).join("/")
                    );
                }
            }
        }
"""
if needle not in source:
    raise SystemExit("Expected renderer staging block was not found; refusing to patch unknown upstream source.")
if "Remotion staticFile() only accepts paths relative to public/." not in source:
    target.write_text(source.replace(needle, replacement, 1), encoding="utf-8")
    print("Patched renderer asset paths.")
else:
    print("Renderer asset-path patch already present.")
