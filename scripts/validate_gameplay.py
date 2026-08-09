from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

game = load(ROOT/"data/rules/game.yaml")["game"]
assert game["version"] == "0.46"

locations = load(ROOT/"data/rules/locations.yaml")["locations"]
ids = [x["id"] for x in locations]
assert len(ids) == len(set(ids)), "Duplicate location ids"

turn = load(ROOT/"data/rules/turn-sequence.yaml")["turn_sequence"]
assert turn["steps"][1]["choose_exactly_one"] == ["explore", "fight", "train", "build"]
assert "2 energi" in turn["actions"]["train"]["effect"]
assert "2 Skydd" in turn["actions"]["build"]["effect"]
assert "slut på energi" in turn["zero_energy"]["rule"]
assert "2 energi" in turn["zero_energy"]["rule"]

shields = load(ROOT/"data/rules/shields.yaml")["shields"]
assert shields["maximum_per_hero"] == 2
assert shields["gain"]["build_action"] == 2
assert shields["gain"]["earth_guardian_build_action"] == 2
assert shields["gain"]["build_distribution"] == "heroes_at_location"
assert shields["gain"]["earth_guardian_distribution"] == "any_heroes"
assert shields["combat_use"]["maximum_per_roll"] == 1

crystals = load(ROOT/"data/rules/crystals.yaml")["crystals"]
assert len(crystals["items"]) == 4

boss = load(ROOT/"data/rules/shadow-master.yaml")["shadow_master"]
assert boss["fight_action"]["failure_energy_loss"] == 1
assert boss["fight_action"]["shield_can_prevent_failure_loss"] is True

element_locations = [x for x in locations if x["type"] == "element"]
assert len(element_locations) == 4
for loc in element_locations:
    assert "location_power" in loc
    assert "element_hero" in loc

adventure = load(ROOT/"data/cards/adventure.yaml")["deck"]
shadow = load(ROOT/"data/cards/shadow.yaml")["deck"]
assert sum(c.get("count", 1) for c in adventure["cards"]) == 12
assert sum(c.get("count", 1) for c in shadow["cards"]) == 8
assert all(not c.get("keep", False) for c in adventure["cards"])

player_count = load(ROOT/"data/rules/player-count.yaml")["player_count_rules"]
assert player_count["version"] == "0.46"
assert player_count["all_heroes_used"] is True
assert len(player_count["hero_order"]) == 4
assert "hjälpkort" not in player_count["state_rule"].lower()

scenario = load(ROOT/"data/scenarios/first-adventure.yaml")["scenario"]
assert scenario["light_start"] == 8
assert scenario["light_end_state"] == "Släckt"
assert "darkness_start" not in scenario and "darkness_limit" not in scenario

reference = load(ROOT/"data/reference/player-reference-a6.yaml")["reference_card"]
assert reference["version"] == "0.46"
ref_text = yaml.safe_dump(reference, allow_unicode=True)
assert "+2 energi" in ref_text
assert "2 Skydd" in ref_text
assert "Äventyrskort" not in ref_text or "Max 2 Skydd och 2 Äventyrskort" not in ref_text
for term in ["Eld", "Vatten", "Vind", "Jord", "Kraftkälla"]:
    assert term in ref_text
assert "slut på energi" in ref_text.lower()

player_files = [
    ROOT/"docs/player/RULEBOOK.md",
    ROOT/"docs/player/QUICKSTART.md",
    ROOT/"docs/player/FAQ.md",
    ROOT/"docs/player/REFERENCE_CARD_A6.md",
]
combined = "\n".join(p.read_text(encoding="utf-8") for p in player_files)
for required in [
    "Version 0.45", "Träna", "2 energi", "Bygg", "2 Skydd",
    "Eldbron", "Vattengrottan", "Vindtoppen", "Jordskogen",
    "slut på energi", "Träningsgården", "Skuggmästaren"
]:
    assert required in combined, f"Missing player-facing concept: {required}"

for forbidden in ["Mörkerspåret", "Mörkermarkör", "Max 2 Skydd och 2 Äventyrskort"]:
    assert forbidden not in combined, f"Legacy term remains: {forbidden}"

print("Gameplay and terminology validation OK - v0.48")
