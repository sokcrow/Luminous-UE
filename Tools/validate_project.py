#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
uproject = root / "Luminus.uproject"
data = json.loads(uproject.read_text(encoding="utf-8"))

assert data["Modules"][0]["Name"] == "Luminus"
plugins = {p["Name"] for p in data.get("Plugins", []) if p.get("Enabled")}
required = {"Paper2D", "EnhancedInput", "Water", "PCG", "Niagara", "PythonScriptPlugin", "EditorScriptingUtilities"}
missing = required - plugins
assert not missing, f"missing plugins: {sorted(missing)}"

required_files = [
    "Source/Luminus/Luminus.Build.cs",
    "Source/Luminus/Luminus.h",
    "Source/Luminus/Luminus.cpp",
    "Source/Luminus/LuminusGameModeBase.h",
    "Source/Luminus/LuminusGameModeBase.cpp",
    "Source/Luminus.Target.cs",
    "Source/LuminusEditor.Target.cs",
    "Content/Python/luminus/bootstrap_project.py",
    "Docs/Migration/FOREST_G_0_3_1_TO_UE.md",
]
for rel in required_files:
    assert (root / rel).exists(), f"missing {rel}"

assert not (root / "index.html").exists(), "legacy Scanner HTML must not remain on UE branch"
print("Luminus UE source scaffold: ok")
