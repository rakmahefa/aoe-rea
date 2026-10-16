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

## Current investigation status (2026-10-16)

The latest baseline analysis is [REA binary analysis #30](https://github.com/rakmahefa/aoe-rea/actions/runs/38452908507) ([artifact 11841443159](https://github.com/rakmahefa/aoe-rea/actions/runs/38452908507/artifacts/11841443159)). It decodes `0x8827d1` as `MOV ECX,dword ptr [EAX + 0x13c]` (6 bytes, `FALL_THROUGH`), still with `procedure=null`. Subsequent one-address probes have recovered an early false-return path and one direct helper call, but Ghidra still does not identify the callback label as a procedure entry. [Run #20](https://github.com/rakmahefa/aoe-rea/actions/runs/38530554944) confirmed `PUSH 0x0` at `0x882809` (2 bytes, `FALL_THROUGH`, `procedure=null`; [artifact 11878127349](https://github.com/rakmahefa/aoe-rea/actions/runs/38530554944/artifacts/11878127349)); [run #21](https://github.com/rakmahefa/aoe-rea/actions/runs/38535073544) confirmed the same at `0x88280b` (artifact 11880091082). [Run #22](https://github.com/rakmahefa/aoe-rea/actions/runs/38536133294) decoded bytes `8d 4c 24 2c` at `0x88280d` as `LEA ECX,[ESP+0x2c]` (4 bytes, `FALL_THROUGH`, `procedure=null`; [artifact 11881235066](https://github.com/rakmahefa/aoe-rea/actions/runs/38536133294/artifacts/11881235066)). [Run #23](https://github.com/rakmahefa/aoe-rea/actions/runs/38543440912) decoded byte `51` at `0x882811` as `PUSH ECX` (1 byte, `FALL_THROUGH`, `procedure=null`; [artifact 11884165751](https://github.com/rakmahefa/aoe-rea/actions/runs/38543440912/artifacts/11884165751)). [Run #24](https://github.com/rakmahefa/aoe-rea/actions/runs/38592966677) decoded bytes `8b 4c 24 28` at `0x882812` as `MOV ECX,dword ptr [ESP+0x28]` (4 bytes, `FALL_THROUGH`, `procedure=null`; [artifact 11909780246](https://github.com/rakmahefa/aoe-rea/actions/runs/38592966677/artifacts/11909780246)). [Run #25](https://github.com/rakmahefa/aoe-rea/actions/runs/38593942037) succeeded: byte `52` at `0x882816` decodes as `PUSH EDX` (1 byte, `FALL_THROUGH`, `procedure=null`; [artifact 11908194310](https://github.com/rakmahefa/aoe-rea/actions/runs/38593942037/artifacts/11908194310)). Run #26 succeeded: bytes `8b 54 24 28` at `0x882817` decode as `MOV EDX,dword ptr [ESP+0x28]` (4 bytes, `FALL_THROUGH`, `procedure=null`; [artifact 11947964421](https://github.com/rakmahefa/aoe-rea/actions/runs/38682182138/artifacts/11947964421)). Run #27 succeeded: byte `51` at `0x88281b` decodes as `PUSH ECX` (1 byte, `FALL_THROUGH`, `procedure=null`; [artifact 11948769728](https://github.com/rakmahefa/aoe-rea/actions/runs/38684233397/artifacts/11948769728)). Run #28 succeeded: byte `52` at `0x88281c` decodes as `PUSH EDX` (1 byte, `FALL_THROUGH`, `procedure=null`; [artifact 11950941183](https://github.com/rakmahefa/aoe-rea/actions/runs/38686269488/artifacts/11950941183)). The sequential callback probe #29 ([GitHub Actions run ID 38691004803](https://github.com/rakmahefa/aoe-rea/actions/runs/38691004803); [artifact 11952515685](https://github.com/rakmahefa/aoe-rea/actions/runs/38691004803/artifacts/11952515685)) completed successfully. It decodes `0x88281d` as `MOV ECX,EAX` (bytes `8b c8`, 2 bytes, `FALL_THROUGH`, `procedure=null`). The one-shot probe workflow's run #30 ([Actions run ID 38731342538](https://github.com/rakmahefa/aoe-rea/actions/runs/38731342538); [artifact 11970986662](https://github.com/rakmahefa/aoe-rea/actions/runs/38731342538/artifacts/11970986662)) then decoded `0x88281f` as `CALL 0x0087157b` (bytes `e8 57 ed fe ff`, 5 bytes, unconditional direct call, `procedure=null`). One-shot probe run #31 ([Actions run ID 38732373199](https://github.com/rakmahefa/aoe-rea/actions/runs/38732373199); [artifact 11971133081](https://github.com/rakmahefa/aoe-rea/actions/runs/38732373199/artifacts/11971133081)) confirms that `0x87157b` is a recognized procedure entry and decodes its first instruction as `MOV EAX,dword ptr [ESP + 0x20]` (bytes `8b 44 24 20`, 4 bytes, `FALL_THROUGH`). This establishes only a stack-relative dword read, not the value's semantic role. The function dossier from probe run #32 is summarized below. One-shot probe run #33 (https://github.com/rakmahefa/aoe-rea/actions/runs/38734503232) analyzes direct helper `FUN_00799898`. The sequential return address after the caller's `CALL` is `0x882824`; prioritize the callee chain first. These probe run numbers are specific to the temporary one-shot workflow and are distinct from the baseline analysis run numbering. The probe workflow used during research is temporary and is not intended to remain in the repository.

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
| `0x882807` | `6a 00` — `PUSH 0x0`, 2 bytes, `FALL_THROUGH` | [Run #19](https://github.com/rakmahefa/aoe-rea/actions/runs/38529441143), [artifact 11878120336](https://github.com/rakmahefa/aoe-rea/actions/runs/38529441143/artifacts/11878120336) |
| `0x882809` | `6a 00` — `PUSH 0x0`, 2 bytes, `FALL_THROUGH`, `procedure=null` | [Run #20](https://github.com/rakmahefa/aoe-rea/actions/runs/38530554944), [artifact 11878127349](https://github.com/rakmahefa/aoe-rea/actions/runs/38530554944/artifacts/11878127349) |
| `0x88280b` | `6a 00` — `PUSH 0x0`, 2 bytes, `FALL_THROUGH`, `procedure=null` | [Run #21](https://github.com/rakmahefa/aoe-rea/actions/runs/38535073544), [artifact 11880091082](https://github.com/rakmahefa/aoe-rea/actions/runs/38535073544/artifacts/11880091082) |
| `0x88280d` | `8d 4c 24 2c` — `LEA ECX,[ESP + 0x2c]`, 4 bytes, `FALL_THROUGH`, `procedure=null` | [Run #22](https://github.com/rakmahefa/aoe-rea/actions/runs/38536133294), [artifact 11881235066](https://github.com/rakmahefa/aoe-rea/actions/runs/38536133294/artifacts/11881235066) |
| `0x882811` | `51` — `PUSH ECX`, 1 byte, `FALL_THROUGH`, `procedure=null` | [Run #23](https://github.com/rakmahefa/aoe-rea/actions/runs/38543440912), [artifact 11884165751](https://github.com/rakmahefa/aoe-rea/actions/runs/38543440912/artifacts/11884165751) |
| `0x882812` | `8b 4c 24 28` — `MOV ECX,dword ptr [ESP + 0x28]`, 4 bytes, `FALL_THROUGH`, `procedure=null` | [Run #24](https://github.com/rakmahefa/aoe-rea/actions/runs/38592966677), [artifact 11909780246](https://github.com/rakmahefa/aoe-rea/actions/runs/38592966677/artifacts/11909780246) |
| `0x882816` | `52` — `PUSH EDX`, 1 byte, `FALL_THROUGH`, `procedure=null` | [Run #25](https://github.com/rakmahefa/aoe-rea/actions/runs/38593942037), [artifact 11908194310](https://github.com/rakmahefa/aoe-rea/actions/runs/38593942037/artifacts/11908194310) |
| `0x882817` | `8b 54 24 28` — `MOV EDX,dword ptr [ESP + 0x28]`, 4 bytes, `FALL_THROUGH`, `procedure=null` | [Run #26](https://github.com/rakmahefa/aoe-rea/actions/runs/38682182138), [artifact 11947964421](https://github.com/rakmahefa/aoe-rea/actions/runs/38682182138/artifacts/11947964421) |
| `0x88281b` | `51` — `PUSH ECX`, 1 byte, `FALL_THROUGH`, `procedure=null` | [Run #27](https://github.com/rakmahefa/aoe-rea/actions/runs/38684233397), [artifact 11948769728](https://github.com/rakmahefa/aoe-rea/actions/runs/38684233397/artifacts/11948769728) |
| `0x88281c` | `52` — `PUSH EDX`, 1 byte, `FALL_THROUGH`, `procedure=null` | [Run #28](https://github.com/rakmahefa/aoe-rea/actions/runs/38686269488), [artifact 11950941183](https://github.com/rakmahefa/aoe-rea/actions/runs/38686269488/artifacts/11950941183) |
| `0x88281d` | `8b c8` — `MOV ECX,EAX`, 2 bytes, `FALL_THROUGH`, `procedure=null` | [Sequential callback probe #29; Actions run ID 38691004803](https://github.com/rakmahefa/aoe-rea/actions/runs/38691004803), [artifact 11952515685](https://github.com/rakmahefa/aoe-rea/actions/runs/38691004803/artifacts/11952515685) |
| `0x88281f` | `e8 57 ed fe ff` — `CALL 0x0087157b`, 5 bytes, unconditional direct call, `procedure=null` | [One-shot probe run #30; Actions run ID 38731342538](https://github.com/rakmahefa/aoe-rea/actions/runs/38731342538), [artifact 11970986662](https://github.com/rakmahefa/aoe-rea/actions/runs/38731342538/artifacts/11970986662) |
| `0x87157b` | `8b 44 24 20` — `MOV EAX,dword ptr [ESP + 0x20]`, 4 bytes, `FALL_THROUGH`, `procedure=0x87157b` | [One-shot probe run #31; Actions run ID 38732373199](https://github.com/rakmahefa/aoe-rea/actions/runs/38732373199), [artifact 11971133081](https://github.com/rakmahefa/aoe-rea/actions/runs/38732373199/artifacts/11971133081) |

**Observed control flow:** both `JZ` instructions (`0x8827d9` and `0x8827e9`) target `0x8827f5`, which zeroes `AL` and is immediately followed by `RET` at `0x8827f7`. Thus this shared branch clears the low return byte `AL` before `RET`; that is consistent with a false Boolean result, but does not prove that the full 32-bit `EAX` register is zero. On the other path, the code loads `[EAX+0x13c]` into `ECX`, branches to the shared `AL=0; RET` block if it is zero, and otherwise passes the dword loaded from `0x00c66664` as an index to `FUN_0044cb21`. The caller then tests the helper's `EAX` result and reaches the same `AL=0; RET` block if it is zero. When nonzero, execution falls through to `0x8827eb` and loads `[EAX+0x80]`. `TEST EAX,EAX` at `0x8827f1` is followed by `JNZ 0x8827f8` at `0x8827f3`; the zero case falls through to the shared `XOR AL,AL; RET` block (which explicitly zeroes `AL`, not necessarily all of `EAX`), while the nonzero case branches to `0x8827f8`. There, `MOV EDX,[ESP+0xc]` loads a dword from the stack, length 4, with `FALL_THROUGH` and `procedure=null`; the next sequential address is `0x8827fc`. There, `PUSH 0x799782` is decoded from bytes `68 82 97 79 00` (5 bytes, `FALL_THROUGH`), with a DATA reference to `0x799782`. Both the stack value's semantic role and the meaning/type of the referenced address remain unknown. At `0x882801`, `0x882803`, `0x882805`, and `0x882807`, bytes `6a 00` decode as `PUSH 0x0` (2 bytes each, `FALL_THROUGH`, `procedure=null`), as documented in runs #16–19. Four consecutive zero pushes are observed, but do not prove a specific calling convention or argument meaning. Run #20 adds a fifth consecutive `PUSH 0x0` at `0x882809`, and run #21 adds a sixth at `0x88280b`. Run #22 decodes `0x88280d` as `LEA ECX,[ESP+0x2c]`, run #23 confirms `PUSH ECX` at `0x882811`, run #24 decodes `0x882812` as `MOV ECX,[ESP+0x28]` (4 bytes), and run #25 confirms `PUSH EDX` at `0x882816` (1 byte). Run #26 decodes `0x882817` as `MOV EDX,[ESP+0x28]` (4 bytes, `FALL_THROUGH`, `procedure=null`; artifact [11947964421](https://github.com/rakmahefa/aoe-rea/actions/runs/38682182138/artifacts/11947964421)). Run #27 decodes `0x88281b` as `PUSH ECX` (1 byte, `FALL_THROUGH`, `procedure=null`; artifact [11948769728](https://github.com/rakmahefa/aoe-rea/actions/runs/38684233397/artifacts/11948769728)). Run #28 decodes `0x88281c` as `PUSH EDX` (1 byte, `FALL_THROUGH`, `procedure=null`; artifact [11950941183](https://github.com/rakmahefa/aoe-rea/actions/runs/38686269488/artifacts/11950941183)). Sequential callback probe #29 ([Actions run ID 38691004803](https://github.com/rakmahefa/aoe-rea/actions/runs/38691004803); [artifact 11952515685](https://github.com/rakmahefa/aoe-rea/actions/runs/38691004803/artifacts/11952515685)) now confirms bytes `8b c8` at `0x88281d` as `MOV ECX,EAX` (2 bytes, `FALL_THROUGH`, `procedure=null`). This is an observed register copy only; the value's domain meaning remains unknown. The one-shot probe run #30 ([Actions run ID 38731342538](https://github.com/rakmahefa/aoe-rea/actions/runs/38731342538); [artifact 11970986662](https://github.com/rakmahefa/aoe-rea/actions/runs/38731342538/artifacts/11970986662)) confirms the next decoded instruction at `0x88281f` is `CALL 0x0087157b` (bytes `e8 57 ed fe ff`, 5 bytes, unconditional direct call, `procedure=null`). The call destination `0x87157b` is a recognized procedure entry: probe run #31 decodes `MOV EAX,[ESP+0x20]` (4 bytes, `FALL_THROUGH`, `procedure=0x87157b`; [artifact 11971133081](https://github.com/rakmahefa/aoe-rea/actions/runs/38732373199/artifacts/11971133081)). This still gives no confirmed domain meaning for the stack value. Probe run #32 is collecting the procedure dossier; if the dossier does not resolve useful context, inspect the next instruction at `0x87157f`. The caller's sequential return address is `0x882824`.

### Function dossier: `FUN_0087157b` — one-shot probe run #32

Evidence: [Actions run #32, ID 38733263497](https://github.com/rakmahefa/aoe-rea/actions/runs/38733263497); [artifact 11970339116](https://github.com/rakmahefa/aoe-rea/actions/runs/38733263497/artifacts/11970339116). The target binary SHA-256 matches the other probes: `b1a1dab7264d2db72e8f8ae1df1e419eecc223b40db00c9d1013a3bc77611d9d`.

- Ghidra identifies a contiguous procedure from `0x87157b` through `0x871808` inclusive (654 bytes). The pseudocode types are low-confidence defaults; keep the `param_N` names unless call-site evidence supports stronger labels.
- The caller at `0x88281f` prepares 11 stack arguments and `ECX`; the callee's return paths use `RET 0x2c` (44 bytes), consistent with 11 four-byte stack arguments. This establishes call/stack mechanics, not semantic names for the arguments.
- The pseudocode treats `param_1` and `param_2` as float pointers and calculates `sqrt((param_2[0]-param_1[0])² + (param_2[2]-param_1[2])²)`. If optional `param_4` points to a threshold greater than this distance, the function returns a truthy value early.
- It references `tempKBPath` at `0x00c14068`, looks up the name via `FUN_0086f5d3` and `FUN_0086d3c5`, then calls `FUN_00799898`. On success it can write the returned identifier through `param_8`; on failure it calls `FUN_00871539` before returning false-like `AL=0`.
- Other incoming call sites are `0x7400f5`, `0x7448e4`, `0x744c65`, and `0x7450cd`; this procedure is not exclusive to the current `kbCanPath2` callback.

**Hypothesis, not a recovered original name:** combined with the registered `kbCanPath2` Boolean-path-check description, the vector/range test and the `tempKBPath` query strongly fit a path-checking method. Exact meanings of the parameters, the object type, and the precise role of `FUN_00799898` remain unresolved. One-shot probe run #33 ([Actions run ID 38734503232](https://github.com/rakmahefa/aoe-rea/actions/runs/38734503232); [artifact 11972660987](https://github.com/rakmahefa/aoe-rea/actions/runs/38734503232/artifacts/11972660987)) recovered the helper behavior summarized below. One-shot probe run #34 ([Actions run ID 38735602782](https://github.com/rakmahefa/aoe-rea/actions/runs/38735602782); [artifact 11974515991](https://github.com/rakmahefa/aoe-rea/actions/runs/38735602782/artifacts/11974515991)) recovered the core-helper behavior summarized below. One-shot probe run #35 (https://github.com/rakmahefa/aoe-rea/actions/runs/38736569975) now analyzes `FUN_00798492`.

### Helper dossier: `FUN_00799898` — one-shot probe run #33

Evidence: [Actions run #33, ID 38734503232](https://github.com/rakmahefa/aoe-rea/actions/runs/38734503232); [artifact 11972660987](https://github.com/rakmahefa/aoe-rea/actions/runs/38734503232/artifacts/11972660987).

- Ghidra identifies a contiguous procedure from `0x799898` through `0x799938` inclusive (161 bytes). Its nine `param_N` types are low-confidence decompiler defaults.
- It calls `FUN_00798492` for `param_2` and `param_3`; if either lookup returns zero, the helper returns zero.
- It reads a signed 16-bit field at offset `+0xac` from each resolved object, then delegates to `FUN_00798815`, passing `param_1`, those two fields, `param_4`, and `param_5`–`param_9`.
- If `FUN_00798815` returns nonzero and the integer at `param_4 + 8` is positive, it calls `FUN_004dfcfb(0, param_2)` and `FUN_004dfcfb(length - 1, param_3)`, then returns one. Otherwise it returns zero.
- Ghidra reports two callers: `FUN_0087157b` at `0x87157b` and `FUN_008722c4` at `0x8722c4`.

**Interpretation remains tentative:** the function resolves two objects, extracts compact IDs/fields, delegates the main decision and conditionally touches the first and last entries of a length-bearing object. The business meaning of those objects, `param_4 + 8`, and `FUN_004dfcfb` is not established. One-shot probe run #34 (https://github.com/rakmahefa/aoe-rea/actions/runs/38735602782) is analyzing `FUN_00798815`, the next directly delegated helper.

### Core helper dossier: `FUN_00798815` — one-shot probe run #34

Evidence: [Actions run #34, ID 38735602782](https://github.com/rakmahefa/aoe-rea/actions/runs/38735602782); [artifact 11974515991](https://github.com/rakmahefa/aoe-rea/actions/runs/38735602782/artifacts/11974515991).

- Ghidra identifies a contiguous 766-byte procedure from `0x798815` through `0x798b12` inclusive. Parameter types and names beyond observed operations remain low-confidence decompiler guesses.
- It bounds-checks `param_2` and `param_3` against a collection-like object in `ECX` (`count` at `+8`, pointer table at `+4`) and rejects if either indexed entry is null.
- It may reset an integer at `param_4 + 8`, then iterates candidates produced by `FUN_004af0c9` / `FUN_004aefb7`. It maintains a float metric via `FUN_00423897` and compares another value against `2.0`; names and units of these measurements are not known.
- For each candidate it resolves an object through `FUN_00798492`, iterates its entries using a count at object offset `+0x4c`, maps each entry through `FUN_00795987` and the `ECX+4` table, and optionally filters it through the function pointer `param_5`.
- Candidate processing then reads vector-like values using `FUN_006f2237` / `FUN_004237e5`, adjusts one float under a flag-dependent branch, uses the already-observed bounded accessor `FUN_0044cb21`, adds a value from `FUN_00795aa3`, and feeds constructed values into `FUN_008caa04`.
- At the end it checks the selected candidate and `param_8`/the candidate object's short at `+0xac`; it traverses a linked field at `+0x24`, calling `FUN_004a5f76` for entries and optionally `FUN_004a5ddd`, then returns through `RET 0x24` (36 bytes, consistent with nine DWORD stack arguments).
- Incoming callers include `FUN_00799898` at `0x799898`, plus `0x753f2e`, `0x86d51e`, `0x86d596`, `0x871809`, `0x873d85`, and `0x87e7f8`.

**Hypothesis:** the candidate traversal, vector measurements and filter callback fit a search/validation routine used by the `tempKBPath` path-check chain. The exact object roles, units, collection meaning and returned boolean semantics remain unproven. One-shot probe run #35 ([Actions run ID 38736569975](https://github.com/rakmahefa/aoe-rea/actions/runs/38736569975); [artifact 11974527446](https://github.com/rakmahefa/aoe-rea/actions/runs/38736569975/artifacts/11974527446)) recovered the coordinate-to-grid lookup summarized below. One-shot probe run #36 ([Actions run ID 38737601357](https://github.com/rakmahefa/aoe-rea/actions/runs/38737601357); [artifact 11973429389](https://github.com/rakmahefa/aoe-rea/actions/runs/38737601357/artifacts/11973429389)) recovered the non-contiguous table/chain-selection behavior summarized below. One-shot probe run #37 ([Actions run ID 38739802167](https://github.com/rakmahefa/aoe-rea/actions/runs/38739802167); [artifact 11975426935](https://github.com/rakmahefa/aoe-rea/actions/runs/38739802167/artifacts/11975426935)) recovered a heap-like root-extraction routine, summarized below. Run #38 documents the doubly linked-list unlink helper `FUN_004af120`; run #39 documents a separate bucketed hash-chain insertion helper `FUN_004aefb7`. Run #40 ([Actions run ID 38742083079](https://github.com/rakmahefa/aoe-rea/actions/runs/38742083079); [artifact 11977520029](https://github.com/rakmahefa/aoe-rea/actions/runs/38742083079/artifacts/11977520029)) recovered the hash mixer summarized below. Run #41 ([Actions run ID 38743002770](https://github.com/rakmahefa/aoe-rea/actions/runs/38743002770); [artifact 11976439859](https://github.com/rakmahefa/aoe-rea/actions/runs/38743002770/artifacts/11976439859)) established the vector-like size/capacity helper used after extraction. Run #42 ([Actions run ID 38743994938](https://github.com/rakmahefa/aoe-rea/actions/runs/38743994938); [artifact 11978560249](https://github.com/rakmahefa/aoe-rea/actions/runs/38743994938/artifacts/11978560249)) confirmed the complementary min-heap insertion routine, documented below. Run #43 (https://github.com/rakmahefa/aoe-rea/actions/runs/38745133893) completed; the `FUN_004ae7b1` dossier below documents the caller behavior.

### Object resolver dossier: `FUN_00798492` — one-shot probe run #35

Evidence: [Actions run #35, ID 38736569975](https://github.com/rakmahefa/aoe-rea/actions/runs/38736569975); [artifact 11974527446](https://github.com/rakmahefa/aoe-rea/actions/runs/38736569975/artifacts/11974527446).

- Ghidra identifies a contiguous 217-byte procedure from `0x798492` through `0x79856a` inclusive.
- The pseudocode treats its input as a pointer to a float vector and uses components `[0]` and `[2]`. It returns zero if a spatial-table pointer at `ECX+0xb4` is null or either coordinate is below approximately zero (`-1e-6`).
- It divides the coordinates by the float scale at `ECX+0xac` and converts them to integer grid coordinates. It checks them against dimensions at `ECX+0xa4` and `ECX+0xa8`.
- It indexes a grid record array at `ECX+0xb4` using a six-byte per-cell stride, reads a signed 16-bit entry index, validates it against the object count at `ECX+8`, and, if valid, returns the pointer from the object pointer table at `ECX+4`. Invalid/missing cells return zero.
- Ghidra lists many callers, including `FUN_00798815` (`0x798815`), `FUN_00799898` (`0x799898`) and `FUN_00799939` (`0x799939`); the resolver is shared beyond this callback chain.

**Interpretation, supported by the code shape:** this is consistent with a coordinate-to-grid lookup returning an object pointer. The domain identity of the grid, what the signed 16-bit slot encodes, the meaning of its scale, and the mapped objects remain unknown.

### Candidate iterator dossier: `FUN_004af0c9` — one-shot probe run #36

Evidence: [Actions run #36, ID 38737601357](https://github.com/rakmahefa/aoe-rea/actions/runs/38737601357); [artifact 11973429389](https://github.com/rakmahefa/aoe-rea/actions/runs/38737601357/artifacts/11973429389).

- Ghidra reports a non-contiguous procedure body of 149 bytes in three ranges: `0x4af0c9–0x4af11f`, `0x4cfdd5–0x4cfe0b`, and `0x4d5cec–0x4d5cf2`. Analyses that inspect only the entry block miss most of its comparison loop and false-return path.
- It calls `FUN_004aefe9` with an output area and then uses values from that area as an integer table index and a float comparison key.
- The function reads an entry from the global table at `DAT_00cafb9c + index*4`. If the entry has a link at offset `+0x28`, it walks that chain and compares `ABS(*(float*)(node+0x14) + *(float*)(node+0x18) + *(float*)(node+0x1c) - key)` against `0.0001`.
- On a match (or when the first node has no link), it calls `FUN_004af120(index, node, &DAT_00cafb9c)`, clears node fields `+0x2c` and `+0x28`, and returns the node pointer. If the chain ends without a match, it calls `FUN_00678a72`; a missing initial entry also reaches that helper.
- Known callers include `FUN_004ae98b` and `FUN_00798815` (`0x7988d3`).

**Interpretation, updated by run #43:** this helper selects/removes a candidate node using a float-derived key. For nodes produced by `FUN_004ae7b1`, run #43 shows that fields `+0x14` and `+0x18` contribute to the combined heap priority, making this helper's comparison of `+0x14 + +0x18 + +0x1c` compatible with candidate matching by a similar score. The role of `+0x1c` across lifecycle paths, the key's exact units, and the remaining domain semantics are still unconfirmed. The `FUN_004aefe9` dossier from run #37 is documented below. Runs #38–42 (`FUN_004af120`, `FUN_004aefb7`, `FUN_004aeee8`, `FUN_0058e2c3`, `FUN_004afb4c`) are documented below; run #43 (https://github.com/rakmahefa/aoe-rea/actions/runs/38745133893) completed and is documented below. Do not assume the table at `DAT_00cafba8` is the same structure as `DAT_00cafb9c` or the heap at `DAT_00cafbb4`.

### Candidate-key producer dossier: `FUN_004aefe9` — one-shot probe run #37

Evidence: [Actions run #37, ID 38739802167](https://github.com/rakmahefa/aoe-rea/actions/runs/38739802167); [artifact 11975426935](https://github.com/rakmahefa/aoe-rea/actions/runs/38739802167/artifacts/11975426935).

- Ghidra reports a non-contiguous 241-byte body split across `0x4aefe9–0x4af0c8`, `0x4aff67–0x4aff6e`, and `0x4d5ce3–0x4d5ceb`.
- It returns false-like `AL=0` when the global count `DAT_00cafbb8` is below two. Otherwise it copies the first pair from `DAT_00cafbb4 + 8` / `+0xc` into the caller-provided output area, moves the last pair to the front, and decrements the count.
- It sifts the replacement downward through an array of 8-byte pairs, comparing the first field as a float and moving a child upward when the replacement key is larger. It writes the settled pair back, calls `FUN_0058e2c3(count-1, 0)`, then returns true-like `AL=1`.
- The second DWORD's meaning, the global queue's domain, and the float key's units remain unconfirmed. Run #41 establishes that `FUN_0058e2c3` maintains an 8-byte-element dynamic array and updates its logical size after extraction.

**Interpretation, medium confidence:** this has the shape of a min-priority-queue pop/extract-min operation: return the root pair, replace it with the final pair, then restore heap order downward. This is an algorithm-shape inference, not a recovered original name or proof of what is prioritized. Runs #38 (https://github.com/rakmahefa/aoe-rea/actions/runs/38740230871) and #39 (https://github.com/rakmahefa/aoe-rea/actions/runs/38740603626) are analyzing adjacent helpers from this candidate-management area.

### Node-unlink helper: `FUN_004af120` — one-shot probe run #38

Evidence: [Actions run #38, ID 38740230871](https://github.com/rakmahefa/aoe-rea/actions/runs/38740230871); [artifact 11975947354](https://github.com/rakmahefa/aoe-rea/actions/runs/38740230871/artifacts/11975947354).

- Ghidra reports a non-contiguous 164-byte body spread across `0x4af120–0x4af160`, `0x4cfe0c–0x4cfe21`, `0x4ee766–0x4ee796`, and `0x678947–0x678962`.
- The function uses an index into the list-head table pointed to by `*param_3`, then finds `param_2` in the doubly linked chain. The `+0x28` field is used as `next`; `+0x2c` is used as `previous`.
- If the removed node is the head, the table entry is updated to the next node and that node's previous pointer is cleared. Otherwise, neighboring links are joined around the node. In all successful removal paths, the target node's `+0x28` and `+0x2c` fields are zeroed.
- Ghidra lists callers `FUN_004af0c9`, `FUN_00678a5f`, and `FUN_008caa04`.

**Interpretation:** generic doubly linked-list removal is strongly supported by the pointer rewrites. The semantic type of the nodes/table is still unknown.

### Alternate candidate-chain insertion: `FUN_004aefb7` — one-shot probe run #39

Evidence: [Actions run #39, ID 38740603626](https://github.com/rakmahefa/aoe-rea/actions/runs/38740603626); [artifact 11976087652](https://github.com/rakmahefa/aoe-rea/actions/runs/38740603626/artifacts/11976087652).

- Ghidra reports a non-contiguous 92-byte body split across `0x4aefb7–0x4aefe8`, `0x4cfe22–0x4cfe3c`, and `0x678a50–0x678a5e`.
- It calls `FUN_004aeee8` with three values derived from `*param_1`, `param_1[2]`, and `*(ECX+0x18)`, masks the returned hash with `0x7ff`, then selects a bucket in global table `DAT_00cafba8` (2,048 possible buckets).
- An empty bucket becomes the new head. Otherwise the helper walks `+0x28` next-pointers to the chain tail, appends the node, writes the tail pointer at the new node's `+0x2c` previous field, and clears its `+0x28` next field.
- Known callers are `FUN_004ae98b` and `FUN_00798815`.

**Interpretation:** this is consistent with separate-chaining hash-table insertion. The hashed key's meaning and relationship to the other global tables remain unresolved. One-shot probe run #40 ([Actions run ID 38742083079](https://github.com/rakmahefa/aoe-rea/actions/runs/38742083079); [artifact 11977520029](https://github.com/rakmahefa/aoe-rea/actions/runs/38742083079/artifacts/11977520029)) recovered a 32-bit mixing routine for hash bucket selection, summarized below. Run #41 (`FUN_0058e2c3`) is documented below; Run #42 (`FUN_004afb4c`) is documented below; run #43 (https://github.com/rakmahefa/aoe-rea/actions/runs/38745133893) completed and is documented below.

### Candidate hash mixer: `FUN_004aeee8` — one-shot probe run #40

Evidence: [Actions run #40, ID 38742083079](https://github.com/rakmahefa/aoe-rea/actions/runs/38742083079); [artifact 11977520029](https://github.com/rakmahefa/aoe-rea/actions/runs/38742083079/artifacts/11977520029).

- Ghidra identifies a contiguous 207-byte routine from `0x4aeee8` through `0x4aefb6`.
- It accepts three 32-bit input values and combines them with repeated add/subtract/XOR operations and variable shifts (observed shift counts include 13, 8, 12, 16, 5, 3, 10 and 15), returning a 32-bit result.
- The caller `FUN_004aefb7` masks that result with `0x7ff` to choose one of 2,048 buckets in `DAT_00cafba8`. Other callers listed by Ghidra are `FUN_004ae7b1` and `FUN_008caa04`.
- The exact input fields' domain meanings and the original algorithm name are not recovered. The table's bucket selection is observed; the meaning of a hash collision or the objects stored in that table is not.

**Interpretation:** `FUN_004aeee8` is a deterministic 32-bit mixing/hash routine used for bucket selection by at least one caller. One-shot probe run #41 ([Actions run ID 38743002770](https://github.com/rakmahefa/aoe-rea/actions/runs/38743002770); [artifact 11976439859](https://github.com/rakmahefa/aoe-rea/actions/runs/38743002770/artifacts/11976439859)) documented the dynamic-array size/capacity helper. Run #42 (`FUN_004afb4c`) is documented below; run #43 (https://github.com/rakmahefa/aoe-rea/actions/runs/38745133893) completed and is documented below.

### Dynamic-array maintenance helper: `FUN_0058e2c3` — one-shot probe run #41

Evidence: [Actions run #41, ID 38743002770](https://github.com/rakmahefa/aoe-rea/actions/runs/38743002770); [artifact 11976439859](https://github.com/rakmahefa/aoe-rea/actions/runs/38743002770/artifacts/11976439859).

- Ghidra reports a non-contiguous 296-byte body in three ranges: `0x58e2c3–0x58e2eb`, `0x58e7b5–0x58e84c`, and `0x64c75c–0x64c7c2`.
- The function operates on a vector-like structure addressed through `ECX`: data pointer at `+0`, logical size at `+4`, capacity at `+8`. Its allocation size is `capacity * 8`, so this container stores 8-byte elements.
- With the optional second argument false, it updates the logical size directly when capacity is sufficient; if a larger size is requested, it grows capacity geometrically (doubling until sufficient) and allocates/reallocates storage. A nonzero flag takes a force-reset/rebuild path. Allocation failures are routed to error/exception helpers.
- In run #37's call site, `ECX` points to `DAT_00cafbb4` and `FUN_004aefe9` calls `FUN_0058e2c3(new_count, 0)` after extracting a root pair. That call updates the dynamic array's logical size after the removal.

**Interpretation:** run #41 establishes that `DAT_00cafbb4` is a vector-like dynamic array of 8-byte entries and that the apparent heap pop reduces its logical size. Combined with the downward float-key reordering in `FUN_004aefe9`, this strengthens the min-heap extraction interpretation; the semantic meaning and units of the priority key are still unknown. Run #42 ([Actions run ID 38743994938](https://github.com/rakmahefa/aoe-rea/actions/runs/38743994938); [artifact 11978560249](https://github.com/rakmahefa/aoe-rea/actions/runs/38743994938/artifacts/11978560249)) confirmed the complementary heap-insertion path, documented below. Run #43 (https://github.com/rakmahefa/aoe-rea/actions/runs/38745133893) completed; its caller findings for `FUN_004ae7b1` are documented below.

### Min-heap insertion: `FUN_004afb4c` — one-shot probe run #42

Evidence: [Actions run #42, ID 38743994938](https://github.com/rakmahefa/aoe-rea/actions/runs/38743994938); [artifact 11978560249](https://github.com/rakmahefa/aoe-rea/actions/runs/38743994938/artifacts/11978560249).

- Ghidra reports a non-contiguous 241-byte body in `0x4afb4c–0x4afc08` and `0x4b00ce–0x4b0101`.
- The function grows the dynamic array at `DAT_00cafbb4` through `FUN_0058e2c3`, writes a two-DWORD entry at an index, and sifts it upward while the new first DWORD interpreted as a float is less than or equal to the parent's key.
- When the array is initially empty, it first creates an entry at index 0 with first DWORD `0xff7fffff` (IEEE-754 negative maximum finite float) and second DWORD `0xffffffff`; the first real entry is then placed starting at index 1. In the normal insertion path, the new pair is bubbled toward the root until its key is greater than its parent's key, then written into the final slot.
- This is consistent with a 1-based min-heap whose index-zero sentinel makes upward bubbling terminate. `FUN_004aefe9` (run #37) is the complementary root-extraction/down-heap path, and `FUN_0058e2c3` (run #41) maintains the array's logical size/capacity. The heap interpretation is strong at the algorithmic level; the priority key's business meaning and second DWORD remain unknown.
- Ghidra lists callers `FUN_004ae7b1` and `FUN_008caa04`. One-shot probe run #43 (https://github.com/rakmahefa/aoe-rea/actions/runs/38745133893) completed and recovered how `FUN_004ae7b1` constructs a priority pair for the heap.

### Candidate/frontier producer: `FUN_004ae7b1` — one-shot probe run #43

Evidence: [Actions run #43, ID 38745133893](https://github.com/rakmahefa/aoe-rea/actions/runs/38745133893); [artifact 11978346441](https://github.com/rakmahefa/aoe-rea/actions/runs/38745133893/artifacts/11978346441).

- Ghidra reports a 583-byte function body spread across five non-contiguous ranges: `0x4ab9bf–0x4ab9d5`, `0x4ae7b1–0x4ae98a`, `0x4aff40–0x4aff5d`, `0x4b1e7a–0x4b1e93` and `0x4b1fd1–0x4b1fee`. Treat this as a Ghidra body address set, not a single linear block.
- The function computes a bucket index by calling `FUN_004aeee8` with `param_1[0]`, `param_1[2]` and a value read from `ECX+0x18`, then masks the result with `0x7ff`. It first queries `DAT_00cafb9c` via `FUN_004ae797`; if no matching entry is found, it queries `DAT_00cafba8` with the same index.
- When constructing/updating an entry, the pseudocode stores a tentative cost in node field `+0x14` (Ghidra's `pfVar6[5]`). That cost is the X/Z-plane Euclidean distance between `param_1` and the optional `param_2`, plus `param_2[5]` when `param_2` is non-null. It separately stores the distance from `param_1` to coordinates read at `ECX+0x0c` and `ECX+0x14` in node field `+0x18` (`pfVar6[6]`).
- It adds those two values and passes the address of local `local_10` to `FUN_004afb4c`. Ghidra's local layout places `local_c` (the masked bucket index) immediately after the four-byte `local_10` score; the call therefore supplies a two-DWORD pair whose first field is the computed float score and whose second field is the same bucket index used for the table lookup. This links the heap entries to the bucket-selection logic without making the heap and either hash table the same structure.
- For an existing entry found in `DAT_00cafb9c`, the caller computes the previous combined value `pfVar6[7] + pfVar6[6] + pfVar6[5]` and later calls `FUN_004b1e94(bucket, previous_value, recomputed_value)`. The alternate-table path can call `FUN_00678a5f`. The exact semantics of these helpers remain to be established.
- The newly initialized entry is also appended to a chain in `DAT_00cafb9c`, using fields `+0x28` and `+0x2c`. This does not collapse the three distinct structures: `DAT_00cafb9c` is a bucketed node table, `DAT_00cafba8` is a separately queried table, and `DAT_00cafbb4` is the dynamic array backing the min-heap.

**Interpretation — strongly supported algorithm shape, not a recovered original name:** the heap priority has the form *accumulated path-like cost + Euclidean distance to a reference position*, which is compatible with an A*-style frontier score. The connection to path-related routines elsewhere makes that hypothesis plausible, but the exact field meanings, units, admissibility of the distance term, and full search algorithm have not been proven. Do not label the function definitively as A*.

**Next target:** inspect the two-byte helper at `FUN_00401fd6`, reached once per record by `FUN_00401fa0`. Run #49 establishes that the loop passes the current record address in `ECX` and the callback pointer in `EAX`; the helper's exact indirect transfer instruction must confirm how the callback is invoked. Keep `FUN_00678a5f` as a secondary target for the alternate path in `FUN_004ae7b1`. The geometry/obstruction/occupancy evidence from runs #20–23 remains a separate track.

### Min-heap priority update: `FUN_004b1e94` — one-shot probe run #44

Evidence: [Actions run #44, ID 38772710258](https://github.com/rakmahefa/aoe-rea/actions/runs/38772710258); [artifact 11991884059](https://github.com/rakmahefa/aoe-rea/actions/runs/38772710258/artifacts/11991884059).

- Ghidra identifies an 817-byte body across six non-contiguous ranges: `0x4b1e94–0x4b1fd0`, `0x4b1fef–0x4b1ff3`, `0x4b1ff7–0x4b210a`, `0x4b22db–0x4b2356`, `0x4b23d7–0x4b240b`, and `0x4b73f6–0x4b741f`.
- The function scans the 8-byte pairs in `DAT_00cafbb4`. It matches a pair's second DWORD against the integer key passed by the caller, then compares the pair's float priority with the supplied old priority using an absolute tolerance that Ghidra decompiles as `0.0001` (the assembly reads the float at `DAT_00ba175c`).
- On a match, it writes the new float priority into the pair's first DWORD, retains the second DWORD, and bubbles the pair upward while the new priority is less than or equal to its parent's float key. The observed body does not insert/remove an entry or update the heap's logical length.
- The `FUN_004ae7b1` call site passes the bucket/index value and its old and recomputed combined scores to this helper. Ghidra's displayed parameter types for `FUN_004b1e94` are low-confidence; the actual call/data flow is more reliable than the inferred prototype.
- If the key/old-priority pair cannot be matched consistently, control reaches small helpers `FUN_00678963`, `FUN_0067896c`, or `FUN_00678975`. Their precise behavior and the reason for Ghidra's terminal-call flow markings are not yet established.
- Ghidra lists callers `FUN_004ae7b1` and `FUN_008caa04`.

**Interpretation — strong algorithmic evidence:** this is an in-place priority update with an upward heap repair, compatible with a *decrease-key* operation. In `FUN_004ae7b1`, the surrounding guard rejects a worse candidate before this update path, strengthening that interpretation. The actual meaning/units of the priority and bucket key remains unresolved. The next probe is `FUN_008caa04`, the other caller, to test whether the same contract appears in a second context.

### Alternate heap caller and candidate promotion: `FUN_008caa04` — one-shot probe run #45

Evidence: [Actions run #45, ID 38774292963](https://github.com/rakmahefa/aoe-rea/actions/runs/38774292963); [artifact 11993540489](https://github.com/rakmahefa/aoe-rea/actions/runs/38774292963/artifacts/11993540489).

- Ghidra identifies a contiguous 459-byte body from `0x8caa04` to `0x8cabce`. Its caller is `FUN_00798815` at `0x798815`.
- Like `FUN_004ae7b1`, it computes an index using `FUN_004aeee8` and `& 0x7ff`, then queries `DAT_00cafb9c` before `DAT_00cafba8`. The matching object is not treated as a heap entry itself; these are separate hash-table/chain structures.
- If the primary table contains a candidate, the function records the old combined key `+0x14 + +0x18 + +0x1c`, refreshes its fields, recomputes the combined float priority, and calls `FUN_004b1e94` with the bucket key and old/new priorities.
- If only `DAT_00cafba8` contains a matching candidate and its `+0x14` field passes the score guard, the function unlinks that node via `FUN_004af120`, reuses it, and takes the promotion path into `DAT_00cafb9c` and the heap. A candidate absent from both tables is allocated/obtained through `FUN_004adea4` and initialized.
- For a new/promoted candidate, the main-table path calls `FUN_004aded1` and then `FUN_004afb4c` to insert the computed score/key pair into the min-heap. The alternate score mode can use `FUN_004237e5`; its exact geometric meaning is not yet verified.
- The function writes coordinate and score-related fields at offsets `+0x00`–`+0x1c` and resets several other fields. Their complete domain meanings remain unknown.

**Interpretation — observed mechanics, inferred lifecycle:** this looks like candidate reuse/promotion between two table-backed states plus a min-heap. It may fit a path-search frontier lifecycle, but the labels “open set” and “closed set” are not proven and must not be used as facts.

**Next target:** inspect `FUN_004aded1` to establish how insertion into `DAT_00cafb9c` differs from the already observed chained insertion into `DAT_00cafba8`. Keep both globals distinct until the code shows more than a shared hash index.

### Primary-table chain insertion: `FUN_004aded1` — one-shot probe run #46

Evidence: [Actions run #46, ID 38775891857](https://github.com/rakmahefa/aoe-rea/actions/runs/38775891857); [artifact 11994206385](https://github.com/rakmahefa/aoe-rea/actions/runs/38775891857/artifacts/11994206385).

- Ghidra reports a 78-byte body split across three ranges: `0x4aded1–0x4adef1`, `0x4b2368–0x4b2385`, and `0x5004bd–0x5004cb`. Treat the disjoint ranges as an address set, not a single linear instruction sequence.
- The pseudocode reads a bucket head from `*param_3 + param_1*4`. If the bucket is empty, it stores `param_2` as the new head and returns.
- For a non-empty bucket, it follows each node's `+0x28` next pointer to the chain tail, sets the tail's `+0x28` to `param_2`, writes the tail pointer into the new node's `+0x2c` previous field, clears the new node's `+0x28` next field, then returns.
- Ghidra reports one direct caller, `FUN_008caa04`, at the call site `0x8cabb2`. The helper itself does not compute the hash; the caller supplies the integer bucket index and a pointer to the table/head array.
- The empty-bucket path does not explicitly initialise the inserted node's link fields. Do not assume this helper clears them in every case; that may be the caller's responsibility or depend on the prior node state.
- This insertion shape is consistent with the separately observed `FUN_004aefb7` insertion into `DAT_00cafba8` (run #39), but `DAT_00cafb9c` and `DAT_00cafba8` remain separate tables until more evidence connects their purpose.

**Interpretation:** confirmed bucketed singly-traversed next-chain append with a previous-link back-pointer on non-empty insertion. The table's domain semantics and the node fields' application-level meanings remain unknown.

**Next target:** inspect `FUN_004ae797`, used by `FUN_004ae7b1` to query `DAT_00cafb9c` before insertion. Determine which fields are compared and what makes two candidates match; do not infer table lifecycle names from the data structure alone.

### Primary-table candidate lookup: `FUN_004ae797` — one-shot probe run #47

Evidence: [Actions run #47, ID 38782180985](https://github.com/rakmahefa/aoe-rea/actions/runs/38782180985); [artifact 11996292779](https://github.com/rakmahefa/aoe-rea/actions/runs/38782180985/artifacts/11996292779).

- Ghidra reports a 127-byte body spread across three non-contiguous ranges: `0x4ae797–0x4ae7b0`, `0x4afeec–0x4aff3f`, and `0x4b2357–0x4b2367`. These ranges should be treated as an address set, not a single linear block.
- The function receives an integer bucket index, a pointer to a float coordinate tuple, and a pointer to a table descriptor. It reads the bucket head at `*param_3 + param_1*4`; if the head is null, it immediately returns null.
- Otherwise it compares candidate floats `[0]` and `[2]` to the query's `[0]` and `[2]`. It continues along the node's `+0x28` next pointer whenever either absolute coordinate difference is at least `1e-6`. A matching node is returned; reaching a null next pointer returns null.
- Ghidra lists two callers: `FUN_004ae7b1` calls it at `0x4ae827` and `0x4ae843`, and `FUN_008caa04` calls it at `0x8caa68` and `0x8caa9d`. In both callers it is used to query `DAT_00cafb9c` and, if necessary, the separate `DAT_00cafba8` table.

**Interpretation — strongly supported at the structural level:** each table is searched by a precomputed bucket and then by near-exact X/Z coordinate equality in its linked chain. This suggests candidate entries are position-associated. It does not establish the tables' business names, why two tables are needed, or the meaning of the third component used by the hash routine.

**Next target:** inspect `FUN_004adea4`, which `FUN_008caa04` calls when neither table returns a matching candidate. Determine whether it allocates a node, pulls from a pool, or performs another initialization step.

### Candidate-record pool allocator: `FUN_004adea4` — one-shot probe run #48

Evidence: [Actions run #48, ID 38783723125](https://github.com/rakmahefa/aoe-rea/actions/runs/38783723125); [artifact 11996853539](https://github.com/rakmahefa/aoe-rea/actions/runs/38783723125/artifacts/11996853539).

- Ghidra reports a 254-byte body in two non-contiguous ranges: `0x4adea4–0x4aded0` and `0x67897f–0x678a4f`. The distant range is part of the reported body set, not a continuation to read linearly from the entry.
- The function uses the ECX-referenced state. If its available-object count (`in_ECX[5]`) is positive, it returns the last pointer from the available-pointer array (`in_ECX[4]`) after requesting a count reduction through `FUN_00401113(count-1, 0)`.
- If no object is available, it chooses the configured batch size (`*in_ECX`), defaulting it to 100 if the value is below one. It allocates `batch_size * 0x34` bytes through `FUN_00401398`; allocation failure returns null.
- It passes the returned block to `FUN_00401fa0(base, 0x34, batch_size, &LAB_008ca934)`, then registers the block and adds pointers to the fixed-stride records (`+0x34` each) to the available-pointer storage. The first record's pointer is returned; bookkeeping/growth paths use `FUN_00401113`.
- The function is called by `FUN_004ae7b1`, `FUN_008caa04`, and `FUN_004b004e`. In `FUN_008caa04`, the caller subsequently zeroes 13 DWORDs before initializing a fresh candidate, which is consistent with reuse of generic fixed-size storage rather than proof that this helper fully constructs a domain object.

**Interpretation — strong allocator-shape evidence:** this behaves like a pool for fixed-size `0x34`-byte records, allocating them in batches of 100 by default and returning recycled pointers before allocating new storage. The exact state layout and the role of `LAB_008ca934` remain unresolved; do not yet claim a specific C++ class or original allocator name.

**Next target:** inspect `FUN_00401fa0`, which receives the block base, stride `0x34`, batch count and callback address `LAB_008ca934`. Determine what initialization/registration occurs for each record.

### Fixed-record callback loop: `FUN_00401fa0` — one-shot probe run #49

Evidence: [Actions run #49, ID 38785347582](https://github.com/rakmahefa/aoe-rea/actions/runs/38785347582); [artifact 11998191528](https://github.com/rakmahefa/aoe-rea/actions/runs/38785347582/artifacts/11998191528).

- Ghidra reports a contiguous 54-byte body from `0x401fa0` through `0x401fd5`. The returned pseudocode declares three arguments, but the epilogue is `RET 0x10` and the body reads a fourth stack argument. The inferred Ghidra signature is therefore incomplete: the machine code consumes four stack arguments.
- The function reads the count from entry-stack offset `+0x0c`, exits when the count is non-positive, and otherwise iterates exactly that many times.
- On each iteration it places the current element address in `ECX`, places the fourth argument in `EAX`, and calls the short helper at `0x401fd6`. It then advances the element address by the second argument (the stride) and repeats.
- In context, `FUN_004adea4` passes a base pointer, stride `0x34`, batch count and `LAB_008ca934`. The observed data flow therefore supports a generic *for-each fixed-stride record callback* loop: `ECX` is the current record address and `EAX` carries the callback target into `FUN_00401fd6`.
- At the time of run #49, the function dossier identified a two-byte helper but did not include its instruction bytes. Follow-up native probe #50 decoded that exact address as `JMP EAX`; the separate function-level dossier from run #51 explains why the direct instruction result matters (see below).

**Interpretation:** the pool allocator delegates per-record initialization/processing through a callback-like pointer rather than directly constructing the record fields in `FUN_00401fa0`. The exact callback semantics and the role of `LAB_008ca934` remain unknown.

### Callback transfer thunk: `0x401fd6` — one-shot probe run #50

Evidence: [Actions run #50, ID 38852450383](https://github.com/rakmahefa/aoe-rea/actions/runs/38852450383); [artifact 12025552949](https://github.com/rakmahefa/aoe-rea/actions/runs/38852450383/artifacts/12025552949).

- The native-instruction probe decodes bytes `ff e0` at `0x401fd6` as `JMP EAX`, length two, with an unconditional computed-jump flow and no direct destination.
- This confirms the data flow inferred from run #49: `FUN_00401fa0` loads the fourth stack argument into `EAX`, puts the current fixed-stride record address in `ECX`, and calls `0x401fd6`. The two-byte helper immediately jumps to the callback pointer, so each callback executes with the current record address in `ECX`.
- Because this is a tail jump, the callback's eventual return goes back to the return address pushed by `CALL 0x401fd6` at `0x401fc3` (the continuation at `0x401fc8`), assuming the callback returns normally.
- The instruction has no direct destination encoded; the actual callee depends on the runtime value passed in `EAX`. For the pool path in `FUN_004adea4`, that value is `LAB_008ca934`.

- A separate function-level dossier for `FUN_00401fd6` in [run #51](https://github.com/rakmahefa/aoe-rea/actions/runs/38852714545) ([artifact 12025049050](https://github.com/rakmahefa/aoe-rea/actions/runs/38852714545/artifacts/12025049050)) emits a decompiler warning that it could not recover the jump table and renders the indirect transfer as a call plus return. Do not treat that synthetic pseudocode return as machine control flow: run #50's native bytes `ff e0` and flow type explicitly show `JMP EAX`.

**Interpretation, now confirmed at the control-flow level:** `FUN_00401fa0` iterates over the block and dispatches a callback for each record through an indirect tail jump. The callback's field-level behavior remains unknown until its entry is traced.

**Result of run #52:** the callback label at `0x8ca934` is not recognized as a procedure entry; its first decoded instruction is `MOV EAX,ECX`. The next target is `0x8ca936`.

### Callback entry instruction: `0x8ca934` — one-shot probe run #52

Evidence: [Actions run #52, ID 38853201623](https://github.com/rakmahefa/aoe-rea/actions/runs/38853201623); [artifact 12025469262](https://github.com/rakmahefa/aoe-rea/actions/runs/38853201623/artifacts/12025469262).

- The native probe decodes `8b c1` at `0x8ca934` as `MOV EAX,ECX`, length two bytes, `FALL_THROUGH`, with `procedure=null`.
- In the context established by runs #49–50, `ECX` carries the current record pointer into the callback. This instruction copies that pointer to `EAX`; it does not by itself establish any field initialization or business meaning.
- Ghidra does not recognize `0x8ca934` as a procedure entry for this probe. Treat it as a code label/internal block unless a later function-body analysis establishes a broader procedure boundary.

**Chronological note after run #52:** runs #53–56 decode the register clear and the two link-field stores. Run #57 then decodes `0x8ca93e` as `RET`, so the observed callback path returns normally here. The next useful address is the caller continuation at `0x401fc8`.

### Callback continuation: clear of `ECX` at `0x8ca936` — one-shot probe run #53

Evidence: [Actions run #53, ID 38853803910](https://github.com/rakmahefa/aoe-rea/actions/runs/38853803910); [artifact 12026795710](https://github.com/rakmahefa/aoe-rea/actions/runs/38853803910/artifacts/12026795710).

- The native probe decodes bytes `33 c9` at `0x8ca936` as `XOR ECX,ECX`, length two, `FALL_THROUGH`, with `procedure=null`.
- The preceding instruction from run #52 is `MOV EAX,ECX` at `0x8ca934`. The observed pair therefore copies the record pointer to `EAX`, then clears `ECX`. This is register data flow only: it does not establish that a field is cleared or reveal the intended callback operation.
- The procedure boundary remains unresolved at both addresses. Keep following sequentially until a decoded branch, call, return, or procedure boundary provides stronger evidence.

### Callback continuation: clear the previous link at `0x8ca938` — one-shot probe run #54

Evidence: [Actions run #54, ID 38854422589](https://github.com/rakmahefa/aoe-rea/actions/runs/38854422589); [artifact 12026542570](https://github.com/rakmahefa/aoe-rea/actions/runs/38854422589/artifacts/12026542570).

- The native probe decodes bytes `89 48 2c` at `0x8ca938` as `MOV dword ptr [EAX + 0x2c],ECX`, length three bytes, `FALL_THROUGH`, with `procedure=null`.
- Runs #52–54 show `MOV EAX,ECX` at `0x8ca934`, `XOR ECX,ECX` at `0x8ca936`, then a DWORD store of `ECX` to `[EAX+0x2c]`. The register flow supports that zero is written at offset `+0x2c` of the record pointer copied to `EAX`.
- Other list-handling routines use `+0x2c` as a previous/back-link. Clearing that field during record setup is a structural interpretation; the callback's full intent remains unproven.
- Run #55's function-level request at `0x8ca934` failed with `No procedure exists at the requested address: 0x8ca934`; no function body or callback boundary was recovered. [Run #55](https://github.com/rakmahefa/aoe-rea/actions/runs/38854789080) · [artifact 12026372536](https://github.com/rakmahefa/aoe-rea/actions/runs/38854789080/artifacts/12026372536).

### Callback continuation: clear the forward link at `0x8ca93b` — one-shot probe run #56

Evidence: [Actions run #56, ID 38855936196](https://github.com/rakmahefa/aoe-rea/actions/runs/38855936196); [artifact 12027357090](https://github.com/rakmahefa/aoe-rea/actions/runs/38855936196/artifacts/12027357090).

- The native probe decodes bytes `89 48 28` at `0x8ca93b` as `MOV dword ptr [EAX + 0x28],ECX`, length three bytes, `FALL_THROUGH`, with `procedure=null`.
- Runs #52–56 establish the observed sequence: copy the incoming record pointer from `ECX` to `EAX`; clear `ECX`; write zero to `[EAX+0x2c]`; then write zero to `[EAX+0x28]`.
- Other list routines associate `+0x28` with a forward/next pointer and `+0x2c` with a previous/back pointer. The two stores are consistent with clearing both links, but do not establish the callback's complete initialization behavior or domain purpose.
- Ghidra continues to report `procedure=null` for the instruction addresses; do not infer a recovered function boundary.

### Callback return: `0x8ca93e` — one-shot probe run #57

Evidence: [Actions run #57, ID 38856897665](https://github.com/rakmahefa/aoe-rea/actions/runs/38856897665); [artifact 12026774512](https://github.com/rakmahefa/aoe-rea/actions/runs/38856897665/artifacts/12026774512).

- The native probe decodes byte `c3` at `0x8ca93e` as `RET`, length one byte, return flow, with `procedure=null`.
- This ends the observed callback instruction sequence. Combined with run #50's native `JMP EAX` thunk and the call to that thunk at `0x401fc3`, a normal `RET` is consistent with resuming at `0x401fc8`; this is a control-flow inference, not recovery of the callback's domain semantics.
- No linear instruction probe should proceed beyond the `RET` as if it were the same execution path. The next useful probe is the caller continuation at `0x401fc8`.

**Do not over-interpret:** `0x00c66234`, `0x00c66664`, offsets `+0x13c`, `+0x58`, `+0x5c`, and `+0x80` have not been assigned confirmed domain meanings. `FUN_0044cb21` behaves like a generic bounds-checked collection accessor based on its code, but that does not establish pathfinding semantics by itself. The callback sequence reaches `0x88281f`, where an unconditional direct call to `0x87157b` is observed. Ghidra recognizes `0x87157b` as a procedure; run #32's function dossier is documented above. Runs #33–37 (`FUN_00799898`, `FUN_00798815`, `FUN_00798492`, `FUN_004af0c9`, `FUN_004aefe9`) are documented below. Runs #38–42 (`FUN_004af120`, `FUN_004aefb7`, `FUN_004aeee8`, `FUN_0058e2c3`, `FUN_004afb4c`) are documented below; run #43 (`FUN_004ae7b1`) is documented above. Keep the tables at `DAT_00cafb9c`, `DAT_00cafba8`, and `DAT_00cafbb4` distinct unless further evidence links them. Keep `0x882824` as the sequential address after the CALL, but prioritize the callee chain while its semantics remain unresolved. Continue with one-address probes, following decoded branch/call/return targets rather than assuming the full continuation is linear. The geometry/obstruction/occupancy track from runs #20–23 remains separate.

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
