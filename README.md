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
2. Enter the repository-relative path of a tracked `.exe` or `.dll`. The default target is `retro/exe et dll/age3y.exe`.
3. By default, the workflow reads the PE optional header and attempts a focused REA function dossier at the declared entry-point address. This is commonly runtime/CRT startup code; **it is not automatically the game's main or gameplay function**. Set `function_selector` to a function name or address to override the automatic selection.
4. Set the optional `search_query` input to search for a gameplay clue. Try one term per run, such as `unit`, `move`, `path`, `food`, `resource`, `build`, `train`, or `AI`. The workflow saves REA's result to `search.json` in the artifact. A hit is only a lead: inspect the match context and cross-references before classifying an address as gameplay code.
5. Download the `rea-analysis` artifact from the completed run. Function-analysis runs contain the overview JSON, PE entry-point metadata, function-selection status, target SHA-256 metadata, provider diagnostics, the selected function dossier, and a `callees/manifest.json` plus up to four direct internal-callee dossiers. Search runs contain `search.json`; search-only runs also include target metadata but intentionally omit `analysis.json` and `function.json`. Artifacts are retained for 14 days.

The workflow pins REA and Ghidra versions, validates that the target is a tracked repository file, and uses read-only GitHub permissions. It attempts a bounded dossier for up to four direct internal callees after a source function has been resolved. These are investigation leads, not automatically verified game-logic functions. When `search_query` is set and `function_selector` is blank, it skips the default entry-point/callee pass so a broad search does not spend time decompiling likely CRT startup code; set a selector on a separate run to inspect a promising hit. It performs analysis only: it does not commit reports to the repository, publish analysis output as a GitHub Release, reconstruct source code automatically, or build a native Linux executable. Workflow dispatch is available once this workflow is present on the repository's default branch.

## Current investigation status (2026-10-12)

The latest verified analysis at the time of this update is [workflow run #14](https://github.com/rakmahefa/aoe-rea/actions/runs/38249737918), which examined `0x5562ad` in `retro/exe et dll/age3y.exe`. The function appears to parse XML child nodes named `Particle`, read values including `filename` and `timeoff`, and delegate a constructed structure to `0x598def`. Together with runs #12–#13, this establishes a particle-definition resource-loading path (`0x555e86` → `0x555c89` → `0x5562ad`), not the core game simulation.

The artifact confirms that `0x5562ad` belongs to the particle-definition loading path: its only recovered string references are `Particle`, `filename`, and `timeoff`, and its direct caller is `0x555c89`. The suggested `0x555de7` is called with a small structure in that same path, but its behavior is unconfirmed; do not prioritize it over gameplay discovery by default. After the optional `search_query` input is available on the default branch, use terms such as `unit`, `move`, `path`, `food`, `resource`, `build`, `train`, or `AI` to find leads, then analyze promising addresses with `function_selector`. Search hits are clues, not proof of simulation behavior. Before every investigation, check whether a newer Actions run exists.

See [the French session handoff](docs/SESSION_HANDOFF.md) for the verified run history, binary identity, workflow steps, current lead, caveats, and a ready-to-copy prompt for a new chat. All interpretations remain provisional Ghidra findings: no original source or native Linux executable has been recovered or built.

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
