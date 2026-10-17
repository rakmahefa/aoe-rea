# Progress dashboard — native Linux reconstruction of Age of Empires III

**Last updated:** 2026-10-17  
**Repository:** [rakmahefa/aoe-rea](https://github.com/rakmahefa/aoe-rea)  
**Reference binary:** `retro/exe et dll/age3y.exe`  
**SHA-256:** `b1a1dab7264d2db72e8f8ae1df1e419eecc223b40db00c9d1013a3bc77611d9d`  
**Latest verified main:** `4dd1e638cb53e77375c4b1061e5f290a6ea73af0`  
**Current documentation PR:** [#17](https://github.com/rakmahefa/aoe-rea/pull/17)

> This dashboard separates what we understand about the original program from progress toward a working native Linux clone. A disassembly is not automatically understood, an understood function is not automatically reconstructed, and a successful compile is not proof of gameplay compatibility.

## Current indicators

| Indicator | Current value | What it means |
|---|---:|---|
| **Essential-system understanding** | **12.45 / 100 ≈ 12%** | Preliminary weighted score across the essential subsystems listed below. It measures the strength and breadth of documented behavioral understanding, not lines of code decompiled. |
| **Whole-program function coverage** | **Not yet measurable** | We do not yet have a verified whole-binary inventory/count of functions, imports, and dependencies to use as the denominator. Do not substitute a count of the functions we happened to inspect. |
| **Working native Linux clone demonstrated** | **0% verified** | No reconstructed game source, working native ELF game executable, or gameplay parity test has been demonstrated yet. This is an evidence-based delivery status, not a claim that preparatory work is zero. |
| **Analysis toolchain** | **Operational for focused probes** | REA 6.4.0 + Ghidra 12.1.4 successfully decode selected instructions and produce retrievable artifacts. This does not mean full-game analysis is automated. |

### How the essential-understanding score is calculated

Each subsystem receives a progress level based on evidence. Its contribution is `subsystem weight × level / 100`. The weights total 100. They are a first-pass estimate of *essentiality* and must be revised when a whole-program inventory and dependency graph are available.

Scoring rubric for the level within each subsystem:

- **0% — undiscovered:** no usable evidence.
- **10% — located:** relevant strings, API registration, imports, or cross-references found; behavior mostly unknown.
- **25% — partially mapped:** some functions, data structures, and call/control-flow paths are supported by concrete evidence, but important branches or semantics remain unresolved.
- **50% — core behavior mapped:** main path, key state/data structures, callers/callees and failure paths are documented; remaining uncertainties are bounded.
- **75% — behavior strongly understood:** alternate paths and side effects documented, with corroborating evidence or comparison against the original.
- **100% — behavior validated:** intended behavior and edge cases are supported by repeatable tests against the original or an equivalent trusted oracle. Confidence and unknowns are recorded.

Do not award points merely because a function has pseudocode. Every nonzero rating must cite evidence in the table below. The 12.45% score is therefore a conservative, explicitly weighted *working estimate*, not a literal percentage of all original code.

## Essential-system scorecard

| Essential subsystem | Weight | Current level | Weighted contribution | Evidence and reason |
|---|---:|---:|---:|---|
| Startup, OS/runtime and external dependencies | 12% | 10% | 1.20 | Startup/runtime functions have been sampled, but there is no complete import, DLL, platform-API, or dependency map. [Runs #6 and #8](https://github.com/rakmahefa/aoe-rea/actions/runs/38177590652). |
| Main game loop, lifecycle and global state | 12% | 0% | 0.00 | No sufficiently supported model of the complete frame/tick loop or lifecycle yet. |
| World, entities, simulation and spatial occupancy | 20% | 25% | 5.00 | Several geometry/obstruction helpers and a grid-membership update path are mapped; field meanings and gameplay behavior remain incomplete. [Run #20](https://github.com/rakmahefa/aoe-rea/actions/runs/38347489501), [#21](https://github.com/rakmahefa/aoe-rea/actions/runs/38350963849), [#22](https://github.com/rakmahefa/aoe-rea/actions/runs/38354872448), [#23](https://github.com/rakmahefa/aoe-rea/actions/runs/38363697748). |
| Pathfinding, navigation and knowledge-base callbacks | 18% | 25% | 4.50 | `kbCanPath2` is registered, and candidate tables, hash buckets, a min-heap and priority updates are partially mapped; complete path semantics, costs and data meanings are unproven. [Run #25](https://github.com/rakmahefa/aoe-rea/actions/runs/38383598678), [run #43](https://github.com/rakmahefa/aoe-rea/actions/runs/38745133893), [run #45](https://github.com/rakmahefa/aoe-rea/actions/runs/38774292963). |
| Gameplay rules, unit orders, AI, economy and construction | 16% | 0% | 0.00 | No sufficiently broad, behaviorally validated model yet. Path-related API names alone do not count as understanding these systems. |
| Rendering, graphics and display pipeline | 10% | 0% | 0.00 | Critical rendering path and replacement requirements not mapped. |
| Input, audio and UI | 5% | 10% | 0.50 | Some Windows message/UI handling has been inspected, but not the complete input/audio/gameplay interface. [Run #10](https://github.com/rakmahefa/aoe-rea/actions/runs/38197841851). |
| Assets, files and resource loading | 5% | 25% | 1.25 | A particle-definition XML loading path is documented; coverage of the overall resource manager and asset formats is unknown. [Run #12](https://github.com/rakmahefa/aoe-rea/actions/runs/38203166028), [#13](https://github.com/rakmahefa/aoe-rea/actions/runs/38205614725), [#14](https://github.com/rakmahefa/aoe-rea/actions/runs/38249737918). |
| Save/load, networking, replay and mod interfaces | 2% | 0% | 0.00 | Not yet investigated enough to score. |
| **Total** | **100%** |  | **12.45%** | **≈12% essential-system understanding** |

## Function-level coverage: the missing denominator

The essential-system score above is a useful planning indicator, but it does **not** answer “what percentage of the entire executable have we understood?” We need a reproducible inventory before that question can be answered.

The next inventory milestone should export, for the exact SHA-256 above:

1. Total functions recognized by Ghidra, with entry address, body size/ranges and whether the function boundary is trustworthy.
2. Imports, imported DLLs, exports (where relevant), strings, executable/data segments and direct/indirect references.
3. Call-graph coverage: discovered callers/callees, unresolved indirect calls, and library/runtime versus likely gameplay functions.
4. A reviewed classification of functions into the essential subsystems above, plus “unknown/unclassified”.

Then report two different function percentages:
- **Function triage coverage** = functions with at least a recorded classification / total inventoried functions.
- **Function behavior understanding** = functions with evidence-backed behavioral summaries / total inventoried functions.

Both must include a denominator, inventory timestamp, target SHA-256, and rules for excluding thunks, duplicated code ranges, or malformed function boundaries. Also report a confidence distribution; a function with a guessed name must not count as understood.

## Native Linux clone delivery gates

These are intentionally independent of the understanding score.

| Gate | Status | Acceptance evidence |
|---|---|---|
| Exact target, version and analysis pipeline | In progress / usable | Reference executable fingerprinted; focused analysis artifacts reproducible. |
| Whole-program and dependency inventory | Not started | Machine-readable inventory of functions, imports/DLLs, strings, segments and indirect-call gaps. |
| Essential behavior specifications | Early research | Major subsystems mapped, facts separated from hypotheses, behavioral contracts written. |
| Differential/regression tests against original | Not started | Repeatable cases and expected observations for each reconstructed subsystem. |
| Reconstructed, maintainable source modules | Not started | Original behavior implemented without copying decompiler pseudocode wholesale. |
| Linux platform/graphics/audio/input compatibility layer | Not started | Required Windows APIs and runtime dependencies replaced or implemented and tested. |
| Native Linux ELF build | Not demonstrated | Reproducible Linux build produces the intended ELF and records architecture/dependencies. |
| Runtime and gameplay validation | Not demonstrated | Launch, representative scenarios, saves/assets where in scope, stability and parity checks pass. |
| Legal packaging and release | Not started | Only distributable/authorized assets included; checksums, known limitations and instructions published. |

**No native clone should be called “working” until the ELF and runtime/gameplay checks pass.** Running the original Windows executable through Wine/Proton is a useful baseline but does not satisfy this gate.

## Recent evidence and immediate next steps

- [Probe #58 — `0x401fc8: ADD ESI,EBP`](https://github.com/rakmahefa/aoe-rea/actions/runs/38923177848) · [artifact](https://github.com/rakmahefa/aoe-rea/actions/runs/38923177848/artifacts/12055028788).
- [Probe #59 — `0x401fca: SUB EDI,0x1`](https://github.com/rakmahefa/aoe-rea/actions/runs/39012977596) · [artifact](https://github.com/rakmahefa/aoe-rea/actions/runs/39012977596/artifacts/12094140406).
- [Probe #60 — `0x401fcd: JNZ 0x00401fbf`](https://github.com/rakmahefa/aoe-rea/actions/runs/39013905352). Its retrievable artifact confirms the instruction bytes `75 f0`, conditional-jump flow and enclosing procedure `0x401fa0`. The next useful address follows the taken branch: `0x401fbf`.

Immediate order of work:

1. Continue tracing the loop and callback at `0x401fbf`, keeping evidence attached to run/artifact IDs.
2. Build the machine-readable whole-binary inventory so function-level progress has a real denominator.
3. Refine weights after subsystem classification and dependency mapping, then update this dashboard only when new evidence changes a score.

## Update policy

Update this file and the session handoff in the same documentation PR when a new finding changes a rating, an evidence link, the function inventory, or a delivery gate. Record score changes with the previous value and the reason; do not silently rewrite historical estimates. Keep geometry/obstruction evidence separate from pathfinding hypotheses until a direct link is demonstrated.
