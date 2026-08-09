# Simuleringsrapport v0.37

## Ändringen som testades

Skuggkortleken innehåller nu:

- 2 × Ljuset falnar
- 2 × Bakhåll
- 1 × Vägen stängs
- 1 × Mörk dimma
- 1 × Skuggornas grepp
- 1 × En lugn stund

Den totala kortleken är fortfarande 8 kort. Inga andra spelregler ändrades.

## Resultat på Normal, 8 Ljus

| Strategi | v0.36 | v0.37 | Skillnad |
|---|---:|---:|---:|
| aggressive | 5.6 % | 44.2 % | +38.6 procentenheter |
| balanced | 1.3 % | 27.3 % | +26.0 procentenheter |
| cautious | 0.2 % | 18.5 % | +18.3 procentenheter |


## Tolkning

Minskningen från fyra till två direkta Ljusförluster är ett rent test av tidspressen. Resultaten är fortfarande hypoteser eftersom simulatorns beslutsregler inte är samma sak som mänskligt spel.

Observera särskilt:

- om vinstfrekvensen närmar sig projektets målintervall 45–70 %
- om balanserad och försiktig strategi kommer närmare aggressiv strategi
- om Utforska och Bygg används oftare utan att bli fällor
- om slutstriden mot Skuggmästaren oftare hinner spelas färdigt

## Rekommendation

Behåll v0.37-regeln som testvariant och kör ett fysiskt speltest med Normal 8 Ljus. Ändra inte fler regler innan ni har sett om Mörk dimma och Skuggornas grepp känns tydliga och roliga vid bordet.
