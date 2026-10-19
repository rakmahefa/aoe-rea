# BATCH_000 — initial review of functions 0–99

Target SHA-256: b1a1dab7264d2db72e8f8ae1df1e419eecc223b40db00c9d1013a3bc77611d9d.
Scope: first 100 index entries in address order, not the first 100 gameplay routines. These are structural hypotheses from Ghidra pseudocode and referenced APIs; no dynamic behavior is validated.

## Per-function disposition

| Index | Address | Narrow static finding | Confidence |
|---:|---|---|---|
| 0 | 0x00401003 | Links a record at a guarded free-list head while holding a critical section | E2 |
| 1 | 0x00401049 | Releases an associated buffer and returns a record to one of six size-class pools | E2 |
| 2 | 0x004010ca | Releases a referenced record when non-null, then clears caller slot | E2 |
| 3 | 0x00401106 | CRT security-cookie/fail-fast path ending in process exit | E2 |
| 4 | 0x00401113 | Resizable container/storage update with allocation and exception paths | E2 |
| 5 | 0x0040113c | Pops from a pool under a critical section; falls back to allocator | E2 |
| 6 | 0x00401192 | Selects a size class and initializes allocation metadata | E2 |
| 7 | 0x004011e6 | Empty body; likely no-op/stub | E2 |
| 8 | 0x004011e7 | Preserves last-error state and resolves thread-local CRT state | E1–E2 |
| 9 | 0x00401213 | Bounds-checked 32-bit array lookup | E2 |
| 10 | 0x00401234 | Calls a virtual/interface slot; object-domain meaning unknown | E1 |
| 11 | 0x004012b5 | Allocates/replaces storage when capacity is insufficient | E2 |
| 12 | 0x0040133f | Clears a pointer-sized field | E2 |
| 13 | 0x00401348 | Returns an object pointer or global fallback | E2 |
| 14 | 0x0040135c | UTF-16 length scan without visible null guard | E2 |
| 15 | 0x00401372 | Null-safe UTF-16 length scan | E2 |
| 16 | 0x00401398 | Passes local argument storage to virtual/interface helper; purpose unknown | E1 |
| 17 | 0x004013b0 | Manages owned UTF-16 buffer across empty/copy/capacity paths | E2 |
| 18 | 0x0040140f | UTF-16 length helper | E2 |
| 19 | 0x00401435 | Copies a caller-sized sequence into resized destination storage | E2 |
| 20 | 0x00401476 | Bounds-checks index, optionally calls helper, reads array element | E2 |
| 21 | 0x004014bf | Returns pointer at object offset +0x20 | E2 |
| 22 | 0x004014c3 | Virtual callbacks under exception-cleanup bookkeeping | E1–E2 |
| 23 | 0x00401548 | Null guard around cleanup/interface helper | E2 |
| 24 | 0x0040155c | 32×32-bit to 64-bit multiplication helper | E2 |
| 25 | 0x00401579 | Multiword 64-bit arithmetic with sign handling; exact operation unresolved | E1–E2 |
| 26 | 0x004015c1 | Reads field at offset +0x0c | E2 |
| 27 | 0x004015c5 | Compares managed UTF-16 buffers/metadata; return semantics need test | E1–E2 |
| 28 | 0x0040160e | UTF-16 length helper | E2 |
| 29 | 0x00401634 | Calls CompareStringW wrapper and converts result to Boolean-like value | E2 |
| 30 | 0x0040166c | Resizable container sharing allocation/exception helpers | E2 |
| 31 | 0x00401695 | Bounds-checked 32-bit array lookup | E2 |
| 32 | 0x004016b3 | Resets four adjacent object fields | E2 |
| 33 | 0x004016c3 | Mixes input in 12-byte chunks with seed 0x9e3779b9; likely hash/checksum | E1–E2 |
| 34 | 0x0040189c | Handles remainder bytes for the preceding mixer | E1–E2 |
| 35 | 0x004018d4 | Thread-local CRT and locale/lowercase helper | E1–E2 |
| 36 | 0x0040193d | UTF-16 comparison; exact locale/ordering contract open | E1–E2 |
| 37 | 0x0040196f | Constructs/assigns a managed UTF-16 string | E1–E2 |
| 38 | 0x0040199f | UTF-16 length helper | E2 |
| 39 | 0x004019c5 | String/object cleanup companion | E1–E2 |
| 40 | 0x004019ff | Reads managed-string metadata; field meaning unknown | E1 |
| 41 | 0x00401a12 | Copies/constructs managed string and updates destination state | E1–E2 |
| 42 | 0x00401a3c | UTF-16 length helper | E2 |
| 43 | 0x00401a62 | String/container cleanup companion | E1 |
| 44 | 0x00401a9c | Calls Win32 CompareStringW with locale/flags/lengths | E2 |
| 45 | 0x00401b81 | Wrapper over shared string comparison | E2 |
| 46 | 0x00401bce | UTF-16 comparison using thread-locale lowercase helper | E2 |
| 47 | 0x00401c51 | Processes UTF-16 buffer with length/flags; purpose unresolved | E1 |
| 48 | 0x00401cdd | Empty-looking body with Ghidra stack-tracking warning; inspect bytes | E0–E1 |
| 49 | 0x00401d10 | Composite CRT/string helper with security-handler path | E1 |
| 50 | 0x00401d9d | Security-cookie/fail-fast path | E2 |
| 51 | 0x00401daa | Empty body/no-op | E2 |
| 52 | 0x00401db3 | Composite string/CRT routine with exception/security support | E1 |
| 53 | 0x00401ea2 | Exception-unwind/cleanup-shaped routine; native validation needed | E1 |
| 54 | 0x00401eb4 | Security error termination handler | E2 |
| 55 | 0x00401ec1 | Empty body/no-op | E2 |
| 56 | 0x00401eca | Converts multibyte text to UTF-16 using MultiByteToWideChar and owned storage | E2 |
| 57 | 0x00401f47 | Tests whether a managed string is non-null/non-empty | E2 |
| 58 | 0x00401f6e | Identity function; returns its argument | E2 |
| 59 | 0x00401f71 | Empty body/no-op | E2 |
| 60 | 0x00401f74 | Dynamic container resize through shared allocator helper | E2 |
| 61 | 0x00401fa0 | Iterates fixed-stride records and invokes callback; loop shape corroborated by native probes | E3 |
| 62 | 0x00401fd6 | Indirect tail-dispatch via EAX; native probe confirmed JMP EAX | E3 |
| 63 | 0x00401fdd | Composite object/state operation; semantics unresolved | E1 |
| 64 | 0x00402001 | Dynamic container resize/capacity operation | E2 |
| 65 | 0x0040202a | Multiword numeric conversion/rounding helper | E1–E2 |
| 66 | 0x00402073 | Multiword 64-bit arithmetic; exact CRT contract open | E1–E2 |
| 67 | 0x004020c3 | Combines object fields into encoded return; meaning unresolved | E1 |
| 68 | 0x00402135 | Runtime/service initialization referencing CoInitialize, performance counter and critical sections | E2 |
| 69 | 0x0040232e | Queries high-resolution performance counter | E2 |
| 70 | 0x0040236e | Floating-point measurement delegated to helper; units unknown | E1 |
| 71 | 0x004023cd | Floating-point result delegated to helper; meaning unknown | E1 |
| 72 | 0x004023e0 | Resolves/returns an object or context pointer through indirect helper | E1 |
| 73 | 0x00402401 | Boolean-like state from fields +0x40 and +0x64 | E2 |
| 74 | 0x0040242f | Floating-point helper call; subsystem unknown | E1 |
| 75 | 0x00402449 | Virtual/object lifecycle-like operation; exact subsystem unknown | E1 |
| 76 | 0x00402464 | Uses QueryPerformanceCounter and stored values to compute elapsed milliseconds | E2 |
| 77 | 0x004024e2 | Updates timer/scheduler-like state under a global critical section | E2 |
| 78 | 0x0040257f | Returns size/count-like result dependent on object type/state | E1 |
| 79 | 0x00402598 | CRT floating-point exceptional-value/control-word logic | E2 |
| 80 | 0x00402635 | Dynamic container resize/capacity operation | E2 |
| 81 | 0x0040265e | Parses/processes buffers under bitmask flags; contract unknown | E1 |
| 82 | 0x00402733 | UTF-16 to multibyte conversion using WideCharToMultiByte | E2 |
| 83 | 0x004027bd | Chooses pooled storage based on requested size plus overhead | E2 |
| 84 | 0x004027fe | Writes UTF-16-to-multibyte conversion into acquired buffer | E2 |
| 85 | 0x0040281d | Returns an allocation to matching size-class pool | E2 |
| 86 | 0x00402866 | Identified Visual Studio CRT ASCII case-insensitive compare | E3 |
| 87 | 0x004028b4 | Thread/locale-backed byte-string comparison helper | E1–E2 |
| 88 | 0x0040295b | Converts a text key, scans candidate records and returns mapped value on match | E2 |
| 89 | 0x00402b59 | Virtual/interface operation with exception bookkeeping; domain unknown | E1 |
| 90 | 0x00402c48 | Returns indexed dynamic-array storage and grows logical size when needed | E2 |
| 91 | 0x00402c76 | Normalizes a key, obtains an index and reads a bounds-checked table value | E2 |
| 92 | 0x00402ce9 | Reads a fixed-stride five-byte record and decodes a flag nibble/type | E2 |
| 93 | 0x00402d23 | Writes field at object offset +0x14 | E2 |
| 94 | 0x00402d2d | Initializes a timer using QueryPerformanceCounter and QueryPerformanceFrequency | E2 |
| 95 | 0x00402dc0 | Bounds-checked lookup in a static nine-entry table | E2 |
| 96 | 0x00402dd8 | D3DXMatrixMultiply bridge-like entry; Ghidra cannot recover implementation here | E1–E2 |
| 97 | 0x00402dde | Bounds-checked pointer lookup for 16-byte records | E2 |
| 98 | 0x00402dff | Uses timeGetTime unless a global flag selects a cached value | E2 |
| 99 | 0x00402e12 | Reads field at object offset +0x608 | E2 |

## What this batch says about the program

- Early address-order entries are mostly low-level runtime services: allocator pools, resizable buffers, managed UTF-16 strings, exception/security helpers, locale and timing.
- These functions should generally map to Rust ownership, standard containers and narrow OS adapters. Do not recreate their internals one-for-one unless a tested external contract requires it.
- Timer helpers do not identify the main simulation tick. A D3DX symbol does not establish the full render pipeline.
- Separately investigate known game-related leads: obstruction/occupancy at 0x004839bb and 0x00483d4c; coordinate-to-grid lookup at 0x00798492; path API registration at 0x00885d07; and path-candidate/heap helpers around 0x004ae7b1, 0x004aefe9, 0x004afb4c and 0x008caa04.

Every entry remains behavior_validated = false. E2 means only that a narrow structural operation is visible in static output; E3 requires corroboration by independent native probes/cross-references.
