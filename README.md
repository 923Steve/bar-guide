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

Games live in `src/data/slate.json`. Channel numbers live in `src/data/channels.js`.  
Phoenix NFL tags are computed in `src/lib/phx.js` — do not hand-tag every row.

### Friday (the command)

```bash
cd C:\Users\steve\GitHubFIles\bar-guide
python pull_week.py
git add src/data/slate.json
git commit -m "Week slate"
git push
```

That pulls full FBS + the four Dakota games + the NFL card from ESPN. Glance the unmapped-team printout, then push. Phone updates in about a minute.

Force a week: `python pull_week.py --cfb-week 2 --nfl-week 1 --year 2026`

### Sunday (NFL only)

In `slate.json`, on the FOX 10 / CBS 5 game set `"phx": "local"`.  
If you get a Ticket number, set `"ticketChannel": "9554"` on that game. Then commit and push.

### If this chat is gone

The phone site is https://923steve.github.io/bar-guide/  
The code is https://github.com/923Steve/bar-guide  
Folder on this PC: `C:\Users\steve\GitHubFIles\bar-guide`

Open that folder in a **new** Cursor chat and say `Friday week 2 refresh` or `Sunday stamp FOX 10 is Bears`. Or run the command above yourself.
