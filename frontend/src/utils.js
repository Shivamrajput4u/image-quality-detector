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

const ISSUE_ICONS = {
  blur: "blur",
  underexposure: "moon",
  overexposure: "sun",
  noise: "droplet",
  low_contrast: "contrast",
  potential_defect: "zap",
};

export function iconForIssueType(type) {
  return ISSUE_ICONS[type] || "alert";
}
