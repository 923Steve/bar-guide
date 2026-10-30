"""NHL pull. ESPN scoreboard → merge into slate.json

  python pull_nhl.py

Keeps CFB / NFL / CBB / racing. Replaces nhl only.
Does not invent RSN numbers. Does not scrape DirecTV.
A miss here must not fail the football job.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone

from pull_week import ET, SLATE_PATH, get, load_old, load_team_ids, parse_event

DAYS = 8
BASE = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard"


def scoreboard(ymd: str) -> dict:
    return get(f"{BASE}?dates={ymd}&limit=50")


def load_slate() -> dict:
    if not SLATE_PATH.exists():
        return {"note": "nhl", "games": []}
    try:
        return json.loads(SLATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"note": "nhl", "games": []}


def main() -> int:
    index = load_team_ids()
    today = datetime.now(timezone.utc).astimezone(ET).date()
    seen: set[str] = set()
    nhl: list[dict] = []

    for offset in range(DAYS):
        day = today + timedelta(days=offset)
        data = scoreboard(day.strftime("%Y%m%d"))
        for event in data.get("events") or []:
            row = parse_event(event, "nhl", index)
            if not row or row["id"] in seen:
                continue
            seen.add(row["id"])
            nhl.append(row)

    keep = [g for g in load_old() if g.get("league") != "nhl"]
    games = keep + nhl
    games.sort(key=lambda g: (g["date"], g["et"], g.get("away") or g.get("name") or ""))

    slate = load_slate()
    slate["games"] = games
    slate["nhlPulled"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    SLATE_PATH.write_text(json.dumps(slate, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {len(nhl)} NHL (kept {len(keep)} other) to {SLATE_PATH}")
    for g in nhl:
        print(f"  {g['date']} {g['et']} {g['away']} @ {g['home']} {g['network']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
