**WHERE'S MY GAME — MARCHING ORDERS**

Live phone site: https://923steve.github.io/bar-guide/  
Code folder: `C:\Users\steve\GitHubFIles\bar-guide`

---

**TUESDAY + FRIDAY (usually automatic)**

Windows task **Bar Guide Slate Pull** runs at **6:15** local on **Tuesday** and **Friday**. It pulls ESPN and pushes if the slate changed. Open the phone with coffee and glance it.

- Tuesday: this week’s Thursday — CFB + TNF
- Friday: last look at Saturday networks

Same travel rule as MLB: PC can sleep, don’t shut down or sign out. If you miss a morning on the road, it runs when the box wakes up.

Log: `C:\Users\steve\GitHubFIles\bar-guide\logs\slate_pull.log`

**Force a pull now** (terminal in Cursor):

```
cd C:\Users\steve\GitHubFIles\bar-guide
powershell -ExecutionPolicy Bypass -File .\friday_run.ps1
```

Or the old four-liner:

```
cd C:\Users\steve\GitHubFIles\bar-guide
python pull_week.py
git add src/data/slate.json
git commit -m "Week slate"
git push
```

Wait about 1 minute. Hard-refresh the phone.

Force a specific week:

```
python pull_week.py --cfb-week 2 --nfl-week 1 --year 2026
git add src/data/slate.json
git commit -m "Week slate"
git push
```

---

**IF YOU FIND A MISTAKE**

Wrong network, wrong time, missing game, dumb team name — don’t retype the week.

1. Open a **new** Cursor chat on the `bar-guide` folder and say what you see:  
   `Ohio State is on FOX not BTN` or `UND is missing` or `kickoff should be 12:30p`
2. Or edit that one row in `src/data/slate.json` (`network`, `et`, `date`) and:

```
cd C:\Users\steve\GitHubFIles\bar-guide
git add src/data/slate.json
git commit -m "Fix slate"
git push
```

The Tue/Fri pull **keeps** `phx` and `ticketChannel` stamps on the same game id. It **will overwrite** network/time if ESPN still has the old value. If ESPN is wrong and you already fixed it, tell the chat so we lock that row — or wait until after the next run to patch it again.

---

**SUNDAY 6:15 (usually automatic)**

Windows task **Bar Guide Sunday Locals** stamps FOX 10 / CBS 5 from Phoenix listings (not DirecTV). Glance the NFL tab with coffee.

Log: `C:\Users\steve\GitHubFIles\bar-guide\logs\sunday_locals.log`

Force it now:

```
cd C:\Users\steve\GitHubFIles\bar-guide
powershell -ExecutionPolicy Bypass -File .\sunday_run.ps1
```

If a local is wrong, tell a chat `Sunday stamp FOX 10 is Bears` and we fix that row.

**NFL Ticket is a block, not a per-game number.**

Out-of-market Sunday games show **9554–9567**. Staff scan that range on the receiver guide. Do not stamp a single 95xx. Week 6 proved the desk matrix is one off the wall.

Locals stay FOX 10 / CBS 5 from the Sunday 6:15 stamp. RedZone is 9551. TNF Prime is 9550. NFL Network is 212.

---

**SPORTS HOME + NASCAR + F1**

Phone opens on big sport buttons: College Football, College Basketball, NFL, NHL, NASCAR, Formula 1.
Last sport is remembered. **Sports** goes back to the buttons.
FIND A TEAM is CFB / CBB / NFL / NHL. Same college pins as football (Midwest, Dakotas). NHL Desert pin is Golden Knights + Utah. Men’s hoops only. No driver picker.

NASCAR board: Truck (Craftsman), O’Reilly (old Xfinity, CW), Cup.
F1 board: Sprint Shootout / Sprint / Qualifying / Race. Practice is skipped.
2026 F1 US rights are Apple TV → **Streaming Only** (no fake DTV #).
ESPN+ is a **block**, not a per-game number: **Bar 9519–9525** (ESPN+ for Business) · **Home 210-1–7** (residential leftover). Do not stamp 95xx per game. B1G+ / SECN+ / ACCNX / MW+ / YouTube stay Streaming Only.
NHL national: ESPN / TNT / ABC use the existing DTV #s. NHL Network is **215**. Do not invent a Knights “local” or any RSN number. ESPN+ hockey uses the same ESPN+ block.

Tue/Fri football pull **keeps** nascar/f1/cbb/nhl rows, then `pull_racing.py`, `pull_cbb.py`, and `pull_nhl.py` refresh those.
A racing, hoops, or NHL miss does not fail the football push.
ESPN often leaves Cup / O’Reilly / F1 stuck on last weekend after the race.
The pull skips finished events and asks ESPN for the next calendar date.

```
cd C:\Users\steve\GitHubFIles\bar-guide
python pull_racing.py
python pull_cbb.py
python pull_nhl.py
git add src/data/slate.json
git commit -m "Racing, hoops, and NHL slate"
git push
```

---

**WHAT YOU NEVER DO**

- Don’t type 70 games
- Don’t run this hourly
- Don’t update CFB on Sunday unless a network actually flipped
- Don’t scrape DirecTV
- Don’t spend Odds API credits on this

---

**IF THIS CHAT IS GONE**

This file lives in the repo: `CHEATSHEET.md`  
New Cursor chat on `bar-guide`: `Tuesday week 2 refresh` or `Sunday stamp FOX 10 is Bears`

---

**HANDING IT TO A BARTENDER**

1. Text them https://923steve.github.io/bar-guide/
2. They open it on **their** phone
3. They tap **Add to Home Screen** and follow the steps

They pick a team. The game shows up. They punch the channel.

**Find a Team. Punch the Channel.**
