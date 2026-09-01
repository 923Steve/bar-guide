import { PINS, TEAMS } from "./data/teams.js";
import { dayHeader, formatEt, formatPhx } from "./lib/time.js";
import { decorate, decoratedSlate, gamesForTeam } from "./lib/lookup.js";
import { SLATE_NOTE, setSlate } from "./lib/slate.js";

const LIVE_URL = "https://923steve.github.io/bar-guide/";
const LIVE_SHOW = "923steve.github.io/bar-guide";

const root = document.getElementById("root");

const state = {
  pickerOpen: false,
  installOpen: false,
  league: "cfb",
  selected: null,
  pickerTab: "cfb",
  copied: false,
};

function render() {
  const slate = decoratedSlate();
  const hits = state.selected
    ? gamesForTeam(state.selected.id).map((g) => decorate(g))
    : null;
  const list = state.selected
    ? hits
    : slate.filter((g) => g.league === state.league);
  const groups = groupByDate(list);

  root.innerHTML = `
    <div class="page">
      <header class="top">
        <div>
          <div class="brand">Bar Guide</div>
          <div class="slogan">Find a Team. Punch the Channel.</div>
          <div class="sub">${SLATE_NOTE} · Phoenix time</div>
        </div>
        <div class="league-toggle">
          <button data-act="cfb" class="${state.league === "cfb" && !state.selected ? "on" : ""}">CFB</button>
          <button data-act="nfl" class="${state.league === "nfl" && !state.selected ? "on" : ""}">NFL</button>
        </div>
      </header>

      <button class="find" data-act="open-picker">
        ${state.selected ? `Team: ${esc(state.selected.name)}` : "Find a team"}
      </button>
      ${state.selected ? `<button class="clear" data-act="clear">Show full slate</button>` : ""}
      ${!state.pickerOpen && !state.installOpen ? `
        <div class="share">
          <button class="add-phone" data-act="install">Add to phone</button>
          <button class="copy" data-act="copy">${state.copied ? "Copied" : "Copy link"}</button>
        </div>
        <p class="share-url">${LIVE_SHOW}</p>
      ` : ""}

      ${emptyHtml(hits)}
      ${groups.map(dayHtml).join("")}
      ${state.pickerOpen ? pickerHtml() : ""}
      ${state.installOpen ? installHtml() : ""}
    </div>
  `;

  root.querySelector("[data-act=cfb]")?.addEventListener("click", () => {
    state.league = "cfb";
    state.selected = null;
    render();
  });
  root.querySelector("[data-act=nfl]")?.addEventListener("click", () => {
    state.league = "nfl";
    state.selected = null;
    render();
  });
  root.querySelector("[data-act=open-picker]")?.addEventListener("click", () => {
    state.pickerOpen = true;
    state.pickerTab = state.selected?.league || state.league;
    render();
  });
  root.querySelector("[data-act=clear]")?.addEventListener("click", () => {
    state.selected = null;
    render();
  });
  root.querySelector("[data-act=install]")?.addEventListener("click", () => {
    state.installOpen = true;
    render();
  });
  root.querySelector("[data-act=copy]")?.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(LIVE_URL);
    } catch {
      window.prompt("Copy this link", LIVE_URL);
    }
    state.copied = true;
    render();
    setTimeout(() => {
      state.copied = false;
      if (!state.installOpen && !state.pickerOpen) render();
    }, 1600);
  });

  if (state.pickerOpen) bindPicker();
  if (state.installOpen) bindInstall();
}

function emptyHtml(hits) {
  if (!state.selected || !hits || hits.length) return "";
  if (state.selected.league === "nfl") {
    return `<div class="empty"><strong>${esc(state.selected.name)}</strong> is not on this week’s loaded NFL slate.</div>`;
  }
  return `<div class="empty"><strong>${esc(state.selected.name)}</strong> is not offered on this week’s slate.</div>`;
}

function dayHtml([date, games]) {
  return `
    <section class="day">
      <h2>${dayHeader(date)}</h2>
      <ul>
        ${games.map((g) => `
          <li class="row">
            <div class="matchup">${esc(g.matchup)}${g.phxLabel ? ` <span class="tag tag-${g.phx}">${esc(g.phxLabel)}</span>` : ""}</div>
            <div class="meta">
              <span>${formatPhx(g.et)}</span>
              <span class="dot">·</span>
              <span class="net">${esc(g.netLabel)}</span>
              <span class="dot">·</span>
              <span class="ch">${g.channel ? g.channel : "no channel"}</span>
              ${g.overflow ? `<span class="overflow"> check ${g.channel}-1</span>` : ""}
            </div>
            <div class="et">${formatEt(g.et)}</div>
          </li>
        `).join("")}
      </ul>
    </section>
  `;
}

