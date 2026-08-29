import Icon from "./Icon";

export default function Badge({ text, tone, withIcon = false }) {
  return (
    <span className={`badge badge-${tone}`}>
      {withIcon && <Icon name={tone === "good" ? "check" : "alert"} size={13} />}
      {text}
    </span>
  );
}
