import { useState } from "react";
import UploadPanel from "./components/UploadPanel";
import HistoryPanel from "./components/HistoryPanel";
import Icon from "./components/Icon";
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState("analyze");

  return (
    <div className="app">
      <header className="app-header">
        <div className="app-brand">
          <span className="app-logo">
            <Icon name="camera" size={20} />
          </span>
          <div>
            <h1>Image Quality &amp; Defect Detector</h1>
            <p className="app-subtitle">AI-powered analysis for blur, exposure, noise &amp; defects</p>
          </div>
        </div>
        <nav className="tabs">
          <button
            className={activeTab === "analyze" ? "tab tab-active" : "tab"}
            onClick={() => setActiveTab("analyze")}
          >
            <Icon name="upload" size={15} />
            Analyze
          </button>
          <button
            className={activeTab === "history" ? "tab tab-active" : "tab"}
            onClick={() => setActiveTab("history")}
          >
            <Icon name="clock" size={15} />
            History
          </button>
        </nav>
      </header>

      <main className="app-main">{activeTab === "analyze" ? <UploadPanel /> : <HistoryPanel />}</main>
    </div>
  );
}

export default App;
