#!/usr/bin/env python3
"""Validate anan_everyday_news JSON data files."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_TOP_LEVEL = ["schema_version", "date", "title", "summary", "cards", "actions"]
REQUIRED_CARD = ["id", "section", "title", "summary", "source_grade", "sources"]
VALID_GRADES = {"A", "B", "C", "自"}


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"{path}: invalid json: {exc}") from exc


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    data = load_json(path)

    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            errors.append(f"{path}: missing top-level key {key}")

    cards = data.get("cards", [])
    if not isinstance(cards, list):
        errors.append(f"{path}: cards must be a list")
        return errors

    seen_ids: set[str] = set()
    for idx, card in enumerate(cards):
        prefix = f"{path}: card[{idx}]"
        if not isinstance(card, dict):
            errors.append(f"{prefix}: card must be object")
            continue
        for key in REQUIRED_CARD:
            if key not in card:
                errors.append(f"{prefix}: missing key {key}")
        card_id = card.get("id")
        if card_id in seen_ids:
            errors.append(f"{prefix}: duplicate id {card_id}")
        if card_id:
            seen_ids.add(card_id)
        if card.get("source_grade") not in VALID_GRADES:
            errors.append(f"{prefix}: source_grade must be one of {sorted(VALID_GRADES)}")
        sources = card.get("sources", [])
        if not isinstance(sources, list) or not sources:
            errors.append(f"{prefix}: sources must be a non-empty list")
        else:
            for s_idx, source in enumerate(sources):
                if not isinstance(source, dict) or not source.get("name") or not source.get("url"):
                    errors.append(f"{prefix}: sources[{s_idx}] must include name and url")
        image = card.get("image")
        if image:
            if not isinstance(image, dict):
                errors.append(f"{prefix}: image must be object")
            else:
                if not (image.get("url") or image.get("local_path")):
                    errors.append(f"{prefix}: image needs url or local_path")
                if not image.get("target_url"):
                    errors.append(f"{prefix}: image.target_url is required so the original page is never lost")
                if not image.get("alt"):
                    errors.append(f"{prefix}: image.alt is required")
        if card.get("section") == "do-now" and "game" in card.get("id", ""):
            if not card.get("decision"):
                errors.append(f"{prefix}: game decision card should include decision object")

    return errors


def main() -> None:
    paths = [Path(arg) for arg in sys.argv[1:]] or [ROOT / "data" / "today.json"]
    all_errors: list[str] = []
    for path in paths:
        if not path.is_absolute():
            path = ROOT / path
        all_errors.extend(validate(path))
    if all_errors:
        print("Data validation failed:")
        for error in all_errors:
            print(f"- {error}")
        sys.exit(1)
    print("Data validation passed.")


if __name__ == "__main__":
    main()
