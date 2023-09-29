import ReactDOM from "react-dom/client";

import App from "./App";

import "./index.css";

const root = ReactDOM.createRoot(
  document.querySelector("body") as HTMLElement
);
root.render(
  <App />
);
