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

## Current investigation status (2026-10-14)

The latest baseline analysis is [REA binary analysis #30](https://github.com/rakmahefa/aoe-rea/actions/runs/38452908507) ([artifact 11841443159](https://github.com/rakmahefa/aoe-rea/actions/runs/38452908507/artifacts/11841443159)). It decodes `0x8827d1` as `MOV ECX,dword ptr [EAX + 0x13c]` (6 bytes, `FALL_THROUGH`), still with `procedure=null`. Subsequent one-address probes have recovered an early false-return path and one direct helper call, but Ghidra still does not identify the callback label as a procedure entry. The probe workflow used during research is temporary and is not intended to remain in the repository.

### Runs #25–30 — pathfinding API registration and callback inspection

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

This establishes that Ghidra decodes a valid x86 instruction at the callback address and that it reads a global/data location. It does **not** identify the meaning of that global, nor prove that the callback's full implementation is only this instruction. At the time of run #29, the next sequential address was `0x8827d1`; the results of subsequent probes are summarized below.

### Run #29 — confirmed details

- URL: [REA binary analysis #29](https://github.com/rakmahefa/aoe-rea/actions/runs/38448930654)
- Input: `instruction_address=0x8827cc`; `function_selector`, `search_query`, and `xref_address` blank.
- Artifact: `rea-analysis`, run ID `38448930654`, artifact ID `11839108635`.
- `instruction.json`: operation `inspect_native_instruction`, status `decoded`, confidence `observed`.
- Target: `retro/exe et dll/age3y.exe`; SHA-256 `b1a1dab7264d2db72e8f8ae1df1e419eecc223b40db00c9d1013a3bc77611d9d`.
- Analyzed commit: `813677b565d1e26535c5908cc194e421603afe90`; REA 6.4.0; Ghidra 12.1.4.
- The workflow's `Inspect native instruction address` step passed. Function analysis, xrefs and string search were correctly skipped for this address-only run.
- Limitation from the report: Ghidra's operand decoder exposes the global address but not more detailed effective-memory addressing context, and `procedure` is null.

### Follow-up probes — callback control flow (14 October 2026)

All probe artifacts below use the same PE32 target and SHA-256 recorded for run #29. Adjacent callback addresses still report `procedure=null` in Ghidra.

| Address | Observed decode | Run and artifact |
|---|---|---|
| `0x8827d1` | `8b 88 3c 01 00 00` — `MOV ECX,dword ptr [EAX + 0x13c]`, 6 bytes, `FALL_THROUGH` | [Run #30](https://github.com/rakmahefa/aoe-rea/actions/runs/38452908507), [artifact 11841443159](https://github.com/rakmahefa/aoe-rea/actions/runs/38452908507/artifacts/11841443159) |
| `0x8827d7` | `85 c9` — `TEST ECX,ECX`, 2 bytes, `FALL_THROUGH` | [Probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38505129056), [artifact 11868005187](https://github.com/rakmahefa/aoe-rea/actions/runs/38505129056/artifacts/11868005187) |
| `0x8827d9` | `74 1a` — `JZ 0x008827f5`, 2 bytes, conditional jump | [Probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38505701574), [artifact 11867433197](https://github.com/rakmahefa/aoe-rea/actions/runs/38505701574/artifacts/11867433197) |
| `0x8827db` | `8b 15 64 66 c6 00` — `MOV EDX,dword ptr [0x00c66664]`, 6 bytes, `FALL_THROUGH` | [Probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38506248967), [artifact 11868017112](https://github.com/rakmahefa/aoe-rea/actions/runs/38506248967/artifacts/11868017112) |
| `0x8827e1` | `52` — `PUSH EDX`, 1 byte, `FALL_THROUGH` | [Probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38506676784), [artifact 11868386272](https://github.com/rakmahefa/aoe-rea/actions/runs/38506676784/artifacts/11868386272) |
| `0x8827e2` | `e8 3a a3 bc ff` — `CALL 0x0044cb21`, 5 bytes | [Probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38507195067), [artifact 11868985480](https://github.com/rakmahefa/aoe-rea/actions/runs/38507195067/artifacts/11868985480) |
| `0x44cb21` | `FUN_0044cb21`: checks whether the integer argument is in `[0, *(ECX+0x5c))`; if so, reads a dword from the array pointer at `ECX+0x58` indexed by that argument, otherwise returns zero. Ghidra reports non-contiguous body ranges `0x44cb21–0x44cb3e` and `0x4649e1–0x4649e5`. | [Function dossier](https://github.com/rakmahefa/aoe-rea/actions/runs/38507674474), [artifact 11868089731](https://github.com/rakmahefa/aoe-rea/actions/runs/38507674474/artifacts/11868089731) |
| `0x8827e7` | `85 c0` — `TEST EAX,EAX`, 2 bytes, `FALL_THROUGH` | [Probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38508299938), [artifact 11868907012](https://github.com/rakmahefa/aoe-rea/actions/runs/38508299938/artifacts/11868907012) |
| `0x8827e9` | `74 0a` — `JZ 0x008827f5`, 2 bytes, conditional jump | [Probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38508675506), [artifact 11869745563](https://github.com/rakmahefa/aoe-rea/actions/runs/38508675506/artifacts/11869745563) |
| `0x8827eb` | `8b 80 80 00 00 00` — `MOV EAX,dword ptr [EAX + 0x80]`, 6 bytes, `FALL_THROUGH` | [Probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38512045239), [artifact 11870287872](https://github.com/rakmahefa/aoe-rea/actions/runs/38512045239/artifacts/11870287872) |
| `0x8827f1` | `85 c0` — `TEST EAX,EAX`, 2 bytes, `FALL_THROUGH` | [Probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38512425597), [artifact 11870802007](https://github.com/rakmahefa/aoe-rea/actions/runs/38512425597/artifacts/11870802007) |
| `0x8827f3` | `75 03` — `JNZ 0x008827f8`, 2 bytes, conditional jump | [Probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38513028245), [artifact 11870374493](https://github.com/rakmahefa/aoe-rea/actions/runs/38513028245/artifacts/11870374493) |
| `0x8827f5` | `32 c0` — `XOR AL,AL`, 2 bytes, `FALL_THROUGH` | [Probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38508468586), [artifact 11868359993](https://github.com/rakmahefa/aoe-rea/actions/runs/38508468586/artifacts/11868359993) |
| `0x8827f7` | `c3` — `RET`, 1 byte, return flow | [Probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38511605181), [artifact 11870545584](https://github.com/rakmahefa/aoe-rea/actions/runs/38511605181/artifacts/11870545584) |
| `0x8827f8` | `8b 54 24 0c` — `MOV EDX,dword ptr [ESP + 0xc]`, 4 bytes, `FALL_THROUGH` | [Run #14](https://github.com/rakmahefa/aoe-rea/actions/runs/38513505693), [artifact 11870019274](https://github.com/rakmahefa/aoe-rea/actions/runs/38513505693/artifacts/11870019274) |
| `0x8827fc` | `68 82 97 79 00` — `PUSH 0x799782`, 5 bytes, `FALL_THROUGH`, DATA reference to `0x799782` | [Run #15](https://github.com/rakmahefa/aoe-rea/actions/runs/38526015005), [artifact 11875972173](https://github.com/rakmahefa/aoe-rea/actions/runs/38526015005/artifacts/11875972173) |
| `0x882801` | `6a 00` — `PUSH 0x0`, 2 bytes, `FALL_THROUGH` | [Run #16](https://github.com/rakmahefa/aoe-rea/actions/runs/38526782966), [artifact 11876875242](https://github.com/rakmahefa/aoe-rea/actions/runs/38526782966/artifacts/11876875242) |
| `0x882803` | `6a 00` — `PUSH 0x0`, 2 bytes, `FALL_THROUGH` | [Run #17](https://github.com/rakmahefa/aoe-rea/actions/runs/38527580929), [artifact 11876802096](https://github.com/rakmahefa/aoe-rea/actions/runs/38527580929/artifacts/11876802096) |
| `0x882805` | `6a 00` — `PUSH 0x0`, 2 bytes, `FALL_THROUGH` | [Run #18](https://github.com/rakmahefa/aoe-rea/actions/runs/38528517211), [artifact 11877336853](https://github.com/rakmahefa/aoe-rea/actions/runs/38528517211/artifacts/11877336853) |

**Observed control flow:** both `JZ` instructions (`0x8827d9` and `0x8827e9`) target `0x8827f5`, which zeroes `AL` and is immediately followed by `RET` at `0x8827f7`. Thus this shared branch clears the low return byte `AL` before `RET`; that is consistent with a false Boolean result, but does not prove that the full 32-bit `EAX` register is zero. On the other path, the code loads `[EAX+0x13c]` into `ECX`, branches to the shared `AL=0; RET` block if it is zero, and otherwise passes the dword loaded from `0x00c66664` as an index to `FUN_0044cb21`. The caller then tests the helper's `EAX` result and reaches the same `AL=0; RET` block if it is zero. When nonzero, execution falls through to `0x8827eb` and loads `[EAX+0x80]`. `TEST EAX,EAX` at `0x8827f1` is followed by `JNZ 0x8827f8` at `0x8827f3`; the zero case falls through to the shared `XOR AL,AL; RET` block (which explicitly zeroes `AL`, not necessarily all of `EAX`), while the nonzero case branches to `0x8827f8`. There, `MOV EDX,[ESP+0xc]` loads a dword from the stack, length 4, with `FALL_THROUGH` and `procedure=null`; the next sequential address is `0x8827fc`. There, `PUSH 0x799782` is decoded from bytes `68 82 97 79 00` (5 bytes, `FALL_THROUGH`), with a DATA reference to `0x799782`. Both the stack value's semantic role and the meaning/type of the referenced address remain unknown. At `0x882801`, `0x882803`, and `0x882805`, bytes `6a 00` decode as `PUSH 0x0` (2 bytes each, `FALL_THROUGH`, `procedure=null`), as documented in runs #16–18. Three consecutive zero pushes are observed, but do not prove a specific calling convention or argument meaning. The next sequential address is `0x882807`.

**Do not over-interpret:** `0x00c66234`, `0x00c66664`, offsets `+0x13c`, `+0x58`, `+0x5c`, and `+0x80` have not been assigned confirmed domain meanings. `FUN_0044cb21` behaves like a generic bounds-checked collection accessor based on its code, but that does not establish pathfinding semantics by itself. Continue along the nonzero branch at `0x8827f8` and inspect further branch/call/return edges. The geometry/obstruction/occupancy track from runs #20–23 remains separate.

### Geometry findings from runs #20–23

- **Run #20**: `FUN_004839bb` checks an object's obstruction-type field, chooses one of two geometry helpers, calls `FUN_00483a6a`, then calls `FUN_0048380f`. That final helper clamps four floating-point bounds to spatial-grid dimensions and updates cell membership; this gives medium-confidence evidence for spatial/occupancy bookkeeping.
- **Run #21**: `FUN_00483d4c` computes four axis-aligned rectangle corners from two coordinate values and two extents, then writes byte fields into a structure.
- **Run #22**: `FUN_004a5558` calculates four coordinate pairs using products/combinations of floating-point parameters and calls `FUN_004a5489`, which compares vertex coordinates and writes byte fields. Compared with #21, its arithmetic is consistent with an oriented quadrilateral/footprint, but the exact parameter and field meanings remain unknown.
- **Run #23**: `FUN_00483a6a` runs conditional checks, returns a code between 0 and 4, and may set bits in the associated object's state byte at offset `+0x1b`. Several calls use unresolved indirect dispatches, so the meanings of the codes and bits remain unknown.
- **Run #24**: xref query for the `kbCanPath2` documentation string at `0xc19dc0` returned `0x889735`, leading to API registration code in #25.

Runs #20–23 provide **medium-confidence evidence of geometry/obstruction/occupancy bookkeeping**. Runs #25–30 and the follow-up probes establish the callback registration, a bounds-checked helper call, and a shared early zero-return block. The success path and the callback's full procedure boundary remain unresolved. Keep geometric occupancy and pathfinding as separate evidence tracks until the callback's behavior and callees are understood.

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
