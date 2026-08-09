# Komponentarkitektur

Projektet är nu uppdelat per komponenttyp.

```text
data/
  board/board.yaml
  heroes/heroes.yaml

scripts/
  generate_board.py
  generate_heroes.py

output/
  board/
  heroes/
```

Varje komponent följer samma kedja:

```text
YAML-data → generator → SVG → preview/print
```

## Principer

- YAML är sanningskälla.
- SVG och PNG i `output/` är genererade filer.
- Bakgrunder och ikoner ligger i `assets/`.
- Layoutregler kan senare flyttas till `templates/`.
