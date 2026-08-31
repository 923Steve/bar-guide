# Bar Guide

Phone-first “where’s the game” board for Arizona sports bars.

- 506-style list (matchup / Phoenix time / network / DTV #)
- Tap-a-team picker — no typing (Midwest, Dakotas, conferences)
- “Not offered” is a valid answer
- NFL rows tag Phoenix: LOCAL (FOX 10 / CBS 5), TICKET (9552–9567), NATIONAL, STREAM / DTV, or REGIONAL (10 or Ticket until Friday stamps the local pick)

No Node/npm. Python 3 is enough.

## Run

```bash
cd bar-guide
python -m http.server 5173
```

Live phone URL: https://923steve.github.io/bar-guide/

On this PC: http://localhost:5173  
Add to Home Screen after opening the live URL.

## Weekly data

Games live in `src/data/slate.js`. Channel numbers live in `src/data/channels.js`.  
Phoenix NFL tags are computed in `src/lib/phx.js` — do not hand-tag every row.

Current slate: Week 1 2026 (Labor Day weekend).

### If this chat is gone

The phone site is https://923steve.github.io/bar-guide/  
The code is https://github.com/923Steve/bar-guide  
Folder on this PC: `C:\Users\steve\GitHubFIles\bar-guide`

Open that folder in a **new** Cursor chat and say: `Friday week 2 refresh` or `Sunday stamp FOX 10 is Bears, Packers 9554`. You do not need this thread.

Or do it yourself:

1. Edit `src/data/slate.js`. One row per game:

   `g("2026-09-13", "16:25", "cardinals", "chargers", "CBS", "at", null, "nfl")`

   Date, ET time, away id, home id, network, `at` or `vs`, optional place, `cfb` or `nfl`.  
   Team ids are in `src/data/teams.js`. Networks must match keys in `channels.js` (FOX, CBS, BTN, Ticket, Prime, …).

2. FOX 10 / CBS 5 pick known: add `"local"` as the last argument.

   `g("2026-09-13", "13:00", "bears", "panthers", "FOX", "at", null, "nfl", "local")`

3. From that folder:

   `git add src/data/slate.js`

   `git commit -m "Week 2 slate"`

   `git push`

4. Wait ~1 minute. Refresh the phone. No app store update.

Friday = replace the week’s rows (or ask a new chat to pull CFBD / ESPN).  
Sunday = stamp `local` and any exact Ticket numbers you get. If you have no Ticket numbers, leave the range.
