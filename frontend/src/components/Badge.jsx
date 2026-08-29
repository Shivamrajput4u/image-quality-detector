export default function Badge({ text, tone }) {
  return <span className={`badge badge-${tone}`}>{text}</span>;
}
