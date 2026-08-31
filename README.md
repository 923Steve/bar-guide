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

On this PC: http://localhost:5173  
On a phone anywhere: the GitHub Pages URL (bookmark / Add to Home Screen).

## Weekly data

Hand-load `src/data/slate.js` Friday from 506sports + Matt Sarz.  
DTV numbers live in `src/data/channels.js`. Overflow (`610-1`) flags when two CFB games share a network and start time.

NFL Phoenix tags are computed in `src/lib/phx.js` (Cardinals market).  
When FOX 10 / CBS 5’s regional pick is known, stamp that game `phx: "local"`; the rest of that net+window flip to Ticket.

Current slate: Week 1 2026 (Labor Day weekend).
