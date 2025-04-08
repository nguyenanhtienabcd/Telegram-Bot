

import os
from dotenv import load_dotenv
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL")
CHARACTER = os.getenv("CHARACTER")

print("✅ TELEGRAM_BOT_TOKEN:", TELEGRAM_BOT_TOKEN)
print("✅ OPENROUTER_API_KEY:", OPENROUTER_API_KEY)
print("✅ MODEL:", MODEL)
print("✅ CHARACTER:", CHARACTER)


def ask_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
         "model": MODEL,         #"model": "anthropic/claude-instant-v1",
        "messages": [
            {"role": "system", "content": CHARACTER},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        print("📥 Status Code:", response.status_code)
        print("📄 Raw Response:", response.text)  # ⚠️ XEM CHÍNH XÁC API TRẢ VỀ GÌ

        response.raise_for_status()
        json_data = response.json()

        if "choices" in json_data:
            return json_data["choices"][0]["message"]["content"]
        elif "error" in json_data:
            return f"❗API error: {json_data['error']['message']}"
        else:
            return "❗Không tìm thấy nội dung trả về từ AI. Vui lòng kiểm tra lại model hoặc API key."

    except requests.exceptions.HTTPError as http_err:
        return f"🚨 Lỗi HTTP: {http_err}"
    except Exception as e:
        return f"🚨 Lỗi khác: {str(e)}"

#  Hàm xử lý tin nhắn Telegram
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    await update.message.reply_text("🤖 Đang suy nghĩ...")
    reply = ask_openrouter(user_input)
    await update.message.reply_text(reply)


def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot đang chạy...")
    app.run_polling()

if __name__ == '__main__':
    main()
