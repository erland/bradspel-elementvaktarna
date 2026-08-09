# Kortsystem v0.17

## Kortlekar

### Äventyrskort - 12 kort

- 3 Kristallens sken
- 3 Skuggvakt
- 2 Kraftkälla
- 1 Hemlig passage
- 1 Hjälpande hand
- 1 Rasande stenar
- 1 Mörk viskning

### Skuggkort - 8 kort

- 4 Mörkret växer
- 2 Bakhåll
- 1 Vägen stängs
- 1 En lugn stund

## Struktur

```text
data/cards/adventure.yaml
data/cards/shadow.yaml
templates/cards/card.svg
assets/icons/cards/
scripts/build_cards.py
```

## Build

```bash
python scripts/build.py
```

## Output

```text
output/pdf/adventure-cards-a4.pdf
output/pdf/shadow-cards-a4.pdf
output/svg/cards/
output/preview/adventure-cards-a4.png
output/preview/shadow-cards-a4.png
```

PDF är rekommenderat utskriftsformat. Äventyrsleken använder två A4-sidor och skuggleken en A4-sida.


## Automatisk rubrikskalning

Kortnamn renderas i 21 pt när de ryms i rubrikfältet. Generatorn minskar stegvis storleken ned till 14 pt utifrån faktisk textbredd, så att längre namn behålls på en rad inom säkerhetszonen.
