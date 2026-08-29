import { useRef, useState } from "react";
import { analyzeImage } from "../api";
import Icon from "./Icon";
import ResultCard from "./ResultCard";

export default function UploadPanel() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [status, setStatus] = useState("idle"); // idle | loading | success | error
  const [result, setResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef(null);

  function selectFile(selected) {
    if (!selected) return;
    setFile(selected);
    setPreviewUrl(URL.createObjectURL(selected));
    setResult(null);
    setStatus("idle");
  }

  function handleFileInput(event) {
    selectFile(event.target.files[0]);
  }

  function handleDrop(event) {
    event.preventDefault();
    setIsDragOver(false);
    selectFile(event.dataTransfer.files[0]);
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
      <div
        className={`dropzone ${isDragOver ? "dropzone-active" : ""} ${previewUrl ? "dropzone-filled" : ""}`}
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragOver(true);
        }}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileInput}
          className="dropzone-input"
        />

        {previewUrl ? (
          <div className="dropzone-preview">
            <img src={previewUrl} alt="Selected preview" />
            <div className="dropzone-preview-overlay">
              <Icon name="upload" size={22} />
              <span>Choose a different image</span>
            </div>
          </div>
        ) : (
          <div className="dropzone-empty">
            <span className="dropzone-icon">
              <Icon name="upload" size={26} />
            </span>
            <p className="dropzone-title">Drag &amp; drop an image, or click to browse</p>
            <p className="dropzone-hint">JPEG, PNG, WebP or BMP — up to 10MB</p>
          </div>
        )}
      </div>

      <button className="analyze-button" onClick={handleAnalyze} disabled={!file || status === "loading"}>
        {status === "loading" ? (
          <>
            <span className="spinner" />
            Analyzing...
          </>
        ) : (
          <>
            <Icon name="zap" size={16} />
            Analyze Image
          </>
        )}
      </button>

      {status === "error" && (
        <p className="error-banner">
          <Icon name="alert" size={16} />
          {errorMessage}
        </p>
      )}
      {status === "success" && result && <ResultCard result={result} />}
    </div>
  );
}
