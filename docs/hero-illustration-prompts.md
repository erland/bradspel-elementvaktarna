# Illustrationsprompter för hjältekort

## Syfte

Prompterna skapar fyra breda 16:9-illustrationer utan text eller kortram, avsedda för hjältekortens bildruta.

## Gemensam standard

- Minst 1600 × 900 px
- Hela huvudet synligt
- Figuren något under bildens vertikala mitt
- Luft ovanför håret och på båda sidor
- Tydlig elementkraft
- Ingen text, logotyp, vattenstämpel eller kortram
- Egen fantasyidentitet utan likhet med etablerade varumärken

## Eldväktaren

```text
Wide 16:9 fantasy adventure illustration for a children's board game. A brave young fire guardian in red and gold armor stands in a confident action pose, shown from knees up with the entire head and hair clearly visible. One hand controls a bright spiral of flame, the other holds a glowing short sword. Warm volcanic landscape and glowing embers in the background, but the hero remains the clear focal point. Friendly determined expression, colorful cinematic lighting, polished animated fantasy style, crisp silhouette, professional board game card art, original character design. No text, no logo, no card border, no watermark, no cropped head, no existing franchise resemblance.
```

## Vattenväktaren

```text
Wide 16:9 fantasy adventure illustration for a children's board game. A calm young water guardian in blue, white and silver armor stands in a graceful action pose, shown from knees up with the entire head clearly visible. One hand shapes a sweeping ribbon of water while the other holds an elegant staff with a blue crystal. Waterfalls, mist and a luminous river form the background, kept softer than the hero. Wise and friendly expression, colorful cinematic lighting, polished animated fantasy style, crisp silhouette, professional board game card art, original character design. No text, no logo, no card border, no watermark, no cropped head, no existing franchise resemblance.
```

## Vindväktaren

```text
Wide 16:9 fantasy adventure illustration for a children's board game. A fast young wind guardian in turquoise, white and dark teal clothing leaps through the air in a dynamic pose, shown from knees up with the entire head clearly visible. Spiraling streams of wind circle the arms and flowing scarf, with floating leaves and distant mountain peaks in the background. Energetic but friendly expression, colorful cinematic lighting, polished animated fantasy style, crisp silhouette, professional board game card art, original character design. No text, no logo, no card border, no watermark, no cropped head, no existing franchise resemblance.
```

## Jordväktaren

```text
Wide 16:9 fantasy adventure illustration for a children's board game. A strong young earth guardian in green, brown and bronze armor stands in a protective stance, shown from knees up with the entire head clearly visible. One arm carries a large stone shield marked with a glowing original rune, while rocks, roots and small crystals rise from the ground around the hero. Forest cliffs and ancient stones in the background, kept softer than the hero. Warm confident expression, colorful cinematic lighting, polished animated fantasy style, crisp silhouette, professional board game card art, original character design. No text, no logo, no card border, no watermark, no cropped head, no existing franchise resemblance.
```

## Målfilnamn

```text
assets/heroes/fire_guardian_wide.png
assets/heroes/water_guardian_wide.png
assets/heroes/wind_guardian_wide.png
assets/heroes/earth_guardian_wide.png
```

## Efter generering

1. Spara bilderna med exakt filnamn ovan.
2. Lägg dem i `assets/heroes/`.
3. Uppdatera `data/heroes/heroes.yaml` till `_wide.png`-filerna.
4. Kör `python scripts/build.py`.
5. Kontrollera `output/pdf/hero-cards-a4.pdf`.
