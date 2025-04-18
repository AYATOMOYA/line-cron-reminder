import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import requests
from datetime import datetime

# .envから読み込む
load_dotenv()
LINE_TOKEN = os.getenv("LINE_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")

# Google認証
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
gc = gspread.authorize(creds)

# シートを開く
SPREADSHEET_KEY = '1bln9goTtV-jkiIGrYvPkPbneE81w2Z9VMPjph0R8_Z4'
worksheet = gc.open_by_key(SPREADSHEET_KEY).worksheet("タスク通知予約②")

# 今日の日付
today = datetime.now().strftime('%Y/%m/%d')

# データ取得（ヘッダー除く）
data = worksheet.get_all_values()[1:]

# 通知タイプが「即時」の行を抽出（D列 → row[3]）
filtered = [row for row in data if row[0] == today and row[3] == "即時"]

# セクションごとに分類（E列 → row[4]）
schedule = []
task = []
confirm = []

for row in filtered:
    content = row[2].strip()  # タスク内容（C列）
    category = row[4].strip()  # 項目（E列）

    if category == "スケジュール":
        schedule.append(content)
    elif category == "タスク":
        task.append(content)
    elif category == "前確":
        confirm.append(content)

# 未入力項目チェック
if not schedule and not task and not confirm:
    raise Exception("即時通知対象のセルが空です。スプレッドシートを確認してください。")

# 通知内容を整形（見やすいデザインへ）
message = f"本日（{today}）の予定\n\n"

message += "📅 スケジュール\n"
message += "※今回はなし\n" if not schedule else "\n".join(schedule)

message += "\n\n📝 タスク\n"
if not task:
    message += "※今回はなし\n"
else:
    message += "\n".join([f"{i+1}. {t.split('】')[0]}】\n　{t.split('】')[1]}" if '】' in t else f"{i+1}. {t}" for i, t in enumerate(task)])

message += "\n\n🔍 前確\n"
if not confirm:
    message += "※今回はなし\n"
else:
    message += "\n".join([f"{i+1}. {c.split('】')[0]}】\n　{c.split('】')[1]}" if '】' in c else f"{i+1}. {c}" for i, c in sorted(enumerate(confirm), key=lambda x: x[1])])

# LINE通知
headers = {
    "Authorization": f"Bearer {LINE_TOKEN}",
    "Content-Type": "application/json"
}
payload = {
    "to": LINE_USER_ID,
    "messages": [{"type": "text", "text": message}]
}
url = "https://api.line.me/v2/bot/message/push"

response = requests.post(url, headers=headers, json=payload)
print(f"LINE送信ステータス: {response.status_code}")
