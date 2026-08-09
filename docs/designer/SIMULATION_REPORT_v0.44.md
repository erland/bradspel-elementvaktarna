# Simuleringsrapport v0.44

## Syfte

Verifiera att regelharmoniseringen i v0.44 reproducerar den etablerade balansen från v0.41/v0.42. Ingen spelmekanisk ändring avsågs.

## Konfiguration

- Konfiguration: `data/simulation/pass-v0.44.yaml`
- Seed: 36001
- 3 000 spel per strategi och svårighetsgrad
- 1 500 spel per ablationstest
- Strategier: aggressiv, balanserad, försiktig
- Svårigheter: Normal 8 Ljus, Svår 7 Ljus, Mycket svår 6 Ljus

## Resultat

| Strategi | Normal | Svår | Mycket svår | Rundor Normal |
|---|---:|---:|---:|---:|
| Aggressiv | 48,9 % | 37,3 % | 22,6 % | 4,60 |
| Balanserad | 56,9 % | 43,2 % | 29,1 % | 5,17 |
| Försiktig | 51,3 % | 36,6 % | 24,6 % | 5,66 |

## Bedömning

Resultaten matchar tidigare verifiering. v0.44-harmoniseringen har därför inte ändrat simulatorns balansutfall. Den balanserade strategin är fortsatt mest lönsam på samtliga svårighetsgrader.

Simuleringarna är hypoteser om mekanisk balans och ersätter inte fysiska speltester.
