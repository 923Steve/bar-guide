/** DirecTV satellite / for-business sports map. Locals are Phoenix.
 *  Overflow (610-1 etc.) is noted in the UI when two games share a net+time.
 *  Stream-only nets have channel: null.
 */
export const CHANNELS = {
  ABC: { label: "ABC", channel: "15", note: "KNXV Phoenix" },
  CBS: { label: "CBS", channel: "5", note: "KPHO Phoenix" },
  NBC: { label: "NBC", channel: "12", note: "KPNX Phoenix" },
  FOX: { label: "FOX", channel: "10", note: "KSAZ Phoenix" },
  CW: { label: "CW", channel: "7", note: "KAZT Phoenix" },
  ESPN: { label: "ESPN", channel: "206" },
  ESPN2: { label: "ESPN2", channel: "209" },
  ESPNU: { label: "ESPNU", channel: "208" },
  FS1: { label: "FS1", channel: "219" },
  FS2: { label: "FS2", channel: "618" },
  BTN: { label: "BTN", channel: "610" },
  SECN: { label: "SECN", channel: "611" },
  ACCN: { label: "ACCN", channel: "612" },
  CBSSN: { label: "CBSSN", channel: "221" },
  TNT: { label: "TNT", channel: "245" },
  USA: { label: "USA", channel: "242" },
  NFLN: { label: "NFLN", channel: "212" },
  Ticket: { label: "Sunday Ticket", channel: "9552–9567", note: "per-game # posts Sunday AM" },
  RedZone: { label: "RedZone", channel: "9551" },
  "ESPN+": { label: "ESPN+", channel: null },
  "SECN+": { label: "SECN+", channel: null },
  Peacock: { label: "Peacock", channel: null },
  "MW+": { label: "MW+", channel: null },
  "HBO Max": { label: "HBO Max", channel: null },
  Netflix: { label: "Netflix", channel: null },
  Prime: { label: "Prime", channel: "9550", note: "TNF feed on DTV" },
};

export function channelFor(network) {
  const key = String(network || "").split("/")[0].trim();
  return CHANNELS[key] || { label: key || "TBD", channel: null };
}
