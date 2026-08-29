import Badge from "./Badge";
import Icon from "./Icon";
import ScoreRing from "./ScoreRing";
import { resolveImageUrl } from "../api";
import { iconForIssueType, toneForLabel, toneForSeverity } from "../utils";

export default function ResultCard({ result }) {
  const { image_url, original_filename, quality_score, quality_label, issues, stats, created_at } = result;
  const labelTone = toneForLabel(quality_label);

  return (
    <div className="result-card">
      <img className="result-image" src={resolveImageUrl(image_url)} alt={original_filename} />

      <div className="result-details">
        <div className="result-header">
          <div>
            <h3 title={original_filename}>{original_filename}</h3>
            <p className="result-meta">{new Date(created_at).toLocaleString()}</p>
          </div>
          <ScoreRing score={quality_score} tone={labelTone} />
        </div>

        <Badge text={quality_label} tone={labelTone} withIcon />

        <h4>Detected Issues</h4>
        {issues.length === 0 ? (
          <p className="no-issues">
            <Icon name="check" size={15} /> No issues detected.
          </p>
        ) : (
          <ul className="issue-list">
            {issues.map((issue) => (
              <li key={issue.type} className={`issue-item issue-item-${toneForSeverity(issue.severity)}`}>
                <span className="issue-icon">
                  <Icon name={iconForIssueType(issue.type)} size={16} />
                </span>
                <span className="issue-type">{issue.type.replace(/_/g, " ")}</span>
                <Badge text={issue.severity} tone={toneForSeverity(issue.severity)} />
                <span className="issue-confidence">{Math.round(issue.confidence * 100)}% confidence</span>
              </li>
            ))}
          </ul>
        )}

        <h4>Image Statistics</h4>
        <div className="stats-grid">
          {Object.entries(stats).map(([key, value]) => (
            <div key={key} className="stat-item">
              <span className="stat-label">{key}</span>
              <span className="stat-value">{value}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
