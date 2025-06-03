import React, { useState, useEffect, useRef } from "react";

const VoicePage = () => {
  const [transcript, setTranscript] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" });
        const formData = new FormData();
        formData.append("audio", audioBlob, "recording.webm");

        try {
          const res = await fetch("http://127.0.0.1:5003/transcribe", {
            method: "POST",
            body: formData,
          });
          const data = await res.json();
          if (data.text) {
            setTranscript(data.text);
          } else {
            alert("❌ 語音辨識失敗");
          }
        } catch (err) {
          console.error(err);
          alert("❌ 錯誤：無法傳送語音");
        }
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (err) {
      console.error(err);
      alert("❌ 無法啟動麥克風錄製，請檢查權限");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const handleSubmit = async () => {
    if (!transcript.trim()) {
      alert("❗ 請先輸入文字或錄音取得內容再送出");
      return;
    }
    setIsSubmitting(true);
    try {
      const res = await fetch("http://127.0.0.1:5003/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: transcript }),
      });
      if (res.ok) {
        alert("✅ 已成功送出到 Notion");
        setTranscript("");
      } else {
        alert("❌ 送出失敗，請稍後再試");
      }
    } catch (err) {
      console.error(err);
      alert("❌ 錯誤：無法連線到後端");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-2 text-[#c9403e]">語音辨識</h1>
      <button
        onClick={isRecording ? stopRecording : startRecording}
        className={`btn-login mb-4 px-4 py-2 rounded text-white ${isRecording ? 'bg-green-700 hover:bg-green-800' : ''}`}
      >
        {isRecording ? "停止錄音" : "開始錄音"}
      </button>

      <div className="mt-4 p-2 border border-gray-300">
        <label htmlFor="editedTranscript" className="block font-medium mb-1">
          手動輸入（或保留上方錄音結果）：
        </label>
        <textarea
          id="editedTranscript"
          className="w-full p-2 border border-gray-300 rounded"
          rows={4}
          value={transcript}
          onChange={(e) => setTranscript(e.target.value)}
          placeholder="請在此輸入文字，或使用上方按鈕進行語音輸入然後再編輯"
        />
        <button
          onClick={handleSubmit}
          disabled={isSubmitting}
          className={`btn-login mt-2 px-4 py-2 rounded text-white ${isSubmitting ? 'bg-gray-400' : ''}`}
        >
          {isSubmitting ? "送出中…" : "送出至 Notion"}
        </button>
      </div>
    </div>
  );
};

export default VoicePage;
