import os
from dotenv import load_dotenv
import json
from notion_client import Client

# ✅ 換成你的 Integration Token
load_dotenv()
notion = Client(auth=os.getenv("NOTION_TOKEN"))

# ✅ 換成你的資料庫 ID
database_id = "201a5eb3721f80909de3d70fe2a84bae"

db = notion.databases.retrieve(database_id=database_id)

# ➕ 防呆處理 icon 為 None 的情況
icon = db.get("icon")
emoji = icon.get("emoji") if icon and icon.get("type") == "emoji" else "（無）"

print("📒 資料庫 Emoji：", emoji)
print("🔍 Notion 資料庫欄位清單：")
for key, prop in db["properties"].items():
    print(f"- {key}（{prop['type']}）")

with open("notion_schema.json", "w", encoding="utf-8") as f:
    json.dump(db["properties"], f, indent=2, ensure_ascii=False)
print("✅ 資料庫欄位已儲存為 notion_schema.json")