function pickerHtml() {
  const tab = state.pickerTab;
  const pool = TEAMS.filter((t) => t.league === (tab === "nfl" ? "nfl" : "cfb"));
  const pins = PINS.filter((p) => pool.some((t) => t.pin === p.id));
  const alpha = [...pool].sort((a, b) => a.name.localeCompare(b.name));
  const letters = groupByLetter(alpha);

  return `
    <div class="sheet" role="dialog" aria-label="Find a team">
      <div class="sheet-top">
        <strong>Find a team</strong>
        <button class="x" data-act="close">Close</button>
      </div>
      <div class="league-toggle">
        <button data-tab="cfb" class="${tab === "cfb" ? "on" : ""}">College</button>
        <button data-tab="nfl" class="${tab === "nfl" ? "on" : ""}">NFL</button>
      </div>
      ${pins.map((p) => `
        <div class="pin-block">
          <div class="pin-label">${esc(p.label)}</div>
          <div class="pills">
            ${pool.filter((t) => t.pin === p.id).map(teamBtn).join("")}
          </div>
        </div>
      `).join("")}
      <div class="pin-label">All teams A–Z</div>
      ${letters.map(([letter, teams]) => `
        <div class="letter-block">
          <div class="letter">${esc(letter)}</div>
          <div class="pills">${teams.map(teamBtn).join("")}</div>
        </div>
      `).join("")}
    </div>
  `;
}

function installHtml() {
  return `
    <div class="sheet" role="dialog" aria-label="Add to phone">
      <div class="sheet-top">
        <strong>Add to phone</strong>
        <button class="x" data-act="close-install">Close</button>
      </div>
      <p class="install-lead">Open this on <em>their</em> phone, then:</p>
      <div class="install-block">
        <div class="pin-label">iPhone</div>
        <ol>
          <li>Tap the Share button (square with the arrow)</li>
          <li>Tap <strong>Add to Home Screen</strong></li>
          <li>Tap <strong>Add</strong></li>
        </ol>
      </div>
      <div class="install-block">
        <div class="pin-label">Android</div>
        <ol>
          <li>Tap the three dots</li>
          <li>Tap <strong>Install app</strong> or <strong>Add to Home Screen</strong></li>
        </ol>
      </div>
      <p class="share-url">${LIVE_SHOW}</p>
      <button class="copy" data-act="copy">${state.copied ? "Copied" : "Copy link"}</button>
    </div>
  `;
}

function bindInstall() {
  root.querySelector("[data-act=close-install]")?.addEventListener("click", () => {
    state.installOpen = false;
    render();
  });
}

function teamBtn(t) {
  return `<button class="pill" data-team="${t.id}">${esc(t.name)}</button>`;
}

function bindPicker() {
  root.querySelector("[data-act=close]")?.addEventListener("click", () => {
    state.pickerOpen = false;
    render();
  });
  root.querySelectorAll("[data-tab]").forEach((b) => {
    b.addEventListener("click", () => {
      state.pickerTab = b.dataset.tab;
      render();
    });
  });
  root.querySelectorAll("[data-team]").forEach((b) => {
    b.addEventListener("click", () => {
      state.selected = TEAMS.find((t) => t.id === b.dataset.team);
      state.league = state.selected.league;
      state.pickerOpen = false;
      render();
    });
  });
}

function groupByLetter(teams) {
  const map = new Map();
  for (const t of teams) {
    const letter = t.name.charAt(0).toUpperCase();
    if (!map.has(letter)) map.set(letter, []);
    map.get(letter).push(t);
  }
  return [...map.entries()];
}

function groupByDate(games) {
  const map = new Map();
  for (const g of games) {
    if (!map.has(g.date)) map.set(g.date, []);
    map.get(g.date).push(g);
  }
  return [...map.entries()];
}

function esc(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/"/g, "&quot;");
}

async function boot() {
  try {
    const res = await fetch(new URL("./data/slate.json", import.meta.url));
    if (!res.ok) throw new Error(String(res.status));
    setSlate(await res.json());
  } catch {
    setSlate({ note: "No slate loaded", games: [] });
  }
  render();
}

boot();
