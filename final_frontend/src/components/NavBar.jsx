import React, { useState } from "react";
import { Link } from "react-router-dom";

const NavBar = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  return (
    <header className="navbar-bar w-full text-[#fefae5] shadow-md rounded-b-lg">
      <nav className="max-w-screen-xl mx-auto px-6 py-4 flex flex-wrap justify-between items-center">
        <div className="flex items-center">
          <img src="/所有草莓人-14拷貝.png" alt="Logo" className="h-10 w-auto mr-4" />
          <div className="text-2xl font-bold tracking-wide">NONO小農語音日記</div>
        </div>
        <div className="flex flex-col md:flex-row md:space-x-4 space-y-2 md:space-y-0 mt-2 md:mt-0">
          <div className="relative">
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="bg-transparent text-[#fefae5] font-semibold hover:text-[#c0d65b] transition duration-300"
            >
              功能選單 ▾
            </button>
            {menuOpen && (
              <div className="absolute left-0 mt-2 w-32 bg-[#b75151] rounded shadow-lg flex flex-col z-10">
                <Link
                  to="/"
                  className="px-4 py-2 text-[#fefae5] hover:text-[#c0d65b] hover:bg-[#a63e3e] transition duration-200 whitespace-nowrap"
                >
                  錄音日記
                </Link>
                <Link
                  to="/dashboard"
                  className="px-4 py-2 text-[#fefae5] hover:text-[#c0d65b] hover:bg-[#a63e3e] transition duration-200 whitespace-nowrap"
                >
                  儀表板
                </Link>
              </div>
            )}
          </div>
          {/* 之後如有上傳頁，可改成 <Link to="/upload">上傳</Link> */}
        </div>
      </nav>
    </header>
  );
};

export default NavBar;