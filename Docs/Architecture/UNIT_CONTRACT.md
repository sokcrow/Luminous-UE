# Luminous Unit Architecture Contract

## Core rule

**Every character that exists and acts in the world is a Unit.**

Species, ancestry, body size, movement type, faction, role, intelligence, player ownership,
NPC status, monster status, flying, swimming or walking do **not** create separate runtime
character classes.

A dragon is a Unit.
A goblin is a Unit.
A horse is a Unit.
A fish is a Unit.
A player avatar is a Unit.
A DM-controlled creature is a Unit.

The distinction between Player and DM is **control policy**, not actor type.

## Unit is the world actor

A Unit owns or exposes the general systems that allow a living actor to participate in the world:

- movement;
- collision and spatial presence;
- interaction;
- inventory/equipment where applicable;
- item use;
- eating and drinking;
- sleeping/resting;
- combat;
- conditions/status effects;
- senses/perception;
- animation state;
- dialogue/speech capability where applicable;
- locomotion modes such as walk, swim, fly or climb;
- world needs and other shared simulation systems.

A mechanic that applies to Units must be implemented once at the Unit/system level.

Do **not** implement a special player eating system, goblin inventory, dragon movement system,
etc. Differences are represented by data, capabilities, components, tags and rules.

## Data changes behavior; it does not create a new actor category

- Size changes collision dimensions, reach, occupied space and presentation.
- Species/ancestry changes statistics, traits and available capabilities.
- A flying creature has a flying locomotion capability/mode.
- A swimming creature has a swimming locomotion capability/mode.
- A creature that cannot use equipment simply lacks or restricts that capability.
- A creature that does not need sleep has data/rules that disable or modify the shared rest mechanic.

All of them remain Units.

## Control model

### Player

A Player is linked to **one Unit as their world avatar**.

The player's input and interaction authority targets that Unit.

```text
Player Account / Session
        |
        v
Player Controller
        |
   fixed binding
        |
        v
      Unit
```

The normal player control policy does not allow freely jumping between Units.

### DM

The DM is not represented by a special world Unit.

The DM has supervisory authority and may possess/control a Unit, move it, interact through it,
speak through it, perform its available Unit actions, release it and switch to another Unit.

```text
DM Session
    |
    v
DM Controller / Authority
    |
    +---- possess ----> Unit A
    |
    +---- switch -----> Unit B
    |
    +---- switch -----> Unit C
```

The Unit itself does not change type when controlled by a Player, DM, AI or nobody.

## Unreal architecture

```text
ALuminousUnit
|
+-- Unit Identity / Data
+-- Unit Stats
+-- Unit Locomotion
+-- Unit Interaction
+-- Unit Inventory / Equipment
+-- Unit Needs
+-- Unit Combat
+-- Unit Conditions
+-- Unit Animation (PaperZD presentation)
+-- Unit Senses / Perception
```

Controller layer:

```text
ALuminousPlayerController
    -> bound to one authorized Unit

ALuminousDMController
    -> can possess/release/switch among Units

AAIController
    -> may control any Unit allowed to use AI
```

The exact Unreal base class (`ACharacter` versus a custom `APawn`) may be selected after
locomotion prototyping, but that choice must not break the single-Unit model.

## Animation rule

PaperZD presents a Unit; it does not define one.

Animation consumes generalized Unit state such as locomotion, facing, speed, combat action,
condition and interaction action.

## Non-negotiable invariants

1. No PlayerCharacter gameplay subclass with exclusive mechanics.
2. No NPCCharacter gameplay subclass with duplicated mechanics.
3. No MonsterCharacter gameplay subclass with duplicated mechanics.
4. Player, DM and AI are control modes over Units.
5. Unit mechanics are generalized first; species, size and capabilities specialize through data.
6. A Unit remains the same Unit when control changes.
7. Save, network and world identity belong to the Unit, not to the temporary controller.
