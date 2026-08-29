export function toneForLabel(label) {
  if (label === "ACCEPTABLE") return "good";
  if (label === "DEGRADED") return "warn";
  return "bad";
}

export function toneForSeverity(severity) {
  if (severity === "low") return "good";
  if (severity === "medium") return "warn";
  return "bad";
}
