import { useState } from "react";
import { analyzeImage } from "../api";
import ResultCard from "./ResultCard";

export default function UploadPanel() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [status, setStatus] = useState("idle"); // idle | loading | success | error
  const [result, setResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  function handleFileSelect(event) {
    const selected = event.target.files[0];
    if (!selected) return;
    setFile(selected);
    setPreviewUrl(URL.createObjectURL(selected));
    setResult(null);
    setStatus("idle");
  }

  async function handleAnalyze() {
    if (!file) return;
    setStatus("loading");
    setErrorMessage("");
    try {
      const analysis = await analyzeImage(file);
      setResult(analysis);
      setStatus("success");
    } catch (error) {
      setErrorMessage(error.message);
      setStatus("error");
    }
  }

  return (
    <div className="upload-panel">
      <div className="upload-box">
        <label className="file-picker">
          <input type="file" accept="image/*" onChange={handleFileSelect} />
          {previewUrl ? "Choose a different image" : "Choose an image"}
        </label>

        {previewUrl && <img className="preview-image" src={previewUrl} alt="Selected preview" />}

        <button className="analyze-button" onClick={handleAnalyze} disabled={!file || status === "loading"}>
          {status === "loading" ? "Analyzing..." : "Analyze Image"}
        </button>
      </div>

      {status === "error" && <p className="error-banner">{errorMessage}</p>}
      {status === "success" && result && <ResultCard result={result} />}
    </div>
  );
}
