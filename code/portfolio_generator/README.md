# Portfolio Generator

Dit project is een Python script dat een portfolio website genereert op basis van een LaTeX CV. Het extraheert informatie uit het LaTeX bestand en genereert een moderne, responsieve website.

## Functionaliteit

- Extraheert persoonlijke informatie uit een LaTeX CV
- Genereert een moderne, responsieve website met:
  - Persoonlijke informatie en foto
  - Vaardigheden
  - Werkervaring
  - Projecten
  - Documenten (CV, scripties, etc.)
- Ondersteunt LaTeX wiskundige notatie via KaTeX
- Kopieert automatisch benodigde assets (foto's, PDF's)

## Vereisten

- Python 3.x
- LaTeX CV met specifieke commando's:
  - `\name{...}`
  - `\email{...}`
  - `\phone{...}`
  - `\printinfo{\faHouseUser}{...}`
  - `\photoL{...}{...}`
  - `\cvsection{Strengths}`
  - `\cvtag{...}`
  - `\experience{...}{...}{...}{...}{...}{...}`
  - `\cvevent{...}{...}{...}{...}`

## Gebruik

1. Zorg dat uw LaTeX CV de juiste commando's gebruikt
2. Plaats uw foto in de `latex` map
3. Plaats uw PDF documenten in de `Docs` map
4. Voer het script uit:
   ```bash
   python generate_site.py
   ```
5. De gegenereerde website staat in de `public` map

## Toekomstige Verbeteringen

- [ ] Betere foutafhandeling
- [ ] Meer configuratie-opties
- [ ] Ondersteuning voor meer LaTeX commando's
- [ ] Verbeterde styling opties
- [ ] Automatische tests
- [ ] Logging systeem 