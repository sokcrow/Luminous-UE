# Forest 0.3.3.1 Module Audit -> Luminous UE

Source reviewed:

- `sokcrow/Luminos-Character-Maker`
- branch: `lab-preview-next`
- monolith: `game-engine/lab/game/forest-0.3.3.1.html`

## Measured shape

The current Forest host is still a large mixed runtime:

- ~1.22 MB HTML
- 20,650 lines
- 998 named inline functions
- 8 script tags
- one large ES module script
- dynamic imports for Three.js plus terrain/water/cave modules

There are also 37 JavaScript modules under `game-engine/src`.

This means the migration should not start by translating the whole HTML. We should
extract contracts and systems in controlled slices.

## Existing external modules

### Core

- `core/EventBus.js`
- `core/GameEngine.js`
- `core/GameRuntime.js`
- `core/RuntimeContracts.js`

### Camera

- `camera/CameraBridgeAdapter.js`
- `camera/CameraProfiles.js`
- `camera/CameraSystem.js`

### Units

- `units/UnitState.js`
- `units/UnitRegistry.js`
- `units/UnitControllerSystem.js`
- `units/UnitMovementSystem.js`
- `units/UnitEnvironmentSystem.js`
- `units/UnitRuntime.js`

### Maps / procedural

- `map/MapBridgeAdapter.js`
- `map/MapRegistry.js`
- `map/MapSystem.js`
- `map/procedural/SeededRandom.js`
- `map/procedural/ProceduralMapSpec.js`
- `map/procedural/ProceduralTerrain.js`
- `map/procedural/ProceduralHydrology.js`
- `map/procedural/ProceduralMapGenerator.js`
- `map/procedural/CrystalCaveGenerator.js`

### World

- `world/WorldSpaceContract.js`
- `world/CombatGeometry.js`
- `world/ContinuousMovement.js`
- `world/TerrainMobility.js`
- `world/TerrainHeightField.js`
- `world/TerrainSurfaceStandard.js`
- `world/WaterBodySystem.js`
- `world/WakeTrailSystem.js`
- `world/WorldFloorTextures.js`

### Integration / presentation

- `dm/DMDirector.js`
- `bridges/luminous/LuminousItemsBridge.js`
- `ui/HudViewModel.js`
- `ui/HudDomAdapter.js`
- `assets/BrowserAssetCache.js`
- `player/createLabPlayer.js`

## Important finding: external UnitRuntime is not the whole authoritative Unit model

The external Unit modules are structurally clean and useful, but Forest later evolved a
richer inline **UNIVERSAL UNIT RUNTIME v3**.

The inline runtime owns concepts that the external v2 modules do not completely model:

- capabilities;
- relationships;
- physics profiles;
- needs;
- animation profiles;
- generic controller switching;
- swim/fly/ground locomotion;
- buoyancy/falling/environment forces;
- Unit interactions;
- Unit needs;
- visual binding;
- DM/local/AI controller switching.

Therefore we must NOT blindly port `src/units/UnitRuntime.js` as the final Unreal Unit.
The inline universal Unit contract is the behavior reference.

## Most valuable migration seam: DM_SYSTEMS

Forest exposes a migration facade near the end of the monolith:

- maps
- rivers
- grid
- movement
- locomotion
- geometry
- collisions
- interactions
- pushables
- transitions
- units
- combat
- missions
- companion
- audit

This facade should become the compatibility boundary for extraction.

Instead of Unreal calling Forest internals, each facade domain gets a native Unreal owner.

## Port classes

### A. Port nearly as rules/math

These are mostly renderer-independent and should be translated deliberately to C++:

- `WorldSpaceContract.js`
- `TerrainMobility.js`
- `CombatGeometry.js`
- D&D continuous movement cost logic from `ContinuousMovement.js`
- `SeededRandom.js`
- procedural map spec normalization/validation
- selected procedural hydrology field math
- selected procedural terrain field math
- universal Unit data/capability/controller contracts

### B. Port the contract, replace the implementation

Keep the API/behavior but let Unreal provide the engine implementation:

- terrain height query
- collision query
- occupancy query
- movement resolution
- water sampling
- world interaction queries
- map activation
- camera following
- line of sight
- spatial queries

Examples:

`terrainSurfaceGroundYAtWorld(x,z)` should become a native world query, not a copied
Three.js height algorithm.

`canOccupyWorld(x,z,r)` should become a native collision/navigation query.

### C. Rebuild as Unreal presentation

Do not translate these renderer implementations line-by-line:

- PaperFX material/shader implementation
- Three.js meshes
- Three.js sprite billboard code
- Water mesh/foam geometry renderer
- Wake trail mesh renderer
- browser texture cache
- DOM HUD adapter
- fullscreen/orientation browser code
- manual scene graph renderer selection

