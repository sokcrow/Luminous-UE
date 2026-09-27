"""Luminus UE editor bootstrap.

Run inside Unreal Editor's Python environment. This script only creates the
canonical Content Browser folders; gameplay remains C++/Blueprint.
"""

import unreal

FOLDERS = [
    "/Game/Luminus",
    "/Game/Luminus/Characters",
    "/Game/Luminus/Characters/Sprites",
    "/Game/Luminus/Characters/Flipbooks",
    "/Game/Luminus/World",
    "/Game/Luminus/World/Maps",
    "/Game/Luminus/World/Terrain",
    "/Game/Luminus/World/Water",
    "/Game/Luminus/World/Foliage",
    "/Game/Luminus/World/Props",
    "/Game/Luminus/Materials",
    "/Game/Luminus/Materials/Water",
    "/Game/Luminus/Materials/Terrain",
    "/Game/Luminus/PCG",
    "/Game/Luminus/UI",
]


def run() -> None:
    for folder in FOLDERS:
        if not unreal.EditorAssetLibrary.does_directory_exist(folder):
            unreal.EditorAssetLibrary.make_directory(folder)
            unreal.log(f"[Luminus] created {folder}")
    unreal.log("[Luminus] editor bootstrap complete")


if __name__ == "__main__":
    run()
