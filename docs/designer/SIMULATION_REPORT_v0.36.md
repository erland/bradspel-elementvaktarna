# Simuleringsrapport v0.36

## Sammanfattning

Det här är ett **hypotesdrivet simuleringspass**, inte ett facit på hur barn spelar. Simulatorn läser projektets karta, kortlekar, hjälteordning, energi, Skydd, hjälpkort, kristaller, platskrafter, kristallbelöningar, Ljuset och slutstriden mot Skuggmästaren.

Huvudresultatet är tydligt: **nuvarande startvärden 8/7/6 Ljus verkar mycket svåra** under samtliga testade beslutsstrategier.

På Normal med 8 Ljus vann:

- aggressiv strategi: **5.6 %**
- balanserad strategi: **1.3 %**
- försiktig strategi: **0.2 %**

Spelen slutade efter ungefär 3.36–3.66 rundor, oftast därför att Ljuset slocknade.

## Testupplägg

- 3 000 spel per strategi och svårighetsgrad
- 3 strategier: aggressiv, balanserad och försiktig
- 3 svårighetsgrader: 8, 7 och 6 Ljus
- totalt 27 000 huvudsimuleringar
- känslighetsanalys för 8–16 Ljus
- ablationstest där en hjälteförmåga, platskraft eller kristallbelöning stängdes av
- slumpfrö och regler finns i `data/simulation/pass-v0.36.yaml`
- simulatorn finns i `scripts/simulate_game.py`

## Resultat per strategi

| Strategi | Ljus | Vinst | Rundor | Utforska | Bygg | Träna |
|---|---:|---:|---:|---:|---:|---:|
| aggressive / normal | 8 | 5.6 % | 3.36 | 11.6 % | 0.2 % | 0.5 % |
| aggressive / hard | 7 | 3.1 % | 3.05 | 12.4 % | 0.1 % | 0.4 % |
| aggressive / very_hard | 6 | 0.7 % | 2.72 | 12.9 % | 0.1 % | 0.5 % |
| balanced / normal | 8 | 1.3 % | 3.57 | 17.3 % | 26.5 % | 4.3 % |
| balanced / hard | 7 | 0.1 % | 3.21 | 15.8 % | 28.1 % | 4.3 % |
| balanced / very_hard | 6 | 0.0 % | 2.82 | 13.9 % | 30.2 % | 4.5 % |
| cautious / normal | 8 | 0.2 % | 3.66 | 20.7 % | 34.4 % | 3.0 % |
| cautious / hard | 7 | 0.0 % | 3.27 | 20.2 % | 36.2 % | 3.1 % |
| cautious / very_hard | 6 | 0.0 % | 2.84 | 20.7 % | 37.9 % | 3.3 % |

## Varför spelet blir så svårt

Skuggkortleken innehåller fyra exemplar av **Ljuset falnar** av totalt åtta kort. Eftersom ett skuggkort dras efter varje hjältes tur blir det fyra skuggkort per hel runda.

Det betyder i genomsnitt ungefär två förlorade Ljus per runda enbart från skuggkortleken. Därtill kommer **Mörk viskning** och misslyckade anfall mot Skuggmästaren.

Med 8 Ljus har gruppen därför ofta bara omkring fyra rundor innan Ljuset slocknar. Simulatorn hinner vanligtvis samla nästan alla kristaller, men slutstriden blir för kort eller påbörjas för sent.

## Känslighetsanalys

När endast startvärdet för Ljuset ändrades nådde aggressiv strategi ungefär målområdet vid **13 Ljus** med 54.5 % vinst.

Balanserad strategi nådde ungefär målområdet vid **15 Ljus** med 53.6 % vinst.

Det betyder inte att spelbrädet bör utökas direkt till 15–16. Det visar snarare att den nuvarande kombinationen av:

- fyra skuggkort per runda
- 50 % chans att ett skuggkort kostar Ljus
- ytterligare Ljusförlust från äventyr och Skuggmästaren

skapar mycket hög tidspress.

## Handlingarnas relevans

