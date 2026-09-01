**BAR GUIDE — MARCHING ORDERS**

Live phone site: https://923steve.github.io/bar-guide/  
Code folder: `C:\Users\steve\GitHubFIles\bar-guide`

---

**FRIDAY (usually automatic)**

Windows task **Bar Guide Friday Pull** runs at **6:15** local. It pulls ESPN and pushes if the slate changed. Open the phone with coffee and glance it.

Same travel rule as MLB: PC can sleep, don’t shut down or sign out. If you miss Friday on the road, it runs when the box wakes up.

Log: `C:\Users\steve\GitHubFIles\bar-guide\logs\friday_pull.log`

**Force a Friday now** (terminal in Cursor):

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

The Friday pull **keeps** `phx` and `ticketChannel` stamps on the same game id. It **will overwrite** network/time if ESPN still has the old value. If ESPN is wrong and you already fixed it, tell the chat so we lock that row — or wait until after Friday’s run to patch it again.

---

**SUNDAY — NFL CHANNELS**

You do **not** need DirecTV for FOX 10 / CBS 5. Check a Phoenix listings page.

**Local pick known** (example: FOX 10 is Bears):  
Tell a chat `Sunday stamp FOX 10 is Bears`  
or in `slate.json` on that game set `"phx": "local"`, then commit and push. The other FOX games in that window flip to NFL Ticket.

**You got all the NFL Ticket numbers** (9552–9567 board):

On each Ticket game in `slate.json` set `"ticketChannel": "9554"` (whatever the board says). Then:

```
cd C:\Users\steve\GitHubFIles\bar-guide
git add src/data/slate.json
git commit -m "Sunday Ticket numbers"
git push
```

Or dump the list in a chat: `Packers 9554, Bills 9558, ...` and we stamp them.

If you only have some numbers, stamp those. The rest stay `9552–9567`. The board still works.

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
New Cursor chat on `bar-guide`: `Friday week 2 refresh` or `Sunday stamp FOX 10 is Bears`

---

**HANDING IT TO A BARTENDER**

1. Text them https://923steve.github.io/bar-guide/
2. They open it on **their** phone
3. They tap **Add to Home Screen** and follow the steps

They pick a team. The game shows up. They punch the channel.

**Find a Team. Punch the Channel.**
