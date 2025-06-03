from fastapi import FastAPI
app = FastAPI()
from fastapi import UploadFile, File
import whisper
import tempfile
import os
import requests
from write_notion import write_to_notion
from notion_client import Client
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()
print("🔍 (app.py) NOTION_API_KEY:", os.getenv("NOTION_API_KEY"))
print("🔍 (app.py) DATABASE_ID:", os.getenv("NOTION_DATABASE_ID"))

# 新增印出 DATABASE_ID 變數
notion = Client(auth=os.getenv("NOTION_API_KEY"))
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
print("🔍 (app.py) DATABASE_ID (變數):", DATABASE_ID)

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

class SaveRequest(BaseModel):
    content: str

app = FastAPI()
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API 正常運作中"}

@app.post("/diary")
def handle_diary(
    env: str = Form(...),
    action: str = Form(...),
    method: str = Form(""),
    weather: str = Form(""),
    status: str = Form(""),
    abnormal: str = Form(""),
    mood: str = Form(""),
    notes: str = Form(""),
    cost_note: str = Form(""),
    sale_method: str = Form(""),
    yield_amount: str = Form(""),
    date: str = Form(""),
    sale_price: float = Form(0),
    cost_amount: str = Form(""),
    income_estimate: float = Form(0),
):
    print("📥 收到的資料：", env, action, date)
    print("📊 DEBUG: env =", env)
    data = {
        "env": env,
        "action": action,
        "method": method,
        "weather": weather,
        "status": status,
        "abnormal": abnormal,
        "mood": mood,
        "notes": notes,
        "cost_note": cost_note,
        "sale_method": sale_method,
        "yield_amount": yield_amount,
        "date": date,
        "sale_price": sale_price,
        "cost_amount": cost_amount,
        "income_estimate": income_estimate
    }
    print("📦 寫入 Notion 的資料：", data)
    print("📦 寫入 Notion 的資料內容（完整）：", data)
   
    try:
        notion_url = write_to_notion(data)
        return {"notion_url": notion_url}
    except Exception as e:
        print("❌ Notion 寫入失敗：", e)
        return {"error": str(e)}


# 新增 /save endpoint
@app.post("/save")
def save_content(req: SaveRequest):
    try:
        # You can wrap the content into a dictionary or pass directly if your write_to_notion supports it
        notion_url = write_to_notion(req.content)
        return {"notion_url": notion_url}
    except Exception as e:
        print("❌ Notion 寫入失敗：", e)
        return {"error": str(e)}


# Whisper 語音轉文字 API
@app.post("/transcribe")
def transcribe_audio(audio: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio.file.read())
            tmp_path = tmp.name

        model = whisper.load_model("base")
        result = model.transcribe(tmp_path, language="zh")
        return {"text": result["text"]}
    except Exception as e:
        return {"error": str(e)}


def fetch_diary_records():
    try:
        response = notion.databases.query(database_id=DATABASE_ID)
        print("📥 Notion 回傳資料：", response)
        return response["results"]
    except Exception as e:
        print("❌ 讀取 Notion 資料庫失敗：", e)
        return []

def simplify_record(page):
    try:
        props = page.get("properties", {})
        abnormal = props.get("異常狀態", {}).get("rich_text", [])
        abnormal_text = abnormal[0]["text"]["content"] if abnormal and abnormal[0].get("text") else ""
        pest_keywords = ["灰黴病", "炭疽病", "白粉病", "萎凋病", "斑點病", "紅蜘蛛", "蚜蟲", "介殼蟲", "枯萎", "蟲", "病", "異常"]
        ignore_keywords = ["無", "正常", "無異常", "健康", "ok", "沒有", "尚可"]
        detail = []
        if abnormal_text.strip() and abnormal_text.strip().lower() not in ignore_keywords:
            detail.append(abnormal_text)
        category = props.get("作物狀態", {}).get("rich_text", [])
        category_text = category[0]["text"]["content"] if category and category[0].get("text") else ""
        cost_detail_raw = props.get("成本紀錄", {}).get("rich_text", [])
        cost_detail_text = cost_detail_raw[0]["text"]["content"] if cost_detail_raw and cost_detail_raw[0].get("text") else ""
        cost_detail_list = [item.strip() for item in cost_detail_text.split(",") if item.strip()]
        income_detail_raw = props.get("銷售方式", {}).get("rich_text", [])
        income_detail_text = income_detail_raw[0]["text"]["content"] if income_detail_raw and income_detail_raw[0].get("text") else ""
        income_detail_list = [item.strip() for item in income_detail_text.split(",") if item.strip()]

        # 日期防呆
        date_val = None
        if "日期" in props and "date" in props["日期"] and props["日期"]["date"]:
            date_val = props["日期"]["date"].get("start")
        # 金額防呆
        cost_val = props.get("成本備註", {}).get("number")
        if cost_val is None:
            cost_val = 0
        income_val = props.get("收入概估", {}).get("number")
        if income_val is None:
            income_val = 0

        record = {
            "date": date_val,
            "cost": cost_val,
            "income": income_val,
            "pest": bool(detail),
            "pest_detail": detail,
            "category": category_text,
            "abnormal": abnormal_text,
            "cost_detail": cost_detail_list,
            "income_detail": income_detail_list
        }
        print("📘 轉換後記錄：", record)
        return record
    except Exception as e:
        print("❌ simplify_record 解析失敗，異常原因：", e)
        # 強制回傳一筆空記錄，避免 crash
        return {
            "date": None, "cost": 0, "income": 0, "pest": False,
            "pest_detail": [], "category": "", "abnormal": "",
            "cost_detail": [], "income_detail": []
        }

