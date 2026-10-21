
import os
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "").strip().lstrip("@")

WELCOME = (
    "🎉 <b>Welcome to LOTTO!</b>\n\n"
    "Choose an option below to get started.\n"
    "Use the buttons to explore the bot."
)

MENU = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🎟️ Lotto Info", callback_data="lotto"),
        InlineKeyboardButton("📋 How It Works", callback_data="how"),
    ],
    [
        InlineKeyboardButton("❓ Help", callback_data="help"),
        InlineKeyboardButton("ℹ️ About", callback_data="about"),
    ],
    [
        InlineKeyboardButton("📩 Contact Admin", callback_data="contact"),
    ],
])

BACK = InlineKeyboardMarkup([
    [InlineKeyboardButton("⬅️ Main Menu", callback_data="menu")]
])

PAGES = {
    "lotto": (
        "🎟️ <b>Lotto Information</b>\n\n"
        "Get lotto information and official announcements here.\n\n"
        "Official results and information should be verified "
        "with the relevant lottery provider."
    ),
    "how": (
        "📋 <b>How It Works</b>\n\n"
        "1. Choose an option from the menu.\n"
        "2. Read the information provided.\n"
        "3. Contact the admin if you need help.\n\n"
        "Lottery outcomes are random. No winnings are guaranteed."
    ),
    "help": (
        "❓ <b>Help Center</b>\n\n"
        "/start — Open the main menu\n"
        "/menu — Show all options\n"
        "/help — Get help"
    ),
    "about": (
        "ℹ️ <b>About LOTTO</b>\n\n"
        "This bot provides lotto information and announcements.\n\n"
        "Please check official sources for verified results "
        "and applicable rules."
    ),
}


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.effective_message.reply_text(
        WELCOME,
        reply_markup=MENU,
        parse_mode="HTML",
    )


async def menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.effective_message.reply_text(
        WELCOME,
        reply_markup=MENU,
        parse_mode="HTML",
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.effective_message.reply_text(
        PAGES["help"],
        reply_markup=BACK,
        parse_mode="HTML",
    )


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    choice = query.data

    if choice == "menu":
        await query.edit_message_text(
            WELCOME,
            reply_markup=MENU,
            parse_mode="HTML",
        )
        return

    if choice == "contact":
        if ADMIN_USERNAME:
            message = (
                "📩 <b>Contact Admin</b>\n\n"
                f"Tap below to message @{ADMIN_USERNAME}."
            )
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "Message Admin",
                        url=f"https://t.me/{ADMIN_USERNAME}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⬅️ Main Menu",
                        callback_data="menu",
                    )
                ],
            ])
        else:
            message = (
                "📩 <b>Contact Admin</b>\n\n"
                "The admin contact is not configured yet."
            )
            keyboard = BACK

    elif choice in PAGES:
        message = PAGES[choice]
        keyboard = BACK

    else:
        message = "Sorry, that option is not available."
        keyboard = BACK

    await query.edit_message_text(
        message,
        reply_markup=keyboard,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):
    logger.error(
        "An error occurred while processing an update",
        exc_info=context.error,
    )


def main():
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise RuntimeError(
            "BOT_TOKEN is missing. Set it in your environment variables."
        )

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_error_handler(error_handler)

    logger.info("LOTTO bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
