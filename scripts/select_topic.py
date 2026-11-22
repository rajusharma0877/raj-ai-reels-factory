#!/usr/bin/env python3
"""Choose a topic for each daily slot; manual topic overrides take priority."""
from datetime import datetime, timezone, timedelta
import os
import re

IST = timezone(timedelta(hours=5, minutes=30))
now = datetime.now(IST)
slot = os.getenv("INPUT_SLOT", "").strip()
if not slot:
    slot = "midday" if os.getenv("SCHEDULE", "") == "30 7 * * *" else "evening"

topics = [
    "When silence starts feeling personal",
    "The psychology of waiting for one reply",
    "Why distance makes small moments matter",
    "When overthinking replaces honest communication",
    "The quiet fear of becoming easy to forget",
    "Why emotional consistency feels safer than grand gestures",
    "How missing someone changes your daily routine",
    "The difference between needing space and withdrawing",
    "Why unanswered messages can feel so loud",
    "How trust survives across miles",
    "The psychology behind mixed signals",
    "Why people hide sadness behind being busy",
    "When memories become part of your routine",
    "How reassurance builds long-distance trust",
    "Why emotional availability matters",
    "The fear of caring more than the other person",
    "How to stay connected without constant texting",
    "Why familiar patterns are hard to break",
    "When love feels like waiting",
    "The power of small promises kept",
    "Why distance tests communication, not just love",
    "How the mind fills gaps in a conversation",
    "When you miss the little everyday things",
    "Why calm communication beats emotional guessing",
    "How two people can feel close from far away",
    "The psychology of emotional safety",
    "When you stop asking for the bare minimum",
    "Why being remembered matters",
    "How patience and effort work together",
    "Why clarity is kinder than mixed signals",
]
day_index = now.timetuple().tm_yday - 1
index = (day_index * 2 + (0 if slot == "midday" else 1)) % len(topics)
topic = os.getenv("INPUT_TOPIC", "").strip() or topics[index]
title = " ".join(re.sub(r"[^A-Za-z0-9 ]+", "", topic).split())[:58]
print(f"topic={topic}")
print(f"title={title}")
print(f"slot={slot}")
