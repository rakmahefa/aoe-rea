# aoe-rea

Reverse-engineering research toward a **native Linux build of Age of Empires III**, using [REA (Reverse Engineer Anything)](https://github.com/morluto/rea) as the analysis toolchain.

The project is not intended to stop at disassembly reports or a Wine/Proton launcher. The long-term goal is to understand the original Windows program, reconstruct the required parts in maintainable source code, build a genuine Linux executable, and publish tested releases on this repository.

> **Status:** early research stage. The repository contains reference EXE/DLL files under [`retro/exe et dll/`](retro/exe%20et%20dll/). A complete native Linux port has not yet been established. Treat all future builds as experimental until their functionality is demonstrated and documented.

## Goal

Work toward a distributable Linux-native game build:

1. **Inventory the original files.** Identify executable and library versions, architectures, dependencies, hashes, and differences between variants.
2. **Analyze with REA.** Use REA with a supported native-analysis provider to inspect binary structure, functions, pseudocode, assembly, references, and call paths. Keep findings tied to the exact input binary and address.
3. **Reconstruct behavior.** Implement the required functionality in source code, preserving evidence and recording unresolved behavior. Decompiler output is evidence, not ready-to-compile original source.
4. **Validate incrementally.** Compare reconstructed behavior against the original where practical and add focused regression tests for each recovered component.
5. **Build natively for Linux.** Produce a Linux ELF executable and package only the files needed and permitted for distribution.
6. **Publish releases.** Use GitHub Actions to run checks, build Linux artifacts, record checksums, and publish versioned assets to [GitHub Releases](https://github.com/rakmahefa/aoe-rea/releases).

## Why this requires reconstruction

Windows `.exe` and `.dll` files are compiled PE binaries, not source code that can simply be recompiled for Linux. REA assists with analysis and evidence collection; it does **not** automatically convert an entire Windows game into a native Linux program.

A genuine native port may require reimplementing or replacing Windows-specific APIs, rendering, audio, input, networking, installers, and other platform-dependent components. The scope must be discovered through analysis rather than assumed in advance.

Running the original Windows binaries through Wine or Proton can be useful as a compatibility baseline or interim option, but it is **not** a native Linux build and is not the final goal of this project.

## Using REA

REA provides CLI and MCP workflows for reverse engineering native binaries. See its documentation for supported providers, setup, and native-analysis workflows:

- [REA repository and quick start](https://github.com/morluto/rea)
- [REA native investigation guide](https://github.com/morluto/rea/blob/main/docs/native-investigation.md)
- [REA CLI guide](https://github.com/morluto/rea/blob/main/docs/cli.md)
- [REA architecture](https://github.com/morluto/rea/blob/main/docs/architecture.mermaid)

A useful investigation should answer one concrete question at a time, such as:

- Which functions and libraries are involved in a particular behavior?
- How does one function call into another module?
- Which operating-system APIs or external libraries does a component require?
- What evidence supports a reconstructed implementation, and what remains uncertain?

For every substantial finding, record the input file/version, relevant function or address, evidence, interpretation, and remaining unknowns. Keep analysis artifacts reproducible and separate verified behavior from hypotheses.

## Running REA analysis in GitHub Actions

The manual [REA binary analysis workflow](.github/workflows/rea-analysis.yml) runs REA and Ghidra on a GitHub-hosted Linux runner:

1. Open **Actions → REA binary analysis → Run workflow**.
2. Keep `target_path` at `retro/exe et dll/age3y.exe` unless there is a documented reason to change the reference binary.
3. Use `search_query` for one literal string term per run, such as `unit`, `move`, `path`, `food`, `resource`, `build`, `train`, or `AI`. Results are string-data addresses, not function entrypoints.
4. Use `xref_address` with an address from `search.json` to inspect references to that string/data, for example `0xc36e20` (unit-obstruction diagnostic) or `0xc19dc0` (the `kbCanPath2` description). The workflow saves `xrefs.json` and its provider diagnostics to the artifact.
5. Once cross-references identify a plausible code address, run again with `function_selector` set to that function address to obtain the function dossier and up to four direct internal-callee dossiers. Do not pass a string address as `function_selector` unless a tool report confirms it is a function.
6. Download `rea-analysis`. Search-only and xref-only runs include target metadata and their respective result files; function-analysis runs include the overview, entry-point metadata, function dossier and callee manifest. Artifacts are retained for 14 days.

When `search_query` or `xref_address` is set without `function_selector`, the workflow skips the default PE entry-point/function pass so focused exploration does not waste time on likely CRT startup code. The workflow is read-only and performs static analysis only: it does not reconstruct source automatically or build a native Linux executable. Search matches and cross-references are leads, not proof of gameplay semantics.

## Current investigation status (2026-10-13)

The latest verified analysis is [REA binary analysis #23](https://github.com/rakmahefa/aoe-rea/actions/runs/38363697748). It used `function_selector=0x483a6a`, the post-geometry helper called by `FUN_004839bb` in run #20.

### Run #23 — post-geometry checks and status flags

REA resolved `FUN_00483a6a` as a non-external, non-thunk procedure. Its pseudocode calls several helpers, checks a property record and a floating-point field, then returns one of the small integer values `0` through `4`. On several paths it modifies a byte at offset `+0x1b` of the associated object, setting bit `0x01` or bit `0x04`.

Observed control flow:
- Calls an indirect-dispatch trampoline with a function pointer loaded from a vtable-like table at offset `+0xac`. If that result is false, returns `0`.
- Calls `FUN_004883dd`. If false, returns `4`.
- If the property/flag condition on the structure at `this+0x5c` permits further checks, calls two more indirect-dispatch trampolines associated with entries at offsets `+0x90` and `+0x98`.
- Depending on those results, sets `associated_object+0x1b |= 0x01` and returns `1` or `2`; or sets `associated_object+0x1b |= 0x04` and returns `3`.
- Some branches use addresses `0x483ee7`, `0x48ce21`, and `0x6a157e–0x6a1597`. Ghidra groups these into non-contiguous body ranges.

`FUN_004883dd` checks fields in the structure at `this+0x5c` and, on a fallback path, compares a float at `this+0x68+8` against approximately `1e-6`; it can call `FUN_006a0831`. This is observed validation/gating behavior, but neither its domain meaning nor the return-code meanings are established. Three short callees (`FUN_00483af4`, `FUN_00487ecc`, `FUN_004a5cb7`) are reported by Ghidra as unresolved computed/indirect dispatches, so their actual targets and semantics are not recovered in these dossiers.

Together with runs #20–22, the evidence suggests this function classifies or validates the result of a geometry/obstruction-related operation and records state bits. Do not assign game-level names to the return codes or flags without corroboration. It does not establish that this function performs pathfinding.

### Geometry findings from runs #20–22

- **Run #20**: `FUN_004839bb` checks an object’s obstruction-type field, chooses one of two geometry helpers, calls `FUN_00483a6a`, then calls `FUN_0048380f`. That final helper clamps four floating-point bounds to spatial-grid dimensions and updates cell membership; this gives medium-confidence evidence for spatial/occupancy bookkeeping.
- **Run #21**: `FUN_00483d4c` computes four axis-aligned rectangle corners from two coordinate values and two extents, then writes byte fields into a structure.
- **Run #22**: `FUN_004a5558` calculates four coordinate pairs using products/combinations of floating-point parameters and calls `FUN_004a5489`, which compares vertex coordinates and writes byte fields. Compared with #21, its arithmetic is consistent with an oriented quadrilateral/footprint, but the exact parameter and field meanings remain unknown.

Taken together, these runs provide **medium-confidence evidence of a geometry representation used in an obstruction-related path with subsequent state validation and spatial-cell handling**. This remains an inference from control flow and arithmetic, not a fully named engine subsystem. Several involved procedures have non-contiguous Ghidra body ranges, and should be checked before treating those ranges as conventional function bodies.

### Reproducibility and next direction

Run #23 used `retro/exe et dll/age3y.exe`, SHA-256 `b1a1dab7264d2db72e8f8ae1df1e419eecc223b40db00c9d1013a3bc77611d9d`, REA 6.4.0 and Ghidra 12.1.4. Artifact: `rea-analysis`, run ID `38363697748`, artifact ID `11797128628`; analyzed commit `ad539edede393f8d954bea01266e8d31fb4121f5`.

The next priority is to move from geometry/occupancy to explicit pathfinding evidence. Run the workflow with `xref_address=0xc19dc0` (the defined-string address for `kbCanPath2`), leaving `function_selector` and `search_query` empty. Inspect the returned reference site; only then select a confirmed code function. Later repeat for `kbCanSimPath` at `0xc19e68`. The gameplay string search from run #18 also contains separate movement, unit-count and economy leads.

Runs #12–#14 documented a particle-definition loading path, still lower priority than gameplay logic. No original source or native Linux executable has been recovered or built.

## Linux build and release plan

The intended release pipeline is:

- Run automated checks and regression tests on Linux.
- Compile the reconstructed source for the target Linux architecture.
- Verify that the output is a Linux ELF executable and document its runtime dependencies.
- Package the executable and permitted supporting files.
- Generate SHA-256 checksums and upload versioned artifacts to a GitHub Release.
- Document known limitations and the exact steps required to run the build.

A release must not be labelled a complete native port merely because compilation succeeds. Runtime testing and a clear list of working features are required.

## Repository contents

- `retro/exe et dll/` — reference Windows executables and libraries currently collected for analysis.
- `scripts/pe_entry_point.py` — reads the declared PE entry-point address using Python's standard library, without executing the binary.
- `tests/test_pe_entry_point.py` — synthetic PE32/PE32+ regression tests for the entry-point parser.
- `README.md` — project objective, workflow, and release direction.

As reconstruction progresses, keep implementation code, tests, evidence notes, and build configuration clearly separated from the original reference binaries.

## Legal and distribution note

Use game files only when obtained lawfully. Do not publish proprietary executables, DLLs, game assets, or other copyrighted material in releases unless redistribution is explicitly authorized. Prefer distributing independently reconstructed code and build instructions, with users supplying any proprietary game files that are legally required.

## Definition of success

The project succeeds when a GitHub Release provides a **genuine Linux-native executable**, reproducible build/release steps, documented dependencies, and an honest account of its tested functionality and limitations.
