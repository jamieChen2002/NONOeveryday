import requests

# 要傳送到 Notion 的十筆文字內容清單
entries = [
    "測試資料 1：草莓田地澆水記錄",
    "測試資料 2：香瓜田地施肥記錄",
    "測試資料 3：今日氣候晴朗",
    "測試資料 4：發現病蟲害，已噴防治藥劑",
    "測試資料 5：草莓採收量 50kg，收入約 5000 元",
    "測試資料 6：香瓜採收量 30kg，收入約 3000 元",
    "測試資料 7：今日成本記錄：肥料 200 元、勞務 300 元",
    "測試資料 8：今日心情良好，作業進度順利",
    "測試資料 9：檢查滴灌系統，有少量漏水已修復",
    "測試資料 10：進行田間除草，耗時 2 小時"
]

url = "http://localhost:5001/save"  # 後端 /save 端點
headers = {"Content-Type": "application/json"}

for idx, text in enumerate(entries, start=1):
    payload = {"content": text}
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            print(f"✅ 第 {idx} 筆送出成功：Notion URL = {data.get('notion_url')}")
        else:
            print(f"❌ 第 {idx} 筆送出失敗，狀態碼：{resp.status_code}，回應：{resp.text}")
    except Exception as e:
        print(f"❌ 第 {idx} 筆請求例外：", e)