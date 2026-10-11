import json
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "pe_entry_point.py"


def make_pe(*, pe32_plus: bool = False, entry_rva: int = 0x1234) -> bytes:
    """Create a minimal synthetic PE header sufficient for entry-point parsing."""
    pe_offset = 0x80
    optional_size = 0xF0 if pe32_plus else 0xE0
    data = bytearray(pe_offset + 4 + 20 + optional_size)
    data[:2] = b"MZ"
    struct.pack_into("<I", data, 0x3C, pe_offset)
    data[pe_offset : pe_offset + 4] = b"PE\0\0"

    coff_offset = pe_offset + 4
    machine = 0x8664 if pe32_plus else 0x014C
    struct.pack_into("<HHIIIHH", data, coff_offset, machine, 0, 0, 0, 0, optional_size, 0)

    optional_offset = coff_offset + 20
    magic = 0x020B if pe32_plus else 0x010B
    struct.pack_into("<H", data, optional_offset, magic)
    struct.pack_into("<I", data, optional_offset + 16, entry_rva)
    if pe32_plus:
        struct.pack_into("<Q", data, optional_offset + 24, 0x140000000)
    else:
        struct.pack_into("<I", data, optional_offset + 28, 0x400000)
    return bytes(data)


class PEEntryPointTests(unittest.TestCase):
    def test_pe32_entry_point(self):
        result = self.run_inspector(make_pe())
        self.assertEqual(result["format"], "PE32")
        self.assertEqual(result["architecture"], "x86")
        self.assertEqual(result["image_base"], "0x400000")
        self.assertEqual(result["entry_point_rva"], "0x1234")
        self.assertEqual(result["entry_point_va"], "0x401234")
        self.assertTrue(result["has_entry_point"])

    def test_pe32_plus_entry_point(self):
        result = self.run_inspector(make_pe(pe32_plus=True))
        self.assertEqual(result["format"], "PE32+")
        self.assertEqual(result["architecture"], "x86_64")
        self.assertEqual(result["image_base"], "0x140000000")
        self.assertEqual(result["entry_point_va"], "0x140001234")

    def test_zero_entry_rva_is_explicitly_unavailable(self):
        result = self.run_inspector(make_pe(entry_rva=0))
        self.assertFalse(result["has_entry_point"])
        self.assertIsNone(result["entry_point_va"])

    def test_optional_header_too_small_is_rejected(self):
        data = bytearray(make_pe())
        coff_offset = 0x80 + 4
        struct.pack_into("<H", data, coff_offset + 16, 24)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "truncated-header.exe"
            path.write_bytes(data)
            process = subprocess.run(
                [sys.executable, str(SCRIPT), str(path)],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertNotEqual(process.returncode, 0)
        self.assertIn("optional header is too small", process.stderr)

    def test_invalid_signature_fails_with_diagnostic(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "invalid.exe"
            path.write_bytes(b"not a PE")
            process = subprocess.run(
                [sys.executable, str(SCRIPT), str(path)],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertNotEqual(process.returncode, 0)
        self.assertIn("PE entry-point inspection failed", process.stderr)

    @staticmethod
    def run_inspector(data: bytes) -> dict:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "synthetic.exe"
            path.write_bytes(data)
            process = subprocess.run(
                [sys.executable, str(SCRIPT), str(path)],
                capture_output=True,
                text=True,
                check=False,
            )
        if process.returncode != 0:
            raise AssertionError(process.stderr)
        return json.loads(process.stdout)


if __name__ == "__main__":
    unittest.main()
