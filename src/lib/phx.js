/** Phoenix NFL market tags.
 *
 * Old sellout blackout is dead. Here "blackout" means: the local station
 * owns the game, so Sunday Ticket cannot show it.
 *
 * PHX = Cardinals market.
 *   Cardinals Sunday afternoon → FOX 10 or CBS 5, never Ticket.
 *   Same network + same window, other games → Ticket 9552–9567.
 *   FOX/CBS when Cards are not on that net/window → one is local, rest
 *   Ticket. Until Friday we stamp `phx: "local"` on the pick, those
 *   rows stay REGIONAL ("10 or Ticket").
 *   NBC / ESPN / ABC / NFLN → NATIONAL (ESPN 206, NFLN 212).
 *   Prime TNF → DTV 9550 (Cardinals also get a local simulcast).
 *   Netflix → STREAM (no DTV # unless Cards are in it — then OTA too).
 *   Ticket game channels are 9552–9567; RedZone is 9551.
 *
 * CFB is not this ruleset.
 */

const LOCAL_TEAM = "cardinals";
const NATIONAL_NETS = new Set(["NBC", "ESPN", "ABC", "NFLN"]);
const STREAM_NETS = new Set(["Prime", "Netflix"]);
const LOCAL_NETS = new Set(["FOX", "CBS"]);

export function netKey(network) {
  return String(network || "").split("/")[0].trim();
}

export function windowKey(et) {
  const [h, m] = String(et).split(":").map(Number);
  const mins = (h || 0) * 60 + (m || 0);
  if (mins < 15 * 60) return "early";
  if (mins < 19 * 60) return "late";
  return "night";
}

function involves(game, teamId) {
  return game.away === teamId || game.home === teamId;
}

function localOnNetWindow(game, all) {
  const net = netKey(game.network);
  const win = windowKey(game.et);
  return all.some(
    (g) =>
      g.league === "nfl" &&
      g.date === game.date &&
      netKey(g.network) === net &&
      windowKey(g.et) === win &&
      (involves(g, LOCAL_TEAM) || g.phx === "local"),
  );
}

/** local | ticket | national | stream | regional | null */
export function phxTag(game, all = []) {
  if (game.league !== "nfl") return null;
  if (game.phx) return game.phx;

  const net = netKey(game.network);
  if (NATIONAL_NETS.has(net)) return "national";
  if (STREAM_NETS.has(net)) return "stream";
  if (net === "Ticket") return "ticket";

  if (LOCAL_NETS.has(net)) {
    if (involves(game, LOCAL_TEAM) || game.phx === "local") return "local";
    if (localOnNetWindow(game, all)) return "ticket";
    return "regional";
  }

  return "national";
}

export function applyPhxDisplay(game, tag, ch) {
  if (!tag) {
    return {
      phx: null,
      phxLabel: null,
      netLabel: ch.label,
      channel: ch.channel,
    };
  }

  if (tag === "local") {
    return {
      phx: tag,
      phxLabel: "LOCAL",
      netLabel: ch.label,
      channel: ch.channel,
    };
  }

  if (tag === "ticket") {
    return {
      phx: tag,
      phxLabel: "NFL TICKET",
      netLabel: "NFL Ticket",
      channel: game.ticketChannel || "9552–9567",
    };
  }

  if (tag === "national") {
    return {
      phx: tag,
      phxLabel: "NATIONAL",
      netLabel: ch.label,
      channel: ch.channel,
    };
  }

  if (tag === "stream") {
    const alsoLocal = involves(game, LOCAL_TEAM);
    const onBox = Boolean(ch.channel);
    return {
      phx: tag,
      phxLabel: alsoLocal ? "STREAM · also local" : onBox ? "DTV" : "STREAM",
      netLabel: ch.label,
      channel: ch.channel,
    };
  }

  const localCh = netKey(game.network) === "FOX" ? "10" : "5";
  return {
    phx: tag,
    phxLabel: "REGIONAL",
    netLabel: ch.label,
    channel: `${localCh} or NFL Ticket`,
  };
}
