from pathlib import Path
import base64, html, math, textwrap, yaml
import xml.etree.ElementTree as ET
import cairosvg

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TEMPLATES = ROOT / "templates"
ASSETS = ROOT / "assets"
OUT_SVG = ROOT / "output/svg"
OUT_PDF = ROOT / "output/pdf"
OUT_PREVIEW = ROOT / "output/preview"

for p in [OUT_SVG, OUT_PDF, OUT_PREVIEW]:
    p.mkdir(parents=True, exist_ok=True)

def replace_tokens(template: str, values: dict[str, object]) -> str:
    result = template
    for key, value in values.items():
        result = result.replace("{{" + key + "}}", str(value))
    return result

def file_data_uri(path: Path, mime: str) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"

def validate_svg(path: Path) -> None:
    ET.parse(path)

def render_svg(svg_path: Path, pdf_path: Path, png_path: Path, png_width: int | None = None) -> None:
    cairosvg.svg2pdf(url=str(svg_path), write_to=str(pdf_path))
    kwargs = {"url": str(svg_path), "write_to": str(png_path)}
    if png_width:
        kwargs["output_width"] = png_width
    cairosvg.svg2png(**kwargs)

# ------------------------------------------------------------------
# HEROES
# ------------------------------------------------------------------
with open(DATA / "heroes/heroes.yaml", encoding="utf-8") as f:
    hero_cfg = yaml.safe_load(f)["heroes"]

card = hero_cfg["card"]
image_frame = hero_cfg["image_frame"]
CW, CH = card["width"], card["height"]
hero_template = (TEMPLATES / "heroes/hero-card.svg").read_text(encoding="utf-8")

def build_hero_svg(hero: dict) -> str:
    energy = []
    for i in range(hero["energy"]):
        cx = 145 + i * 52
        energy.append(
            f'<circle cx="{cx}" cy="349" r="18" fill="{hero["color"]}" '
            f'stroke="#111111" stroke-width="2"/>'
        )
        energy.append(
            f'<text x="{cx}" y="356" text-anchor="middle" '
            f'font-family="DejaVu Sans, Arial, sans-serif" font-size="17" '
            f'font-weight="700" fill="#FFFFFF">*</text>'
        )

    ability_lines = []
    y = 451
    for line in textwrap.wrap(hero["ability"], width=34)[:4]:
        ability_lines.append(
            f'<text x="{CW/2}" y="{y}" text-anchor="middle" '
            f'font-family="DejaVu Sans, Arial, sans-serif" font-size="19" '
            f'fill="#111111">{html.escape(line)}</text>'
        )
        y += 26

    flavor_lines = []
    y = 556
    for line in textwrap.wrap(hero["flavor"], width=42)[:2]:
        flavor_lines.append(
            f'<text x="{CW/2}" y="{y}" text-anchor="middle" '
            f'font-family="DejaVu Sans, Arial, sans-serif" font-size="14" '
            f'font-style="italic" fill="#555555">{html.escape(line)}</text>'
        )
        y += 18

    values = {
        "CARD_WIDTH": CW,
        "CARD_HEIGHT": CH,
        "OUTER_WIDTH": CW - 8,
        "OUTER_HEIGHT": CH - 8,
        "CORNER_RADIUS": card["corner_radius"],
        "HEADER_WIDTH": CW - 36,
        "CENTER_X": CW / 2,
        "ART_WIDTH": CW - 76,
        "ABILITY_WIDTH": CW - 60,
        "COLOR": hero["color"],
        "NAME": html.escape(hero["name"].upper()),
        "ELEMENT": html.escape(hero["element"].upper()),
        "ICON_TEXT": html.escape(hero["element"][0].upper()),
        "IMAGE_DATA": file_data_uri(ROOT / hero["image"], "image/png"),
        "CLIP_ID": f'hero-art-{hero["id"]}',
        "IMAGE_X": image_frame["x"],
        "IMAGE_Y": image_frame["y"] + hero.get("image_offset_y", 0),
        "IMAGE_WIDTH": image_frame["width"],
        "IMAGE_HEIGHT": image_frame["height"],
        "IMAGE_RADIUS": image_frame["corner_radius"],
        "IMAGE_ASPECT": image_frame["preserve_aspect_ratio"], 
        "ENERGY_MARKERS": "\n".join(energy),
        "ABILITY_NAME": html.escape(hero["ability_name"].upper()),
        "ABILITY_LINES": "\n".join(ability_lines),
        "FLAVOR_LINES": "\n".join(flavor_lines),
    }
    return replace_tokens(hero_template, values)

