#!/usr/bin/env bash

# -------------------------------------------------------------------
# 將以下兩行改成你的 Notion 整合 Token 與 Database ID
NOTION_API_KEY="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"
NOTION_DATABASE_ID="201a5eb3721f80909de3d70fe2a84bae"
# -------------------------------------------------------------------

# 每筆都將用同樣的 parent/database_id
BASE_URL="https://api.notion.com/v1/pages"
AUTH_HEADER="Authorization: Bearer ${NOTION_API_KEY}"
VERSION_HEADER="Notion-Version: 2022-06-28"
CONTENT_HEADER="Content-Type: application/json"


# 一筆筆列出 30 筆資料
# 環境 都寫「田間草莓區」，其餘欄位對應 5 月 1 日到 5 月 30 日的模擬資料
# 當回傳狀態為 200 或 201 即視為成功，否則列印失敗提醒

function upload_one() {
  local JSON_PAYLOAD="$1"
  local DATE="$2"

  HTTP_CODE=$(echo "$JSON_PAYLOAD" | curl -s -o /dev/null -w "%{http_code}" -X POST "${BASE_URL}" \
    -H "${AUTH_HEADER}" \
    -H "${VERSION_HEADER}" \
    -H "${CONTENT_HEADER}" \
    --data @-)

  if [ "$HTTP_CODE" == "200" ] || [ "$HTTP_CODE" == "201" ]; then
    echo "✔ 已建立：${DATE}"
  else
    echo "✘ 建立失敗：${DATE} (HTTP ${HTTP_CODE})"
  fi
}


# ------- 2025 April 模擬資料開始 -------
# 1. 2025-04-01
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-01" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"心情平穩" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"無異常" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"多雲" } }] },
    "備註事件": { "rich_text":[{ "text":{ "content":"花苞陸續冒出，苗勢穩定。" } }] }
  }
}' "2025-04-01"

# 2. 2025-04-02
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-02" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"心情平穩" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"無異常" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"小雨" } }] },
    "備註事件": { "rich_text":[{ "text":{ "content":"葉片濕潤但無病斑，狀況良好。" } }] }
  }
}' "2025-04-02"

# 3. 2025-04-03
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-03" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"心情愉快" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"無異常" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"晴" } }] },
    "備註事件": { "rich_text":[{ "text":{ "content":"花苞數量明顯增加。" } }] }
  }
}' "2025-04-03"

# 4. 2025-04-04
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-04" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"輕微白粉病" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"晴" } }] },
    "成本備註": { "number":200 },
    "備註事件": { "rich_text":[{ "text":{ "content":"已剪除白粉病葉片。" } }] }
  }
}' "2025-04-04"

# 5. 2025-04-05
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-05" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"無異常" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"多雲" } }] },
    "備註事件": { "rich_text":[{ "text":{ "content":"花期高峰，田間香氣撲鼻。" } }] }
  }
}' "2025-04-05"

# 6. 2025-04-06
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-06" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"無異常" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"陣雨" } }] },
    "備註事件": { "rich_text":[{ "text":{ "content":"土壤濕潤，苗勢穩定。" } }] }
  }
}' "2025-04-06"

# 7. 2025-04-07
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-07" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"斑點病" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"多雲" } }] },
    "成本備註": { "number":300 },
    "備註事件": { "rich_text":[{ "text":{ "content":"已剪除受斑點病影響葉片。" } }] }
  }
}' "2025-04-07"

# 8. 2025-04-08
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-08" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"無異常" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"晴" } }] },
    "備註事件": { "rich_text":[{ "text":{ "content":"花朵盛開，田間景色美麗。" } }] }
  }
}' "2025-04-08"

# 9. 2025-04-09
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-09" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"輕微蚜蟲" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"多雲" } }] },
    "備註事件": { "rich_text":[{ "text":{ "content":"手工去除蚜蟲並觀察後續情形。" } }] }
  }
}' "2025-04-09"

# 10. 2025-04-10
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-10" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"無異常" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"晴" } }] },
    "備註事件": { "rich_text":[{ "text":{ "content":"花期延續。" } }] }
  }
}' "2025-04-10"

# 11. 2025-04-11
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-11" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"心情放鬆" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"無異常" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"晴" } }] },
    "備註事件": { "rich_text":[{ "text":{ "content":"清晨有露水，葉片濕潤，無病害出現。" } }] }
  }
}' "2025-04-11"

