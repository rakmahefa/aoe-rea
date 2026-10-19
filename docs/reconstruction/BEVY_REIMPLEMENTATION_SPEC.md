# Native RTS reconstruction specification — Rust + Bevy

Status: architecture proposal, not feature-parity evidence.
Reference target: age3y.exe, SHA-256 b1a1dab7264d2db72e8f8ae1df1e419eecc223b40db00c9d1013a3bc77611d9d.
Engine baseline: pin Bevy 0.20.0 and a matching Rust toolchain. See https://bevy.org/news/bevy-0-20/ and https://bevy.org/learn/quick-start/getting-started/ecs/.

## 1. Goal and boundary

Build a maintainable native Linux RTS that reproduces observable core gameplay contracts as evidence accumulates: world/map rules, entity lifecycle, occupancy, navigation, orders, deterministic simulation, assets, rendering, UI and persistence.

Use a clean-room implementation. Do not transliterate decompiler pseudocode or ship the original executable, proprietary art/audio/maps/scenario text or other restricted assets as part of the clone. Use original, generated or appropriately licensed assets and document provenance. Keep the target binary and dossiers outside release packages.

## 2. Evidence baseline

The latest dossier workflow indexed 30,581 entries; every entry has a note; 30,576 decompilations succeeded and five failed. Existing reviewed clues include geometry/obstruction and spatial-grid helpers; coordinate-to-grid lookup; candidate tables, hash buckets and priority-heap operations near a path-query family; knowledge-base API registration for kbCanPath2 and kbCanSimPath; Win32 startup/UI paths; and one particle-definition XML path.

Not yet proven: full frame/tick loop, movement/path cost semantics, order transitions, economy/construction, combat, AI, critical render path, complete imports/dependencies/call graph, save/load, networking or gameplay parity. The subsystem scorecard is a planning measure, not a percentage of code understood. Decompiled notes are not behaviorally validated.

## 3. Essential system map

| Priority | System | Contract to discover | Current posture |
|---|---|---|---|
| P0 | Lifecycle and simulation clock | Startup, scenario loading, pause/resume, tick order, shutdown | Main lifecycle/tick not mapped |
| P0 | World/map and spatial occupancy | Coordinates, bounds, terrain, footprints, occupancy add/move/remove, passability | Partial static evidence |
| P0 | Orders and navigation | Accept/reject, route query, move/blocked/repath/arrive/cancel | Candidate internals partly mapped; semantics open |
| P0 | Entities and deterministic state | Stable IDs, ownership, lifecycle, fixed-tick ordering and replayable commands | To be specified/tested |
| P1 | Economy and construction | Resource ledger, gather, placement, work progress and cancellation | Not validated |
| P1 | Combat and damage | Target/range/visibility, cooldown, damage, death and occupancy removal | Not validated |
| P1 | Rendering, camera, selection and UI | World draw, camera, click-to-world, selection and command feedback | Bevy replaces presentation; old contract unmapped |
| P1 | Asset/resource catalog | Manifest, dependencies, load failures, caches and lifetimes | One narrow XML lead |
| P2 | Save/load, replay, network/mod interfaces | Versioned state snapshots and stable identifiers | Insufficient evidence |
| P2 | Audio/effects | Trigger contract, asset mapping and fallback behavior | Scope to decide |

Exhaustive batches cover every index in order, while semantic investigation should start from the known spatial/navigation candidates. Once runtime helpers are understood as a family, avoid spending the same effort on every wrapper.

## 4. Rust workspace boundary

Keep domain rules testable without a renderer. Proposed workspace:

    crates/
      game-domain/       typed IDs, commands, rules and value objects
      game-map/          map bounds, terrain and occupancy grid
      game-navigation/   path interface and request queue
      game-simulation/   fixed-tick orchestration, orders, economy and combat
      game-assets/       manifest/catalog and safe data import
      game-persistence/  versioned saves, checkpoints and replay events
      game-bevy/         Bevy app, rendering, input, camera, UI and audio adapters
    apps/
      native-game/       native Linux entry point
      scenario-runner/   headless tests and deterministic playback

Use Bevy ECS for identity-linked components and systems, but keep authoritative rules in pure Rust modules. Proposed components: StableEntityId, WorldPosition, GridCell, Footprint, CollisionClass, OccupancyMembership, OwnerId, TeamId, UnitArchetypeId, Health, MovementProfile, CurrentOrder, AttackProfile, Cooldown, ResourceStore, GatherTask and ConstructionProgress. Render transforms, animation and selection are projections, not gameplay truth.

