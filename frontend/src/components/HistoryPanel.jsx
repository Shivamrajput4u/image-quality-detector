import { useEffect, useState } from "react";
import { fetchHistory, resolveImageUrl } from "../api";
import Badge from "./Badge";
import ResultCard from "./ResultCard";
import { toneForLabel } from "../utils";

export default function HistoryPanel() {
  const [items, setItems] = useState([]);
  const [status, setStatus] = useState("loading"); // loading | success | error
  const [errorMessage, setErrorMessage] = useState("");
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    let cancelled = false;
    fetchHistory()
      .then((data) => {
        if (cancelled) return;
        setItems(data.results);
        setStatus("success");
      })
      .catch((error) => {
        if (cancelled) return;
        setErrorMessage(error.message);
        setStatus("error");
      });
    return () => {
      cancelled = true;
    };
  }, []);

  if (status === "loading") return <p className="status-message">Loading history...</p>;
  if (status === "error") return <p className="error-banner">{errorMessage}</p>;
  if (items.length === 0) {
    return <p className="status-message">No analyses yet — upload an image to get started.</p>;
  }

  return (
    <div className="history-panel">
      <div className="history-grid">
        {items.map((item) => (
          <button key={item.id} className="history-thumb" onClick={() => setSelected(item)}>
            <img src={resolveImageUrl(item.image_url)} alt={item.original_filename} />
            <div className="history-thumb-info">
              <span>{item.quality_score}</span>
              <Badge text={item.quality_label} tone={toneForLabel(item.quality_label)} />
            </div>
          </button>
        ))}
      </div>

      {selected && (
        <div className="history-detail">
          <button className="close-detail" onClick={() => setSelected(null)}>
            Close ✕
          </button>
          <ResultCard result={selected} />
        </div>
      )}
    </div>
  );
}
