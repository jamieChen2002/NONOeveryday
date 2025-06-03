import os
import whisper
from pathlib import Path
import tempfile
from typing import BinaryIO
from werkzeug.datastructures import FileStorage

def whisper_transcribe(file: FileStorage) -> str:
    """
    將語音檔案 (FileStorage) 使用 Whisper 模型轉為文字。
    
    Args:
        file (FileStorage): 來自 Flask 的上傳語音檔案物件
    
    Returns:
        str: 語音內容的轉換文字
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        file.save(tmp.name)
        return transcribe_audio(tmp.name)

# Whisper 模型載入（你可根據效能選 tiny / base / small / medium / large）
MODEL_NAME = os.getenv("WHISPER_MODEL", "small")
model = whisper.load_model(MODEL_NAME)

def transcribe_audio(file_path: str) -> str:
    """
    使用 OpenAI Whisper 模型將語音檔轉成文字。

    Args:
        file_path (str): 音訊檔案路徑 (.wav / .mp3 / .m4a / .webm 等)

    Returns:
        str: 轉換後的純文字內容
    """
    if not Path(file_path).exists():
        raise FileNotFoundError(f"找不到音訊檔案：{file_path}")

    print(f"🔍 開始轉換音訊：{file_path}")
    result = model.transcribe(file_path, language="zh")
    text = result.get("text", "")
    print(f"✅ 轉換完成：{text}")
    return text

# 若要測試：
if __name__ == "__main__":
    from pathlib import Path
    from backend.classify import classify_text  # 新增 import
    base_dir = Path(__file__).resolve().parent.parent
    test_path = str(base_dir / "data/test_audio.wav")
    output_text = transcribe_audio(test_path)
    print("📝 語音轉文字結果：", output_text)

    structured_result = classify_text(output_text)
    print("📊 結構化分類結果：", structured_result)
