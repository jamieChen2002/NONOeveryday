from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import whisper
import tempfile
import os
from dotenv import load_dotenv
from notion_client import Client
from datetime import datetime
from collections import Counter, defaultdict
import json

import google.generativeai as genai
from notion_client import Client as NotionClient
from datetime import date, timedelta, datetime

# Initialize Gemini API client
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
notion = NotionClient(auth=os.getenv("NOTION_API_KEY"))
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

from write_notion import write_to_notion
from notion_api import get_data_for_month, get_prev_month
from gpt_summary import generate_insights

load_dotenv()
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
print("🔍 (app.py) NOTION_API_KEY:", os.getenv("NOTION_API_KEY"))
print("🔍 (app.py) DATABASE_ID:", os.getenv("NOTION_DATABASE_ID"))

notion = Client(auth=os.getenv("NOTION_API_KEY"))
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
print("🔍 (app.py) DATABASE_ID (變數):", DATABASE_ID)

def get_all_pages_for_month(month_str):
    """一次撈回當月所有 Notion 頁面（自動分頁）。"""
    year, month = parse_month_str(month_str)
    start = date(year, month, 1)
    end = (start + timedelta(days=32)).replace(day=1)
    all_results = []
    start_cursor = None
    while True:
        query = {
            "database_id": DATABASE_ID,
            "filter": {
                "property": "日期",
                "date": {"on_or_after": start.isoformat(), "before": end.isoformat()}
            },
            "page_size": 100,
            "sorts": [{"property": "日期", "direction": "ascending"}]
        }
        if start_cursor:
            query["start_cursor"] = start_cursor
        resp = notion.databases.query(**query)
        all_results.extend(resp.get("results", []))
        if not resp.get("has_more"):
            break
        start_cursor = resp.get("next_cursor")
    return all_results

app = FastAPI()

origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def parse_month_str(month_str):
    dt = datetime.strptime(month_str, "%Y-%m")
    return dt.year, dt.month

class SaveRequest(BaseModel):
    content: str

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
    try:
        notion_url = write_to_notion(data)
        return {"notion_url": notion_url}
    except Exception as e:
        print("❌ Notion 寫入失敗：", e)
        return {"error": str(e)}

@app.post("/save")
def save_content(req: SaveRequest):
    try:
        notion_url = write_to_notion(req.content)
        return {"notion_url": notion_url}
    except Exception as e:
        print("❌ Notion 寫入失敗：", e)
        return {"error": str(e)}

@app.post("/transcribe")
def transcribe_audio(audio: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio.file.read())
            tmp_path = tmp.name

        model = whisper.load_model("base", download_root="/tmp")
        result = model.transcribe(tmp_path, language="zh")
        return {"text": result["text"]}
    except Exception as e:
        return {"error": str(e)}

def simplify_record(page):
    try:
        props = page.get("properties", {})
        abnormal = props.get("異常狀態", {}).get("rich_text", [])
        abnormal_text = abnormal[0]["text"]["content"] if abnormal and abnormal[0].get("text") else ""
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

        date_val = None
        if "日期" in props and "date" in props["日期"] and props["日期"]["date"]:
            date_val = props["日期"]["date"].get("start")
        cost_val = props.get("成本備註", {}).get("number") or 0
        income_val = props.get("收入概估", {}).get("number") or 0

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
        return record
    except Exception as e:
        print("❌ simplify_record 解析失敗，異常原因：", e)
        return {
            "date": None, "cost": 0, "income": 0, "pest": False,
            "pest_detail": [], "category": "", "abnormal": "",
            "cost_detail": [], "income_detail": []
        }

# --- Dashboard Helper Functions ---
def fetch_monthly_stats(month_str):
    results = get_all_pages_for_month(month_str)
    total_income = 0
    total_cost = 0
    pest_count = 0
    for page in results:
        props = page["properties"]
        income = props.get("收入概估", {}).get("number") or 0
        cost   = props.get("成本備註", {}).get("number") or 0
        anomaly = props.get("異常狀態", {}).get("rich_text") or []
        total_income += income
        total_cost   += cost
        if anomaly and any(r["plain_text"].strip() for r in anomaly):
            pest_count += 1
    return {"income": total_income, "cost": total_cost, "pest": pest_count}

def calc_pct_change(curr: int, prev: int):
    if prev == 0:
        return None
    return round((curr - prev) / prev * 100, 1)

