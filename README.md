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
- `README.md` — project objective, workflow, and release direction.

As reconstruction progresses, keep implementation code, tests, evidence notes, and build configuration clearly separated from the original reference binaries.

## Legal and distribution note

Use game files only when obtained lawfully. Do not publish proprietary executables, DLLs, game assets, or other copyrighted material in releases unless redistribution is explicitly authorized. Prefer distributing independently reconstructed code and build instructions, with users supplying any proprietary game files that are legally required.

## Definition of success

The project succeeds when a GitHub Release provides a **genuine Linux-native executable**, reproducible build/release steps, documented dependencies, and an honest account of its tested functionality and limitations.
