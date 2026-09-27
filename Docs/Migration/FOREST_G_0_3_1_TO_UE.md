# Forest G 0.3.1 -> Unreal Engine migration contract

## Principle

This is a behavioral port. We do **not** translate Three.js source line by line.

A Forest feature is considered ported only when the Unreal implementation preserves
the same player-facing contract and can be measured against the Forest reference.

## Runtime language split

- **C++**: authoritative runtime systems, movement, world queries, streaming hooks,
  water gameplay queries, save/runtime state.
- **Blueprints**: level-specific composition and presentation glue.
- **Materials**: terrain/water/foam shading and animation.
- **Paper2D**: player/NPC sprite and flipbook presentation in 3D.
- **PCG / instancing**: vegetation and repeated environmental props.
- **Python**: Editor automation, import, asset setup and repeatable content builds.
  Python must not become a gameplay dependency.

## Port map

### 1. World scale

Forest contract:
- logical tiles;
- current Limbus convention: 1 tile = 5 ft;
- local sectors/chunks used as gameplay organization.

UE target:
- centimeters as native units;
- one Forest tile maps to a single constant `LUMINUS_TILE_CM`;
- gameplay data keeps tile coordinates where useful, renderer converts at boundaries.

First implementation constant:
`5 ft = 152.4 cm`.

### 2. Terrain textures

Forest:
- seamless textures;
- explicit repeat/tiling;
- slope/elevation material decisions.

UE:
- Texture2D assets;
- master terrain Material;
- Material Instances per biome;
- TextureCoordinate/world-aligned tiling;
- Landscape material layers for authored terrain;
- PCG/material parameters for procedural regions.

Do not bake biome identity into one giant texture.

### 3. Water

Forest contract to preserve:
- water body knows surface height/depth;
- river/lake/ocean can have different visual profiles;
- shoreline foam is separate from terrain and follows the bank;
- foam belongs to world rendering, never overlays the player;
- river motion and foam motion can be animated independently;
- calm shoulder water may exist between strong current and land.

UE implementation:
- Water plugin for River/Lake/Ocean/Custom body topology and gameplay queries;
- Luminus master water Material for the Forest visual language;
- separate shoreline foam material/mesh/FX layer;
- water gameplay queries exposed through a Luminus C++ subsystem so combat/movement
  do not depend directly on a material or Blueprint.

### 4. 2D actor in 3D world

Forest:
- 2D player/NPC presentation in a 3D/2.5D world.

UE:
- PaperSprite/PaperFlipbook component;
- a C++ Character/Pawn owns movement/collision;
- sprite presentation is a child component and may billboard toward the camera;
- gameplay collision must never be derived from sprite pixels.

### 5. Camera

Forest behavior to capture before implementation:
- horizontal mobile presentation;
- free local orbit where allowed;
- fixed/authorial camera zones where required;
- camera collision/occlusion policy.

UE:
- CameraComponent + SpringArmComponent;
- Enhanced Input actions for orbit;
- camera profile data assets for Forest-like presets.

### 6. Streaming and LOD

Forest:
- local chunk/relevance ideas;
- frustum/distance culling;
- repeated props and vegetation.

UE:
- World Partition for spatial streaming;
- HLOD for far world representation;
- ISM/HISM for repeated meshes;
- PCG for density/biome placement;
- gameplay simulation relevance separated from render distance.

### 7. Data migration

Do not hard-code map definitions into Actor construction code.

Forest JSON/module-like definitions should become one of:
- PrimaryDataAsset;
- DataTable;
- JSON imported into DataAssets;
- PCG parameters.

This keeps future Limbus rules engine integration independent from rendering.

## Phase 0 acceptance

Before moving systems:
1. Pin the exact Forest G 0.3.1 file/commit.
2. Inventory its terrain textures and water assets.
3. Record numeric constants for scale, water motion, foam, camera and player movement.
4. Capture reference screenshots/video and one performance sample.
5. Only then implement parity in Unreal.

Until #1 is complete, no other Forest revision may silently substitute as the source.