Their visual contracts/assets can be preserved, but Unreal Materials, Niagara, PaperZD,
UMG and native rendering replace the JS implementation.

### D. Retire as Three.js compensation

These should not become Luminous gameplay architecture:

- manual render-distance object visibility management;
- Three.js scene chunk visibility toggling;
- manual shadow/mesh LOD switches that World Partition/HLOD/ISM/HISM replace;
- browser network loading fallbacks;
- DOM/iframe bridges;
- JS collision broadphase used only to compensate for the web renderer/runtime.

Semantic grid and D&D occupancy rules remain useful; the web broadphase itself does not.

## Inline Forest systems still trapped in the HTML

The following large sections are currently mixed into the 20k-line host and should be
extracted before/while porting:

1. **World Scale / Geometry**
   - 1 tile = 5 ft
   - geometry height standards
   - zone gate standards
   - common conversions

2. **World Time / Rest**
   - world clock
   - Short Rest +2 h
   - Long Rest +8 h
   - time phase/profile rules

3. **Biome / Geography / Geology**
   - Biome Composer
   - climate/landform/hydrology composition
   - geography modifiers
   - geology placement rules
   - coast continuous field

4. **Hydrology Gameplay**
   - stable river data contract
   - current
   - water depth/immersion
   - calm river shoulder
   - water-owned-height contract
   - lakes/coast fields

5. **World Interaction**
   - generic interaction registration
   - eligibility
   - range/vertical/facing rules
   - action resolution

6. **Authoritative Grid / World Query**
   - map grid compilation
   - grid cell queries
   - occupancy
   - combat arena extraction
   - elevation/stair/ledge queries

7. **Universal Unit Runtime v3**
   - Unit registry
   - Unit state
   - capabilities
   - relationships
   - controller policy
   - movement
   - physics
   - locomotion
   - environment
   - animation state
   - interactions
   - needs

8. **Transitions**
   - zone transitions
   - interior transitions
   - overpass/two-level surfaces

9. **Ecology**
   - tree species
   - forest floor ecology
   - flowers
   - shrubs
   - mushrooms
   - coast ecology

10. **DM / QA facades**
    - `DM_SYSTEMS`
    - `PaperUnits`
    - architecture tests
    - functional audit

## Target Unreal ownership

| Forest contract | Luminous UE target |
| --- | --- |
| Universal Unit Runtime | `ALuminousUnit` + Unit components/subsystems |
| Unit controller switching | Player/DM/AI Controller policy |
| World-space conversion | `LuminousWorldUnits` |
| Terrain mobility rules | `LuminousTerrainRules` |
| World queries | `ULuminousWorldQuerySubsystem` |
| Map registry/runtime | `ULuminousMapSubsystem` |
| Grid/combat geometry | `ULuminousTacticalGridSubsystem` / rules library |
| Interaction controller | `ULuminousInteractionSubsystem` + interactable interface |
| Hydrology gameplay | `ULuminousWaterSubsystem` |
| Water visual | Unreal Water + Luminous Material/Niagara |
| Procedural map/biome | PCG + native data assets + deterministic generation helpers |
| DM_SYSTEMS facade | `ULuminousDMSubsystem` calling native systems |
| Paper sprite state | PaperZD animation bridge |
| HUD DOM | UMG |
| Forest streaming | World Partition/HLOD/ISM/HISM |

## Extraction order

### Phase 1 — Rules that can be parity-tested without rendering

1. World scale/unit conversion
2. Unit contract/capabilities/control policy
3. Terrain mobility/slope rules
4. Combat geometry
5. Interaction eligibility
6. Grid/tactical queries
7. Water gameplay sample contract

### Phase 2 — World simulation contracts

8. World time/rest
9. Map definition/registry
10. Zone transitions
11. Hydrology fields
12. Procedural terrain/biome data

### Phase 3 — Unreal-native implementation

13. ALuminousUnit + controllers
14. WorldQuerySubsystem
15. InteractionSubsystem
16. WaterSubsystem
17. PaperZD animation bridge
18. Map/World Partition integration
19. PCG/ecology
20. Materials/Niagara presentation

## Rule for every extracted function

Each Forest function must be labeled one of:

- **PORT_RULE** — algorithm/rule should move to C++ with parity tests.
- **PORT_CONTRACT** — preserve inputs/outputs/behavior, replace implementation.
- **PORT_DATA** — preserve constants/catalog/data as Unreal DataAssets/DataTables.
- **REBUILD_PRESENTATION** — rebuild in Unreal Materials/PaperZD/Niagara/UMG.
- **RETIRE_WEB** — browser/Three.js compensation; do not port.

No function moves merely because it exists in Forest.
