"""Sunday Phoenix locals. TV Passport FOX 10 / CBS 5 -> phx: local

  python stamp_phx_locals.py
  python stamp_phx_locals.py --date 2026-09-20

Does not touch Ticket numbers. Does not scrape DirecTV.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.error import HTTPError
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
SLATE_PATH = ROOT / "src" / "data" / "slate.json"
TEAMS_PATH = ROOT / "src" / "data" / "teams.js"
PHX = ZoneInfo("America/Phoenix")
UA = {"User-Agent": "Mozilla/5.0"}

STATIONS = (
    ("CBS 5", "https://www.tvpassport.com/tv-listings/stations/cbs-kpho-phoenix-az/1179"),
    ("FOX 10", "https://www.tvpassport.com/tv-listings/stations/fox-ksaz-phoenix-az/6331"),
)

CITY_ALIASES = {
    "new england": "patriots",
    "new england patriots": "patriots",
    "new york jets": "jets",
    "ny jets": "jets",
    "new york giants": "giants",
    "ny giants": "giants",
    "los angeles chargers": "chargers",
    "la chargers": "chargers",
    "los angeles rams": "rams",
    "la rams": "rams",
    "las vegas": "raiders",
    "las vegas raiders": "raiders",
    "tampa bay": "buccaneers",
    "tampa bay buccaneers": "buccaneers",
    "green bay": "packers",
    "green bay packers": "packers",
    "kansas city": "chiefs",
    "kansas city chiefs": "chiefs",
    "san francisco": "49ers",
    "san francisco 49ers": "49ers",
    "san fran": "49ers",
    "niners": "49ers",
    "washington": "commanders",
    "washington commanders": "commanders",
    "arizona": "cardinals",
    "arizona cardinals": "cardinals",
}


def get(url: str) -> str:
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=45) as resp:
                return resp.read().decode("utf-8", "replace")
        except HTTPError as err:
            last = err
            if err.code in (403, 429, 500, 502, 503) and attempt < 3:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise
    raise last


def next_sunday(today: date) -> date:
    if today.weekday() == 6:
        return today
    return today + timedelta(days=(6 - today.weekday()) % 7)


def load_nfl_aliases() -> list[tuple[str, str]]:
    text = TEAMS_PATH.read_text(encoding="utf-8")
    aliases: dict[str, str] = {}
    for mid, name, league in re.findall(
        r'id:\s*"([^"]+)",\s*name:\s*"([^"]+)"[^}]*league:\s*"(nfl|cfb)"',
        text,
    ):
        if league != "nfl":
            continue
        aliases[name.lower()] = mid
        aliases[mid.replace("-", " ")] = mid
    aliases.update(CITY_ALIASES)
    return sorted(aliases.items(), key=lambda kv: len(kv[0]), reverse=True)


def teams_in_title(title: str, aliases: list[tuple[str, str]]) -> list[str]:
    blob = f" {re.sub(r'[^a-z0-9]+', ' ', title.lower())} "
    found: list[str] = []
    used: set[str] = set()
    for alias, tid in aliases:
        token = f" {alias} "
        if token in blob and tid not in used:
            found.append(tid)
            used.add(tid)
            blob = blob.replace(token, " ")
    return found


def nfl_titles(html: str) -> list[str]:
    titles: list[str] = []
    for tag in re.findall(r"<[^>]+data-showName=\"NFL Football\"[^>]*>", html):
        ep = re.search(r'data-episodeTitle="([^"]+)"', tag)
        show = re.search(r'data-showTitle="([^"]+)"', tag)
        raw = (ep.group(1) if ep else "") or (show.group(1) if show else "")
        raw = raw.replace("NFL Football - ", "").replace("NFL Football", "").strip()
        if raw:
            titles.append(raw)
    if titles:
        return titles
    for m in re.finditer(r"NFL Football\s+([A-Za-z0-9 .'\-]+?\s+(?:at|vs\.?)\s+[A-Za-z0-9 .'\-]+)", html):
        titles.append(m.group(1).strip())
    return titles


def match_game(ids: list[str], games: list[dict], sunday: date) -> dict | None:
    if len(ids) < 2:
        return None
    pair = {ids[0], ids[1]}
    day = sunday.isoformat()
    hits = [
        g
        for g in games
        if g.get("league") == "nfl"
        and {g.get("away"), g.get("home")} == pair
        and g.get("date") == day
    ]
    if not hits:
        hits = [
            g
            for g in games
            if g.get("league") == "nfl" and {g.get("away"), g.get("home")} == pair
        ]
    return hits[0] if len(hits) == 1 else None


def main() -> int:
    today = datetime.now(PHX).date()
    p = argparse.ArgumentParser(description="Stamp Phoenix FOX 10 / CBS 5 locals")
    p.add_argument("--date", help="YYYY-MM-DD Sunday to stamp")
    args = p.parse_args()
    sunday = date.fromisoformat(args.date) if args.date else next_sunday(today)

    slate = json.loads(SLATE_PATH.read_text(encoding="utf-8"))
    games = slate.get("games") or []
    aliases = load_nfl_aliases()
    stamped: list[str] = []
    missed: list[str] = []

    for label, base in STATIONS:
        html = get(f"{base}/{sunday.isoformat()}")
        titles = nfl_titles(html)
        print(f"{label} {sunday}: {len(titles)} NFL listing(s)")
        if not titles:
            print(f"  (none yet)")
            continue
        for title in titles:
            ids = teams_in_title(title, aliases)
            game = match_game(ids, games, sunday)
            if not game:
                missed.append(f"{label}: {title} -> {ids or 'no teams'}")
                print(f"  skip {title} ({', '.join(ids) or 'unmapped'})")
                continue
            if game.get("phx") != "local":
                game["phx"] = "local"
            stamped.append(f"{game['id']} ({label})")
            print(f"  local {game['id']}  {title}")

    if stamped:
        SLATE_PATH.write_text(json.dumps(slate, indent=2) + "\n", encoding="utf-8")
        print("Stamped: " + "; ".join(stamped))
    else:
        print("No Phoenix locals stamped.")
    for row in missed:
        print("Unmatched: " + row)
    return 0


if __name__ == "__main__":
    sys.exit(main())
