/** Arizona stays MST. Eastern springs forward / falls back.
 *  EDT → PHX is −3. EST → PHX is −2. Do not hardcode this.
 */

function zoneOffsetHours(timeZone, when) {
  const name = new Intl.DateTimeFormat("en-US", {
    timeZone,
    timeZoneName: "shortOffset",
  })
    .formatToParts(when)
    .find((p) => p.type === "timeZoneName")?.value || "";
  const m = name.match(/([+-])(\d{1,2})(?::(\d{2}))?/);
  if (!m) return timeZone === "America/Phoenix" ? -7 : -5;
  const hours = Number(m[2]) + Number(m[3] || 0) / 60;
  return m[1] === "-" ? -hours : hours;
}

export function etToPhxHours(isoDate) {
  const when = isoDate ? new Date(`${isoDate}T16:00:00Z`) : new Date();
  return zoneOffsetHours("America/Phoenix", when) - zoneOffsetHours("America/New_York", when);
}

export function formatPhx(etHHMM, isoDate) {
  if (!etHHMM) return "";
  const [h, m] = String(etHHMM).split(":").map(Number);
  let hour = h + etToPhxHours(isoDate);
  const nextDay = hour < 0;
  if (hour < 0) hour += 24;
  hour = hour % 24;
  const ampm = hour >= 12 ? "p" : "a";
  let h12 = hour % 12;
  if (h12 === 0) h12 = 12;
  const min = m === 0 ? "" : `:${String(m).padStart(2, "0")}`;
  return `${h12}${min}${ampm} PHX${nextDay ? " (+1)" : ""}`;
}

export function formatEt(etHHMM) {
  if (!etHHMM) return "";
  const [h, m] = String(etHHMM).split(":").map(Number);
  const ampm = h >= 12 ? "p" : "a";
  let h12 = h % 12;
  if (h12 === 0) h12 = 12;
  const min = m === 0 ? "" : `:${String(m).padStart(2, "0")}`;
  return `${h12}${min}${ampm} ET`;
}

const DAYS = [
  "Sunday",
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
];
const MONTHS = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

export function dayHeader(isoDate) {
  const [y, mo, d] = isoDate.split("-").map(Number);
  const dt = new Date(Date.UTC(y, mo - 1, d, 17));
  const mon = MONTHS[mo - 1].slice(0, 3).toUpperCase();
  return `${DAYS[dt.getUTCDay()].toUpperCase()}  ${mon} ${d}`;
}
