import "@fontsource/space-grotesk/400.css";
import "@fontsource/space-grotesk/500.css";
import "@fontsource/space-grotesk/700.css";

import "@fontsource/inter/400.css";
import "@fontsource/inter/500.css";
import "@fontsource/inter/600.css";

import React from "react";
import ReactDOM from "react-dom/client";

import "./index.css";
import App from "./App";

import {
  AnalysisProvider,
} from "./context/AnalysisContext";

ReactDOM.createRoot(
  document.getElementById("root")
).render(
  <React.StrictMode>
    <AnalysisProvider>
      <App />
    </AnalysisProvider>
  </React.StrictMode>
);