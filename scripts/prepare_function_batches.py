#!/usr/bin/env python3
"""Build exhaustive 100-function worklists and a heuristic review queue.

This performs structural triage only. It never infers behavior validation.
"""
from __future__ import annotations
import argparse, csv, json, re, sys, math
from collections import Counter
from pathlib import Path

INTERNAL = re.compile(r"\b(?:thunk_)?FUN_([0-9a-fA-F]{6,8})\s*\(")
CALL = re.compile(r"\b([A-Za-z_][A-Za-z0-9_@$]*)\s*\(")
CONTROL = {"if", "while", "for", "switch", "return", "sizeof", "catch", "case", "default", "do", "else", "goto"}
CATEGORY_RULES = {
    "pathfinding/navigation": ("kbCanPath", "kbCanSimPath", "tempKBPath", "pathfinder", "PathNode"),
    "world/spatial": ("obstruction", "Occupancy", "Grid", "Footprint", "collision", "spatial"),
    "rendering/graphics": ("Direct3D", "D3D", "D3DX", "TextureID", "Shader", "DrawPrimitive", "Present"),
    "assets/resources": ("particleSet", "ParticleSet", "LoadLibrary", "LoadFile", "Resource", "CreateFile", "ReadFile"),
    "input/window-ui": ("PeekMessage", "DispatchMessage", "TranslateMessage", "CreateWindow", "DialogBox", "SendMessage", "ImmGetContext"),
    "startup/platform": ("GetStartupInfo", "GetCommandLine", "GetModuleHandle", "WinMain", "ExitProcess", "CoInitialize"),
    "timing/synchronization": ("QueryPerformanceCounter", "QueryPerformanceFrequency", "timeGetTime", "GetTickCount", "EnterCriticalSection", "CreateMutex"),
    "string/locale/runtime": ("WideCharToMultiByte", "MultiByteToWideChar", "CompareString", "stricmp", "towlower", "wcslen", "___ascii_stricmp"),
}
CATEGORY_WEIGHT = {"pathfinding/navigation": 35, "world/spatial": 32, "rendering/graphics": 24, "input/window-ui": 18, "assets/resources": 15, "startup/platform": 8, "timing/synchronization": 5}
SIGNAL_RULES = {
    "graphics-api": ("Direct3D", "D3D", "D3DX", "TextureID"),
    "window-message-loop": ("PeekMessage", "GetMessage", "DispatchMessage", "TranslateMessage"),
    "file-io": ("CreateFile", "ReadFile", "WriteFile", "fopen", "fread"),
    "timing": ("QueryPerformanceCounter", "QueryPerformanceFrequency", "timeGetTime", "GetTickCount"),
    "indirect-dispatch": ("JMP EAX", "(*(code *)", "(**", "LAB_"),
    "allocation": ("malloc", "free(", "realloc", "HeapAlloc", "GlobalAlloc", "LocalAlloc"),
}


