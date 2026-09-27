#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import sys
import zipfile
from collections import Counter
from pathlib import Path

SOURCE = Path(sys.argv[1] if len(sys.argv) > 1 else "source")
OUT = Path(sys.argv[2] if len(sys.argv) > 2 else "dist")
PACK = OUT / "Luminous_Iconography_Main"
REGISTRY = SOURCE / "js/item-icon-registry.js"

IMAGE_EXTS = {".png", ".svg", ".webp", ".jpg", ".jpeg"}
ROOTS = [
    SOURCE / "Assets/Icons",
    SOURCE / "Assets/Images/Buttons",
    SOURCE / "Assets/Images/Weather",
]

def rel(path: Path) -> str:
    return path.relative_to(SOURCE).as_posix()

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def family(path: str) -> str:
    parts = path.split("/")
    if path.startswith("Assets/Icons/items/") and len(parts) >= 4:
        return f"items/{parts[3]}"
    if path.startswith("Assets/Images/Buttons/"):
        return "ui/buttons"
    if path.startswith("Assets/Images/Weather/"):
        return "ui/weather"
    return "other"

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if PACK.exists():
        shutil.rmtree(PACK)
    PACK.mkdir(parents=True)

    registry_text = REGISTRY.read_text(encoding="utf-8")
    registered = set(re.findall(
        r"""[\"'\`]([^\"'\`]*Assets/[^\"'\`]+\.(?:png|svg|webp|jpg|jpeg))[\"'\`]""",
        registry_text,
        flags=re.I,
    ))

    files: list[Path] = []
    for root in ROOTS:
        if not root.exists():
            continue
        files.extend(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS)
    files = sorted(set(files), key=lambda p: rel(p).lower())

    rows = []
    family_counts = Counter()
    registered_count = 0
    total_bytes = 0

    for src in files:
        rp = rel(src)
        dest = PACK / rp
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        is_registered = rp in registered
        registered_count += int(is_registered)
        size = src.stat().st_size
        total_bytes += size
        fam = family(rp)
        family_counts[fam] += 1
        rows.append({
            "id": src.stem,
            "family": fam,
            "path": rp,
            "extension": src.suffix.lower().lstrip("."),
            "bytes": size,
            "registered_in_item_icon_registry": is_registered,
            "sha256": sha256(src),
        })

    registry_dir = PACK / "RegistrySource"
    registry_dir.mkdir(parents=True, exist_ok=True)
    for pattern in [
        "js/item-icon-registry.js",
        "js/item-catalog-*.js",
        "js/item-economy-standard.js",
        "game-engine/lab/player-menu-icon-only.js",
    ]:
        for src in SOURCE.glob(pattern):
            if not src.is_file():
                continue
            dest = registry_dir / rel(src)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)

    catalog_dir = PACK / "Catalog"
    catalog_dir.mkdir(parents=True, exist_ok=True)
    with (catalog_dir / "icon_manifest.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [
            "id","family","path","extension","bytes","registered_in_item_icon_registry","sha256"
        ])
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "pack": "Luminous Iconography Main",
        "source_repository": "sokcrow/Luminos-Character-Maker",
        "source_branch": "main",
        "source_commit": (SOURCE / ".source_commit").read_text(encoding="utf-8").strip()
            if (SOURCE / ".source_commit").exists() else None,
        "total_files": len(rows),
        "total_bytes": total_bytes,
        "registered_item_icons": registered_count,
        "unregistered_or_ui_files": len(rows) - registered_count,
        "families": dict(sorted(family_counts.items())),
        "notes": [
            "registered_in_item_icon_registry marks paths referenced by js/item-icon-registry.js",
            "UI buttons/weather are intentionally included even when not item-registry entries",
            "Files are copied without recompression or resizing",
            "Preserve alpha/transparency on PNG import into Unreal",
        ],
        "files": rows,
    }
    (catalog_dir / "icon_manifest.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    readme = f"""LUMINOUS ICONOGRAPHY PACK — MAIN

Source:
  sokcrow/Luminos-Character-Maker @ main
  commit: {metadata['source_commit'] or 'unknown'}

Contents:
  {len(rows)} icon/UI image files
  {registered_count} files referenced by js/item-icon-registry.js
  {len(rows)-registered_count} additional UI/unregistered image files
  {total_bytes} source bytes

Families:
"""
    for name, count in sorted(family_counts.items()):
        readme += f"  {name}: {count}\n"
    readme += """
Unreal import notes:
  - Import the PNG/SVG-derived raster assets into /Game/Luminous/UI/Icons by family.
  - Do not resize or recompress the source pack before import.
  - Preserve alpha/transparency.
  - Treat Catalog/icon_manifest.json as the canonical migration index.
  - RegistrySource preserves the current JS registry/catalog context for mapping IDs.

This package is an archival/import bundle. Unreal .uasset files should be generated by
the Unreal Editor and should not replace the original PNG/SVG sources.
"""
    (PACK / "README_IMPORT_UE.txt").write_text(readme, encoding="utf-8")

    zip_path = OUT / "Luminous_Iconography_Main.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_STORED, allowZip64=True) as z:
        for p in sorted(PACK.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(PACK.parent).as_posix())

    print(json.dumps({
        "zip": str(zip_path),
        "files": len(rows),
        "registered": registered_count,
        "bytes": total_bytes,
        "zip_bytes": zip_path.stat().st_size,
        "families": dict(sorted(family_counts.items())),
    }))

if __name__ == "__main__":
    main()
