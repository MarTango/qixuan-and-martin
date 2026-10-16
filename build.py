#!/usr/bin/env python3
"""Resize photos from originals/ into web-sized photos/ and thumbs/, then write photos.json.

Usage: python3 build.py
Requires macOS `sips` (built in). Re-running skips files already processed.
"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
ORIGINALS = ROOT / "originals"
PHOTOS = ROOT / "photos"
THUMBS = ROOT / "thumbs"
EXTS = {".jpg", ".jpeg", ".png", ".heic"}
FULL_PX = 2000
THUMB_PX = 600


def resize(src: Path, dest: Path, px: int) -> None:
    if dest.exists():
        return
    subprocess.run(
        ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "80",
         "-Z", str(px), str(src), "--out", str(dest)],
        check=True, capture_output=True,
    )


def dimensions(path: Path) -> tuple[int, int]:
    out = subprocess.run(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
        check=True, capture_output=True, text=True,
    ).stdout
    vals = {l.split(":")[0].strip(): int(l.split(":")[1]) for l in out.splitlines()[1:]}
    return vals["pixelWidth"], vals["pixelHeight"]


def main() -> None:
    PHOTOS.mkdir(exist_ok=True)
    THUMBS.mkdir(exist_ok=True)
    sources = sorted(p for p in ORIGINALS.rglob("*") if p.suffix.lower() in EXTS)
    if not sources:
        print(f"No photos found in {ORIGINALS}/ - add some and re-run.")
        return

    manifest = []
    for src in sources:
        name = src.stem.replace(" ", "-") + ".jpg"
        resize(src, PHOTOS / name, FULL_PX)
        resize(src, THUMBS / name, THUMB_PX)
        w, h = dimensions(THUMBS / name)
        manifest.append({"full": f"photos/{name}", "thumb": f"thumbs/{name}", "w": w, "h": h})
        print("ok", name)

    (ROOT / "photos.json").write_text(json.dumps(manifest, indent=1))
    print(f"Wrote photos.json with {len(manifest)} photos")


if __name__ == "__main__":
    main()
