# Simuleringsrapport v0.38

## Ändringen som testades

- Träna ger 2 energi.
- Bygg ger 2 Skydd att fördela mellan hjältar på platsen.
- Jordväktaren får fördela de 2 Skydden mellan valfria hjältar.
- Ljuset, skuggkortleken och Skuggmästaren är oförändrade.

## Resultat på Normal, 8 Ljus

| Strategi | v0.37 | v0.38 | Skillnad | Bygg | Träna |
|---|---:|---:|---:|---:|---:|
| aggressive | 44.2 % | 44.1 % | -0.0 pp | 0.3 % | 0.7 % |
| balanced | 27.3 % | 32.5 % | +5.2 pp | 16.1 % | 2.9 % |
| cautious | 18.5 % | 23.5 % | +5.0 pp | 20.6 % | 3.3 % |


## Tolkning

Detta är ett hypotesdrivet test av handlingsekonomin. Resultaten visar om starkare Träna och Bygg gör balanserat och försiktigt spel mer konkurrenskraftigt.

## Fysiskt test

Observera om:

- Bygg känns värt en hel tur.
- Skyddsfördelningen är lätt att förstå.
- Jordväktarens globala fördelning känns hjälpsam utan att bli administrativ.
- Träna väljs frivilligt.