individual = {}
for hero in hero_cfg["items"]:
    svg = build_hero_svg(hero)
    path = OUT_SVG / f'{hero["id"]}.svg'
    path.write_text(svg, encoding="utf-8")
    validate_svg(path)
    individual[hero["id"]] = svg

# A4 landscape master sheet, 2 × 2
A4W, A4H = 1123, 794
scale = 0.54
positions = [(70, 55), (633, 55), (70, 405), (633, 405)]
sheet_parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{A4W}" height="{A4H}" viewBox="0 0 {A4W} {A4H}">',
    f'<rect width="{A4W}" height="{A4H}" fill="#FFFFFF"/>'
]
for hero, (x, y) in zip(hero_cfg["items"], positions):
    inner = individual[hero["id"]].split(">", 1)[1].rsplit("</svg>", 1)[0]
    sheet_parts.append(f'<g transform="translate({x},{y}) scale({scale})">{inner}</g>')
sheet_parts.append("</svg>")

heroes_master = OUT_SVG / "hero-cards-a4.svg"
heroes_master.write_text("\n".join(sheet_parts), encoding="utf-8")
validate_svg(heroes_master)
render_svg(
    heroes_master,
    OUT_PDF / "hero-cards-a4.pdf",
    OUT_PREVIEW / "hero-cards-a4.png",
    png_width=1400,
)

# ------------------------------------------------------------------
# BOARD
# ------------------------------------------------------------------
with open(DATA / "board/board.yaml", encoding="utf-8") as f:
    board = yaml.safe_load(f)["board"]

W, H = board["canvas"]["width"], board["canvas"]["height"]
area = board["board_area"]
background_layout = board.get("background_layout", {"x": 0, "y": 0, "width": W, "height": H})
locs = {loc["id"]: loc for loc in board["locations"]}
theme = board["theme"]
SRC_W, SRC_H = 794, 629

def tx(x):
    return area["x"] + x * area["width"] / SRC_W

def ty(y):
    return area["y"] + y * area["height"] / SRC_H

paths = ['<g id="paths" fill="none" stroke-linecap="round">']
for a, b in board["paths"]:
    p, q = locs[a], locs[b]
    x1, y1, x2, y2 = tx(p["x"]), ty(p["y"]), tx(q["x"]), ty(q["y"])
    paths.append(
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{theme["path_outer"]}" stroke-width="12" opacity=".80"/>'
    )
    paths.append(
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{theme["path_inner"]}" stroke-width="6" stroke-dasharray="16 10"/>'
    )
paths.append("</g>")

nodes = ['<g id="nodes">']
labels = ['<g id="labels" font-family="DejaVu Sans, Arial, sans-serif">']
icons = ['<g id="icons">']
LABEL_W, LABEL_H = 166, 40

for p in board["locations"]:
    x, y = tx(p["x"]), ty(p["y"])
    nodes.append(
        f'<circle cx="{x}" cy="{y}" r="34" fill="{theme["node_fill"]}" '
        f'stroke="{theme["node_stroke"]}" stroke-width="4"/>'
    )
    ly = y + 42 if p["label"]["position"] == "bottom" else y - (LABEL_H + 44)
    labels.append(
        f'<rect x="{x-LABEL_W/2}" y="{ly}" width="{LABEL_W}" height="{LABEL_H}" '
        f'rx="8" fill="{theme["label_fill"]}" stroke="{theme["accent"]}" stroke-width="3"/>'
    )
    labels.append(
        f'<text x="{x}" y="{ly + LABEL_H/2 + 5}" text-anchor="middle" '
        f'font-size="14" font-weight="700" fill="{theme["label_text"]}">'
        f'{html.escape(p["name"].upper())}</text>'
    )

    icon_path = ASSETS / "icons" / f'{p["icon"]}.svg'
    icon_uri = file_data_uri(icon_path, "image/svg+xml")
    icons.append(
        f'<image href="{icon_uri}" x="{x-11}" y="{y-11}" width="22" height="22"/>'
    )

nodes.append("</g>")
labels.append("</g>")
icons.append("</g>")