# 12. 2025-04-12
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-12" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"無異常" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"晴" } }] },
    "收入概估": { "number":1600 },
    "收成量": { "number":8 },
    "備註事件": { "rich_text":[{ "text":{ "content":"品質良好。" } }] }
  }
}' "2025-04-12"

# 13. 2025-04-13
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-13" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"輕微白粉病" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"多雲" } }] },
    "成本備註": { "number":400 },
    "備註事件": { "rich_text":[{ "text":{ "content":"已局部噴藥防治。" } }] }
  }
}' "2025-04-13"

# 14. 2025-04-14
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-14" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"無異常" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"小雨" } }] },
    "備註事件": { "rich_text":[{ "text":{ "content":"田間排水順暢。" } }] }
  }
}' "2025-04-14"

# 15. 2025-04-15
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-15" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"無異常" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"晴" } }] },
    "備註事件": { "rich_text":[{ "text":{ "content":"花朵數量穩定。" } }] }
  }
}' "2025-04-15"

# 16. 2025-04-16
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-16" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"輕微斑點" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"多雲" } }] },
    "備註事件": { "rich_text":[{ "text":{ "content":"已處理斑點葉片。" } }] }
  }
}' "2025-04-16"

# 17. 2025-04-17
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-17" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"無異常" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"晴" } }] },
    "備註事件": { "rich_text":[{ "text":{ "content":"苗勢良好。" } }] }
  }
}' "2025-04-17"

# 18. 2025-04-18
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-18" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"心情愉快" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"無異常" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"微風" } }] },
    "備註事件": { "rich_text":[{ "text":{ "content":"花朵持續盛開。" } }] }
  }
}' "2025-04-18"

# 19. 2025-04-19
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-19" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"輕微蚜蟲" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"多雲" } }] },
    "備註事件": { "rich_text":[{ "text":{ "content":"手工摘除蚜蟲，苗勢未受影響。" } }] }
  }
}' "2025-04-19"

# 20. 2025-04-20
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-20" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"無異常" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"陣雨" } }] },
    "備註事件": { "rich_text":[{ "text":{ "content":"排水正常。" } }] }
  }
}' "2025-04-20"

# 21. 2025-04-21
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-21" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"無異常" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"陰" } }] },
    "備註事件": { "rich_text":[{ "text":{ "content":"苗床濕度較高。" } }] }
  }
}' "2025-04-21"

# 22. 2025-04-22
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-22" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"無異常" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"多雲" } }] },
    "備註事件": { "rich_text":[{ "text":{ "content":"花期漸入尾聲，果實逐漸膨大。" } }] }
  }
}' "2025-04-22"

# 23. 2025-04-23
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-23" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"輕微缺氮" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"陰" } }] },
    "成本備註": { "number":400 },
    "備註事件": { "rich_text":[{ "text":{ "content":"已施肥補救。" } }] }
  }
}' "2025-04-23"

# 24. 2025-04-24
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-24" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"無異常" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"晴" } }] },
    "備註事件": { "rich_text":[{ "text":{ "content":"果實逐漸轉紅。" } }] }
  }
}' "2025-04-24"

# 25. 2025-04-25
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-25" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"無異常" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"晴" } }] },
    "收入概估": { "number":2000 },
    "收成量": { "number":10 },
    "備註事件": { "rich_text":[{ "text":{ "content":"品質佳。" } }] }
  }
}' "2025-04-25"

# 26. 2025-04-26
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-26" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"無異常" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"微風" } }] },
    "備註事件": { "rich_text":[{ "text":{ "content":"苗勢穩定。" } }] }
  }
}' "2025-04-26"

# 27. 2025-04-27
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-27" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"輕微蚜蟲" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"多雲" } }] },
    "成本備註": { "number":600 },
    "備註事件": { "rich_text":[{ "text":{ "content":"已噴灑生物防治劑處理。" } }] }
  }
}' "2025-04-27"

# 28. 2025-04-28
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-28" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"無異常" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"晴" } }] },
    "備註事件": { "rich_text":[{ "text":{ "content":"果實成熟度提升。" } }] }
  }
}' "2025-04-28"

# 29. 2025-04-29
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-29" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"無異常" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"小雨" } }] },
    "備註事件": { "rich_text":[{ "text":{ "content":"土壤濕度略高，無病害擴散。" } }] }
  }
}' "2025-04-29"

