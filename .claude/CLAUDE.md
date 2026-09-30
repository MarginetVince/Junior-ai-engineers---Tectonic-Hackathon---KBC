# Projectinstructies voor AI

Project: Junior AI Engineers – Tectonic Hackathon (KBC)

## Logging van AI-werk
- Alle prompts, bestandswijzigingen en uitgevoerde commando's worden **automatisch** gelogd in
  `.claude/logs/ai-activity.md` via een hook (zie `.claude/settings.json`). Pas die log niet handmatig aan.
- Houd daarnaast bij elke betekenisvolle wijziging een korte, menselijke samenvatting bij in
  `.claude/CHANGELOG-AI.md` (nieuwste bovenaan), in dit formaat:

  ```
  ## YYYY-MM-DD – korte titel
  - Wat: wat er veranderd is (bestanden/features)
  - Waarom: reden of vraag van de gebruiker
  ```
