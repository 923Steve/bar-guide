/** Sept 2026: AZ is MST, rest of US is still on DST → ET − 3 = Phoenix. */
const ET_TO_PHX = 3;

export function formatPhx(etHHMM) {
  const [h, m] = etHHMM.split(":").map(Number);
  let hour = h - ET_TO_PHX;
  const nextDay = hour < 0;
  if (hour < 0) hour += 24;
  const ampm = hour >= 12 ? "p" : "a";
  let h12 = hour % 12;
  if (h12 === 0) h12 = 12;
  const min = m === 0 ? "" : `:${String(m).padStart(2, "0")}`;
  return `${h12}${min}${ampm} PHX${nextDay ? " (+1)" : ""}`;
}

export function formatEt(etHHMM) {
  const [h, m] = etHHMM.split(":").map(Number);
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
