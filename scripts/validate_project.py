#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json
import subprocess
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "PROJECT_STATUS.md",
    "CHANGELOG.md",
    "RELEASE_INVENTORY.json",
    "data/board/board.yaml",
    "data/heroes/heroes.yaml",
    "data/cards/adventure.yaml",
    "data/cards/shadow.yaml",
    "data/reference/player-reference-a6.yaml",
    "docs/player/RULEBOOK.md",
    "docs/player/QUICKSTART.md",
    "docs/player/FAQ.md",
    "scripts/build.py",
    "scripts/validate_gameplay.py",
    "templates/board/board.svg",
]

EXPECTED_PRINT_PDFS = {
    "adventure-cards-a4.pdf",
    "board-a4.pdf",
    "board-a4-ink-friendly.pdf",
    "crystal-tokens-a4.pdf",
    "hero-cards-a4.pdf",
    "player-reference-a6.pdf",
    "shadow-cards-a4.pdf",
    "shield-tokens-a4.pdf",
}

def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(2)

def load_yaml(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"Kan inte läsa YAML {path.relative_to(ROOT)}: {exc}")

def check_required_files() -> None:
    missing = [p for p in REQUIRED_FILES if not (ROOT / p).is_file()]
    if missing:
        fail("Obligatoriska filer saknas: " + ", ".join(missing))

def check_yaml_files() -> None:
    yaml_files = sorted((ROOT / "data").rglob("*.yaml"))
    if not yaml_files:
        fail("Inga YAML-filer hittades under data/.")
    for path in yaml_files:
        load_yaml(path)
    print(f"OK: {len(yaml_files)} YAML-filer kunde läsas.")

def check_board_references() -> None:
    board = load_yaml(ROOT / "data/board/board.yaml")["board"]
    backgrounds = board.get("backgrounds", {})
    if board.get("background"):
        backgrounds = {"default": board["background"], **backgrounds}
    for name, rel in backgrounds.items():
        path = ROOT / rel
        if not path.is_file():
            fail(f"Spelplansbakgrund saknas ({name}): {rel}")

    overlay = board.get("light_track", {}).get("overlay_asset")
    if overlay and not (ROOT / overlay).is_file():
        fail(f"Ljusindikator-overlay saknas: {overlay}")

    locations = board.get("locations", [])
    ids = [item["id"] for item in locations]
    if len(ids) != len(set(ids)):
        fail("Dubbla plats-id:n i data/board/board.yaml.")
    known = set(ids)
    for a, b in board.get("paths", []):
        if a not in known or b not in known:
            fail(f"Väg refererar okänd plats: {a} -> {b}")
    for item in locations:
        icon = item.get("icon")
        if icon and not (ROOT / f"assets/icons/{icon}.svg").is_file():
            fail(f"Platsen {item['id']} refererar saknad ikon: {icon}.svg")
    print(f"OK: spelplanens {len(locations)} platser, vägar, bakgrunder och overlay är konsekventa.")

def check_hero_references() -> None:
    heroes = load_yaml(ROOT / "data/heroes/heroes.yaml")["heroes"]["items"]
    for hero in heroes:
        rel = hero.get("image")
        if not rel or not (ROOT / rel).is_file():
            fail(f"Hjälten {hero.get('id')} refererar saknad bild: {rel}")
    print(f"OK: {len(heroes)} hjältebilder finns.")

def check_card_icons() -> None:
    total = 0
    for deck_name in ("adventure", "shadow"):
        deck = load_yaml(ROOT / f"data/cards/{deck_name}.yaml")["deck"]
        for card in deck["cards"]:
            total += card.get("count", 1)
            icon = card.get("icon")
            if icon and not (ROOT / f"assets/icons/cards/{icon}.svg").is_file():
                fail(f"Kortet {card.get('id')} refererar saknad ikon: {icon}.svg")
    print(f"OK: kortreferenser och ikoner validerade ({total} kort inklusive kopior).")

def check_release_inventory() -> None:
    path = ROOT / "RELEASE_INVENTORY.json"
    try:
        inventory = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"RELEASE_INVENTORY.json kan inte läsas: {exc}")
    recommended = inventory.get("recommended_print", [])
    names = {Path(p).name for p in recommended}
    if names != EXPECTED_PRINT_PDFS:
        missing = sorted(EXPECTED_PRINT_PDFS - names)
        extra = sorted(names - EXPECTED_PRINT_PDFS)
        fail(f"recommended_print stämmer inte med förväntad printuppsättning. Saknas={missing}, extra={extra}")
    print("OK: release-inventeringen listar exakt den rekommenderade printuppsättningen.")

def run_gameplay_validation() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_gameplay.py")],
        cwd=ROOT,
    )
    if result.returncode != 0:
        fail("Gameplay-/terminologivalideringen misslyckades.")

def main() -> int:
    check_required_files()
    check_yaml_files()
    check_board_references()
    check_hero_references()
    check_card_icons()
    check_release_inventory()
    run_gameplay_validation()
    print("PROJECT VALIDATION OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
