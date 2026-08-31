export let GAMES = [];
export let SLATE_NOTE = "";

export function setSlate(data) {
  GAMES = Array.isArray(data.games) ? data.games : [];
  SLATE_NOTE = data.note || "";
}
