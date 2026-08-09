from pathlib import Path
import base64, html, textwrap, yaml, subprocess, sys
from PIL import Image, ImageFont
import cairosvg
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/cards"
ASSETS = ROOT / "assets/icons/cards"
TEMPLATE = (ROOT / "templates/cards/card.svg").read_text(encoding="utf-8")
OUT_SVG = ROOT / "output/svg/cards"
OUT_PDF = ROOT / "output/pdf"
OUT_PREVIEW = ROOT / "output/preview"
TEMP = ROOT / "output/.card-pages"

for p in [OUT_SVG, OUT_PDF, OUT_PREVIEW, TEMP]:
    p.mkdir(parents=True, exist_ok=True)

CARD_W, CARD_H = 226, 316
A4_W, A4_H = 794, 1123
POSITIONS = [
    (40, 55), (284, 55), (528, 55),
    (40, 385), (284, 385), (528, 385),
    (40, 715), (284, 715), (528, 715),
]

def data_uri(path: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")

def fill(template: str, values: dict) -> str:
    out = template
    for key, value in values.items():
        out = out.replace("{{" + key + "}}", str(value))
    return out

def wrap_text_pixels(text: str, font, max_width: int) -> list[str]:
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = word if not current else current + " " + word
        width = font.getlength(candidate)
        if width <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def choose_title_font_size(title: str, max_width: int = 184) -> int:
    """Return the largest title size that fits the card header on one line."""
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
    title = title.upper()
    for font_size in (21, 20, 19, 18, 17, 16, 15, 14):
        font = ImageFont.truetype(font_path, font_size)
        if font.getlength(title) <= max_width:
            return font_size
    return 14

def build_card(card: dict, deck: dict) -> str:
    theme = deck["theme"]

    # The description box keeps a fixed safe zone above the footer.
    max_text_width = 160
    box_top = 160
    box_height = 105
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    selected = None
    for font_size in (14, 13, 12, 11, 10):
        font = ImageFont.truetype(font_path, font_size)
        lines = wrap_text_pixels(card["text"], font, max_text_width)
        line_height = font_size + 4
        total_height = len(lines) * line_height
        if len(lines) <= 6 and total_height <= 88:
            selected = (font_size, line_height, lines, font)
            break

    if selected is None:
        font_size = 10
        font = ImageFont.truetype(font_path, font_size)
        lines = wrap_text_pixels(card["text"], font, max_text_width)[:7]
        line_height = 13
    else:
        font_size, line_height, lines, font = selected

    total_height = len(lines) * line_height
    y = box_top + (box_height - total_height) / 2 + font_size

    line_elements = []
    for line in lines:
        # Final safety check against the actual font metrics.
        assert font.getlength(line) <= max_text_width + 0.5, (card["id"], line)
        line_elements.append(
            f'<text x="{CARD_W/2}" y="{y:.1f}" text-anchor="middle" '
            f'font-family="DejaVu Sans, Arial, sans-serif" font-size="{font_size}" '
            f'fill="{theme["text"]}">{html.escape(line)}</text>'
        )
        y += line_height




    title_font_size = choose_title_font_size(card["title"])

    values = {
        "CARD_W": CARD_W, "CARD_H": CARD_H,
        "OUTER_W": CARD_W-6, "OUTER_H": CARD_H-6,
        "HEADER_W": CARD_W-26, "TEXT_W": CARD_W-38,
        "CX": CARD_W/2, "ICON_X": CARD_W/2-26,
        "PRIMARY": theme["primary"], "SECONDARY": theme["secondary"],
        "TEXT_COLOR": theme["text"],
        "TITLE": html.escape(card["title"].upper()),
        "TITLE_FONT_SIZE": title_font_size,
        "TYPE": html.escape(card["type"].upper()),
        "ICON_DATA": data_uri(ASSETS/f'{card["icon"]}.svg', "image/svg+xml"),
        "TEXT_LINES": "\n".join(line_elements),
        "DECK_NAME": html.escape(deck["name"].upper()),
        "STATUS_BANNER": (
            '<text x="113" y="282" text-anchor="middle" font-family="DejaVu Sans" font-size="9" font-weight="700" fill="' + theme["primary"] + '">BEHÅLL - MAX 2 HJÄLPKORT</text>'
            if card.get("keep") else (
                '<text x="113" y="282" text-anchor="middle" font-family="DejaVu Sans" font-size="9" font-weight="700" fill="' + theme["primary"] + '">LÄGG FRAMFÖR HJÄLTEN</text>'
                if card.get("persistent") else ""
            )
        ),
    }
    return fill(TEMPLATE, values)

def expand_cards(deck: dict) -> list[dict]:
    expanded = []
    for card in deck["cards"]:
        for i in range(card.get("count", 1)):
            copy = dict(card)
            copy["copy_index"] = i + 1
            expanded.append(copy)
    return expanded

def merge_pdfs(paths: list[Path], output: Path) -> None:
    writer = PdfWriter()
    for path in paths:
        reader = PdfReader(str(path))
        for page in reader.pages:
            writer.add_page(page)
    with output.open("wb") as f:
        writer.write(f)

def build_deck(filename: str) -> None:
    with open(DATA/filename, encoding="utf-8") as f:
        deck = yaml.safe_load(f)["deck"]
    cards = expand_cards(deck)
    card_svgs = [build_card(c, deck) for c in cards]
    page_paths = []
    page_pngs = []

    for page_index in range((len(cards)+8)//9):
        page_cards = card_svgs[page_index*9:(page_index+1)*9]
        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{A4_W}" height="{A4_H}" viewBox="0 0 {A4_W} {A4_H}">',
            f'<rect width="{A4_W}" height="{A4_H}" fill="#FFFFFF"/>'
        ]
        for svg, (x, y) in zip(page_cards, POSITIONS):
            inner = svg.split(">", 1)[1].rsplit("</svg>", 1)[0]
            parts.append(f'<g transform="translate({x},{y})">{inner}</g>')
        parts.append("</svg>")
        svg_path = OUT_SVG/f'{deck["id"]}-cards-a4-page-{page_index+1}.svg'
        svg_path.write_text("\n".join(parts), encoding="utf-8")

        pdf_page = TEMP/f'{deck["id"]}-page-{page_index+1}.pdf'
        png_page = TEMP/f'{deck["id"]}-page-{page_index+1}.png'
        cairosvg.svg2pdf(url=str(svg_path), write_to=str(pdf_page))
        cairosvg.svg2png(url=str(svg_path), write_to=str(png_page), output_width=1200)
        page_paths.append(pdf_page)
        page_pngs.append(png_page)

    merge_pdfs(page_paths, OUT_PDF/f'{deck["id"]}-cards-a4.pdf')

    # Preview uses first page; for adventure also create a simple two-page contact sheet.
    if len(page_pngs) == 1:
        (OUT_PREVIEW/f'{deck["id"]}-cards-a4.png').write_bytes(page_pngs[0].read_bytes())
    else:
        images = [Image.open(p).convert("RGB") for p in page_pngs]
        width = max(i.width for i in images)
        height = sum(i.height for i in images)
        canvas = Image.new("RGB", (width, height), "white")
        yy = 0
        for image in images:
            canvas.paste(image, (0, yy))
            yy += image.height
        canvas.save(OUT_PREVIEW/f'{deck["id"]}-cards-a4.png', quality=94)

    print(OUT_PDF/f'{deck["id"]}-cards-a4.pdf')
    print(OUT_PREVIEW/f'{deck["id"]}-cards-a4.png')

build_deck("adventure.yaml")
build_deck("shadow.yaml")
