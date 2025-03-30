

import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def ask_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "anthropic/claude-instant-v1",
        "messages": [
            {"role": "system", "content": "Bạn là một luật sư AI chuyên tư vấn pháp luật Việt Nam."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

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