# 30. 2025-04-30
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-04-30" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"—" } }] },
    "異常狀態": { "rich_text":[{ "text":{ "content":"無異常" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"晴" } }] },
    "收入概估": { "number":2400 },
    "收成量": { "number":12 },
    "備註事件": { "rich_text":[{ "text":{ "content":"田間狀況穩定。" } }] }
  }
}' "2025-04-30"

# ------- 2025 April 模擬資料結束 -------

# 1. 2025-05-01
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-01" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"今天田間土壤偏乾，草莓苗葉緣開始捲曲，懷疑高溫影響。同時發現有少量白粉狀粉末。" } }] },
    "成本備註": { "number":500 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"高溫、乾旱、白粉病" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"晴" } }] }
  }
}' "2025-05-01"

# 2. 2025-05-02
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-02" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"上午天氣悶熱，用水管淋灌，下午下小雨。部分葉片已有小斑點。" } }] },
    "成本備註": { "number":300 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"葉斑病、乾旱" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"少雨" } }] }
  }
}' "2025-05-02"

# 3. 2025-05-03
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-03" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"昨晚連續降雨約 3 小時，現場積水已退。土壤回軟，但有幾株根部有輕微腐爛跡象。" } }] },
    "成本備註": { "number":200 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"根腐病" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"短暫陣雨" } }] }
  }
}' "2025-05-03"

# 4. 2025-05-04
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-04" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"天氣陰涼，翻土檢查根部，剪除壞根並撒了少量石灰粉。未見新異常。" } }] },
    "成本備註": { "number":400 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"多雲" } }] }
  }
}' "2025-05-04"

# 5. 2025-05-05
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-05" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"開始分批採收首批成熟草莓，共 20 公斤，預估可售收入約 4000 元。" } }] },
    "成本備註": { "number":0 },
    "收入概估": { "number":4000 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"晴" } }] }
  }
}' "2025-05-05"

# 6. 2025-05-06
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-06" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"田裡發現少量葉片出現灰霉斑點，已噴灑生物製劑進行防治。午後氣溫升高。" } }] },
    "成本備註": { "number":600 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"灰黴病" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"晴" } }] }
  }
}' "2025-05-06"

# 7. 2025-05-07
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-07" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"上午天氣悶熱，部分花蕾提早凋零，疑似熱害。降溫後無明顯擴散。" } }] },
    "成本備註": { "number":0 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"熱害" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"高溫" } }] }
  }
}' "2025-05-07"

# 8. 2025-05-08
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-08" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"今早檢查苗床，一株苗萎凋死亡，懷疑根部黑腐，已清理病株。" } }] },
    "成本備註": { "number":100 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"萎凋病" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"多雲" } }] }
  }
}' "2025-05-08"

# 9. 2025-05-09
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-09" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"天氣轉陰，提供通風降低濕度，無新增病斑。" } }] },
    "成本備註": { "number":0 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"陰" } }] }
  }
}' "2025-05-09"

# 10. 2025-05-10
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-10" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"田裡發現小面積蚜蟲侵襲，新噴環保農藥防治。並補水灌溉。" } }] },
    "成本備註": { "number":800 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"蚜蟲" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"少雨" } }] }
  }
}' "2025-05-10"

# 11. 2025-05-11
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-11" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"昆蟲防治結束後，測量土壤濕度偏低，下午再澆水一次。" } }] },
    "成本備註": { "number":200 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"晴" } }] }
  }
}' "2025-05-11"

# 12. 2025-05-12
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-12" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"有 15 公斤草莓收成，品質尚可，午后下小雨，病害狀況緩解。" } }] },
    "成本備註": { "number":0 },
    "收入概估": { "number":3000 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"陣雨" } }] }
  }
}' "2025-05-12"

# 13. 2025-05-13
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-13" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"上午修剪側芽並撒覆有機肥，午後氣溫升高，觀察葉片無新病斑。" } }] },
    "成本備註": { "number":500 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"晴" } }] }
  }
}' "2025-05-13"

# 14. 2025-05-14
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-14" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"梅雨前夕，日間溫度高達 28°C，晚間有短暫陣雨，注意通風。" } }] },
    "成本備註": { "number":0 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"高溫" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"陣雨" } }] }
  }
}' "2025-05-14"

# 15. 2025-05-15
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-15" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"雨勢不大，僅土壤回軟。葉面偶有水痕，無嚴重泥濘。" } }] },
    "成本備註": { "number":0 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"小雨" } }] }
  }
}' "2025-05-15"

