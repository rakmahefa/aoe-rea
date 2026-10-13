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

The latest verified analysis is [REA binary analysis #29](https://github.com/rakmahefa/aoe-rea/actions/runs/38448930654). This is the first successful use of the workflow's new `instruction_address` input to inspect the callback label `0x8827cc` without treating it as a function entry.

### Runs #25–29 — pathfinding API registration and callback inspection

Run #25 resolved xref site `0x889735` to `FUN_00885d07`, a large routine spanning `0x885d07–0x890373` (42,605 bytes). Its pseudocode registers script-callable knowledge-base APIs by name, callback pointer, argument count, parameter metadata and description:
- `kbCanSimPath` → `LAB_0088277e` (address `0x88277e`), 8 arguments.
- `kbCanPath2` → `LAB_008827cc` (address `0x8827cc`), 8 arguments.

The embedded descriptions define both as Boolean path checks for a unit type between two vectors, with a range. In run #25's assembly, the registration sequence around `0x88960a` includes `PUSH 0x8827cc` followed by a call to `FUN_00624f52`, consistent with passing the callback address during registration. This proves the registration reference, not the callback's whole implementation.

Runs #26–27 attempted `function_selector=0x8827cc` and failed because REA reported `No procedure exists at the requested address: 0x8827cc`. Run #28 queried xrefs for `0x8827cc` and returned only the known registration site `0x88960a`.

Run #29 used `instruction_address=0x8827cc`; the new workflow step succeeded and decoded the address as:
- Bytes: `a1 34 62 c6 00` (5 bytes)
- Instruction: `MOV EAX,[0x00c66234]`
- Flow: `FALL_THROUGH`, non-conditional, no direct destinations
- Data reference: reads address `0x00c66234`
- Procedure: `null` (Ghidra does not currently associate this address with a recovered procedure)

This establishes that Ghidra decodes a valid x86 instruction at the callback address and that it reads a global/data location. It does **not** identify the meaning of that global, nor prove that the callback's full implementation is only this instruction. Since the decoded instruction length is 5 bytes and control flow is fall-through, the next adjacent address to inspect is `0x8827d1`. Continue inspecting adjacent instructions until control flow, a function boundary, or a meaningful branch/call becomes apparent; do not label the callback based on a single instruction.

### Run #29 — confirmed details

- URL: [REA binary analysis #29](https://github.com/rakmahefa/aoe-rea/actions/runs/38448930654)
- Input: `instruction_address=0x8827cc`; `function_selector`, `search_query`, and `xref_address` blank.
- Artifact: `rea-analysis`, run ID `38448930654`, artifact ID `11839108635`.
- `instruction.json`: operation `inspect_native_instruction`, status `decoded`, confidence `observed`.
- Target: `retro/exe et dll/age3y.exe`; SHA-256 `b1a1dab7264d2db72e8f8ae1df1e419eecc223b40db00c9d1013a3bc77611d9d`.
- Analyzed commit: `813677b565d1e26535c5908cc194e421603afe90`; REA 6.4.0; Ghidra 12.1.4.
- The workflow's `Inspect native instruction address` step passed. Function analysis, xrefs and string search were correctly skipped for this address-only run.
- Limitation from the report: Ghidra's operand decoder exposes the global address but not more detailed effective-memory addressing context, and `procedure` is null.

### Geometry findings from runs #20–23

- **Run #20**: `FUN_004839bb` checks an object's obstruction-type field, chooses one of two geometry helpers, calls `FUN_00483a6a`, then calls `FUN_0048380f`. That final helper clamps four floating-point bounds to spatial-grid dimensions and updates cell membership; this gives medium-confidence evidence for spatial/occupancy bookkeeping.
- **Run #21**: `FUN_00483d4c` computes four axis-aligned rectangle corners from two coordinate values and two extents, then writes byte fields into a structure.
- **Run #22**: `FUN_004a5558` calculates four coordinate pairs using products/combinations of floating-point parameters and calls `FUN_004a5489`, which compares vertex coordinates and writes byte fields. Compared with #21, its arithmetic is consistent with an oriented quadrilateral/footprint, but the exact parameter and field meanings remain unknown.
- **Run #23**: `FUN_00483a6a` runs conditional checks, returns a code between 0 and 4, and may set bits in the associated object's state byte at offset `+0x1b`. Several calls use unresolved indirect dispatches, so the meanings of the codes and bits remain unknown.
- **Run #24**: xref query for the `kbCanPath2` documentation string at `0xc19dc0` returned `0x889735`, leading to API registration code in #25.

Runs #20–23 provide **medium-confidence evidence of geometry/obstruction/occupancy bookkeeping**. Runs #25–29 have traced the script API registration and begun inspecting the callback's native instruction, but the full pathfinding implementation is still unresolved. Keep geometric occupancy and pathfinding as separate evidence tracks until the callback's control flow and callees are understood.

Several earlier functions have non-contiguous Ghidra body ranges; verify control flow before treating every distant range as a conventional function body. Runs #12–14 documented a separate particle-definition loading path, still lower priority than gameplay logic. No original source or native Linux executable has been recovered or built.

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
