#!/usr/bin/env python3
"""Create the upstream generator's documented input/scripts/input-scripts.json."""
import json, os, re
from pathlib import Path

topic = os.environ["TOPIC"].strip()
title = os.environ["TITLE"].strip()
script = (
    f"{topic}. [Visual: cinematic long distance relationship, emotional close up]\n"
    "Sometimes the hardest part is not the miles. It is the silence between two messages. [Visual: person looking at phone at night, cinematic film still]\n"
    "Your mind starts filling every quiet moment with questions. [Visual: rainy window, lonely city lights, moody cinematic]\n"
    "But healthy love is not measured by constant texting. It is built through honesty, reassurance, and consistent effort. [Visual: two people video calling, warm cinematic lighting]\n"
    "Distance can test communication. It does not have to decide the strength of a connection. [Visual: sunrise horizon, hopeful cinematic wide shot]"
)
payload = [{
    "id": "raju-daily-reel",
    "title": title,
    "script": script,
    "orientation": "portrait",
    "voice": "en-US-JennyNeural",
    "showText": True,
    "language": "english"
}]
out = Path("engine/input/scripts/input-scripts.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {out}")
