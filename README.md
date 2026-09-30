# KBC Gedragsanalyse – Hackathon Proof of Concept

KBC kijkt naar **hoe** een klant de app gebruikt (openen, sluiten, refreshen). Een "AI-model" bekijkt telkens de **laatste 5 acties** en voorspelt in welke situatie de klant zit, zodat KBC op het juiste moment kan helpen, of niets doet als alles in orde is.

## Bestanden

| Bestand | Inhoud |
|---|---|
| `main.py` | De API, het "model" en de demodata |
| `index.html` | Nagebootste KBC-app voor de demo |
| `Dockerfile` | Alles draaien met één commando |

## Installeren en starten

Enkel **Docker Desktop** is nodig (Python hoeft niet geïnstalleerd te zijn).

```bash
docker build -t kbc-behaviour .
docker run --rm -p 8000:8000 kbc-behaviour
```

Open daarna:

- **Demo-app:** http://localhost:8000
- **API-documentatie (Swagger):** http://localhost:8000/docs

Stoppen: `Ctrl+C` in de terminal.

## De API

`POST /api/v1/behaviour-analysis` met body `{"user_uuid": "..."}`

**Regel van het huidige model:** 3 of meer keer `APP_REFRESHED` in de laatste 5 acties → `USER_STRESSED`, anders `USER_NEUTRAL`.

### Voorbeeld-requests

Met **Git Bash**:

```bash
curl -X POST http://localhost:8000/api/v1/behaviour-analysis -H "Content-Type: application/json" -d '{"user_uuid": "aaa-aaa-aaa-aaa"}'
```

Met **PowerShell**:

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/v1/behaviour-analysis -ContentType "application/json" -Body '{"user_uuid": "aaa-aaa-aaa-aaa"}'
```

Vervang `aaa-aaa-aaa-aaa` door `bbb-bbb-bbb-bbb` of `ccc-ccc-ccc-ccc` voor de andere gebruikers.

### Verwachte responses

**Gebruiker A** (`aaa-aaa-aaa-aaa`) → `200`
```json
{"user_uuid": "aaa-aaa-aaa-aaa", "analysed_actions": ["APP_OPENED", "APP_REFRESHED", "APP_OPENED", "APP_CLOSED"], "prediction": "USER_NEUTRAL", "reason": "1 keer refresh in de laatste 4 acties."}
```

**Gebruiker B** (`bbb-bbb-bbb-bbb`) → `200`
```json
{"user_uuid": "bbb-bbb-bbb-bbb", "analysed_actions": ["APP_OPENED", "APP_CLOSED", "APP_OPENED", "APP_CLOSED", "APP_OPENED"], "prediction": "USER_NEUTRAL", "reason": "0 keer refresh in de laatste 5 acties."}
```

**Gebruiker C** (`ccc-ccc-ccc-ccc`) → `200`
```json
{"user_uuid": "ccc-ccc-ccc-ccc", "analysed_actions": ["APP_OPENED", "APP_REFRESHED", "APP_REFRESHED", "APP_REFRESHED", "APP_REFRESHED"], "prediction": "USER_STRESSED", "reason": "4 keer refresh in de laatste 5 acties."}
```

**Onbekende gebruiker** → `404`
```json
{"error": {"code": "USER_NOT_FOUND", "message": "No user found with uuid 'zzz'."}}
```

**Ongeldige request** (geen JSON, `user_uuid` ontbreekt of is leeg) → `400`
```json
{"error": {"code": "INVALID_REQUEST", "message": "Body must be JSON like {\"user_uuid\": \"aaa-aaa-aaa-aaa\"}."}}
```

## Uitbreiden

- **Nieuwe actie of uitkomst:** voeg een waarde toe aan de enum `Action` of `Prediction` in `main.py`.
- **Echt AI-model:** schrijf een nieuwe klasse die `Predictor` implementeert en vervang de regel `predictor = RuleBasedPredictor()`. De API blijft hetzelfde.

## Voor de pitch: van demo naar 2,3 miljoen klanten

Vandaag beslist een eenvoudige regel. Maar het "model" zit achter één vaste aansluiting, dus we kunnen het later vervangen door een echt AI-model zonder dat de app, chatbot Kate of de advisor iets moeten veranderen. Dat model leert uit de gedragsdata die KBC vandaag al logt, en uit hoe klanten reageren op de hulp die ze krijgen. Zo wordt het elke dag slimmer. Omdat het model telkens maar naar de laatste paar acties van één klant kijkt, is elke voorspelling klein en snel, en kan het voor alle 2,3 miljoen klanten tegelijk draaien zonder manuele campagnes. Nieuwe situaties, zoals "wacht op zijn loon" of "vindt iets niet", voegen we stap voor stap toe.
