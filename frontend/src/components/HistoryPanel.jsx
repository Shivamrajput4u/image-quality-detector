import { useEffect, useState } from "react";
import { fetchHistory, resolveImageUrl } from "../api";
import Badge from "./Badge";
import Icon from "./Icon";
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

  if (status === "loading") {
    return (
      <div className="status-message">
        <span className="spinner spinner-dark" />
        Loading history...
      </div>
    );
  }
  if (status === "error") {
    return (
      <p className="error-banner">
        <Icon name="alert" size={16} />
        {errorMessage}
      </p>
    );
  }
  if (items.length === 0) {
    return (
      <div className="status-message">
        <Icon name="image" size={28} />
        <p>No analyses yet — upload an image to get started.</p>
      </div>
    );
  }

  return (
    <div className="history-panel">
      <div className="history-grid">
        {items.map((item) => (
          <button key={item.id} className="history-thumb" onClick={() => setSelected(item)}>
            <div className="history-thumb-image">
              <img src={resolveImageUrl(item.image_url)} alt={item.original_filename} />
              <span className="history-thumb-hint">View details</span>
            </div>
            <div className="history-thumb-info">
              <span className="history-thumb-score">{item.quality_score}</span>
              <Badge text={item.quality_label} tone={toneForLabel(item.quality_label)} />
            </div>
          </button>
        ))}
      </div>

      {selected && (
        <div className="history-detail">
          <button className="close-detail" onClick={() => setSelected(null)}>
            <Icon name="x" size={14} />
            Close
          </button>
          <ResultCard result={selected} />
        </div>
      )}
    </div>
  );
}
