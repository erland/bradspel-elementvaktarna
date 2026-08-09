# Buildarkitektur v1

## Princip

SVG är den enda visuella sanningskällan.

```text
YAML-data
    +
SVG-mallar
    +
grafiska assets
        ↓
scripts/build.py
        ↓
master-SVG
        ↓
PDF för utskrift
        ↓
PNG-preview från samma SVG
```

## Viktiga konsekvenser

- PDF och PNG byggs från exakt samma SVG.
- Det finns inte längre en separat Pillow-layout för preview.
- Ändringar görs i YAML, SVG-mallar eller assets.
- Filer i `output/` är genererade och ska inte handredigeras.

## Källor

```text
data/board/board.yaml
data/heroes/heroes.yaml
templates/board/board.svg
templates/heroes/hero-card.svg
assets/
scripts/build.py
```

## Output

```text
output/svg/board-a4.svg
output/svg/hero-cards-a4.svg

output/pdf/board-a4.pdf
output/pdf/hero-cards-a4.pdf

output/preview/board-a4.png
output/preview/hero-cards-a4.png
```

PDF är rekommenderat utskriftsformat. PNG är endast en snabb preview.

## Build

```bash
python scripts/build.py
```
