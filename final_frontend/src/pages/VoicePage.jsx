import React, { useState, useEffect } from "react";
import VoiceRecorder from "../components/VoiceRecorder";

const VoicePage = () => {
  const [transcript, setTranscript] = useState("");
  const [status, setStatus] = useState("");

  const sendToNotion = async (text) => {
    try {
      const res = await fetch('http://127.0.0.1:5003/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: text }),
      });
      const data = await res.json();
      if (data.notion_url) {
        setStatus(`✅ 已寫入 Notion：${data.notion_url}`);
      } else {
        setStatus(`❌ 寫入失敗：${data.error || '未知錯誤'}`);
      }
    } catch (err) {
      setStatus(`❌ 送到 Notion 失敗：${err.message}`);
    }
  };

  useEffect(() => {
    if (transcript) {
      sendToNotion(transcript);
      setTranscript(""); // 清空，避免重複送
    }
  }, [transcript]);

  return (
    <div className="min-h-screen bg-[var(--bg-color)] flex items-center justify-center px-4 py-6">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-6 sm:p-8">
        <div className="flex flex-col sm:flex-row items-center justify-center mb-6 space-y-2 sm:space-y-0 sm:space-x-4">
          <img src="/所有草莓人-07拷貝.png" alt="Logo" className="h-12 w-auto" />
          <h1 className="text-2xl sm:text-3xl font-bold tracking-wide text-[#404040] text-center">
            開始錄音吧
          </h1>
          <img src="/所有草莓人-07拷貝.png" alt="Logo" className="h-12 w-auto" />
        </div>

        <div className="flex justify-center mb-4">
          <VoiceRecorder onTranscriptChange={setTranscript} />
        </div>

        {!transcript && (
          <p className="text-gray-400 text-center text-sm sm:text-base mb-4 px-2">
            點擊上方按鈕開始錄音，我會幫你轉成文字
          </p>
        )}

        {transcript && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
            <p className="font-medium text-gray-700 mb-2">辨識結果：</p>
            <p className="text-green-800 font-mono leading-relaxed">{transcript}</p>
          </div>
        )}

        {status && (
          <p
            className={`text-center font-medium ${
              status.startsWith("✅") ? "text-green-600" : "text-red-600"
            } mb-2`}
          >
            {status}
          </p>
        )}

        <div className="flex justify-center mt-4">
          <a
            href="/dashboard"
            className="btn-login px-4 sm:px-6 py-2 rounded-full text-white font-semibold transition"
          >
            查看儀表板
          </a>
        </div>
      </div>
    </div>
  );
};

export default VoicePage;