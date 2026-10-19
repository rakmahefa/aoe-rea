# Function-analysis protocol: batches of 100

## Identity and scope

- Target: retro/exe et dll/age3y.exe
- SHA-256: b1a1dab7264d2db72e8f8ae1df1e419eecc223b40db00c9d1013a3bc77611d9d
- Ghidra: 12.1.4
- Dossier run: https://github.com/rakmahefa/aoe-rea/actions/runs/39106827655
- Inventory: 30,581 entries; 30,576 decompilations marked successful; five failed; every entry has a Markdown note.

A different target hash is a different dataset. Do not silently combine inventories.

## Review strategy

1. Generate structural information for every function and divide stable index order into groups of 100: BATCH_000 = indices 0–99, and so on. There are 306 batches; the final batch has 81 rows.
2. Maintain a separate priority queue to elevate game-specific imports/strings, script API registrations, large/high-fan-in routines, indirect dispatch, world/occupancy, navigation, tick/lifecycle, rendering and file/resource paths.
3. Group compiler/runtime/allocator/string helpers by family. Map them to Rust/platform facilities where possible instead of cloning each helper one by one.
4. For each candidate, inspect callers, callees, cross-references, globals/strings, data layout and error paths. A callee address or function name is not a semantic explanation.
5. Record a disposition for every indexed entry. Keep unknown behavior explicitly unknown.

## Required function record

For every reviewed entry, capture:
- target SHA, address, Ghidra name and source note;
- purpose hypothesis; arguments and return contract, if known;
- state read/written and side effects;
- direct callees, indirect calls/callbacks, relevant strings/globals and data structures;
- error paths, edge conditions, allocation/synchronization;
- evidence grade, open questions, candidate replacement module and proposed repeatable test;
- behavior_validated = true only after a test against the original or trusted oracle is recorded with conditions/results.

## Evidence levels

| Grade | Meaning |
|---|---|
| E0 | Unknown: address/name only |
| E1 | Signal: string, import or registration hints at a role |
| E2 | Structure: body/data flow proves a narrow operation |
| E3 | Corroborated: callers/callees/xrefs/native instructions support a system interpretation |
| E4 | Behavior validated: repeatable observation confirms the contract |

Decompiler success is a pipeline status, not an evidence grade. Static-only findings should remain E1–E2 and behavior_validated = false.

## Generated reports

Run:

    python3 scripts/prepare_function_batches.py --input function-dossiers --output function-batches --batch-size 100

The workflow artifact contains:
- function-batch-index.csv: every entry with structural cues and pending status;
- priority-review-queue.csv plus a top-500 Markdown view: heuristic investigation order, not confidence ranking;
- batches/BATCH_NNN.md: exhaustive worklists with original note paths;
- a manifest and README with coverage counts.

## Failure handling

Keep the five failed decompilations as explicit work items. Review workflow logs and native bytes; do not invent pseudocode. Track non-contiguous bodies, thunks, jump tables and unresolved indirect targets separately from successful decompilation.
