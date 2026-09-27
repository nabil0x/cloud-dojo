# Spaced Review — how to keep it

Import `flashcards/cloud-dojo.csv` into Anki (File > Import, tab-separated),
or read it raw. Rebuild any time the glossary changes:

```bash
python3 shared/build_flashcards.py
```

## Schedule
- **Daily (5 min):** clear the Anki due queue before new quests.
- **Per boss fight:** review that phase's terms (search the deck by phase group).
- **Pre-capstone:** full-deck pass; anything you miss twice goes back into its STUDY.md.

The deck mirrors `GLOSSARY.md` one-to-one: fix a card by fixing the glossary line, then rebuild.