def get_three_indicators(month_str):
    year, month = parse_month_str(month_str)
    curr = fetch_monthly_stats(month_str)
    # 計算上個月
    if month == 1:
        prev_year, prev_month = year - 1, 12
    else:
        prev_year, prev_month = year, month - 1
    prev_month_str = f"{prev_year}-{str(prev_month).zfill(2)}"
    prev = fetch_monthly_stats(prev_month_str)
    return {
        "income": {
            "value": curr["income"],
            "pct": calc_pct_change(curr["income"], prev["income"])
        },
        "cost": {
            "value": curr["cost"],
            "pct": calc_pct_change(curr["cost"], prev["cost"])
        },
        "pest": {
            "value": curr["pest"],
            "pct": calc_pct_change(curr["pest"], prev["pest"])
        }
    }

def fetch_daily_costs(month_str):
    year, month = parse_month_str(month_str)
    start = date(year, month, 1)
    end = (start + timedelta(days=32)).replace(day=1)
    daily_costs = []
    d = start
    while d < end:
        results = get_all_pages_for_month(month_str)
        day_cost = sum(
            page["properties"].get("成本備註", {}).get("number", 0) for page in results
            if page["properties"]["日期"]["date"] and page["properties"]["日期"]["date"]["start"][:10] == d.isoformat()
        )
        daily_costs.append(day_cost)
        d += timedelta(days=1)
    return daily_costs

def check_alerts(month_str):
    indicators = get_three_indicators(month_str)
    pest_pct = indicators["pest"]["pct"]
    alerts = []
    if pest_pct is not None and pest_pct > 50:
        alerts.append(f"病蟲害筆數較上月增加 {pest_pct}%，請注意防治。")

    daily_costs = fetch_daily_costs(month_str)
    if daily_costs:
        avg = sum(daily_costs) / len(daily_costs)
        for idx, c in enumerate(daily_costs, start=1):
            if c > avg * 2:
                alerts.append(f"{month_str} 第 {idx} 天單日成本 {c} 元，遠高於平均 {avg:.1f} 元。")
                break

    results = get_all_pages_for_month(month_str)
    year, month = parse_month_str(month_str)
    start = date(year, month, 1)
    end = (start + timedelta(days=32)).replace(day=1)
    dates_with_records = {page["properties"]["日期"]["date"]["start"][:10] for page in results if page["properties"]["日期"]["date"]}
    missing_streak = 0
    d = start
    while d < end:
        if d.isoformat() not in dates_with_records:
            missing_streak += 1
            if missing_streak >= 3:
                alerts.append(f"{month_str} 有連續 3 天以上無日誌記錄。")
                break
        else:
            missing_streak = 0
        d += timedelta(days=1)

    return alerts

def build_summary_prompt(month_str):
    stats = fetch_monthly_stats(month_str)
    alert_msgs = check_alerts(month_str)
    year, month = parse_month_str(month_str)
    prompt = f"""
請依下列農務月度重點，以繁體中文撰寫段落式摘要，包含整體營收/成本概況、病蟲害情況、天氣影響及建議：
• 年月：{year} 年 {month} 月
• 總收入：{stats['income']} 元
• 總成本：{stats['cost']} 元
• 病蟲害筆數：{stats['pest']} 次
• 主要異常警示：{"；".join(alert_msgs) if alert_msgs else "無"}
• 其他簡要說明：本月天氣偏多雨，土壤排水不良；花期為 {year}/{month}/15 ~ {year}/{month}/20
"""
    return prompt.strip()