# 16. 2025-05-16
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-16" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"土壤濕度良好，但發現少量葉片出現白粉病斑，噴防治劑。" } }] },
    "成本備註": { "number":600 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"白粉病" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"多雲" } }] }
  }
}' "2025-05-16"

# 17. 2025-05-17
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-17" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"今早採收 18 公斤草莓，天氣多雲，無雨。下午施放生物有機肥促長。" } }] },
    "成本備註": { "number":0 },
    "收入概估": { "number":3600 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"多雲" } }] }
  }
}' "2025-05-17"

# 18. 2025-05-18
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-18" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"午後忽然降雨 2 小時，溼度飆高，觀察苗床有少量霉菌痕跡，稍後通風乾燥。" } }] },
    "成本備註": { "number":0 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"灰黴病" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"陣雨" } }] }
  }
}' "2025-05-18"

# 19. 2025-05-19
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-19" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"天氣晴朗，翻土除草，並補拍田間照片紀錄。無異常標註。" } }] },
    "成本備註": { "number":300 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"晴" } }] }
  }
}' "2025-05-19"

# 20. 2025-05-20
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-20" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"本日採收 12 公斤草莓，部分果實有輕微畸形，疑似熱害所致。" } }] },
    "成本備註": { "number":0 },
    "收入概估": { "number":2400 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"熱害" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"晴" } }] }
  }
}' "2025-05-20"

# 21. 2025-05-21
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-21" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"天氣多雲，檢查田間發現少量蚜蟲重新孳生，已再次防治。" } }] },
    "成本備註": { "number":700 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"蚜蟲" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"多雲" } }] }
  }
}' "2025-05-21"

# 22. 2025-05-22
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-22" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"今早雨勢稍大，午後放晴，拍照記錄土壤濕度回升，無明顯病害。" } }] },
    "成本備註": { "number":0 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"陣雨" } }] }
  }
}' "2025-05-22"

# 23. 2025-05-23
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-23" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"檢查苗床根部，發現兩株輕微根腐，已拔除並噴灑殺菌劑。" } }] },
    "成本備註": { "number":400 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"根腐病" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"多雲" } }] }
  }
}' "2025-05-23"

# 24. 2025-05-24
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-24" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"天氣晴朗，施放有機肥，加強日灌水一次，午後無雨。" } }] },
    "成本備註": { "number":500 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"晴" } }] }
  }
}' "2025-05-24"

# 25. 2025-05-25
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-25" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"上午採收 20 公斤草莓，果實飽滿。午後氣溫驟降，小雨持續約 2 小時。" } }] },
    "成本備註": { "number":0 },
    "收入概估": { "number":4000 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"小雨" } }] }
  }
}' "2025-05-25"

# 26. 2025-05-26
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-26" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"發現有幾株葉片泛黃，疑似缺氮症狀，施加液肥補充養分。" } }] },
    "成本備註": { "number":600 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"缺氮" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"多雲" } }] }
  }
}' "2025-05-26"

# 27. 2025-05-27
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-27" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"今早霧氣濃重，午後放晴，無新增異常；繼續澆灌，下周預計降雨。" } }] },
    "成本備註": { "number":0 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"陰有霧" } }] }
  }
}' "2025-05-27"

# 28. 2025-05-28
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-28" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"土壤濕度稍高，抽水保持排水通暢，檢查後沒見病斑。" } }] },
    "成本備註": { "number":0 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"小雨" } }] }
  }
}' "2025-05-28"

# 29. 2025-05-29
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-29" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"田裡少量白粉病再度發生，已噴灑生物製劑防治，並加強通風。" } }] },
    "成本備註": { "number":600 },
    "收入概估": { "number":0 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"白粉病" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"多雲" } }] }
  }
}' "2025-05-29"

# 30. 2025-05-30
upload_one '{
  "parent": { "database_id": "'"${NOTION_DATABASE_ID}"'" },
  "properties": {
    "環境": { "title":[{ "text":{ "content":"田間草莓區" } }] },
    "日期": { "date":{ "start":"2025-05-30" } },
    "心情與觀察": { "rich_text":[{ "text":{ "content":"今晨採收 22 公斤草莓，今天氣候舒適，無病害擴散情形，準備月底大檢查。" } }] },
    "成本備註": { "number":0 },
    "收入概估": { "number":4400 },
    "異常狀態": { "rich_text":[{ "text":{ "content":"" } }] },
    "氣候狀況": { "rich_text":[{ "text":{ "content":"晴" } }] }
  }
}' "2025-05-30"

# 腳本結束