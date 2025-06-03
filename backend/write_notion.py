from notion_client import Client
import os
from dotenv import load_dotenv
import datetime

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

FIELD_KEYWORDS = {
    "環境": [
        "吉軒", "農場", "草莓田", "香瓜田", "苗栗", "西湖", "大棚", "溫室", "高架", "戶外", "田間", "茅仔埔", "園區", "地塊", "土耕區", "產地"
    ],
    "作物狀態": [
        "成熟", "開花", "結實", "著果", "幼苗", "長高", "長葉", "長勢", "病害", "黃葉", "枯萎", "缺水", "發芽", "斷根", "異常", "萎縮", "果實變色", "果實裂果", "結果", "產果期", "壞果", "漂亮", "存活", "白斑", "白粉病",
        "灰黴病", "灰黴", "花萎凋", "炭疽病", "炭疽", "黑斑", "褐色病斑",
        "白色粉末", "灰色霉狀", "白粉", "葉枯", "圓形病斑",
        "疫病", "水漬狀", "腐爛", "根腐病", "根腐", "根部黑化", "葉斑病", 
        "葉斑", "斑點", "黃化", "矮化", "病毒病", "細菌性斑點病",
        "葉片反捲", "葉緣焦枯", "葉色暗沉", "葉脈透明", "葉片變厚", "葉片捲曲", "葉面黃化", "葉柄黑化", "葉子皺縮"
    ],
    "收成量": [
        "收成", "採收", "產量", "一箱", "一籃", "一筐", "幾箱", "幾斤", "沒收", "豐收", "搶收", "滿滿", "成果", "沒幾顆", "收成還不錯", "收獲"
    ],
    "農事行動": [
        "整理", "除草", "手拔草", "灑藥", "噴藥", "施肥", "撒肥", "灌溉", "澆水", "移苗", "補苗", "搭棚", "修剪", "綁藤", "鋪草", "套袋", "翻地", "翻土", "疏花", "放蜂", "補網", "整理田區", "除蟲", "捕蟲", "巡田", "噴有機資材", "噴營養劑", "換行", "整枝", "播種", "下田", "收割", "整地", "撿拾", "整修", "農藥檢測", "檢測", "報告"
    ],
    "種植方式": [
        "有機", "無毒", "無農藥", "自然農法", "友善耕作", "慣行", "輪作", "轉作", "新法", "環保", "無毒栽培"
    ],
    "日期": [
        "今天", "昨日", "今早", "早上", "下午", "晚上", "202", "2024", "2025", "三月份", "四月份", "夏天", "春天", "本月", "上週", "這週", "去年", "近日", "每年", "月底", "年初"
    ],
    "氣候狀況": [
        "大太陽", "艷陽", "陰天", "晴天", "天氣晴朗", "好天氣", "下雨", "大雨", "小雨", "雨停", "午後雷陣雨",
        "濕氣重", "天氣熱", "溫度高", "高溫", "寒流", "冷", "涼", "霜降", "寒冷", "濕冷", "乾旱", "悶熱", "炎熱",
        "下霧", "下小雨", "下毛毛雨", "多雲", "多雲時晴", "陰雨", "暴雨", "降雨", "晴時多雲", "忽冷忽熱",
        "氣候", "早晚溫差大", "天氣變化大", "天氣不穩", "天氣轉涼", "春天", "夏天", "秋天", "冬天"
    ],
    "心情與觀察": [
        "很累", "辛苦", "充實", "很開心", "期待", "滿意", "感謝", "感恩", "快樂", "很煩", "幸福", "無奈", "好險", "可惜", "努力", "有趣", "有收穫", "感動", "無力", "擔心", "疲憊", "覺得", "很有趣", "損失比較多", "堅持", "簡單", "難", "沒辦法持久", "想休息", "休息"
    ],
    "成本紀錄": [
        "花了", "買肥料", "買資材", "請工", "請人幫忙", "加班", "花成本", "多花", "支出", "投入", "工錢", "薪水", "租地", "材料費", "機械費", "水費", "電費", "農藥費", "肥料費", "保養", "檢測費", "報告費"
    ],
    "成本備註": [
        "有點貴", "便宜", "划算", "預算", "追加", "扣掉", "剩下", "極限", "ppm", "偵測極限"
    ],
    "銷售方式": [
        "宅配", "自取", "現場", "網購", "團購", "通路", "合作社", "市場", "批發", "零售", "預購", "訂單",
        "LINE", "臉書私訊", "FB訂單", "Messenger", "粉專私訊", "群組訂單", "親友訂單", "現場直送",
        "農夫市集", "快閃市集", "攤販", "路邊攤", "臨時接單", "展售會", "農業展", "台北快閃", "外送", "同學團", "親友團",
        "訂購", "預約", "來店自取", "門市取貨", "現場發貨", "自家配送", "物流", "黑貓宅急便", "新竹貨運",
        "line訂單", "line群組", "臉書留言", "fb留言", "現場下單", "直接下單", "一箱出貨", "冷藏宅配", "冷凍宅配"
    ],
    "銷售價格": [
        "元", "一盒", "一斤", "一台斤", "售價", "價格", "一箱", "優惠", "原價", "特價", "價格", "報價"
    ],
    "收入概估": [
        "賣了", "收入", "營收", "進帳", "現金", "刷卡", "收現", "總額", "合計"
    ],
    "備註事件": [
        # 親子/體驗
        "親子", "採草莓", "草莓體驗", "親子採果", "草莓小農夫", "草莓 DIY", "親子 DIY", "親子旅遊", "草莓農場活動", "體驗營", "導覽", "團體活動", "親子樂園", "互動課程", "農事體驗", "摘果", "農場導覽", 
        # 訪客/交流/事件
        "里長來訪", "訪客", "參觀", "農友交流", "活動", "拜訪", "媒體", "展覽", "客人", "親友", "意外", "修繕", "新設備", "招待", "順便", 
        # 檢測/報告/特殊
        "農藥檢測", "檢測", "農藥0檢出", "報告", "證明", "極限", "偵測", "化學農藥", "無農藥", "0檢出", "土壤線蟲", "氟派瑞", "生產履歷", "說明"
    ],
}