dt = board["light_track"]
light_track_background = ""
light_track = ['<g id="light-track" font-family="DejaVu Sans, Arial, sans-serif">']
if dt.get("enabled"):
    overlay_path = ROOT / dt["overlay_asset"]
    light_track_background = (
        f'<image id="light-track-overlay" href="{file_data_uri(overlay_path, "image/svg+xml")}" '
        f'x="{dt["x"]}" y="{dt["y"]}" width="{dt["width"]}" height="{dt["height"]}" '
        f'preserveAspectRatio="none"/>'
    )
    x = dt["number_x"]
    y = dt["number_start_y"]
    spacing = dt["spacing"]
    start_value = dt["start"]

    light_track.append(
        f'<text x="{x}" y="{dt["y"]+68}" text-anchor="middle" font-size="23" '
        f'font-weight="700" fill="#3d3327">{html.escape(dt["label"])}</text>'
    )

    for index in range(start_value):
        cy = y + index * spacing
        value = start_value - index
        # Markörfältens vita bakgrund ligger i dekorlagret; här genereras bara värdet.
        light_track.append(
            f'<text x="{x}" y="{cy+7}" text-anchor="middle" font-size="21" '
            f'font-weight="700" fill="#2f2a25">{value}</text>'
        )

    end_y = dt.get("end_center_y", dt["y"] + dt["height"] - 46)
    light_track.append(
        f'<text x="{x}" y="{end_y+7}" text-anchor="middle" font-size="13" '
        f'font-weight="700" fill="#4c3e52">{html.escape(dt["end_label"])}</text>'
    )

light_track.append("</g>")

background_path = ROOT / board["background"]
board_values = {
    "WIDTH": W,
    "HEIGHT": H,
    "BACKGROUND_X": background_layout["x"],
    "BACKGROUND_Y": background_layout["y"],
    "BACKGROUND_WIDTH": background_layout["width"],
    "BACKGROUND_HEIGHT": background_layout["height"],
    "BOARD_X": area["x"],
    "BOARD_Y": area["y"],
    "BOARD_WIDTH": area["width"],
    "BOARD_HEIGHT": area["height"],
    "BACKGROUND_DATA": file_data_uri(background_path, "image/png"),
    "PATHS": "\n".join(paths),
    "NODES": "\n".join(nodes),
    "LABELS": "\n".join(labels),
    "ICONS": "\n".join(icons),
    "LIGHT_TRACK_BACKGROUND": light_track_background,
    "LIGHT_TRACK": "\n".join(light_track),
}
board_template = (TEMPLATES / "board/board.svg").read_text(encoding="utf-8")
board_svg = replace_tokens(board_template, board_values)
board_master = OUT_SVG / "board-a4.svg"
board_master.write_text(board_svg, encoding="utf-8")
validate_svg(board_master)
render_svg(
    board_master,
    OUT_PDF / "board-a4.pdf",
    OUT_PREVIEW / "board-a4.png",
    png_width=1600,
)

# Optional additional board background variants (for example ink-friendly).
for variant, background_rel in board.get("backgrounds", {}).items():
    if variant == "standard":
        continue
    variant_values = dict(board_values)
    variant_values["BACKGROUND_DATA"] = file_data_uri(ROOT / background_rel, "image/png")
    variant_svg = replace_tokens(board_template, variant_values)
    suffix = variant.replace("_", "-")
    variant_master = OUT_SVG / f"board-a4-{suffix}.svg"
    variant_master.write_text(variant_svg, encoding="utf-8")
    validate_svg(variant_master)
    render_svg(
        variant_master,
        OUT_PDF / f"board-a4-{suffix}.pdf",
        OUT_PREVIEW / f"board-a4-{suffix}.png",
        png_width=1600,
    )

print(heroes_master)
print(OUT_PDF / "hero-cards-a4.pdf")
print(OUT_PREVIEW / "hero-cards-a4.png")
print(board_master)
print(OUT_PDF / "board-a4.pdf")
print(OUT_PREVIEW / "board-a4.png")


# Build card decks
import runpy
runpy.run_path(str(ROOT / "scripts/build_cards.py"), run_name="__main__")


# Validate gameplay and build documentation
import subprocess, sys
subprocess.run([sys.executable, str(ROOT/"scripts/validate_gameplay.py")], check=True)
subprocess.run([sys.executable, str(ROOT/"scripts/build_docs.py")], check=True)

# Build crystal tokens
import runpy
runpy.run_path(str(ROOT/"scripts/build_tokens.py"), run_name="__main__")

# Build shield tokens
import runpy
runpy.run_path(str(ROOT/"scripts/build_shields.py"), run_name="__main__")

# Build single-sided landscape A6 player reference card
import runpy
runpy.run_path(str(ROOT / "scripts/build_reference_card.py"), run_name="__main__")
