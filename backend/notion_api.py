from datetime import datetime
from notion_client import Client
import os
from flask import Flask, request, jsonify
from write_notion import write_to_notion

# 初始化 Flask 應用，用於接收語音轉文字後的資料並寫入 Notion
app = Flask(__name__)

def fill_missing_fields(data):
    fields = ["env", "method", "weather", "action", "status", "abnormal", "mood"]
    return {field: data.get(field, "無資料") for field in fields}

@app.route("/summary", methods=["POST"])
def summary():
    audio_data = request.files.get("audio")
    if not audio_data:
        return jsonify({"error": "No audio file provided"}), 400

    # 假設這裡有語音分析及分類的邏輯，結果存在 classification_result
    classification_result = {
        # 範例資料，實際應由語音分析結果產生
        "env": "溫室",
        "method": "高架",
        "weather": "晴天",
        "action": "澆水",
        "status": "健康",
        "abnormal": "無",
        "mood": "安心"
    }

    # 補齊欄位
    filled_data = fill_missing_fields(classification_result)

    try:
        notion_id = write_to_notion(filled_data)
        return {"status": "success", "notion_page_id": notion_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

@app.route("/", methods=["GET"])
def home():
    return "🧪 農友日記 API 啟動成功"


# Notion client and database setup
notion = Client(auth=os.getenv("NOTION_API_KEY"))
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

def get_data_for_month(month_str: str):
    from datetime import timedelta

    # Define the first day of the month in ISO format
    start = f"{month_str}-01T00:00:00.000Z"
    
    # Compute the first day of the next month
    month_dt = datetime.strptime(month_str, "%Y-%m")
    if month_dt.month == 12:
        next_month = month_dt.replace(year=month_dt.year + 1, month=1)
    else:
        next_month = month_dt.replace(month=month_dt.month + 1)
    end = next_month.strftime("%Y-%m-%dT00:00:00.000Z")

    print(f"🔎 get_data_for_month: start={start}, end={end}")

    response = notion.databases.query(
        **{
            "database_id": DATABASE_ID,
            "filter": {
                "property": "日期",
                "date": {
                    "on_or_after": start,
                    "before": end,
                },
            },
            "page_size": 10
        }
    )
    results = response["results"]
    print(f"🔎 篩選到 {month_str} 的資料筆數：{len(results)}")
    return results

def get_prev_month(month_str: str):
    date = datetime.strptime(month_str + "-01", "%Y-%m-%d")
    if date.month == 1:
        prev = date.replace(year=date.year - 1, month=12)
    else:
        prev = date.replace(month=date.month - 1)
    return prev.strftime("%Y-%m")
