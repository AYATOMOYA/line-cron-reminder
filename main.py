import requests

# LINE Messaging APIのチャネルアクセストークン
LINE_ACCESS_TOKEN = "Yis8B6NjIZ0Pbn24iMuL+BzXA2b/a1P3dp7HYdkejPmOEKdV9DISoHGnRkRRwsuRHSZhsoOzARHVUM1tB8fpTqao9o2IRSz02cwtouUigJ8NzStDdIkZHvjF6bUaRcZKM0Lv4400yFHCVFCJA7+k1AdB04t89/1O/w1cDnyilFU="

# 通知メッセージ
message = "🔔 テスト送信：PythonからLINEに通知できました！"

# リクエスト内容
headers = {
    "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}
data = {
    "to": "U7f0e1283e0aa71f58a737598191da23c",  # ユーザーID（←テスト通知先）
    "messages": [
        {
            "type": "text",
            "text": message
        }
    ]
}

# LINEのPush通知エンドポイントへ送信
response = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=data)

# 結果表示（失敗時はエラー表示）
print("✅ 通知成功" if response.status_code == 200 else f"❌ 通知失敗: {response.text}")
