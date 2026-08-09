# Buildguide för spelbrädet

## Grundkommando

Kör från projektets rot:

```bash
python scripts/generate_board.py
```

## Input

Generatorn läser:

```text
data/board.yaml
assets/backgrounds/board-background-v0.2.png
assets/icons/*.svg
```

## Output

Generatorn skapar:

```text
output/board/board-overlay-v0.2.svg
output/board/board-preview-v0.2.png
```

## Hur filerna kombineras

`board-overlay-v0.2.svg` är transparent och innehåller endast spelinformation.

`board-preview-v0.2.png` byggs så här:

```text
board-background-v0.2.png
        +
board-overlay-v0.2.svg
        =
board-preview-v0.2.png
```

För framtida builds kan overlayn delas upp i flera filer:

```text
output/board/layers/paths.svg
output/board/layers/nodes.svg
output/board/layers/labels.svg
output/board/layers/icons.svg
output/board/layers/darkness-track.svg
```

och sedan sättas ihop till:

```text
output/board/board-overlay.svg
```

## Viktig princip

Bakgrundsbilden ska inte behöva genereras om när:

- en plats flyttas
- en väg ändras
- en textruta flyttas
- en ikon byts
- mörkerspåret ändras

Dessa ändringar ska komma från `data/board.yaml` och overlay-lagren.
