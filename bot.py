
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

WELCOME_MESSAGE = """
⚽ Welcome to Football News Hub! 📰

Stay updated with the world of football!

🔥 Football News
📅 Match Fixtures
🏆 Match Results
🌍 Team Updates

Thanks for joining us. Enjoy the beautiful game! ⚽
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)

def main():
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise RuntimeError("BOT_TOKEN is missing!")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))

    print("Football News Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
