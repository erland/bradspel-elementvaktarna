#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
DIST = ROOT / "dist"

DOCS = [
    ("docs/player/RULEBOOK.md", "docs/RULEBOOK.md"),
    ("docs/player/QUICKSTART.md", "docs/QUICKSTART.md"),
    ("docs/player/FAQ.md", "docs/FAQ.md"),
    ("docs/player/REFERENCE_CARD_A6.md", "docs/REFERENCE_CARD_A6.md"),
    ("output/pdf/rulebook.pdf", "docs/rulebook.pdf"),
    ("output/pdf/quickstart.pdf", "docs/quickstart.pdf"),
    ("output/pdf/faq.pdf", "docs/faq.pdf"),
]

OPTIONAL_PRINT_SVGS = [
    ("output/svg/board-a4.svg", "print/svg/board-a4.svg"),
    ("output/svg/board-a4-ink-friendly.svg", "print/svg/board-a4-ink-friendly.svg"),
]

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def copy_required(src: Path, dst: Path) -> None:
    if not src.is_file():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True, help="Exempel: v0.58 eller v1.0.0")
    parser.add_argument("--output-dir", default="dist")
    args = parser.parse_args()

    version = args.version
    if not version.startswith("v"):
        print("ERROR: version måste börja med v.", file=sys.stderr)
        return 2

    dist = ROOT / args.output_dir
    release_root = dist / f"elementvaktarna-{version}"
    if release_root.exists():
        shutil.rmtree(release_root)
    release_root.mkdir(parents=True, exist_ok=True)

    inventory = json.loads((ROOT / "RELEASE_INVENTORY.json").read_text(encoding="utf-8"))
    recommended = inventory["recommended_print"]

    copied = []
    for rel in recommended:
        name = Path(rel).name
        src = OUT / "pdf" / name
        dst = release_root / "print/pdf" / name
        copy_required(src, dst)
        copied.append(dst)

    for src_rel, dst_rel in DOCS:
        src = ROOT / src_rel
        dst = release_root / dst_rel
        copy_required(src, dst)
        copied.append(dst)

    for src_rel, dst_rel in OPTIONAL_PRINT_SVGS:
        src = ROOT / src_rel
        if src.is_file():
            dst = release_root / dst_rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied.append(dst)

    readme = release_root / "README.md"
    readme.write_text(
        f"# Elementväktarna {version}\n\n"
        "Detta är en automatiskt byggd print-and-play-release.\n\n"
        "## Rekommenderade printfiler\n\n"
        + "\n".join(f"- `print/pdf/{Path(p).name}`" for p in recommended)
        + "\n\nPDF är rekommenderat utskriftsformat. SVG-filerna för spelplanen "
          "finns med som källnära exportformat.\n",
        encoding="utf-8",
    )
    copied.append(readme)

    manifest = {
        "release": version,
        "generated_by": "scripts/package_release.py",
        "recommended_print": [f"print/pdf/{Path(p).name}" for p in recommended],
        "files": [],
    }
    for path in sorted(copied):
        rel = path.relative_to(release_root).as_posix()
        manifest["files"].append({
            "path": rel,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })

    manifest_path = release_root / "RELEASE_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    checksum_path = release_root / "checksums.sha256"
    checksum_lines = []
    for item in manifest["files"]:
        checksum_lines.append(f"{item['sha256']}  {item['path']}")
    checksum_path.write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")

    archive = dist / f"elementvaktarna-{version}-print.zip"
    if archive.exists():
        archive.unlink()
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for path in sorted(release_root.rglob("*")):
            if path.is_file():
                z.write(path, arcname=f"{release_root.name}/{path.relative_to(release_root).as_posix()}")

    print(release_root)
    print(archive)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