def get_notion_fields():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
    }
    resp = requests.get(url, headers=headers)
    props = resp.json()["properties"]
    return {k: v["type"] for k, v in props.items()}

import requests

import jieba

def extract_keywords(text: str) -> set:
    return set(jieba.cut(text))

def auto_map_to_fields(text):
    fields = get_notion_fields()
    result = {field: [] for field in fields}
    tokens = extract_keywords(text)
    for field, kw_list in FIELD_KEYWORDS.items():
        # 僅允許 FIELD_KEYWORDS["成本紀錄"] 關鍵字進入成本紀錄
        if field == "成本紀錄":
            result["成本紀錄"] = []
            for kw in FIELD_KEYWORDS["成本紀錄"]:
                if kw in text:
                    result["成本紀錄"].append(kw)
            continue
        for kw in kw_list:
            if kw in text:
                result[field].append(kw)
    # 成本備註自動加總成本紀錄金額
    if "成本備註" in fields:
        import re
        cost_keywords = FIELD_KEYWORDS["成本紀錄"]
        total_cost = 0
        for kw in cost_keywords:
            matches = re.findall(fr'{kw}[^\d]*(\d+\.?\d*)\s*元', text)
            for m in matches:
                total_cost += float(m)
        if total_cost > 0:
            result["成本備註"] = [str(total_cost)]
    import re
    # 自動抓「售價」「價格」「特價」「原價」「每箱」「一箱」「一斤」「一盒」「報價」後的數字元，對應銷售價格欄位
    if "銷售價格" in fields:
        price_matches = re.findall(r'(售價|價格|特價|原價|每箱|一箱|一斤|一盒|報價)[^\d]*(\d+\.?\d*)\s*元', text)
        if price_matches:
            result["銷售價格"].extend([f"{m[1]}元" for m in price_matches])
        else:
            # 若沒匹配到上述模式，仍嘗試抓所有「數字+元」
            price_only = re.findall(r'(\d+\.?\d*)\s*元', text)
            if price_only:
                result["銷售價格"].extend([f"{x}元" for x in price_only])
    # 自動抓「收入」「進帳」「營收」「合計」「總額」「賣了」等後的數字元，對應收入概估欄位
    if "收入概估" in fields:
        income_matches = re.findall(r'(收入|進帳|營收|合計|總額|賣了)[^\d]*(\d+\.?\d*)\s*元', text)
        if income_matches:
            result["收入概估"].extend([f"{m[1]}元" for m in income_matches])
        # 補充抓現金、刷卡、收現描述
        cash_matches = re.findall(r'(現金|刷卡|收現)[^\d]*(\d+\.?\d*)\s*元', text)
        if cash_matches:
            result["收入概估"].extend([f"{m[1]}元" for m in cash_matches])

    # 額外加入分類與異常狀態標記
    if "分類" in fields:
        farming_keywords = {
            "施肥": ["肥", "有機肥", "化肥"],
            "澆水": ["灌溉", "水", "澆"],
            "除草": ["雜草", "割草", "除草"],
            "收成": ["採收", "收成", "摘"],
            "播種": ["播種", "種子", "種下"]
        }
        category = "其他"
        for k, wordlist in farming_keywords.items():
            if any(w in tokens for w in wordlist):
                category = k
                break
        result["分類"] = [category]

    # 移除所有 "異常現象" 相關欄位處理，僅處理 "異常狀態"
    if "異常狀態" in fields:
        exclusion_phrases = ["無異常", "沒有異常", "看起來正常", "很正常", "無病蟲害", "未發現異常", "尚可", "狀況不錯"]
        abnormal_keywords = [
            "白斑", "白粉病", "斑點", "葉斑", "葉病", "灰黴", "灰黴病", "炭疽", "炭疽病",
            "白色粉末", "灰色霉狀", "白粉", "葉枯", "疫病", "水漬狀", "腐爛", "根腐", 
            "根部黑化", "矮化", "病毒", "病毒病", "細菌性斑點病", "葉片反捲", 
            "葉緣焦枯", "葉色暗沉", "葉脈透明", "葉片變厚", "葉片捲曲", "葉面黃化", 
            "葉柄黑化", "葉子皺縮"
        ]
        if any(phrase in text for phrase in exclusion_phrases):
            result["異常狀態"] = ["正常"]
        else:
            detected = []
            for ab in abnormal_keywords:
                if ab in text:
                    detected.append(ab)
            if detected:
                result["異常狀態"] = list(set(detected))
            else:
                result["異常狀態"] = ["異常：" + text]
    # 產生 Notion 需要的格式
    notion_properties = {}
    for field, vals in result.items():
        t = fields[field]
        if not vals:
            continue
        if field == "異常狀態":
            # 直接寫入原文
            notion_properties[field] = {"rich_text": [{"text": {"content": text}}]}
            continue
        value_str = "、".join(list(set(vals)))
        if t == "title":
            notion_properties[field] = {"title": [{"text": {"content": value_str}}]}
        elif t == "rich_text":
            notion_properties[field] = {"rich_text": [{"text": {"content": value_str}}]}
        elif t == "number":
            try:
                # 特別處理金額格式
                nums = [float(re.sub("[^0-9.]", "", s)) for s in vals if re.search(r'\d', s)]
                notion_properties[field] = {"number": nums[0] if nums else 0}
            except:
                notion_properties[field] = {"number": 0}
        elif t == "date":
            pass  # 日期由後面 today 自動補
    # 備註事件欄位：若有此欄位則存全文
    if "備註事件" in fields:
        notion_properties["備註事件"] = {"rich_text": [{"text": {"content": text}}]}
    # 自動填今天日期
    if "日期" in fields and "日期" not in notion_properties:
        import datetime
        notion_properties["日期"] = {"date": {"start": datetime.date.today().isoformat()}}
    # 新增：顯示異常狀態與分類的推論結果
    print("🔍 判斷異常狀態：", result.get("異常狀態"))
    print("🔍 自動分類：", result.get("分類"))
    print("🧩 mapping 後的 notion_properties：", notion_properties)
    return notion_properties

def write_to_notion(text):
    """
    自動提取農事內容、mapping 對應欄位，寫入 Notion
    """
    print("📝 傳入 write_to_notion() 的內容：", text)
    # 新增：若 text 是 dict，則提取 "notes" 欄位作為文字
    if isinstance(text, dict):
        text = text.get("notes", "")
    notion = Client(auth=NOTION_API_KEY)
    properties = auto_map_to_fields(text)
    print("🔍 判斷異常狀態：", properties.get("異常狀態"))
    print("🔍 自動分類：", properties.get("分類"))
    print("🔍 自動 mapping properties：", properties)
    try:
        response = notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties=properties
        )
        print("✅ 已成功寫入 Notion")
        return response.get("url", "")
    except Exception as e:
        print("❌ Notion API 呼叫失敗，錯誤訊息：", e)
        raise
