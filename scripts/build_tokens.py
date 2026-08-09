from pathlib import Path
import yaml, html, cairosvg
ROOT=Path(__file__).resolve().parents[1]
cfg=yaml.safe_load((ROOT/"data/tokens/crystals.yaml").read_text(encoding="utf-8"))["crystal_tokens"]
OUTSVG=ROOT/"output/svg/tokens"; OUTPDF=ROOT/"output/pdf"; OUTPRE=ROOT/"output/preview"
for p in [OUTSVG,OUTPDF,OUTPRE]: p.mkdir(parents=True,exist_ok=True)
W,H=794,1123
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       '<rect width="794" height="1123" fill="#fff"/>',
       '<text x="397" y="75" text-anchor="middle" font-family="DejaVu Sans Condensed" font-size="30" font-weight="700" fill="#245b46">KRISTALLMARKÖRER</text>']
positions=[(180,290),(610,290),(180,720),(610,720)]
for item,(x,y) in zip(cfg["items"],positions):
    c=item["color"]; name=html.escape(item["name"].upper())
    points=[(x,y-105),(x+72,y-30),(x+48,y+90),(x-48,y+90),(x-72,y-30)]
    pts=" ".join(f"{a},{b}" for a,b in points)
    parts.append(f'<polygon points="{pts}" fill="{c}" stroke="#17211c" stroke-width="7"/>')
    parts.append(f'<path d="M{x},{y-105} L{x-48},{y+90} M{x},{y-105} L{x+48},{y+90} M{x-72},{y-30} L{x+72},{y-30}" stroke="#fff" stroke-width="4" opacity=".75"/>')
    parts.append(f'<text x="{x}" y="{y+145}" text-anchor="middle" font-family="DejaVu Sans" font-size="22" font-weight="700" fill="#17211c">{name}</text>')
parts.append('</svg>')
svg=OUTSVG/"crystal-tokens-a4.svg"; svg.write_text("\n".join(parts),encoding="utf-8")
cairosvg.svg2pdf(url=str(svg),write_to=str(OUTPDF/"crystal-tokens-a4.pdf"))
cairosvg.svg2png(url=str(svg),write_to=str(OUTPRE/"crystal-tokens-a4.png"),output_width=1200)
print(OUTPDF/"crystal-tokens-a4.pdf")
