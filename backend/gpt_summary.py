import os
from opencc import OpenCC  # 改用 opencc-python-reimplemented 提供的同名介面
cc = OpenCC('s2t')  # 簡體轉繁體

import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def gemini_summarize_text(text):
    if not text:
        return ""
    prompt = f"請將以下農務日誌內容，整理成不超過120字的月度摘要，重點統整農事、天氣、異常、收成、心情變化：\n\n{text}"
    try:
        response = genai.generate_text(
            model="gemini-1.5-flash",
            prompt=prompt,
            temperature=0.3,
            max_output_tokens=150,
        )
        # Gemini 回傳預設為簡體，轉繁體
        return cc.convert(response.result.strip())
    except Exception as e:
        print("🧨 Gemini 摘要過程發生錯誤：", e)
        return "AI 摘要失敗，請檢查資料格式或內容。"

def classify_text(text):
    """根據關鍵字分類農務紀錄"""
    if not isinstance(text, str):
        text = str(text)
    if "灑藥" in text or "農藥" in text:
        return "病蟲害"
    elif "施肥" in text:
        return "施肥"
    elif "巡田" in text:
        return "巡田"
    elif "澆水" in text:
        return "澆水"
    else:
        return "其他"

def extract_rich_text(page, field):
    arr = page.get("properties", {}).get(field, {}).get("rich_text", [])
    if arr and "plain_text" in arr[0]:
        return arr[0]["plain_text"]
    return ""

def generate_insights(notion_data):
    """接收 Notion 紀錄資料列表，產出摘要分析結果（繁體）"""
    print("🧠 開始分析 Notion 資料...")
    print("🧾 原始資料筆數：", len(notion_data))

    try:
        all_text = "\n".join([extract_rich_text(page, "心情與觀察") for page in notion_data])
        print("📝 擷取後文字長度：", len(all_text))
        print("📝 前 100 字：", all_text[:100])

        if not all_text.strip():
            return "無法產生摘要，資料不足或格式錯誤。"
        
        result = gemini_summarize_text(all_text)
        print("✅ Gemini 摘要完成")
        return result

    except Exception as e:
        print("🧨 Gemini 摘要過程發生錯誤：", e)
        return "AI 摘要失敗，請檢查資料格式或內容。"
