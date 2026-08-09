# Simuleringsrapport v0.40

## Ändringen som testades

**Kraftkälla:** välj att få 1 energi eller återfå 1 Ljus, upp till spelets startvärde.

Inga andra spelregler ändrades.

## Resultat på Normal, 8 Ljus

| Strategi | v0.39 | v0.40 | Skillnad | Utforska |
|---|---:|---:|---:|---:|
| aggressive | 42.3 % | 42.4 % | +0.1 pp | 14.3 % |
| balanced | 30.2 % | 37.5 % | +7.4 pp | 15.8 % |
| cautious | 20.5 % | 33.0 % | +12.5 pp | 28.0 % |


## Tolkning

Detta är ett kontrollerat test av om Utforska kan köpa tillbaka tid utan att återinföra sparade kort eller extra administration.

Simulatorn låter:

- aggressiv strategi välja Ljus främst i akut läge
- balanserad strategi välja Ljus när tidspressen blivit tydlig
- försiktig strategi prioritera återställt Ljus oftare

Resultaten är balanshypoteser och bör följas upp med fysiskt speltest.