def read_index(root: Path) -> list[dict[str, str]]:
    with (root / "index.csv").open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    required = {"index", "address", "name", "decompile_status", "note_file"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("Input must contain a non-empty index.csv with Ghidra dossier columns")
    return rows


def read_code(root: Path, note_file: str) -> tuple[str, str]:
    try:
        note = (root / note_file).read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        raise RuntimeError(f"Missing dossier {note_file}: {e}") from e
    fence = chr(96) * 3
    m = re.search(re.escape(fence) + r"c\s*(.*?)\s*" + re.escape(fence), note, re.S)
    return note, (m.group(1) if m else "")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def prepare(source: Path, output: Path, batch_size: int) -> dict:
    source_rows = read_index(source)
    rows: list[dict[str, str]] = []
    edge_lists: list[list[str]] = []
    for src in source_rows:
        note, code = read_code(source, src["note_file"])
        calls = []
        for name in CALL.findall(code):
            if name not in CONTROL and name != src["name"] and name not in calls:
                calls.append(name)
        body = code.split("{", 1)[1] if "{" in code else code
        edges = list(dict.fromkeys("0x" + h.lower() for h in INTERNAL.findall(body)))
        edge_lists.append(edges)
        hay = note + "\n" + code + "\n" + " ".join(calls)
        categories = [c for c, terms in CATEGORY_RULES.items() if any(t in hay for t in terms)]
        if not categories:
            categories = ["math/geometry-candidate" if any(t in hay for t in ("sqrt", "sin", "cos", "Vector", "Matrix")) else "unclassified/manual-review"]
        signals = [s for s, terms in SIGNAL_RULES.items() if any(t in hay for t in terms)] or ["none-extracted"]
        prefix = re.sub(r"/\*.*?\*/|//[^\n]*", " ", code.split("{", 1)[0], flags=re.S)
        signature = " ".join(x.strip() for x in prefix.splitlines() if x.strip())[:240] or "(signature unavailable)"
        rows.append({
            "index": src["index"], "address": src["address"], "name": src["name"],
            "thunk": src.get("thunk", ""), "external": src.get("external", ""),
            "decompile_status": src["decompile_status"], "batch_id": f"BATCH_{int(src['index']) // batch_size:03d}",
            "signature": signature, "likely_categories": ";".join(categories),
            "structural_signals": ";".join(signals), "code_chars": str(len(code)),
            "code_lines": str(len(code.splitlines())), "internal_callee_count": str(len(edges)),
            "internal_callees": ";".join(edges[:60]), "other_call_names": ";".join(calls[:60]),
            "caller_count": "0", "priority_score": "0", "priority_reasons": "pending-call-graph",
            "note_file": src["note_file"], "semantic_status": "pending-human-or-agent-review",
            "behavior_validated": "false",
        })
    callers: Counter[str] = Counter()
    for edges in edge_lists:
        callers.update(edge.lower() for edge in edges)
    for n, row in enumerate(rows):
        fan_in = callers.get(row["address"].lower(), 0)
        row["caller_count"] = str(fan_in)
        cats = row["likely_categories"].split(";")
        sigs = row["structural_signals"].split(";")
        reasons = [f"candidate:{c}" for c in cats if c in CATEGORY_WEIGHT]
        score = sum(CATEGORY_WEIGHT.get(c, 0) for c in cats)
        for sig in sigs:
            weight = {"graphics-api": 16, "window-message-loop": 11, "file-io": 7, "timing": 2, "indirect-dispatch": 3}.get(sig, 0)
            score += weight
            if weight:
                reasons.append(f"signal:{sig}")
        out_degree = len(edge_lists[n])
        if out_degree >= 10:
            score += 4
            reasons.append(f"calls-many-internal:{out_degree}")
        if fan_in >= 20:
            score += min(8, int(math.log2(fan_in + 1)))
            reasons.append(f"high-fan-in:{fan_in}")
        if int(row["code_lines"]) >= 150:
            score += 3
            reasons.append("large-body-needs-context")
        if row["decompile_status"] != "ok":
            score += 8
            reasons.append("decompilation-failed-needs-native-review")
        row["priority_score"] = str(score)
        row["priority_reasons"] = ";".join(reasons) or "no-strong-heuristic-signal"

    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / "function-batch-index.csv", rows)
    prioritized = sorted(rows, key=lambda r: (int(r["priority_score"]), int(r["caller_count"]), int(r["code_lines"])), reverse=True)
    write_csv(output / "priority-review-queue.csv", prioritized)
    tick = chr(96)
    lines = ["# Whole-program priority review queue", "", f"- Functions indexed: **{len(rows)}**", "- Heuristic score is an investigation order, not semantic confidence.", "- Stable 100-entry batches remain the exhaustive coverage queue.", "", "| Rank | Score | Address | Name | Candidate categories | Signals | Callers | Reasons | Dossier |", "|---:|---:|---|---|---|---|---:|---|---|"]
    for rank, r in enumerate(prioritized[:500], 1):
        why = r["priority_reasons"].replace(";", ", ")[:120]
        lines.append(f"| {rank} | {r['priority_score']} | {tick}{r['address']}{tick} | {tick}{r['name']}{tick} | {r['likely_categories']} | {r['structural_signals']} | {r['caller_count']} | {why} | {tick}function-dossiers/{r['note_file']}{tick} |")
    (output / "priority-review-queue.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    batch_dir = output / "batches"
    batch_dir.mkdir(parents=True, exist_ok=True)
    for start in range(0, len(rows), batch_size):
        batch = rows[start:start + batch_size]
        ok = sum(r["decompile_status"] == "ok" for r in batch)
        fail = len(batch) - ok
        report = [f"# BATCH_{start // batch_size:03d}: static triage worklist", "", f"- Entries: **{len(batch)}**; decompiled: **{ok}**; failed: **{fail}**.", "- Static cues only; semantic behavior remains unvalidated.", "", "Review each note for purpose, arguments/return, state read/written, direct/indirect callees, edge cases, evidence grade, clone module and a proposed test.", "", "| Index | Address | Name | Status | Lines | Candidate categories | Structural signals | Internal callees | Dossier |", "|---:|---|---|---|---:|---|---|---|---|"]
        for r in batch:
            callees = r["internal_callees"].replace(";", ", ") or "—"
            if len(callees) > 120:
                callees = callees[:117] + "..."
            report.append(f"| {r['index']} | {tick}{r['address']}{tick} | {tick}{r['name']}{tick} | {r['decompile_status']} | {r['code_lines']} | {r['likely_categories']} | {r['structural_signals']} | {callees} | {tick}function-dossiers/{r['note_file']}{tick} |")
        report.extend(["", "## Review findings", "", "- Confirmed common-purpose routines:", "- Possible game-domain routines:", "- CRT/runtime functions safe to de-prioritize after family-level review:", "- Unresolved indirect calls/data dependencies:", "- Test ideas and reviewer/commit:", ""])
        (batch_dir / f"BATCH_{start // batch_size:03d}.md").write_text("\n".join(report), encoding="utf-8")
    status = Counter(r["decompile_status"] for r in rows)
    manifest = {"total_entries": len(rows), "batch_size": batch_size, "batch_count": (len(rows) + batch_size - 1) // batch_size, "decompilation_status": dict(status), "priority_queue": "priority-review-queue.csv and top-500 Markdown summary", "note": "Structural triage only; not semantic validation."}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (output / "README.md").write_text(f"# Semantic-review worklists\n\n- Entries: **{len(rows)}**\n- Stable batches: **{manifest['batch_count']}** of up to {batch_size}\n- function-batch-index.csv: exhaustive structural index.\n- priority-review-queue.csv / .md: heuristic investigation order.\n- batches/BATCH_NNN.md: index-order coverage.\n\nAll labels are heuristic. Read the source dossier and caller/callee evidence before concluding behavior. The behavior_validated field remains false until a repeatable oracle/test is recorded.\n", encoding="utf-8")
    return manifest


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True, help="Extracted artifact directory with index.csv and function notes")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--batch-size", type=int, default=100)
    a = p.parse_args()
    if a.batch_size < 1:
        p.error("--batch-size must be at least 1")
    try:
        print(json.dumps(prepare(a.input, a.output, a.batch_size), indent=2))
        return 0
    except (OSError, ValueError, RuntimeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
