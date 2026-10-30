"""Men's college basketball pull. ESPN scoreboard → merge into slate.json

  python pull_cbb.py

Keeps CFB / NFL / racing. Replaces cbb only.
Does not stamp Ticket. Does not scrape DirecTV.
A miss here must not fail the football job.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone

from pull_week import ET, SLATE_PATH, get, load_old, load_team_ids, parse_event

DAYS = 9
BASE = "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard"


def scoreboard(ymd: str) -> dict:
    return get(f"{BASE}?dates={ymd}&groups=50&limit=300")


def load_slate() -> dict:
    if not SLATE_PATH.exists():
        return {"note": "cbb", "games": []}
    try:
        return json.loads(SLATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"note": "cbb", "games": []}


def main() -> int:
    index = load_team_ids()
    known = set(index.values())
    today = datetime.now(timezone.utc).astimezone(ET).date()
    seen: set[str] = set()
    cbb: list[dict] = []

    for offset in range(DAYS):
        day = today + timedelta(days=offset)
        data = scoreboard(day.strftime("%Y%m%d"))
        for event in data.get("events") or []:
            row = parse_event(event, "cbb", index)
            if not row or row["id"] in seen:
                continue
            if row["away"] not in known and row["home"] not in known:
                continue
            seen.add(row["id"])
            cbb.append(row)

    keep = [g for g in load_old() if g.get("league") != "cbb"]
    games = keep + cbb
    games.sort(key=lambda g: (g["date"], g["et"], g.get("away") or g.get("name") or ""))

    slate = load_slate()
    slate["games"] = games
    slate["cbbPulled"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    SLATE_PATH.write_text(json.dumps(slate, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {len(cbb)} CBB (kept {len(keep)} other) to {SLATE_PATH}")
    for g in cbb:
        print(f"  {g['date']} {g['et']} {g['away']} @ {g['home']} {g['network']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
