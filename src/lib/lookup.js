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

export function matchupLine(game) {
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