Resources: SimulationClock, WorldMap, OccupancyGrid, TerrainCatalog, CommandQueue, PathRequestQueue, Ruleset, seeded RNG, event log, catalogs/manifests, save version and state hash.

## 5. Bevy plugin plan

- BootPlugin: configuration, lifecycle, scenario selection and diagnostics.
- AssetCatalogPlugin: asynchronous asset state, manifests, cache and error reporting.
- WorldGridPlugin: terrain, map bounds and occupancy synchronization.
- EntitySimulationPlugin: stable identity, ownership and entity lifecycle.
- OrdersPlugin: validation, command queue, cancellation and completion.
- NavigationPlugin: passability, path requests, movement intents and re-pathing.
- EconomyConstructionPlugin: resource accounting, work tasks, placement and progress.
- CombatPlugin: target validation, cooldown, damage, death and cleanup.
- AiKnowledgePlugin: typed decision interface, implementing only evidence-supported behavior.
- CameraInputPlugin and GameUiPlugin: selection, commands and user feedback.
- WorldRenderPlugin: terrain/entities/effects as a projection of simulation state.
- PersistencePlugin: versioned save/load, command/event recording and replay.
- DiagnosticsPlugin: state hashes, counters, traces and overlays.

## 6. Fixed-tick contract

Simulation time must be independent of variable render frames. The original tick interval, speed controls and pause rules are unknown until measured. Initial ordered phases:

1. Apply commands in stable sequence order.
2. Advance decision/AI systems and create typed orders.
3. Validate or recompute navigation requests from the current world snapshot.
4. Compute movement intents.
5. Resolve collision/occupancy and atomically commit entity positions.
6. Update gathering, construction and other work progress.
7. Resolve attacks, damage, death and entity cleanup.
8. Publish events, update derived UI and optionally capture state hashes.

Invariants: centralized world/grid conversion; occupancy changes idempotent or explicitly rejected; deterministic command/tie ordering; seeded RNG independent of render cadence; renderer callbacks never mutate authoritative rules; save/load followed by the same command sequence reproduces a state hash for supported scenarios.

## 7. Navigation contract

The heap/candidate/hash evidence does not prove A*. Hide the algorithm behind a Pathfinder trait until callers and scenarios reveal the cost model.

Specify input (start/goal, movement/footprint profile, terrain constraints, flags/callback), results (already-there, reachable, blocked goal, no route, invalid input, stale/cancelled, error), and edge rules (diagonals/corner cutting, occupied endpoints, footprint clearance, terrain costs, tie breaks, dynamic blockage and invalidation).

Tests: tiny known grids, rectangular/rotated footprints, narrow passages, blocked endpoints, out-of-bounds coordinates, equal-cost paths, dynamic obstacles and stress maps. First vertical slice: load a test map, spawn/select one entity, issue move, route around an obstacle, render movement and assert arrival plus occupancy integrity.

## 8. Delivery gates

| Gate | Deliverable | Pass condition |
|---|---|---|
| G0 — inventory | target fingerprint, imports/strings/call graph and failures | reproducible artifacts tied to SHA |
| G1 — system map | address-linked subsystem graph and reviewed dossiers | claims cite evidence and open questions |
| G2 — behavior contracts | repeatable original/oracle scenarios | state transitions recorded |
| G3 — vertical slice | map, select, move, avoid obstacle, arrive | headless tests and deterministic state pass |
| G4 — gameplay increments | economy/construction, combat, AI, UI as scoped | regression suite passes; divergences logged |
| G5 — native Linux | reproducible build and dependency report | executable launches and completes scenarios |
| G6 — parity/release | compatibility report, asset provenance, checksums | no “complete clone” claim without measured support |

## 9. Immediate execution order

1. Freeze the fingerprint and preserve the dossier artifact.
2. Generate all 100-entry worklists, failure report, API/import inventory, data/string cross-references and direct/indirect call graph.
3. Rank candidates using entry-point reachability, callers/callees, specific APIs/strings and world/path clues; keep ranking separate from evidence grade.
4. Trace spatial membership and the kbCanPath2/kbCanSimPath paths. Write contracts and tiny scenario tests before coding.
5. Establish lifecycle/tick and typed order flow, then build the occupancy/navigation vertical slice.
6. Add economy, construction, combat, rendering/UI and persistence in evidence-guided increments.
7. Record unresolved facts, test coverage, asset/license decisions, build environment and release limitations.

No native clone is demonstrated yet. A successful compile alone is not proof of compatible gameplay.
