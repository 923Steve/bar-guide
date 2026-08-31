"""Friday slate pull. ESPN scoreboard → src/data/slate.json

  python pull_week.py
  python pull_week.py --cfb-week 1 --nfl-week 1 --year 2026

Then: git add src/data/slate.json && git commit && git push
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
SLATE_PATH = ROOT / "src" / "data" / "slate.json"
TEAMS_PATH = ROOT / "src" / "data" / "teams.js"
ET = ZoneInfo("America/New_York")
UA = {"User-Agent": "Mozilla/5.0"}

DAKOTA_ESPN_IDS = {"155", "233", "2449", "2571"}

NET_MAP = {
    "BTN": "BTN",
    "ACC NETWORK": "ACCN",
    "ACCN": "ACCN",
    "SEC NETWORK": "SECN",
    "SECN": "SECN",
    "SECN+": "SECN+",
    "SEC NETWORK+": "SECN+",
    "CBSSN": "CBSSN",
    "CBS SPORTS NETWORK": "CBSSN",
    "USA NET": "USA",
    "USA NETWORK": "USA",
    "USA": "USA",
    "CW": "CW",
    "THE CW": "CW",
    "ESPN": "ESPN",
    "ESPN2": "ESPN2",
    "ESPNU": "ESPNU",
    "ESPN+": "ESPN+",
    "ESPN/DISNEY+": "ESPN",
    "ABC": "ABC",
    "ABC/DISNEY+": "ABC",
    "ABC/ESPN": "ESPN",
    "ESPN/ABC": "ESPN",
    "CBS": "CBS",
    "NBC": "NBC",
    "FOX": "FOX",
    "FS1": "FS1",
    "FS2": "FS2",
    "TNT": "TNT",
    "PEACOCK": "Peacock",
    "NETFLIX": "Netflix",
    "PRIME": "Prime",
    "PRIME VIDEO": "Prime",
    "AMAZON PRIME": "Prime",
    "AMAZON": "Prime",
    "NFL NETWORK": "NFLN",
    "NFLN": "NFLN",
    "MW+": "MW+",
    "HBO MAX": "HBO Max",
    "TRUTV": "TNT",
}

ABBR = {
    "OSU": "ohio-state",
    "OKST": "oklahoma-state",
    "MIA": "miami",
    "M-OH": "miami-oh",
    "MISS": "ole-miss",
    "MSST": "mississippi-state",
    "PSU": "penn-state",
    "NCSU": "nc-state",
    "PITT": "pitt",
    "TA&M": "texas-am",
    "TAMU": "texas-am",
    "NDSU": "north-dakota-state",
    "SDST": "south-dakota-state",
    "SDAK": "south-dakota",
    "UND": "north-dakota",
    "MASS": "umass",
    "CONN": "uconn",
    "HAW": "hawaii",
    "APP": "app-state",
    "USF": "usf",
    "USM": "southern-miss",
    "ULM": "ulm",
    "ULL": "louisiana",
    "MSU": "michigan-state",
    "MOST": "missouri-state",
    "WASH": "washington",
    "WSU": "washington-state",
    "CAL": "cal",
    "FSU": "florida-state",
    "VT": "virginia-tech",
    "UVA": "virginia",
    "UNC": "north-carolina",
    "GT": "georgia-tech",
    "BC": "boston-college",
    "SDSU": "san-diego-state",
    "FRES": "fresno-state",
    "SJSU": "san-jose-state",
    "CSU": "colorado-state",
    "USU": "utah-state",
    "NMSU": "new-mexico-state",
    "UNT": "north-texas",
    "TXST": "texas-state",
    "WKU": "western-kentucky",
    "MTSU": "middle-tennessee",
    "LT": "louisiana-tech",
    "FAU": "fau",
    "FIU": "fiu",
    "GSU": "georgia-state",
    "GASO": "georgia-southern",
    "CCU": "coastal-carolina",
    "ODU": "old-dominion",
    "JMU": "james-madison",
    "KENN": "kennesaw-state",
    "JVST": "jacksonville-state",
    "SHSU": "sam-houston",
    "ARST": "arkansas-state",
    "USA": "south-alabama",
    "TROY": "troy",
    "BGSU": "bowling-green",
    "CMU": "central-michigan",
    "EMU": "eastern-michigan",
    "WMU": "western-michigan",
    "NIU": "northern-illinois",
    "BALL": "ball-state",
    "KSU": "kansas-state",
    "TTU": "texas-tech",
    "ASU": "arizona-state",
    "AFA": "air-force",
    "ARMY": "army",
    "NAVY": "navy",
    "ND": "notre-dame",
}

ALIASES = {
    "ole miss": "ole-miss",
    "miami (oh)": "miami-oh",
    "miami (ohio)": "miami-oh",
    "miami ohio": "miami-oh",
    "n dakota st": "north-dakota-state",
    "s dakota st": "south-dakota-state",
    "north dakota st": "north-dakota-state",
    "south dakota st": "south-dakota-state",
    "massachusetts": "umass",
    "uconn": "uconn",
    "connecticut": "uconn",
    "pittsburgh": "pitt",
    "nc state": "nc-state",
    "n.c. state": "nc-state",
    "texas a&m": "texas-am",
    "hawai'i": "hawaii",
    "hawaii": "hawaii",
    "app state": "app-state",
    "appalachian st": "app-state",
    "southern miss": "southern-miss",
    "ul monroe": "ulm",
    "louisiana monroe": "ulm",
    "sam houston": "sam-houston",
    "florida atlantic": "fau",
    "south florida": "usf",
    "utsa": "utsa",
    "uab": "uab",
    "utep": "utep",
    "ucf": "ucf",
    "unlv": "unlv",
    "lsu": "lsu",
    "usc": "usc",
    "ucla": "ucla",
    "smu": "smu",
    "tcu": "tcu",
    "byu": "byu",
    "cal": "cal",
}


def get(url: str) -> dict:
    import time
    from urllib.error import HTTPError

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


def slugify(text: str) -> str:
    s = text.lower().replace("&", " and ").replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def load_team_ids() -> dict[str, str]:
    """name/id lowercase → id, from teams.js"""
    text = TEAMS_PATH.read_text(encoding="utf-8")
    out = {}
    for mid, name in re.findall(r'id:\s*"([^"]+)",\s*name:\s*"([^"]+)"', text):
        out[mid] = mid
        out[name.lower()] = mid
        out[slugify(name)] = mid
    out.update(ALIASES)
    return out


NFL_ABBR = {
    "ARI": "cardinals",
    "ATL": "falcons",
    "BAL": "ravens",
    "BUF": "bills",
    "CAR": "panthers",
    "CHI": "bears",
    "CIN": "bengals",
    "CLE": "browns",
    "DAL": "cowboys",
    "DEN": "broncos",
    "DET": "lions",
    "GB": "packers",
    "HOU": "texans",
    "IND": "colts",
    "JAX": "jaguars",
    "KC": "chiefs",
    "LAC": "chargers",
    "LAR": "rams",
    "MIA": "dolphins",
    "MIN": "vikings",
    "NE": "patriots",
    "NO": "saints",
    "NYG": "giants",
    "NYJ": "jets",
    "LV": "raiders",
    "PHI": "eagles",
    "PIT": "steelers",
    "SF": "49ers",
    "SEA": "seahawks",
    "TB": "buccaneers",
    "TEN": "titans",
    "WSH": "commanders",
    "WAS": "commanders",
}


def team_id(team: dict, index: dict[str, str], league: str) -> str:
    abbr = (team.get("abbreviation") or "").upper()
    if league == "nfl" and abbr in NFL_ABBR:
        return NFL_ABBR[abbr]
    short = (team.get("shortDisplayName") or "").strip()
    loc = (team.get("location") or "").strip()
    for key in (short.lower(), slugify(short), loc.lower(), slugify(loc)):
        if key in index:
            return index[key]
    if abbr in ABBR:
        return ABBR[abbr]
    return slugify(short or loc or team.get("displayName") or "unknown")


def norm_net(raw: str) -> str:
    key = re.sub(r"\s+", " ", (raw or "").strip()).upper()
    if not key:
        return "TBD"
    if key in NET_MAP:
        return NET_MAP[key]
    first = key.split("/")[0].strip()
    return NET_MAP.get(first, raw.strip().split("/")[0].strip() or "TBD")


def et_parts(iso: str) -> tuple[str, str]:
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(ET)
    return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M")


def parse_event(event: dict, league: str, index: dict[str, str]) -> dict | None:
    comps = event.get("competitions") or []
    if not comps:
        return None
    c = comps[0]
    sides = {x.get("homeAway"): x for x in c.get("competitors") or []}
    if "home" not in sides or "away" not in sides:
        return None
    away = team_id(sides["away"]["team"], index, league)
    home = team_id(sides["home"]["team"], index, league)
    day, et = et_parts(event.get("date") or c.get("date") or "")
    site = "vs" if c.get("neutralSite") else "at"
    place = None
    if c.get("neutralSite"):
        addr = (c.get("venue") or {}).get("address") or {}
        city = addr.get("city")
        if city:
            place = city
    return {
        "id": f"{day}-{away}-{home}",
        "date": day,
        "et": et,
        "away": away,
        "home": home,
        "network": norm_net(c.get("broadcast") or ""),
        "site": site,
        "place": place,
        "league": league,
        "phx": None,
        "ticketChannel": None,
    }


def involves_dakota(event: dict) -> bool:
    comps = event.get("competitions") or []
    if not comps:
        return False
    for x in comps[0].get("competitors") or []:
        if str((x.get("team") or {}).get("id")) in DAKOTA_ESPN_IDS:
            return True
    return False


def scoreboard(kind: str, year: int, week: int, extra: str = "") -> dict:
    if kind == "cfb":
        base = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard"
    else:
        base = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    url = f"{base}?week={week}&seasontype=2&dates={year}&limit=300{extra}"
    return get(url)


def calendar_week(kind: str, year: int, today: date) -> int:
    data = scoreboard(kind, year, 1)
    leagues = data.get("leagues") or []
    cal = (leagues[0].get("calendar") if leagues else None) or []
    entries = []
    for block in cal:
        if not isinstance(block, dict):
            continue
        if str(block.get("value")) not in {"2", "1"} and block.get("label") not in {
            "Regular Season",
            "Preseason",
        }:
            if block.get("entries"):
                entries.extend(block.get("entries") or [])
            continue
        entries.extend(block.get("entries") or [])
    if kind == "cfb":
        for block in cal:
            if isinstance(block, dict) and block.get("label") == "Regular Season":
                entries = block.get("entries") or []
                break
    if kind == "nfl":
        for block in cal:
            if isinstance(block, dict) and "Regular" in str(block.get("label", "")):
                entries = block.get("entries") or []
                break
        if not entries:
            entries = []
            for block in cal:
                if isinstance(block, dict):
                    entries.extend(block.get("entries") or [])

    def parse_start(entry: dict) -> date | None:
        raw = entry.get("startDate")
        if not raw:
            return None
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).date()

    current = None
    upcoming = None
    for entry in entries:
        start = parse_start(entry)
        end_raw = entry.get("endDate")
        if not start or not end_raw:
            continue
        end = datetime.fromisoformat(end_raw.replace("Z", "+00:00")).date()
        num = int(entry.get("value") or 0)
        if num <= 0 or num >= 900:
            continue
        if start <= today <= end:
            current = num
            break
        if start > today and upcoming is None:
            upcoming = num
    return current or upcoming or 1


def merge_stamps(games: list[dict], old: list[dict]) -> None:
    prev = {g["id"]: g for g in old}
    for g in games:
        was = prev.get(g["id"])
        if not was:
            continue
        if was.get("phx"):
            g["phx"] = was["phx"]
        if was.get("ticketChannel"):
            g["ticketChannel"] = was["ticketChannel"]


def load_old() -> list[dict]:
    if not SLATE_PATH.exists():
        return []
    try:
        return json.loads(SLATE_PATH.read_text(encoding="utf-8")).get("games") or []
    except json.JSONDecodeError:
        return []


def main() -> int:
    today = datetime.now(timezone.utc).astimezone(ET).date()
    p = argparse.ArgumentParser(description="Pull CFB + NFL slate from ESPN")
    p.add_argument("--year", type=int, default=today.year)
    p.add_argument("--cfb-week", type=int)
    p.add_argument("--nfl-week", type=int)
    p.add_argument("--week", type=int, help="Set both CFB and NFL week")
    args = p.parse_args()
    year = args.year
    if args.week:
        cfb_week = nfl_week = args.week
    else:
        cfb_week = args.cfb_week or calendar_week("cfb", year, today)
        nfl_week = args.nfl_week or calendar_week("nfl", year, today)

    index = load_team_ids()
    games: list[dict] = []
    seen: set[str] = set()

    fbs = scoreboard("cfb", year, cfb_week, "&groups=80")
    fcs = scoreboard("cfb", year, cfb_week, "&groups=81")
    nfl = scoreboard("nfl", year, nfl_week)

    for event in fbs.get("events") or []:
        row = parse_event(event, "cfb", index)
        if row and row["id"] not in seen:
            seen.add(row["id"])
            games.append(row)
    for event in fcs.get("events") or []:
        if not involves_dakota(event):
            continue
        row = parse_event(event, "cfb", index)
        if row and row["id"] not in seen:
            seen.add(row["id"])
            games.append(row)
    for event in nfl.get("events") or []:
        row = parse_event(event, "nfl", index)
        if row and row["id"] not in seen:
            seen.add(row["id"])
            games.append(row)

    games.sort(key=lambda g: (g["date"], g["et"], g["away"]))
    merge_stamps(games, load_old())

    missing = []
    known = set(index.values())
    for g in games:
        for tid in (g["away"], g["home"]):
            if tid not in known and tid not in missing:
                missing.append(tid)

    note = f"CFB week {cfb_week} / NFL week {nfl_week} / ESPN"
    payload = {
        "note": note,
        "year": year,
        "cfbWeek": cfb_week,
        "nflWeek": nfl_week,
        "pulled": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "games": games,
    }
    SLATE_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    n_cfb = sum(1 for g in games if g["league"] == "cfb")
    n_nfl = sum(1 for g in games if g["league"] == "nfl")
    print(f"Wrote {len(games)} games ({n_cfb} CFB, {n_nfl} NFL) to {SLATE_PATH}")
    print(note)
    if missing:
        print("Unmapped team ids (still on the board, not in picker):")
        for tid in missing:
            print(f"  {tid}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
