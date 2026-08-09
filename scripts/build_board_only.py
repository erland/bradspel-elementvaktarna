
from pathlib import Path
import base64, html, yaml
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

def replace_tokens(template, values):
    result = template
    for key, value in values.items():
        result = result.replace("{{" + key + "}}", str(value))
    return result

def file_data_uri(path, mime):
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"

with open(DATA / "board/board.yaml", encoding="utf-8") as f:
    board = yaml.safe_load(f)["board"]

W, H = board["canvas"]["width"], board["canvas"]["height"]
area = board["board_area"]
background_layout = board.get("background_layout", {"x": 0, "y": 0, "width": W, "height": H})
locs = {loc["id"]: loc for loc in board["locations"]}
theme = board["theme"]
SRC_W, SRC_H = 794, 629

def tx(x): return area["x"] + x * area["width"] / SRC_W
def ty(y): return area["y"] + y * area["height"] / SRC_H

paths = ['<g id="paths" fill="none" stroke-linecap="round">']
for a, b in board["paths"]:
    p, q = locs[a], locs[b]
    x1, y1, x2, y2 = tx(p["x"]), ty(p["y"]), tx(q["x"]), ty(q["y"])
    paths.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{theme["path_outer"]}" stroke-width="12" opacity=".80"/>')
    paths.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{theme["path_inner"]}" stroke-width="6" stroke-dasharray="16 10"/>')
paths.append("</g>")

nodes = ['<g id="nodes">']
labels = ['<g id="labels" font-family="DejaVu Sans, Arial, sans-serif">']
icons = ['<g id="icons">']
LABEL_W, LABEL_H = 166, 40
for p in board["locations"]:
    x, y = tx(p["x"]), ty(p["y"])
    nodes.append(f'<circle cx="{x}" cy="{y}" r="34" fill="{theme["node_fill"]}" stroke="{theme["node_stroke"]}" stroke-width="4"/>')
    ly = y + 42 if p["label"]["position"] == "bottom" else y - (LABEL_H + 44)
    labels.append(f'<rect x="{x-LABEL_W/2}" y="{ly}" width="{LABEL_W}" height="{LABEL_H}" rx="8" fill="{theme["label_fill"]}" stroke="{theme["accent"]}" stroke-width="3"/>')
    labels.append(f'<text x="{x}" y="{ly + LABEL_H/2 + 5}" text-anchor="middle" font-size="14" font-weight="700" fill="{theme["label_text"]}">{html.escape(p["name"].upper())}</text>')
    icon_path = ASSETS / "icons" / f'{p["icon"]}.svg'
    icons.append(f'<image href="{file_data_uri(icon_path, "image/svg+xml")}" x="{x-11}" y="{y-11}" width="22" height="22"/>')
nodes.append("</g>"); labels.append("</g>"); icons.append("</g>")

dt = board["light_track"]
light_track_background = ""
light_track = ['<g id="light-track" font-family="DejaVu Sans, Arial, sans-serif">']
if dt.get("enabled"):
    overlay_path = ROOT / dt["overlay_asset"]
    light_track_background = (
        f'<image id="light-track-overlay" href="{file_data_uri(overlay_path, "image/svg+xml")}" '
        f'x="{dt["x"]}" y="{dt["y"]}" width="{dt["width"]}" height="{dt["height"]}" preserveAspectRatio="none"/>'
    )
    x = dt["number_x"]; y = dt["number_start_y"]; spacing = dt["spacing"]; start_value = dt["start"]
    light_track.append(f'<text x="{x}" y="{dt["y"]+68}" text-anchor="middle" font-size="23" font-weight="700" fill="#3d3327">{html.escape(dt["label"])}</text>')
    for index in range(start_value):
        cy = y + index * spacing
        value = start_value - index
        light_track.append(f'<text x="{x}" y="{cy+7}" text-anchor="middle" font-size="21" font-weight="700" fill="#2f2a25">{value}</text>')
    end_y = dt.get("end_center_y", dt["y"] + dt["height"] - 46)
    light_track.append(f'<text x="{x}" y="{end_y+7}" text-anchor="middle" font-size="13" font-weight="700" fill="#4c3e52">{html.escape(dt["end_label"])}</text>')
light_track.append("</g>")

backgrounds = board.get("backgrounds", {"standard": board["background"]})
board_template = (TEMPLATES / "board/board.svg").read_text(encoding="utf-8")

for variant, background_rel in backgrounds.items():
    background_path = ROOT / background_rel
    values = {
        "WIDTH": W, "HEIGHT": H,
        "BACKGROUND_X": background_layout["x"], "BACKGROUND_Y": background_layout["y"],
        "BACKGROUND_WIDTH": background_layout["width"], "BACKGROUND_HEIGHT": background_layout["height"],
        "BOARD_X": area["x"], "BOARD_Y": area["y"],
        "BOARD_WIDTH": area["width"], "BOARD_HEIGHT": area["height"],
        "BACKGROUND_DATA": file_data_uri(background_path, "image/png"),
        "PATHS": "\n".join(paths), "NODES": "\n".join(nodes),
        "LABELS": "\n".join(labels), "ICONS": "\n".join(icons),
        "LIGHT_TRACK_BACKGROUND": light_track_background,
        "LIGHT_TRACK": "\n".join(light_track),
    }
    svg = replace_tokens(board_template, values)
    suffix = "" if variant == "standard" else f"-{variant.replace('_', '-')}"
    svg_path = OUT_SVG / f"board-a4{suffix}.svg"
    svg_path.write_text(svg, encoding="utf-8")
    ET.parse(svg_path)
    cairosvg.svg2pdf(url=str(svg_path), write_to=str(OUT_PDF / f"board-a4{suffix}.pdf"))
    cairosvg.svg2png(url=str(svg_path), write_to=str(OUT_PREVIEW / f"board-a4{suffix}.png"), output_width=1600)
    print(svg_path)
