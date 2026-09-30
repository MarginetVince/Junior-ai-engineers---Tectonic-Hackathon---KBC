# AI-changelog

Door AI bijgehouden samenvatting van wijzigingen (nieuwste bovenaan).

## 2026-09-30 – Live animatie van acties in de demo-app
- Wat: `index.html` – bij het kiezen van een gebruiker verschijnen de acties één voor één (1 sec ertussen) met slide-in, icoon-pop, oplichtende rij, springende tellers en een "Live"-indicator; oudste actie fadet weg bij meer dan 5 (sliding window); analyseknop uitgeschakeld tijdens afspelen
- Waarom: de demo moet aanvoelen alsof het gedrag live binnenkomt

## 2026-09-30 – Actielijst in demo-app professioneler gemaakt
- Wat: `index.html` – "Recente activiteit"-kaart met tijdlijn, iconen, Nederlandse labels, telling per actie en "Nieuwste"-label; compactere layout; resultaat scrolt automatisch in beeld
- Waarom: de oude lijst met technische namen was niet mooi en niet duidelijk genoeg voor de demo

## 2026-09-30 – Proof of concept gedragsanalyse-API + demo-frontend
- Wat: `main.py` (FastAPI, endpoint `POST /api/v1/behaviour-analysis`, `Predictor`-interface met rule-based model, sliding window van 5), `index.html` (nagebootste KBC-app), `Dockerfile`, `README.md`
- Waarom: hackathon-demo voor de KBC-case; alles draait in één Docker-container

## 2026-09-30 – Basis .claude-setup
- Wat: `.claude/settings.json` (hooks), `.claude/hooks/log-activity.js`, `.claude/CLAUDE.md`, deze changelog
- Waarom: alles wat AI in de repo doet moet genoteerd worden in `.claude`
