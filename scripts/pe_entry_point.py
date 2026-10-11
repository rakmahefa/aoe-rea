#!/usr/bin/env python3
"""Extract a PE image's declared entry point without running the binary.

This reports the PE optional-header address only. It does not prove that the
address is a recovered function or that it is the game's main/gameplay entry.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

MACHINE_NAMES = {
    0x014C: "x86",
    0x8664: "x86_64",
    0x01C0: "ARM",
    0x01C4: "ARMNT",
    0xAA64: "ARM64",
}


class PEFormatError(ValueError):
    """The input is not a structurally readable PE image."""


def _read_uint(data: bytes, offset: int, size: int, field: str) -> int:
    if offset < 0 or offset + size > len(data):
        raise PEFormatError(f"Truncated PE while reading {field}.")
    return int.from_bytes(data[offset : offset + size], "little", signed=False)


def inspect_entry_point(path: Path) -> dict[str, Any]:
    """Return the PE format, machine, image base, and declared entry point."""
    data = path.read_bytes()

    if len(data) < 0x40 or data[:2] != b"MZ":
        raise PEFormatError("Missing or truncated DOS MZ header.")

    pe_offset = _read_uint(data, 0x3C, 4, "e_lfanew")
    if pe_offset + 4 + 20 > len(data):
        raise PEFormatError("PE header offset points outside the file.")
    if data[pe_offset : pe_offset + 4] != b"PE\0\0":
        raise PEFormatError("Missing PE signature at e_lfanew.")

    coff_offset = pe_offset + 4
    machine = _read_uint(data, coff_offset, 2, "COFF machine")
    optional_size = _read_uint(data, coff_offset + 16, 2, "optional-header size")
    optional_offset = coff_offset + 20

    if optional_size < 2 or optional_offset + optional_size > len(data):
        raise PEFormatError("Truncated or missing PE optional header.")

    magic = _read_uint(data, optional_offset, 2, "optional-header magic")
    if magic == 0x010B:  # PE32
        pe_format = "PE32"
        image_base_offset, image_base_size = 28, 4
    elif magic == 0x020B:  # PE32+
        pe_format = "PE32+"
        image_base_offset, image_base_size = 24, 8
    else:
        raise PEFormatError(f"Unsupported PE optional-header magic: 0x{magic:04x}.")

    required_optional_size = max(20, image_base_offset + image_base_size)
    if optional_size < required_optional_size:
        raise PEFormatError("PE optional header is too small for the entry point and image base.")

    entry_rva = _read_uint(data, optional_offset + 16, 4, "AddressOfEntryPoint")
    image_base = _read_uint(
        data,
        optional_offset + image_base_offset,
        image_base_size,
        "ImageBase",
    )
    entry_va = image_base + entry_rva if entry_rva else None
    if entry_va is not None and entry_va > 0xFFFFFFFFFFFFFFFF:
        raise PEFormatError("Computed entry-point address exceeds 64-bit address space.")

    return {
        "path": str(path),
        "format": pe_format,
        "machine": f"0x{machine:04x}",
        "architecture": MACHINE_NAMES.get(machine, "unknown"),
        "image_base": f"0x{image_base:x}",
        "entry_point_rva": f"0x{entry_rva:x}",
        "entry_point_va": f"0x{entry_va:x}" if entry_va is not None else None,
        "has_entry_point": entry_va is not None,
        "interpretation": (
            "Declared PE entry address only; it may be a runtime/CRT startup stub "
            "and is not proof of the game's main or gameplay function."
        ),
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"Usage: {Path(argv[0]).name} PATH_TO_EXE_OR_DLL", file=sys.stderr)
        return 2

    try:
        result = inspect_entry_point(Path(argv[1]))
    except (OSError, PEFormatError) as exc:
        print(f"PE entry-point inspection failed: {exc}", file=sys.stderr)
        return 2

    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
