# Buildguide för spelbrädet

## Grundkommando

Kör från projektets rot:

```bash
python scripts/build_board_only.py
```

Hela projektet byggs med:

```bash
python scripts/build.py
```

## Input

Spelplansbygget använder:

```text
data/board/board.yaml
assets/backgrounds/board-background-standard.png
assets/backgrounds/board-background-ink-friendly.png
assets/board/light-track/light-track-overlay.svg
assets/icons/*.svg
```

`data/board/board.yaml` är sanningskälla för platser, vägar, etiketter och ljusspårets placering.

## Output

Generatorn skapar bland annat:

```text
output/svg/board-a4.svg
output/svg/board-a4-ink-friendly.svg
output/pdf/board-a4.pdf
output/pdf/board-a4-ink-friendly.pdf
output/preview/board-a4.png
output/preview/board-a4-ink-friendly.png
```

Filer i `output/` är genererade och ska inte versionsspåras.

## Princip

Bakgrundsbilderna innehåller illustration och pergamentyta. Spelmekaniskt innehåll läggs ovanpå från YAML/SVG-lager. Flytta därför platser och ljusindikator via `data/board/board.yaml`, inte genom att redigera färdig PDF eller PNG.
