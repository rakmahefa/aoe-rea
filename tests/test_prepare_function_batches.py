import csv
import tempfile
import unittest
from pathlib import Path

from scripts.prepare_function_batches import prepare


class PrepareFunctionBatchesTests(unittest.TestCase):
    def test_stable_100_entry_batches_and_partial_tail(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source, out = root / "source", root / "out"
            source.mkdir()
            rows = []
            fence = chr(96) * 3
            for i in range(205):
                note_file = f"functions/{i:03d}.md"
                (source / note_file).parent.mkdir(parents=True, exist_ok=True)
                (source / note_file).write_text(
                    f"# Function dossier: FUN_{i:06x}\n\n## Decompiler output\n{fence}c\nvoid FUN_{i:06x}(void)\n{{\n  GetTickCount();\n}}\n{fence}\n",
                    encoding="utf-8",
                )
                rows.append({"index": str(i), "address": f"0x{i + 0x401000:08x}", "name": f"FUN_{i:06x}", "thunk": "false", "external": "false", "decompile_status": "ok", "note_file": note_file})
            with (source / "index.csv").open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            manifest = prepare(source, out, batch_size=100)
            self.assertEqual(manifest["total_entries"], 205)
            self.assertEqual(manifest["batch_count"], 3)
            self.assertTrue(all((out / "batches" / f"BATCH_{n:03d}.md").is_file() for n in range(3)))
            with (out / "function-batch-index.csv").open(encoding="utf-8", newline="") as f:
                index = list(csv.DictReader(f))
            with (out / "priority-review-queue.csv").open(encoding="utf-8", newline="") as f:
                priority = list(csv.DictReader(f))
            self.assertEqual(len(index), 205)
            self.assertEqual(len(priority), 205)
            self.assertTrue((out / "priority-review-queue.md").is_file())
            self.assertEqual(index[0]["behavior_validated"], "false")
            self.assertTrue(all(r["semantic_status"] == "pending-human-or-agent-review" for r in index))


if __name__ == "__main__":
    unittest.main()
