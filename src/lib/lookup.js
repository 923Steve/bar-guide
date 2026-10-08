import { channelFor } from "../data/channels.js";
import { TEAM_BY_ID } from "../data/teams.js";
import { applyPhxDisplay, phxTag } from "./phx.js";
import { GAMES } from "./slate.js";

export function teamName(id) {
  if (TEAM_BY_ID[id]) return TEAM_BY_ID[id].name;
  return id
    .split("-")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}

const NASCAR_SERIES = {
  truck: "Truck",
  oreilly: "O'Reilly",
  cup: "Cup",
};

const F1_SESSION = {
  shootout: "Sprint Shootout",
  sprint: "Sprint",
  quali: "Qualifying",
  race: "Race",
};

export function matchupLine(game) {
  if (game.league === "nascar") {
    const series = NASCAR_SERIES[game.series] || game.series || "NASCAR";
    return `${series} · ${game.name || game.place || "Race"}`;
  }
  if (game.league === "f1") {
    const session = F1_SESSION[game.series] || game.series || "F1";
    return `${session} · ${game.name || game.place || "Grand Prix"}`;
  }
  const a = teamName(game.away);
  const h = teamName(game.home);
  const joiner = game.site === "vs" ? "vs" : "@";
  const place = game.place ? ` (${game.place})` : "";
  return `${a} ${joiner} ${h}${place}`;
}

export function gamesForTeam(teamId) {
  return GAMES.filter((g) => g.away === teamId || g.home === teamId);
}

export function decorate(game, all = GAMES) {
  const ch = channelFor(game.network);
  const clash = all.filter(
    (g) =>
      g.id !== game.id &&
      g.date === game.date &&
      g.et === game.et &&
      g.network === game.network &&
      ch.channel,
  );
  const tag = phxTag(game, all);
  const display = applyPhxDisplay(game, tag, ch);
  return {
    ...game,
    matchup: matchupLine(game),
    netLabel: display.netLabel,
    channel: display.channel,
    overflow: game.league !== "nfl" && clash.length > 0,
    phx: display.phx,
    phxLabel: display.phxLabel,
  };
}

export function decoratedSlate() {
  return GAMES.map((g) => decorate(g));
}
