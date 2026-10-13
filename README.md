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

The latest verified analysis is [REA binary analysis #22](https://github.com/rakmahefa/aoe-rea/actions/runs/38354872448). It used `function_selector=0x4a5558`, the alternative geometry helper called from `FUN_004839bb` (run #20).

### Run #22 — alternative geometry path

REA successfully resolved `FUN_004a5558` as a native Ghidra procedure. Its pseudocode:
- takes an output structure, two coordinate-like values, and four further floating-point parameters;
- combines those parameters multiplicatively to calculate four coordinate pairs and writes them at offsets `+0x20`–`+0x3c`;
- calls `FUN_004a5489`, which compares the generated vertex coordinates and writes four byte fields at offsets `+0x1c`–`+0x1f`;
- writes an additional byte at `+0x19` derived from one parameter scaled by 64 and the sign of another parameter.

Unlike the axis-aligned corners written by `FUN_00483d4c` in run #21, the formula used here combines two coordinate components in each corner. This is consistent with computing a rotated/oriented quadrilateral or footprint. That interpretation is plausible from the arithmetic; the exact meanings of the floating-point parameters and structure fields are not identified by symbols.

`FUN_004a5558` calls `FUN_004a5489`. The callee appears to select corner/edge-related index values from comparisons among the stored vertex coordinates, then stores those indices in the structure. It has no further callees or referenced strings in its dossier. Ghidra reports multiple non-contiguous body ranges for both procedures, so these inferred function boundaries still merit caution.

The caller context matters: run #20 showed `FUN_004839bb` choosing between `FUN_00483d4c` and `FUN_004a5558` based on a property/flag test. Run #21 showed `FUN_00483d4c` calculate an axis-aligned four-corner rectangle; run #22 shows the alternative path using more general coordinate combinations. Taken together with `FUN_0048380f` from run #20, this gives **medium-confidence evidence for a geometry/occupancy representation used in an obstruction-related code path**. It does not yet prove the exact game-level object type or the pathfinding algorithm.

### Reproducibility and limits

The run used `retro/exe et dll/age3y.exe`, SHA-256 `b1a1dab7264d2db72e8f8ae1df1e419eecc223b40db00c9d1013a3bc77611d9d`, REA 6.4.0 and Ghidra 12.1.4. The analysis artifact is `rea-analysis` from run ID `38354872448` (artifact ID `11792938137`). The function body for `FUN_004a5558` has 265 bytes over three ranges, with a total address span of 80,534 bytes; its callee `FUN_004a5489` has 251 bytes over three ranges. The earlier caller `FUN_004839bb` also spans non-contiguous regions across more than 2.2 MB. Do not assume every distant range is a conventional linear body without further instruction-flow verification.

The next useful target is `0x483a6a`, called after either geometry branch by `FUN_004839bb`. After that, return to the string leads for pathfinding — `kbCanPath2` (`0xc19dc0`) and `kbCanSimPath` (`0xc19e68`) — using xrefs to identify code addresses before selecting functions. Movement, economy and AI clues remain separate research tracks.

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
