import { useState } from "react";
import UploadPanel from "./components/UploadPanel";
import HistoryPanel from "./components/HistoryPanel";
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState("analyze");

  return (
    <div className="app">
      <header className="app-header">
        <h1>Image Quality &amp; Defect Detector</h1>
        <nav className="tabs">
          <button
            className={activeTab === "analyze" ? "tab tab-active" : "tab"}
            onClick={() => setActiveTab("analyze")}
          >
            Analyze
          </button>
          <button
            className={activeTab === "history" ? "tab tab-active" : "tab"}
            onClick={() => setActiveTab("history")}
          >
            History
          </button>
        </nav>
      </header>

      <main className="app-main">{activeTab === "analyze" ? <UploadPanel /> : <HistoryPanel />}</main>
    </div>
  );
}

export default App;
