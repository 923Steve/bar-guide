/**
 * Week 1 hand-load (Labor Day weekend 2026).
 * Source: NCAA.com TV page + Sports Media Watch, Friday-style dump.
 * Times are ET. Networks match CHANNELS keys.
 * Not a complete FCS dump — bar-relevant FBS + the four Dakota teams.
 */
export const SLATE_NOTE = "Week 1 · hand-loaded · confirm Friday";

export const GAMES = [
  // Thursday 9/3
  g("2026-09-03", "18:00", "umass", "rutgers", "BTN", "at"),
  g("2026-09-03", "19:00", "akron", "wake-forest", "ACCN", "at"),
  g("2026-09-03", "20:00", "colorado", "georgia-tech", "ESPN", "at"),
  g("2026-09-03", "20:00", "eastern-illinois", "minnesota", "Peacock", "at"),
  g("2026-09-03", "20:00", "arkansas-pine-bluff", "missouri", "SECN", "at"),
  g("2026-09-03", "21:00", "idaho", "utah", "ESPNU", "at"),
  g("2026-09-03", "21:00", "uab", "illinois", "BTN", "at"),

  // Friday 9/4
  g("2026-09-04", "18:30", "san-jose-state", "eastern-michigan", "ESPN+", "at"),
  g("2026-09-04", "19:00", "indiana-state", "purdue", "BTN", "at"),
  g("2026-09-04", "20:00", "toledo", "michigan-state", "FS1", "at"),
  g("2026-09-04", "20:00", "utep", "oklahoma", "SECN+", "at"),
  g("2026-09-04", "20:00", "liu", "kansas", "ESPNU", "at"),
  g("2026-09-04", "21:00", "miami", "stanford", "ESPN", "at"),
  g("2026-09-04", "21:00", "fresno-state", "usc", "FOX", "at"),

  // Saturday 9/5 — noon
  g("2026-09-05", "12:00", "east-carolina", "alabama", "ABC", "at"),
  g("2026-09-05", "12:00", "oregon-state", "houston", "ESPN", "at"),
  g("2026-09-05", "12:00", "coastal-carolina", "west-virginia", "TNT", "at"),
  g("2026-09-05", "12:00", "new-hampshire", "syracuse", "ACCN", "at"),
  g("2026-09-05", "12:00", "north-texas", "indiana", "FOX", "at"),
  g("2026-09-05", "12:00", "ohio", "nebraska", "FS1", "at"),
  g("2026-09-05", "12:00", "bryant", "army", "CBSSN", "at"),
  g("2026-09-05", "12:00", "liberty", "james-madison", "ESPNU", "at"),
  g("2026-09-05", "12:30", "ball-state", "ohio-state", "BTN", "at"),
  g("2026-09-05", "12:30", "miami-oh", "pitt", "CW", "at"),
  g("2026-09-05", "12:45", "kent-state", "south-carolina", "SECN", "at"),

  // Saturday afternoon
  g("2026-09-05", "15:00", "tennessee-state", "georgia", "SECN+", "at"),
  g("2026-09-05", "15:30", "baylor", "auburn", "ABC", "vs", "Atlanta"),
  g("2026-09-05", "15:30", "boise-state", "oregon", "CBS", "at"),
  g("2026-09-05", "15:30", "texas-state", "texas", "ESPN", "at"),
  g("2026-09-05", "15:30", "marshall", "penn-state", "FS1", "at"),
  g("2026-09-05", "15:30", "boston-college", "cincinnati", "FOX", "at"),
  g("2026-09-05", "15:30", "tulane", "duke", "ACCN", "at"),
  g("2026-09-05", "15:30", "fordham", "north-dakota-state", "MW+", "at"),
  g("2026-09-05", "15:45", "oklahoma-state", "tulsa", "ESPNU", "at"),
  g("2026-09-05", "16:15", "northern-illinois", "iowa", "BTN", "at"),
  g("2026-09-05", "16:15", "north-alabama", "arkansas", "SECN", "at"),

  // Saturday night
  g("2026-09-05", "18:00", "wyoming", "colorado-state", "USA", "at"),
  g("2026-09-05", "19:00", "missouri-state", "texas-am", "ESPN", "at"),
  g("2026-09-05", "19:00", "abilene-christian", "texas-tech", "FS1", "at"),
  g("2026-09-05", "19:30", "clemson", "lsu", "ABC", "at"),
  g("2026-09-05", "19:30", "western-michigan", "michigan", "NBC", "at"),
  g("2026-09-05", "19:30", "ulm", "mississippi-state", "ESPNU", "at"),
  g("2026-09-05", "19:30", "vmi", "virginia-tech", "ACCN", "at"),
  g("2026-09-05", "19:45", "fau", "florida", "SECN", "at"),
  g("2026-09-05", "20:00", "hampton", "maryland", "BTN", "at"),
  g("2026-09-05", "20:00", "south-dakota-state", "northwestern", "BTN", "at"),
  g("2026-09-05", "20:00", "south-dakota", "northern-colorado", "ESPN+", "at"),
  g("2026-09-05", "21:30", "northern-arizona", "arizona", "ESPN+", "at"),
  g("2026-09-05", "22:00", "morgan-state", "arizona-state", "ESPN+", "at"),
  g("2026-09-05", "22:00", "unlv", "hawaii", "CW", "at"),
  g("2026-09-05", "22:00", "central-michigan", "new-mexico", "FS1", "at"),
  g("2026-09-05", "22:30", "ucla", "cal", "ESPN", "at"),

  // Sunday 9/6
  g("2026-09-06", "16:00", "washington-state", "washington", "NBC", "at"),
  g("2026-09-06", "19:30", "wisconsin", "notre-dame", "NBC", "vs", "Green Bay"),
  g("2026-09-06", "19:30", "louisville", "ole-miss", "ABC", "vs", "Nashville"),

  // Monday 9/7
  g("2026-09-07", "19:30", "smu", "florida-state", "ESPN", "at"),

  // NFL Week 1 — kickoff / Australia / Sunday / MNF
  g("2026-09-09", "20:20", "patriots", "seahawks", "NBC", "at", null, "nfl"),
  g("2026-09-10", "20:35", "rams", "49ers", "Netflix", "vs", "Melbourne", "nfl"),

  // Sunday 9/13 — FOX/CBS regionals. Cards @ Chargers is the PHX local.
  // Other same-net same-window games tag TICKET. Early window stays
  // REGIONAL until Friday we stamp phx: "local" on FOX 10 / CBS 5.
  g("2026-09-13", "13:00", "bears", "panthers", "FOX", "at", null, "nfl"),
  g("2026-09-13", "13:00", "buccaneers", "bengals", "FOX", "at", null, "nfl"),
  g("2026-09-13", "13:00", "saints", "lions", "FOX", "at", null, "nfl"),
  g("2026-09-13", "13:00", "falcons", "steelers", "FOX", "at", null, "nfl"),
  g("2026-09-13", "13:00", "bills", "texans", "CBS", "at", null, "nfl"),
  g("2026-09-13", "13:00", "ravens", "colts", "CBS", "at", null, "nfl"),
  g("2026-09-13", "13:00", "browns", "jaguars", "CBS", "at", null, "nfl"),
  g("2026-09-13", "13:00", "jets", "titans", "CBS", "at", null, "nfl"),
  g("2026-09-13", "16:25", "cardinals", "chargers", "CBS", "at", null, "nfl"),
  g("2026-09-13", "16:25", "packers", "vikings", "CBS", "at", null, "nfl"),
  g("2026-09-13", "16:25", "dolphins", "raiders", "FOX", "at", null, "nfl"),
  g("2026-09-13", "16:25", "commanders", "eagles", "FOX", "at", null, "nfl"),
  g("2026-09-13", "20:20", "cowboys", "giants", "NBC", "at", null, "nfl"),

  g("2026-09-14", "20:15", "broncos", "chiefs", "ESPN", "at", null, "nfl"),
];

function g(date, et, away, home, network, site, place, league = "cfb", phx) {
  return {
    id: `${date}-${away}-${home}`,
    date,
    et,
    away,
    home,
    network,
    site,
    place: place || null,
    league,
    phx: phx || null,
  };
}