def generate_monthly_summary(month_str):
    # 先取得該月的統計數字
    stats = fetch_monthly_stats(month_str)
    try:
        # 嘗試呼叫 Gemini 生成摘要
        prompt = build_summary_prompt(month_str)
        response = genai.chat.create(
            model="models/text-bison-001",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response["candidates"][0]["content"]
    except Exception:
        # 若 AI 產生失敗，就回傳最基本的 fallback 文字
        income = stats.get("income", 0)
        cost = stats.get("cost", 0)
        pest = stats.get("pest", 0)
        return f"本月總收入：{income} 元；總成本：{cost} 元；病蟲害筆數：{pest} 次。"

@app.get("/api/dashboard")
def get_dashboard(month: str = None):
    if not month:
        month = datetime.now().strftime("%Y-%m")
    prev_month = get_prev_month(month)

    pages = get_all_pages_for_month(month)
    prev_pages = get_all_pages_for_month(prev_month)

    records = []
    for p in pages:
        record = simplify_record(p)
        records.append(record)

    total_cost = sum(r["cost"] for r in records)
    total_income = sum(r["income"] for r in records)
    pest_count = sum(1 for r in records if r["pest"])
    record_count = len(records)

    detail_counter = Counter()
    category_counter = Counter()
    cost_detail_counter = Counter()
    income_detail_counter = Counter()
    category_money = defaultdict(float)
    income_money = defaultdict(float)
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
        # 收入拆標籤分配金額
        incomes = r.get("income_detail", [])
        income_amount = r.get("income", 0)
        if incomes:
            share_i = income_amount / len(incomes)
            for inc in incomes:
                income_money[inc] += share_i
        if r["date"]:
            daily_record_counter[r["date"]] += 1
            if r["pest"]:
                daily_pest_counter[r["date"]] += 1

    try:
        summary_this = generate_monthly_summary(month)
        summary_prev = generate_monthly_summary(prev_month)
        ai_summary = {
            month: summary_this,
            prev_month: summary_prev
        }
    except Exception as e:
        print("🧨 AI 摘要產生失敗：", e)
        ai_summary = {
            month: "AI 摘要失敗，請檢查資料格式或內容。",
            prev_month: "AI 摘要失敗，請檢查資料格式或內容。"
        }

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
        "income_money_detail": [{"name": k, "value": round(v, 1)} for k, v in income_money.items()],
        "daily_counts": [{"date": k, "count": v} for k, v in sorted(daily_record_counter.items())],
        "daily_pest_counts": [{"date": k, "count": v} for k, v in sorted(daily_pest_counter.items())],
        "ai_summary": ai_summary,
        "summary": ai_summary.get(month, "")
    }

# --- Dashboard Indicator/Alerts/Summary Endpoints ---
@app.get("/api/dashboard/indicators")
def api_three_indicators(month: str = None):
    if not month:
        month = datetime.now().strftime("%Y-%m")
    # 先取三大指標
    indicators = get_three_indicators(month)
    # 再取 Dashboard 所有統計明細（cost_detail、income_detail、cost_money_detail、pest_detail、daily_counts、daily_pest_counts）
    dashboard = get_dashboard(month)
    # 將三大指標併入 dashboard 結果中
    result = dict(dashboard)
    result["indicators"] = indicators
    return result

@app.get("/api/dashboard/alerts")
def api_alerts(month: str = None):
    if not month:
        month = datetime.now().strftime("%Y-%m")
    return {"alerts": check_alerts(month)}

@app.get("/api/dashboard/summary")
def api_summary(month: str = None):
    if not month:
        month = datetime.now().strftime("%Y-%m")
    return {"summary": generate_monthly_summary(month)}

# --- Pest Advice Route ---
from fastapi import Query
import requests

@app.get("/api/pest_advice")
def get_pest_advice(pests: str = Query(..., description="以逗號或頓號分隔的病蟲害名稱")):
    """
    接收前端傳來的 pests 字串，例如 "白粉病,灰黴病,葉斑病"。將其拆分成 list，
    再依序對每個病蟲害名稱呼叫 Brave Search API 取得防治建議。
    """
    from collections import Counter

    # 印出 debug 訊息，確認後端收到的參數
    print(f"[DEBUG] Received pests parameter: {pests}")

    # 將頓號替換成逗號，並拆分成清單，忽略空字串
    raw_list = [s.strip() for s in pests.replace("、", ",").split(",") if s.strip()]
    if not raw_list:
        return {"results": []}

    all_results = []
    for pest_name in raw_list:
        # 若名稱開頭有「草莓」，先去除，避免重複
        search_target = pest_name
        if search_target.startswith("草莓"):
            search_target = search_target.replace("草莓", "", 1).strip()

        # 每個病蟲害名稱都去呼叫 Brave Search API 搜尋前 3 筆結果
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": BRAVE_API_KEY,
        }
        query_text = f"草莓 {search_target} 防治 建議"
        params = {"q": query_text, "count": 3}
        try:
            response = requests.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers=headers,
                params=params,
                timeout=5000
            )
            if response.status_code == 200:
                data = response.json()
                for item in data.get("web", {}).get("results", []):
                    all_results.append({
                        "pest": pest_name,
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "description": item.get("description", "")
                    })
        except Exception as e:
            print(f"[WARN] Brave API error for '{pest_name}': {e}")

    return {"results": all_results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5003, reload=True)
