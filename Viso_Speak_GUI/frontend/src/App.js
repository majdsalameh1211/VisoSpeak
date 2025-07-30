import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

// Import pages
import HomePage from "./pages/HomePage";
import LipNetEndToEnd from "./pages/LipNetEndToEnd";
import TransformerEndToEnd from "./pages/TransformerEndToEnd";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/LipNetEndToEnd" element={<LipNetEndToEnd />} />
        <Route path="/TransformerEndToEnd" element={<TransformerEndToEnd />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
