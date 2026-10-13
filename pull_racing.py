"""NASCAR + F1 pull. ESPN scoreboard → merge into slate.json

  python pull_racing.py

Keeps CFB / NFL rows. Replaces nascar + f1 only.
Does not stamp Ticket. Does not scrape DirecTV.

ESPN racing scoreboard often stays on last weekend after the checkered
flag. Skip finished events and, when the default board is stale, ask
for the next date on the league calendar.
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
SLATE_PATH = ROOT / "src" / "data" / "slate.json"
ET = ZoneInfo("America/New_York")
UA = {
    "User-Agent": "bar-guide/1.0 (+https://923steve.github.io/bar-guide/)",
    "Accept": "application/json",
}

NET_MAP = {
    "FOX": "FOX",
    "FS1": "FS1",
    "FS2": "FS2",
    "NBC": "NBC",
    "USA": "USA",
    "USA NET": "USA",
    "USA NETWORK": "USA",
    "CW": "CW",
    "THE CW": "CW",
    "ESPN": "ESPN",
    "ESPN2": "ESPN2",
    "ABC": "ABC",
    "HBO MAX": "HBO Max",
    "APPLE TV": "Apple TV",
    "PRIME": "Prime",
    "PRIME VIDEO": "Prime",
}

NASCAR = (
    ("nascar-truck", "nascar", "truck"),
    ("nascar-secondary", "nascar", "oreilly"),
    ("nascar-premier", "nascar", "cup"),
)

# Skip practice. Keep the sessions a bartender will get asked about.
F1_KEEP = {
    "Qual": "quali",
    "SS": "shootout",
    "SR": "sprint",
    "Race": "race",
}

NASCAR_PREFIX = (
    "NASCAR O'Reilly Auto Parts Series at ",
    "NASCAR Truck Series at ",
    "NASCAR Cup Series at ",
    "NASCAR O'Reilly Auto Parts Series ",
    "NASCAR Truck Series ",
    "NASCAR Cup Series ",
)


def get(url: str) -> dict:
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=45) as resp:
                return json.load(resp)
        except HTTPError as err:
            last = err
            if err.code in (403, 429, 500, 502, 503) and attempt < 3:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise
    raise last


def scoreboard(slug: str, dates: str | None = None) -> dict:
    url = f"https://site.api.espn.com/apis/site/v2/sports/racing/{slug}/scoreboard"
    if dates:
        url += f"?dates={dates}"
    return get(url)


def event_state(event: dict) -> str:
    comps = event.get("competitions") or []
    if not comps:
        return ""
    states = []
    for c in comps:
        st = str(((c.get("status") or {}).get("type") or {}).get("state") or "").lower()
        if st:
            states.append(st)
    if "in" in states:
        return "in"
    if "pre" in states:
        return "pre"
    return states[0] if states else ""


def event_iso(event: dict) -> str:
    return event.get("date") or ((event.get("competitions") or [{}])[0].get("date")) or ""


def keep_event(event: dict, today_et: str) -> bool:
    state = event_state(event)
    if state in {"pre", "in"}:
        return True
    iso = event_iso(event)
    if not iso:
        return False
    return et_parts(iso)[0] == today_et


def date_candidates(item: dict) -> list[str]:
    seen: list[str] = []
    hit: set[str] = set()
    for key in ("startDate", "endDate"):
        raw = item.get(key)
        if not raw:
            continue
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        for ymd in (
            dt.strftime("%Y%m%d"),
            dt.astimezone(ET).strftime("%Y%m%d"),
            (dt - timedelta(days=1)).strftime("%Y%m%d"),
        ):
            if ymd not in hit:
                hit.add(ymd)
                seen.append(ymd)
    return seen


def next_events(slug: str) -> list[dict]:
    data = scoreboard(slug)
    today_et = datetime.now(ET).strftime("%Y-%m-%d")
    keep = [e for e in (data.get("events") or []) if keep_event(e, today_et)]
    if keep:
        return keep

    now = datetime.now(timezone.utc)
    cal = (data.get("leagues") or [{}])[0].get("calendar") or []
    tried: set[str] = set()
    for item in cal:
        end_raw = item.get("endDate") or item.get("startDate")
        if not end_raw:
            continue
        end = datetime.fromisoformat(end_raw.replace("Z", "+00:00"))
        if end < now:
            continue
        for ymd in date_candidates(item):
            if ymd in tried:
                continue
            tried.add(ymd)
            nxt = scoreboard(slug, ymd)
            found = [e for e in (nxt.get("events") or []) if keep_event(e, today_et)]
            if found:
                return found
    return []


def norm_net(raw: str) -> str:
    key = re.sub(r"\s+", " ", (raw or "").strip()).upper()
    if not key:
        return "TBD"
    first = key.split("/")[0].strip()
    return NET_MAP.get(key, NET_MAP.get(first, raw.strip().split("/")[0].strip() or "TBD"))


def et_parts(iso: str) -> tuple[str, str]:
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(ET)
    return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M")


def slugify(text: str) -> str:
    s = text.lower().replace("&", " and ").replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def clean_nascar_name(raw: str) -> str:
    name = (raw or "").strip()
    for prefix in NASCAR_PREFIX:
        if name.startswith(prefix):
            name = name[len(prefix) :]
            break
    return name or raw


TWO_WORD_GPS = {
    "united states",
    "emilia romagna",
    "saudi arabia",
    "great britain",
}


def clean_f1_name(raw: str) -> str:
    name = (raw or "").strip()
    stem = re.sub(r"\s+(Grand Prix|GP)$", "", name, flags=re.I).strip()
    words = stem.split()
    if len(words) >= 2 and " ".join(words[-2:]).lower() in TWO_WORD_GPS:
        return f"{words[-2]} {words[-1]} Grand Prix"
    if words:
        return f"{words[-1]} Grand Prix"
    return name or raw


def parse_nascar(event: dict, series: str) -> dict | None:
    comps = event.get("competitions") or []
    if not comps:
        return None
    c = comps[0]
    raw_name = event.get("shortName") or event.get("name") or "NASCAR"
    name = clean_nascar_name(raw_name)
    day, et = et_parts(event.get("date") or c.get("date") or "")
    return {
        "id": f"{day}-nascar-{series}-{slugify(name)}",
        "date": day,
        "et": et,
        "away": series,
        "home": name,
        "network": norm_net(c.get("broadcast") or ""),
        "site": "at",
        "place": name,
        "league": "nascar",
        "series": series,
        "name": name,
        "phx": None,
        "ticketChannel": None,
    }


def parse_f1(event: dict) -> list[dict]:
    raw_name = event.get("name") or event.get("shortName") or "Grand Prix"
    name = clean_f1_name(raw_name)
    rows: list[dict] = []
    seen: set[str] = set()
    for c in event.get("competitions") or []:
        abbr = str(((c.get("type") or {}).get("abbreviation") or "")).strip()
        session = F1_KEEP.get(abbr)
        if not session:
            continue
        day, et = et_parts(c.get("date") or event.get("date") or "")
        rid = f"{day}-f1-{session}-{slugify(name)}"
        if rid in seen:
            continue
        seen.add(rid)
        rows.append(
            {
                "id": rid,
                "date": day,
                "et": et,
                "away": session,
                "home": name,
                "network": norm_net(c.get("broadcast") or ""),
                "site": "at",
                "place": name,
                "league": "f1",
                "series": session,
                "name": name,
                "phx": None,
                "ticketChannel": None,
            }
        )
    return rows


def load_slate() -> dict:
    if not SLATE_PATH.exists():
        return {"note": "racing", "games": []}
    try:
        return json.loads(SLATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"note": "racing", "games": []}


def main() -> int:
    keep = [
        g
        for g in (load_slate().get("games") or [])
        if g.get("league") not in {"nascar", "f1"}
    ]
    racing: list[dict] = []
    seen: set[str] = set()

    for slug, league, series in NASCAR:
        for event in next_events(slug):
            row = parse_nascar(event, series)
            if row and row["id"] not in seen:
                seen.add(row["id"])
                racing.append(row)

    for event in next_events("f1"):
        for row in parse_f1(event):
            if row["id"] not in seen:
                seen.add(row["id"])
                racing.append(row)

    racing.sort(key=lambda g: (g["date"], g["et"], g.get("series") or ""))
    games = keep + racing
    games.sort(key=lambda g: (g["date"], g["et"], g.get("away") or g.get("name") or ""))

    slate = load_slate()
    slate["games"] = games
    slate["racingPulled"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    SLATE_PATH.write_text(json.dumps(slate, indent=2) + "\n", encoding="utf-8")

    n_nas = sum(1 for g in racing if g["league"] == "nascar")
    n_f1 = sum(1 for g in racing if g["league"] == "f1")
    print(f"Wrote {n_nas} NASCAR + {n_f1} F1 (kept {len(keep)} football) to {SLATE_PATH}")
    for g in racing:
        print(f"  {g['date']} {g['et']} {g['league']}/{g['series']} {g['name']} {g['network']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