from notion_api import get_data_for_month, get_prev_month
from gpt_summary import generate_insights

@app.get("/api/dashboard")
def get_dashboard(month: str = None):
    if not month:
        month = datetime.now().strftime("%Y-%m")
    prev_month = get_prev_month(month)

    print("✅ 月份查詢：", month)
    pages = get_data_for_month(month)
    print("✅ 本月資料頁面數量：", len(pages))
    print("📄 頁面範例（第 1 筆）：", pages[0] if pages else "無資料")
    prev_pages = get_data_for_month(prev_month)
    print("✅ 上月資料頁面數量：", len(prev_pages))

    import json

    records = []
    for i, p in enumerate(pages):
        try:
            record = simplify_record(p)
            records.append(record)
        except Exception as e:
            print(f"❌ 第 {i+1} 筆資料處理錯誤：", e)
            print("🔍 問題頁面內容：", json.dumps(p, ensure_ascii=False, indent=2))

    total_cost = sum(r["cost"] for r in records)
    total_income = sum(r["income"] for r in records)
    pest_count = sum(1 for r in records if r["pest"])
    record_count = len(records)

    from collections import Counter, defaultdict

    detail_counter = Counter()
    category_counter = Counter()
    cost_detail_counter = Counter()
    income_detail_counter = Counter()
    category_money = defaultdict(float)
    daily_record_counter = defaultdict(int)
    daily_pest_counter = defaultdict(int)

    for r in records:
        detail_counter.update(r.get("pest_detail", []))
        if r.get("category"):
            category_counter[r["category"]] += 1
        cost_detail_counter.update(r.get("cost_detail", []))
        income_detail_counter.update(r.get("income_detail", []))
        categories = r.get("cost_detail", [])
        amount = r.get("cost", 0)
        if categories:
            share = amount / len(categories)
            for c in categories:
                category_money[c] += share
        if r["date"]:
            daily_record_counter[r["date"]] += 1
            if r["pest"]:
                daily_pest_counter[r["date"]] += 1

    try:
        print("🧠 本月摘要產生中...")
        summary_this = generate_insights(pages)
        print("🧠 上月摘要產生中...")
        summary_prev = generate_insights(prev_pages)
        ai_summary = {
            month: summary_this,
            prev_month: summary_prev
        }
    except Exception as e:
        print("🧨 AI 摘要產生失敗：", e)
        ai_summary = {
            month: "AI 摘要產生錯誤",
            prev_month: "AI 摘要產生錯誤"
        }

    print("🔢 成本總和：", total_cost)
    print("🔢 收入總和：", total_income)

    import json
    try:
        print("🟡 測試 json.dumps 輸出")
        print(json.dumps({
            "total_cost": total_cost,
            "total_income": total_income,
            "pest_count": pest_count,
            "record_count": record_count,
            "pest_detail": [{"name": k, "value": v} for k, v in detail_counter.items()],
            "category_detail": [{"name": k, "value": v} for k, v in category_counter.items()],
            "cost_detail": [{"name": k, "value": v} for k, v in cost_detail_counter.items()],
            "income_detail": [{"name": k, "value": v} for k, v in income_detail_counter.items()],
            "cost_money_detail": [{"name": k, "value": round(v, 1)} for k, v in category_money.items()],
            "daily_counts": [{"date": k, "count": v} for k, v in sorted(daily_record_counter.items())],
            "daily_pest_counts": [{"date": k, "count": v} for k, v in sorted(daily_pest_counter.items())],
            "ai_summary": ai_summary
        }, ensure_ascii=False))
    except Exception as e:
        print("🛑 json.dumps 爆炸：", e)

    return {
        "total_cost": total_cost,
        "total_income": total_income,
        "pest_count": pest_count,
        "record_count": record_count,
        "pest_detail": [{"name": k, "value": v} for k, v in detail_counter.items()],
        "category_detail": [{"name": k, "value": v} for k, v in category_counter.items()],
        "cost_detail": [{"name": k, "value": v} for k, v in cost_detail_counter.items()],
        "income_detail": [{"name": k, "value": v} for k, v in income_detail_counter.items()],
        "cost_money_detail": [{"name": k, "value": round(v, 1)} for k, v in category_money.items()],
        "daily_counts": [{"date": k, "count": v} for k, v in sorted(daily_record_counter.items())],
        "daily_pest_counts": [{"date": k, "count": v} for k, v in sorted(daily_pest_counter.items())],
        "ai_summary": ai_summary
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5003, reload=True)
