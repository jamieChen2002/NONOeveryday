// src/App.jsx
import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import NavBar from "./components/NavBar";
import Footer from "./components/Footer";
import VoicePage from "./pages/VoicePage";
import Dashboard from "./pages/Dashboard";

const App = () => {
  return (
    <BrowserRouter>
      {/* 全站最上方的導覽列 */}
      <NavBar />

      {/* 中間的主要內容區，根據路由顯示不同頁面 */}
      <div className="min-h-screen bg-[#fefae5] text-[#333] px-4 py-6">
        <Routes>
          <Route path="/" element={<VoicePage />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </div>

      {/* 全站最下方的頁腳 */}
      <Footer />
    </BrowserRouter>
  );
};

export default App;