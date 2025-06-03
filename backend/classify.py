from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def classify_text(text: str) -> dict:
    prompt = f"""
請根據以下農友日記內容，自動提取並填寫下列欄位（若無資訊可填寫空字串）：
📅 時間：
🛖 環境：
🪴 種植方式：
🌤 氣候狀況：
🌱 農事行動：
🌾 作物狀態：
🐛 異常現象：
🧠 心情與觀察：
📌 備註事件：
💸 成本紀錄：
🧺 收成量：
🤝 銷售方式：
💵 銷售價格：
📊 收入概估：
🧾 成本備註：

日記內容如下：
{text}

請以 JSON 格式回傳。
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    
    import json
    try:
        output = json.loads(response.choices[0].message.content)
        key_map = {
            "📅 時間": "date",
            "🛖 環境": "env",
            "🪴 種植方式": "method",
            "🌤 氣候狀況": "weather",
            "🌱 農事行動": "action",
            "🌾 作物狀態": "status",
            "🐛 異常現象": "abnormal",
            "🧠 心情與觀察": "mood",
            "📌 備註事件": "notes",
            "💸 成本紀錄": "cost_note",
            "🧺 收成量": "yield_amount",
            "🤝 銷售方式": "sale_method",
            "💵 銷售價格": "sale_price",
            "📊 收入概估": "income_estimate",
            "🧾 成本備註": "cost_amount"
        }
        converted = {key_map.get(k, k): v for k, v in output.items()}
        return converted
    except Exception:
        output = {"錯誤": "無法解析 GPT 回應"}
        return output