#!/usr/bin/env python3
"""Calculate evidence-based progress metrics from a Ghidra inventory and ledgers.

This deliberately separates:
- function dossier coverage (inventory ledger entries / Ghidra function count),
- behavior validated by tests against an oracle, and
- weighted understanding of essential subsystems.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as stream:
        data = json.load(stream)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def load_csv(path: Path, required_columns: set[str]) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None:
            raise ValueError(f"{path} has no CSV header")
        missing = required_columns.difference(reader.fieldnames)
        if missing:
            raise ValueError(f"{path} is missing required columns: {sorted(missing)}")
        rows = list(reader)
    if not rows:
        raise ValueError(f"{path} has no data rows")
    return rows


def calculate(inventory: dict[str, Any], ledger_rows: list[dict[str, str]],
              scorecard_rows: list[dict[str, str]]) -> dict[str, Any]:
    target = inventory.get("target") or {}
    functions = inventory.get("functions") or {}
    total_functions = functions.get("total")
    if not isinstance(total_functions, int) or total_functions <= 0:
        raise ValueError("inventory.functions.total must be a positive integer")

    addresses: set[str] = set()
    validated_count = 0
    for row_number, row in enumerate(ledger_rows, start=2):
        address = row["address"].strip().lower()
        if not address.startswith("0x") or len(address) < 4:
            raise ValueError(f"FUNCTION_LEDGER row {row_number}: invalid address {address!r}")
        if address in addresses:
            raise ValueError(f"FUNCTION_LEDGER contains duplicate address {address}")
        addresses.add(address)
        evidence_url = row["evidence_url"].strip()
        if not evidence_url.startswith("https://github.com/"):
            raise ValueError(f"FUNCTION_LEDGER row {row_number}: expected a GitHub evidence URL")
        validated = row["behavior_validated"].strip().lower()
        if validated not in {"true", "false"}:
            raise ValueError(
                f"FUNCTION_LEDGER row {row_number}: behavior_validated must be true or false"
            )
        validated_count += validated == "true"

    if len(addresses) > total_functions:
        raise ValueError(
            f"Ledger has {len(addresses)} dossier addresses but inventory only has "
            f"{total_functions} functions"
        )

    weight_total = 0.0
    essential_score = 0.0
    scorecard_result: list[dict[str, Any]] = []
    for row_number, row in enumerate(scorecard_rows, start=2):
        try:
            weight = float(row["weight"])
            level = float(row["current_level"])
        except (ValueError, TypeError) as exc:
            raise ValueError(f"Scorecard row {row_number}: weight and current_level must be numbers") from exc
        if not math.isfinite(weight) or weight < 0:
            raise ValueError(f"Scorecard row {row_number}: weight must be a finite nonnegative number")
        if not math.isfinite(level) or not 0 <= level <= 100:
            raise ValueError(f"Scorecard row {row_number}: current_level must be between 0 and 100")
        contribution = weight * level / 100.0
        weight_total += weight
        essential_score += contribution
        scorecard_result.append({
            "subsystem": row["subsystem"],
            "weight": weight,
            "current_level": level,
            "weighted_contribution": round(contribution, 4),
            "evidence_reason": row["evidence_reason"],
        })

    if not math.isclose(weight_total, 100.0, rel_tol=0.0, abs_tol=1e-6):
        raise ValueError(f"Scorecard weights must total 100; got {weight_total}")

    return {
        "schema_version": 1,
        "target": {
            "path": target.get("path"),
            "sha256": target.get("sha256"),
            "inventory_source_commit": target.get("source_commit"),
        },
        "inventory": {
            "provider": (inventory.get("analysis") or {}).get("provider", "Ghidra headless"),
            "ghidra_version": (inventory.get("analysis") or {}).get("ghidra_version"),
            "total_functions": total_functions,
            "internal_function_entries": functions.get("internal"),
            "external_function_entries": functions.get("external"),
            "thunks": functions.get("thunks"),
            "body_ranges_sum": functions.get("body_ranges_sum"),
            "memory_blocks": (inventory.get("memory") or {}).get("block_count"),
            "external_library_count": inventory.get("external_library_count"),
        },
        "function_dossier_coverage": {
            "count": len(ledger_rows),
            "denominator": total_functions,
            "percent": round(len(ledger_rows) / total_functions * 100.0, 6),
            "definition": "Unique function addresses with an evidence-backed dossier entry in FUNCTION_LEDGER.csv; entries may be partial.",
        },
        "function_behavior_validated": {
            "count": validated_count,
            "denominator": total_functions,
            "percent": round(validated_count / total_functions * 100.0, 6),
            "definition": "Function entries whose behavior has repeatable validation against the original or an equivalent trusted oracle.",
        },
        "essential_system_understanding": {
            "score": round(essential_score, 4),
            "weight_total": round(weight_total, 4),
            "definition": "Sum of subsystem weight multiplied by its evidence-based current level, divided by 100.",
            "scorecard": scorecard_result,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, required=True, help="Ghidra inventory summary.json")
    parser.add_argument("--ledger", type=Path, default=Path("docs/FUNCTION_LEDGER.csv"))
    parser.add_argument("--scorecard", type=Path, default=Path("docs/ESSENTIAL_SYSTEM_SCORECARD.csv"))
    parser.add_argument("--output", type=Path, required=True, help="Output progress_metrics.json path")
    args = parser.parse_args()

    try:
        inventory = load_json(args.inventory)
        ledger = load_csv(args.ledger, {
            "address", "ghidra_name", "subsystem", "summary", "evidence_level",
            "evidence_url", "notes", "behavior_validated",
        })
        scorecard = load_csv(args.scorecard, {
            "subsystem", "weight", "current_level", "evidence_reason",
        })
        metrics = calculate(inventory, ledger, scorecard)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8") as stream:
            json.dump(metrics, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
    except (OSError, ValueError, json.JSONDecodeError, csv.Error) as exc:
        print(f"progress metrics error: {exc}", file=sys.stderr)
        return 2

    dossier = metrics["function_dossier_coverage"]
    validated = metrics["function_behavior_validated"]
    essential = metrics["essential_system_understanding"]
    inventory_metrics = metrics["inventory"]
    print("## Evidence-based progress metrics")
    print()
    print(f"- **Target SHA-256:** `{metrics['target']['sha256']}`")
    print(f"- **Ghidra functions inventoried:** {inventory_metrics['total_functions']:,}")
    print(f"- **Function dossier coverage:** {dossier['count']:,}/{dossier['denominator']:,} "
          f"({dossier['percent']:.4f}%) — partial dossiers are not full understanding.")
    print(f"- **Functions validated against an oracle:** {validated['count']:,}/{validated['denominator']:,} "
          f"({validated['percent']:.4f}%).")
    print(f"- **Essential-system weighted understanding:** {essential['score']:.2f}/100.")
    print(f"- **External libraries:** {inventory_metrics['external_library_count']}; "
          f"**Ghidra body ranges:** {inventory_metrics['body_ranges_sum']:,}.")
    print()
    print(f"Detailed machine-readable output: `{args.output}`.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