Den aggressiva strategin var klart bäst, trots att den Utforskade mindre än projektets målintervall. Balanserad och försiktig strategi använde Bygg ofta, men förlorade tid och vann mer sällan.

Det tyder på en möjlig konflikt:

- Skydd är användbart mot energiförlust.
- Skydd kan inte skydda Ljuset.
- Varje Bygg-handling förlänger spelet och utlöser ännu ett skuggkort.

I nuvarande modell blir **Bygg därför ofta en fälla**, särskilt när Ljuset är den vanligaste förlustorsaken.

Träna användes sällan. Det beror på att hjältar som når 0 energi automatiskt återvänder till Träningsgården med 2 energi, vilket gör frivillig återhämtning mindre attraktiv under stark tidspress.

## Elementens relevans

Ablationstesten på 8 Ljus gav ett golvproblem: nästan alla spel förlorades, så små skillnader gick inte att tolka. Därför kördes ett separat relevanstest med 15 Ljus och balanserad strategi, där grundvinsten var 53,4 %.

Tydligast påverkan när funktionen stängdes av:

- `hero:fire_guardian`: vinstfrekvensen ändrades med -6.0 procentenheter.
- `hero:wind_guardian`: vinstfrekvensen ändrades med -3.7 procentenheter.
- `reward:water_crystal`: vinstfrekvensen ändrades med -3.1 procentenheter.

Eldväktarens stridsförmåga och Vindväktarens rörelseförmåga hade tydlig positiv betydelse. Vattenkristallens gruppenergi hade också märkbar betydelse.

Flera andra effekter låg nära noll eller gav små motstridiga utslag. Det betyder inte säkert att de är irrelevanta. Det kan bero på simulatorns beslutsregler, att effekten aktiveras sällan eller att andra system kompenserar för den.

Särskilt värda att observera i fysiska speltest:

- Jordväktarens extra Skydd
- Jordskogens skydd mot energiförlust
- Eldbrons platskraft
- Vattengrottans platskraft
- Eld- och Vindkristallens engångsbelöningar

## Balanshypoteser

### Hypotes 1: Ljusförlusten är för snabb

Starkaste indikationen. Normal på 8 Ljus gav 1–6 % vinst beroende på strategi.

### Hypotes 2: Bygg konkurrerar dåligt med tidspressen

Bygg skyddar energi men inte Ljus. En Bygg-handling följs ändå av ett skuggkort, vilket gör att försiktigt spel straffas.

### Hypotes 3: Spelet premierar rak kapplöpning

Aggressiv strategi vann tydligt oftare än balanserad och försiktig strategi. Det minskar värdet av Utforska, Träna och Bygg.

### Hypotes 4: Några elementeffekter märks för lite

Eld- och Vindväktarna gav tydlig simulerad effekt. Flera platskrafter och Jordväktarens förmåga gav små utslag och behöver observeras vid bordet.

## Rekommenderat nästa test

Ändra inte flera saker samtidigt. Testa först en av följande små varianter:

1. Dra ett skuggkort efter **varannan hjältes tur** i stället för efter varje.
2. Behåll fyra skuggkort per runda men minska **Ljuset falnar** från fyra till två kort.
3. Låt gruppen börja med 8 Ljus men förlora Ljus först när två Ljus-symboler har dragits under samma runda.

Min första rekommendation är alternativ 2. Det behåller turstrukturen men sänker den genomsnittliga Ljusförlusten från skuggkort från cirka två till cirka ett per runda.

Kör därefter samma simulator igen och jämför vinstfrekvens, rundor, Utforska-andel och användning av Bygg.

## Begränsningar

- Simulatorn representerar beslutsregler, inte barns faktiska beteende.
- Alla fyra hjältar används alltid; 2–4 spelare ger därför samma mekaniska simulering. Spelarantal påverkar fortfarande samarbete, förståelse och väntetid i verkligheten.
- Kortval och resursfördelning är automatiserade approximationer.
- Ett litet eller negativt ablationsresultat är inte bevis på att en komponent saknar värde.
- Rolighet, dramatik och begriplighet måste testas med människor.
